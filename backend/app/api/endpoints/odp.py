from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.odp import ODP, ODPCreate, ODPUpdate
from app.models.odp import ODP as ODPModel

router = APIRouter()


@router.get("/", response_model=List[ODP])
def get_odps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all ODPs"""
    odps = db.query(ODPModel).offset(skip).limit(limit).all()
    return odps


@router.get("/{odp_id}", response_model=ODP)
def get_odp(odp_id: int, db: Session = Depends(get_db)):
    """Get ODP by ID"""
    odp = db.query(ODPModel).filter(ODPModel.id == odp_id).first()
    if not odp:
        raise HTTPException(status_code=404, detail="ODP not found")
    return odp


@router.post("/", response_model=ODP)
def create_odp(odp: ODPCreate, db: Session = Depends(get_db)):
    """Create new ODP"""
    # Check if ODP with same name exists
    existing = db.query(ODPModel).filter(ODPModel.name == odp.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="ODP with this name already exists"
        )
    
    # Create ODP
    db_odp = ODPModel(**odp.dict())
    db_odp.available_ports = db_odp.total_ports  # Initially all ports available
    
    db.add(db_odp)
    db.commit()
    db.refresh(db_odp)
    
    return db_odp


@router.put("/{odp_id}", response_model=ODP)
def update_odp(odp_id: int, odp: ODPUpdate, db: Session = Depends(get_db)):
    """Update ODP"""
    db_odp = db.query(ODPModel).filter(ODPModel.id == odp_id).first()
    if not db_odp:
        raise HTTPException(status_code=404, detail="ODP not found")
    
    # Update fields
    update_data = odp.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_odp, field, value)
    
    # Recalculate available ports
    if 'total_ports' in update_data:
        db_odp.available_ports = db_odp.total_ports - db_odp.used_ports
    
    db.commit()
    db.refresh(db_odp)
    
    return db_odp


@router.delete("/{odp_id}")
def delete_odp(odp_id: int, db: Session = Depends(get_db)):
    """Delete ODP"""
    db_odp = db.query(ODPModel).filter(ODPModel.id == odp_id).first()
    if not db_odp:
        raise HTTPException(status_code=404, detail="ODP not found")
    
    db.delete(db_odp)
    db.commit()
    
    return {"message": "ODP deleted successfully"}
