from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ODPBase(BaseModel):
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    total_ports: int = 8
    splitter_ratio: str = "1:8"
    description: Optional[str] = None
    notes: Optional[str] = None


class ODPCreate(ODPBase):
    port_id: Optional[int] = None


class ODPUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    port_id: Optional[int] = None
    total_ports: Optional[int] = None
    splitter_ratio: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class ODP(ODPBase):
    id: int
    port_id: Optional[int] = None
    used_ports: int
    available_ports: int
    status: str
    installation_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
