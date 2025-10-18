from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.schemas.onu import ONU, ONUCreate, ONUUpdate
from app.models.onu import ONU as ONUModel
from app.models.olt import OLT as OLTModel
from app.services.snmp_client import SNMPClient

router = APIRouter()


@router.get("/", response_model=List[ONU])
def get_onus(
    skip: int = 0,
    limit: int = 100,
    olt_id: Optional[int] = Query(None),
    port_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all ONUs with optional filters"""
    query = db.query(ONUModel)
    
    if olt_id:
        query = query.filter(ONUModel.olt_id == olt_id)
    if port_id:
        query = query.filter(ONUModel.port_id == port_id)
    if status:
        query = query.filter(ONUModel.status == status)
    
    onus = query.offset(skip).limit(limit).all()
    return onus


@router.get("/{onu_id}", response_model=ONU)
def get_onu(onu_id: int, db: Session = Depends(get_db)):
    """Get ONU by ID"""
    onu = db.query(ONUModel).filter(ONUModel.id == onu_id).first()
    if not onu:
        raise HTTPException(status_code=404, detail="ONU not found")
    return onu


@router.post("/", response_model=ONU)
def create_onu(onu: ONUCreate, db: Session = Depends(get_db)):
    """Create/Register new ONU"""
    # Check if ONU with same SN exists
    existing = db.query(ONUModel).filter(ONUModel.sn == onu.sn).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="ONU with this serial number already exists"
        )
    
    # Verify OLT exists
    olt = db.query(OLTModel).filter(OLTModel.id == onu.olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Create ONU
    db_onu = ONUModel(**onu.dict())
    db.add(db_onu)
    db.commit()
    db.refresh(db_onu)
    
    return db_onu


@router.put("/{onu_id}", response_model=ONU)
def update_onu(onu_id: int, onu: ONUUpdate, db: Session = Depends(get_db)):
    """Update ONU"""
    db_onu = db.query(ONUModel).filter(ONUModel.id == onu_id).first()
    if not db_onu:
        raise HTTPException(status_code=404, detail="ONU not found")
    
    # Update fields
    update_data = onu.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_onu, field, value)
    
    db.commit()
    db.refresh(db_onu)
    
    return db_onu


@router.delete("/{onu_id}")
def delete_onu(onu_id: int, db: Session = Depends(get_db)):
    """Delete ONU"""
    db_onu = db.query(ONUModel).filter(ONUModel.id == onu_id).first()
    if not db_onu:
        raise HTTPException(status_code=404, detail="ONU not found")
    
    db.delete(db_onu)
    db.commit()
    
    return {"message": "ONU deleted successfully"}


@router.post("/{onu_id}/refresh")
def refresh_onu_status(onu_id: int, db: Session = Depends(get_db)):
    """Refresh ONU status from OLT via SNMP"""
    db_onu = db.query(ONUModel).filter(ONUModel.id == onu_id).first()
    if not db_onu:
        raise HTTPException(status_code=404, detail="ONU not found")
    
    # Get OLT
    olt = db.query(OLTModel).filter(OLTModel.id == db_onu.olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Create SNMP client
    snmp = SNMPClient(
        host=olt.ip_address,
        community=olt.snmp_community,
        port=olt.snmp_port,
        version=olt.snmp_version
    )
    
    # Get ONU details from OLT
    # Note: Need slot/port/onu_id - this is simplified
    if db_onu.onu_id:
        # Extract slot/port from port_id or use default
        slot = 1  # TODO: get from port
        port = 1  # TODO: get from port
        
        details = snmp.get_onu_details(slot, port, db_onu.onu_id)
        
        # Update ONU in database
        if details.get("status"):
            db_onu.status = "online" if details["status"] == "1" else "offline"
        
        if details.get("rx_power"):
            try:
                db_onu.rx_power = float(details["rx_power"])
            except:
                pass
        
        if details.get("tx_power"):
            try:
                db_onu.tx_power = float(details["tx_power"])
            except:
                pass
        
        if details.get("distance"):
            try:
                db_onu.distance = int(details["distance"])
            except:
                pass
        
        db_onu.updated_at = datetime.now()
        db.commit()
        db.refresh(db_onu)
    
    return db_onu


@router.get("/olt/{olt_id}/discover")
def discover_onus(olt_id: int, db: Session = Depends(get_db)):
    """Discover ONUs on OLT"""
    olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Create SNMP client
    snmp = SNMPClient(
        host=olt.ip_address,
        community=olt.snmp_community,
        port=olt.snmp_port,
        version=olt.snmp_version
    )
    
    # Test connection
    if not snmp.test_connection():
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to OLT"
        )
    
    # Get ONU list
    onus = snmp.get_onu_list()
    
    return {
        "olt_id": olt_id,
        "onus_discovered": len(onus),
        "onus": onus
    }
