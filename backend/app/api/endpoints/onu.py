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
        
        db.commit()
        db.refresh(db_onu)
    
    return {"message": "ONU refreshed"}


@router.get("/olt/{olt_id}/discover")
def discover_onus(olt_id: int, db: Session = Depends(get_db)):
    """Discover ONUs on OLT and persist them"""
    from app.models.olt import Slot, Port  # local import to avoid circulars
    olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    snmp = SNMPClient(
        host=olt.ip_address,
        community=olt.snmp_community,
        port=olt.snmp_port,
        version=olt.snmp_version
    )
    
    if not snmp.test_connection():
        raise HTTPException(status_code=503, detail="Cannot connect to OLT")
    
    discovered = snmp.get_onu_list()
    created = 0
    updated = 0
    errors = 0
    
    for item in discovered:
        try:
            slot_num = int(item.get("slot"))
            port_num = int(item.get("port"))
            onu_id = int(item.get("onu_id"))
            
            slot = db.query(Slot).filter(Slot.olt_id == olt.id, Slot.slot_number == slot_num).first()
            if not slot:
                slot = Slot(olt_id=olt.id, slot_number=slot_num, status="online")
                db.add(slot)
                db.flush()
            
            port = db.query(Port).filter(Port.slot_id == slot.id, Port.port_number == port_num).first()
            if not port:
                port = Port(slot_id=slot.id, port_number=port_num, status="up")
                db.add(port)
                db.flush()
            
            details = snmp.get_onu_details(slot_num, port_num, onu_id) or {}
            sn = details.get("sn")
            if not sn:
                # Skip if serial number cannot be read (column is non-null)
                continue
            
            existing = db.query(ONUModel).filter(ONUModel.sn == sn).first()
            status_val = details.get("status")
            status_str = "online" if status_val == "1" else "offline"
            
            if existing:
                existing.port_id = port.id
                existing.olt_id = olt.id
                existing.onu_id = onu_id
                existing.status = status_str
                try:
                    if details.get("rx_power") is not None:
                        existing.rx_power = float(details["rx_power"])
                    if details.get("tx_power") is not None:
                        existing.tx_power = float(details["tx_power"])
                    if details.get("distance") is not None:
                        existing.distance = int(float(details["distance"]))
                except Exception:
                    pass
                updated += 1
            else:
                db_onu = ONUModel(
                    sn=sn,
                    olt_id=olt.id,
                    port_id=port.id,
                    onu_id=onu_id,
                    status=status_str,
                    auth_status="unauthorized"
                )
                try:
                    if details.get("rx_power") is not None:
                        db_onu.rx_power = float(details["rx_power"])
                    if details.get("tx_power") is not None:
                        db_onu.tx_power = float(details["tx_power"])
                    if details.get("distance") is not None:
                        db_onu.distance = int(float(details["distance"]))
                except Exception:
                    pass
                db.add(db_onu)
                created += 1
        except Exception:
            errors += 1
            continue
    
    db.commit()
    
    return {
        "olt_id": olt_id,
        "onus_discovered": len(discovered),
        "onus_created": created,
        "onus_updated": updated,
        "errors": errors
    }
