from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import RootModel
from database import Base, engine, SessionLocal
import crud
import models  # ✅ Needed for direct DB queries in dashboard
from schemas import GarageOut, ParkingTransactionOut
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "This is the backend for PGA!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    # Fetch ORM objects directly (not Pydantic response models)
    garages = db.query(models.Garage).all()

    data = []
    for g in garages:
        level_data = []
        for level in g.levels:
            total_bays = sum(len(zone.bays) for zone in level.zones)
            available_bays = sum(
                sum(1 for bay in zone.bays if bay.status == "available")
                for zone in level.zones
            )
            level_data.append({
                "level_name": level.name,
                "total_bays": total_bays,
                "available_bays": available_bays
            })
        data.append({
            "garage_name": g.name,
            "levels": level_data
        })

    return templates.TemplateResponse("dashboard.html.j2", {
        "request": request,
        "data": data
    })
