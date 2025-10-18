from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class CableRouteBase(BaseModel):
    source_type: str  # olt, odp, onu
    source_id: int
    destination_type: str  # odp, onu
    destination_id: int
    cable_type: Optional[str] = None
    fiber_count: Optional[int] = None
    cable_length: Optional[float] = None
    route_coordinates: Optional[List[Dict]] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class CableRouteCreate(CableRouteBase):
    pass


class CableRoute(CableRouteBase):
    id: int
    status: str
    installation_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
