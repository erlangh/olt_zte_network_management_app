from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class OLT(Base):
    __tablename__ = "olts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=False)  # Support IPv6
    description = Column(Text)
    
    # SNMP Configuration
    snmp_community = Column(String(100), default="public")
    snmp_version = Column(String(10), default="2c")  # 1, 2c, 3
    snmp_port = Column(Integer, default=161)
    
    # Telnet/SSH Configuration
    telnet_enabled = Column(Boolean, default=True)
    telnet_port = Column(Integer, default=23)
    telnet_username = Column(String(50))
    telnet_password = Column(String(255))  # Should be encrypted
    
    # Status
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True))
    status = Column(String(20), default="unknown")  # online, offline, unknown
    
    # Device Info (from SNMP)
    vendor = Column(String(50), default="ZTE")
    model = Column(String(50), default="C320")
    firmware_version = Column(String(50))
    serial_number = Column(String(100))
    uptime = Column(Integer)  # in seconds
    
    # Metadata
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    slots = relationship("Slot", back_populates="olt", cascade="all, delete-orphan")
    onus = relationship("ONU", back_populates="olt")


class Slot(Base):
    __tablename__ = "slots"
    
    id = Column(Integer, primary_key=True, index=True)
    olt_id = Column(Integer, ForeignKey("olts.id", ondelete="CASCADE"), nullable=False)
    slot_number = Column(Integer, nullable=False)
    card_type = Column(String(50))  # GPON, EPON, etc
    status = Column(String(20), default="unknown")  # online, offline, empty
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    olt = relationship("OLT", back_populates="slots")
    ports = relationship("Port", back_populates="slot", cascade="all, delete-orphan")


class Port(Base):
    __tablename__ = "ports"
    
    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id", ondelete="CASCADE"), nullable=False)
    port_number = Column(Integer, nullable=False)
    status = Column(String(20), default="unknown")  # up, down, disabled
    description = Column(Text)
    
    # Port Statistics
    total_onus = Column(Integer, default=0)
    online_onus = Column(Integer, default=0)
    offline_onus = Column(Integer, default=0)
    
    # Optical Power
    rx_power = Column(Float)  # in dBm
    tx_power = Column(Float)  # in dBm
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    slot = relationship("Slot", back_populates="ports")
    onus = relationship("ONU", back_populates="port")
    odps = relationship("ODP", back_populates="port")
