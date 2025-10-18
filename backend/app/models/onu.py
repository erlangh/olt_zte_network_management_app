from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class ONU(Base):
    __tablename__ = "onus"
    
    id = Column(Integer, primary_key=True, index=True)
    olt_id = Column(Integer, ForeignKey("olts.id", ondelete="CASCADE"), nullable=False)
    port_id = Column(Integer, ForeignKey("ports.id", ondelete="CASCADE"), nullable=False)
    odp_id = Column(Integer, ForeignKey("odps.id", ondelete="SET NULL"))
    
    # ONU Identification
    sn = Column(String(50), unique=True, index=True, nullable=False)  # Serial Number
    mac_address = Column(String(17))
    onu_id = Column(Integer)  # ONU ID on the port
    
    # Customer Info
    customer_name = Column(String(100))
    customer_phone = Column(String(20))
    customer_address = Column(Text)
    service_plan = Column(String(100))
    
    # Status
    status = Column(String(20), default="offline")  # online, offline, los, dying-gasp
    auth_status = Column(String(20), default="unauthorized")  # authorized, unauthorized
    
    # Signal Quality
    rx_power = Column(Float)  # OLT RX power (from ONU) in dBm
    tx_power = Column(Float)  # ONU TX power in dBm
    olt_rx_power = Column(Float)  # ONU RX power (from OLT) in dBm
    distance = Column(Integer)  # Distance in meters
    temperature = Column(Float)  # ONU temperature
    voltage = Column(Float)  # ONU voltage
    
    # Device Info
    vendor = Column(String(50))
    model = Column(String(50))
    firmware_version = Column(String(50))
    hardware_version = Column(String(50))
    
    # Configuration
    vlan = Column(Integer)
    bandwidth_profile = Column(String(50))
    description = Column(Text)
    
    # Network Statistics
    uptime = Column(Integer)  # in seconds
    last_online = Column(DateTime(timezone=True))
    last_offline = Column(DateTime(timezone=True))
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    olt = relationship("OLT", back_populates="onus")
    port = relationship("Port", back_populates="onus")
    odp = relationship("ODP", back_populates="onus")
