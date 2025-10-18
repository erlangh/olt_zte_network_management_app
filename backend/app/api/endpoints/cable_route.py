from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.cable_route import CableRoute, CableRouteCreate
from app.models.cable_route import CableRoute as CableRouteModel

router = APIRouter()


@router.get("/", response_model=List[CableRoute])
def get_cable_routes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all cable routes"""
    routes = db.query(CableRouteModel).offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=CableRoute)
def get_cable_route(route_id: int, db: Session = Depends(get_db)):
    """Get cable route by ID"""
    route = db.query(CableRouteModel).filter(CableRouteModel.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Cable route not found")
    return route


@router.post("/", response_model=CableRoute)
def create_cable_route(route: CableRouteCreate, db: Session = Depends(get_db)):
    """Create new cable route"""
    db_route = CableRouteModel(**route.dict())
    
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    
    return db_route


@router.delete("/{route_id}")
def delete_cable_route(route_id: int, db: Session = Depends(get_db)):
    """Delete cable route"""
    db_route = db.query(CableRouteModel).filter(CableRouteModel.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Cable route not found")
    
    db.delete(db_route)
    db.commit()
    
    return {"message": "Cable route deleted successfully"}
