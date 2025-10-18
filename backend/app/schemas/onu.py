from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ONUBase(BaseModel):
    sn: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    service_plan: Optional[str] = None
    description: Optional[str] = None


class ONUCreate(ONUBase):
    olt_id: int
    port_id: int
    odp_id: Optional[int] = None
    vlan: Optional[int] = None


class ONUUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    service_plan: Optional[str] = None
    odp_id: Optional[int] = None
    vlan: Optional[int] = None
    description: Optional[str] = None


class ONU(ONUBase):
    id: int
    olt_id: int
    port_id: int
    odp_id: Optional[int] = None
    mac_address: Optional[str] = None
    onu_id: Optional[int] = None
    status: str
    auth_status: str
    rx_power: Optional[float] = None
    tx_power: Optional[float] = None
    olt_rx_power: Optional[float] = None
    distance: Optional[int] = None
    temperature: Optional[float] = None
    voltage: Optional[float] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    vlan: Optional[int] = None
    uptime: Optional[int] = None
    last_online: Optional[datetime] = None
    last_offline: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
