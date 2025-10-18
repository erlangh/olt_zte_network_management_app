from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class ODP(Base):
    __tablename__ = "odps"
    
    id = Column(Integer, primary_key=True, index=True)
    port_id = Column(Integer, ForeignKey("ports.id", ondelete="SET NULL"))
    
    # ODP Identification
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True)  # ODP Code/ID
    
    # Location
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Capacity
    total_ports = Column(Integer, default=8)  # Total splitter ports
    used_ports = Column(Integer, default=0)
    available_ports = Column(Integer, default=8)
    
    # Splitter Info
    splitter_ratio = Column(String(10), default="1:8")  # 1:8, 1:16, 1:32, etc
    
    # Status
    status = Column(String(20), default="active")  # active, inactive, maintenance
    
    # Additional Info
    installation_date = Column(DateTime(timezone=True))
    description = Column(Text)
    notes = Column(Text)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    port = relationship("Port", back_populates="odps")
    onus = relationship("ONU", back_populates="odp")
