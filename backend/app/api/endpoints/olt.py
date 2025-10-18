from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.schemas.olt import OLT, OLTCreate, OLTUpdate, OLTStatus
from app.models.olt import OLT as OLTModel, Port
from app.services.snmp_client import SNMPClient

router = APIRouter()


@router.get("/", response_model=List[OLT])
def get_olts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all OLTs"""
    olts = db.query(OLTModel).offset(skip).limit(limit).all()
    return olts


@router.get("/{olt_id}", response_model=OLT)
def get_olt(olt_id: int, db: Session = Depends(get_db)):
    """Get OLT by ID"""
    olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    return olt


@router.post("/", response_model=OLT)
def create_olt(olt: OLTCreate, db: Session = Depends(get_db)):
    """Create new OLT"""
    # Check if OLT with same name or IP exists
    existing = db.query(OLTModel).filter(
        (OLTModel.name == olt.name) | (OLTModel.ip_address == olt.ip_address)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OLT with this name or IP already exists"
        )
    
    # Create OLT
    db_olt = OLTModel(**olt.dict())
    db.add(db_olt)
    db.commit()
    db.refresh(db_olt)
    
    return db_olt


@router.put("/{olt_id}", response_model=OLT)
def update_olt(olt_id: int, olt: OLTUpdate, db: Session = Depends(get_db)):
    """Update OLT"""
    db_olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not db_olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Update fields
    update_data = olt.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_olt, field, value)
    
    db.commit()
    db.refresh(db_olt)
    
    return db_olt


@router.delete("/{olt_id}")
def delete_olt(olt_id: int, db: Session = Depends(get_db)):
    """Delete OLT"""
    db_olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not db_olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    db.delete(db_olt)
    db.commit()
    
    return {"message": "OLT deleted successfully"}


@router.post("/{olt_id}/test", response_model=OLTStatus)
def test_olt_connection(olt_id: int, db: Session = Depends(get_db)):
    """Test connection to OLT via SNMP"""
    db_olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not db_olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Create SNMP client
    snmp = SNMPClient(
        host=db_olt.ip_address,
        community=db_olt.snmp_community,
        port=db_olt.snmp_port,
        version=db_olt.snmp_version
    )
    
    # Test connection
    start_time = datetime.now()
    is_reachable = snmp.test_connection()
    response_time = (datetime.now() - start_time).total_seconds()
    
    if is_reachable:
        # Get system info
        sys_info = snmp.get_system_info()
        
        # Update OLT status in database
        db_olt.status = "online"
        db_olt.last_seen = datetime.now()
        
        if sys_info.get("uptime"):
            try:
                db_olt.uptime = int(sys_info["uptime"])
            except:
                pass
        
        db.commit()
        
        # Count ONUs
        total_onus = db.query(OLTModel).filter(OLTModel.id == olt_id).count()
        
        return OLTStatus(
            olt_id=olt_id,
            status="online",
            is_reachable=True,
            response_time=response_time,
            uptime=db_olt.uptime,
            total_onus=total_onus,
            online_onus=0,  # TODO: implement actual count
            offline_onus=0
        )
    else:
        # Update status to offline
        db_olt.status = "offline"
        db.commit()
        
        return OLTStatus(
            olt_id=olt_id,
            status="offline",
            is_reachable=False,
            response_time=response_time
        )


@router.post("/{olt_id}/sync")
def sync_olt_data(olt_id: int, db: Session = Depends(get_db)):
    """Sync OLT data from device (discover ONUs)"""
    db_olt = db.query(OLTModel).filter(OLTModel.id == olt_id).first()
    if not db_olt:
        raise HTTPException(status_code=404, detail="OLT not found")
    
    # Create SNMP client
    snmp = SNMPClient(
        host=db_olt.ip_address,
        community=db_olt.snmp_community,
        port=db_olt.snmp_port,
        version=db_olt.snmp_version
    )
    
    # Test connection
    if not snmp.test_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot connect to OLT"
        )
    
    # Get system info
    sys_info = snmp.get_system_info()
    db_olt.status = "online"
    db_olt.last_seen = datetime.now()
    
    # Get ONU list
    onus = snmp.get_onu_list()
    
    db.commit()
    
    return {
        "message": "OLT data synced successfully",
        "system_info": sys_info,
        "onus_discovered": len(onus)
    }
