from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OLTBase(BaseModel):
    name: str
    ip_address: str
    description: Optional[str] = None
    snmp_community: str = "public"
    snmp_version: str = "2c"
    snmp_port: int = 161
    telnet_enabled: bool = True
    telnet_port: int = 23
    telnet_username: Optional[str] = None
    telnet_password: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class OLTCreate(OLTBase):
    pass


class OLTUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    description: Optional[str] = None
    snmp_community: Optional[str] = None
    telnet_username: Optional[str] = None
    telnet_password: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class OLT(OLTBase):
    id: int
    is_active: bool
    status: str
    last_seen: Optional[datetime] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    serial_number: Optional[str] = None
    uptime: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OLTStatus(BaseModel):
    olt_id: int
    status: str
    is_reachable: bool
    response_time: Optional[float] = None
    uptime: Optional[int] = None
    total_onus: int = 0
    online_onus: int = 0
    offline_onus: int = 0
