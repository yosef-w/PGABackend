from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    levels = relationship("Level", back_populates="garage")

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    garage = relationship("Garage", back_populates="levels")
    zones = relationship("Zone", back_populates="level")

class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"))
    level = relationship("Level", back_populates="zones")
    bays = relationship("Bay", back_populates="zone")

class Bay(Base):
    __tablename__ = "bays"
    id = Column(Integer, primary_key=True, index=True)
    bay_number = Column(String, index=True)
    status = Column(String, index=True)
    reservation_status = Column(String, nullable=True)
    overstayer_status = Column(String, nullable=True)
    license_plate = Column(String, nullable=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    zone = relationship("Zone", back_populates="bays")

class ParkingTransaction(Base):
    __tablename__ = "parking_transactions"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, index=True)
    spot_id = Column(String)
    garage_id = Column(Integer)
    level_id = Column(Integer)
    zone_id = Column(Integer)
    timestamp_entry = Column(DateTime, default=datetime.utcnow)
    timestamp_exit = Column(DateTime, nullable=True)
    photo_base64 = Column(Text, nullable=True)
