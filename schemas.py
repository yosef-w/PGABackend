from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BayBase(BaseModel):
    bay_number: str
    status: str
    reservation_status: Optional[str] = None
    overstayer_status: Optional[str] = None
    license_plate: Optional[str] = None

class BayOut(BayBase):
    id: int
    class Config:
        from_attributes = True

class ZoneOut(BaseModel):
    id: int
    name: str
    bays: List[BayOut]
    class Config:
        from_attributes = True

class LevelOut(BaseModel):
    id: int
    name: str
    zones: List[ZoneOut]
    class Config:
        from_attributes = True

class GarageOut(BaseModel):
    id: int
    name: str
    levels: List[LevelOut]
    class Config:
        from_attributes = True

class ParkingTransactionOut(BaseModel):
    id: int
    license_plate: str
    spot_id: str
    garage_id: int
    level_id: Optional[int]
    zone_id: Optional[int]
    timestamp_entry: datetime
    timestamp_exit: Optional[datetime]
    photo_base64: Optional[str]
    class Config:
        from_attributes = True
