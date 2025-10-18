from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.db.database import Base


class CableRoute(Base):
    __tablename__ = "cable_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Source and Destination
    source_type = Column(String(20), nullable=False)  # olt, odp, onu
    source_id = Column(Integer, nullable=False)
    destination_type = Column(String(20), nullable=False)  # odp, onu
    destination_id = Column(Integer, nullable=False)
    
    # Cable Info
    cable_type = Column(String(50))  # Single Mode, Multi Mode
    fiber_count = Column(Integer)  # Number of fibers in cable
    cable_length = Column(Float)  # Length in meters
    
    # Route Path (for visualization)
    # Stores array of coordinates [{lat, lng}, ...]
    route_coordinates = Column(JSON)
    
    # Status
    status = Column(String(20), default="active")  # active, inactive, damaged
    
    # Additional Info
    installation_date = Column(DateTime(timezone=True))
    description = Column(Text)
    notes = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
