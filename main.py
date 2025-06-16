from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import RootModel
from database import Base, engine, SessionLocal
import crud
from schemas import GarageOut, ParkingTransactionOut
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use RootModel for dynamic JSON bodies
class OccupancyPayload(RootModel[dict]):
    pass

class LicensePlatePayload(RootModel[dict]):
    pass

@app.post("/api/indect/occupancy")
async def receive_occupancy(payload: OccupancyPayload, db: Session = Depends(get_db)):
    crud.update_occupancy(db, payload.root)
    return {"status": "occupancy processed"}

@app.post("/api/indect/license-plate")
async def receive_license_plate(payload: LicensePlatePayload, db: Session = Depends(get_db)):
    crud.save_license_plate(db, payload.root)
    return {"status": "license plate processed"}

@app.get("/api/availability", response_model=List[GarageOut])
def get_availability(db: Session = Depends(get_db)):
    return crud.get_availability(db)

@app.get("/api/find-car/{plate}", response_model=ParkingTransactionOut)
def find_car(plate: str, db: Session = Depends(get_db)):
    tx = crud.find_car(db, plate)
    if tx:
        return tx
    return {"status": "car not found"}
