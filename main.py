from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
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
api_router = APIRouter(prefix="/api")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html.j2", {
        "request": request,
        "base_url": "https://pgabackend-udmn.onrender.com"
    })

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


@api_router.post("/indect/occupancy")
async def receive_occupancy(
    payload: OccupancyPayload, db: Session = Depends(get_db)
):
    try:
        crud.update_occupancy(db, payload.root)
    except Exception as exc:  # pragma: no cover - simple safety
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "occupancy processed"}


@api_router.post("/indect/license-plate")
async def receive_license_plate(
    payload: LicensePlatePayload, db: Session = Depends(get_db)
):
    try:
        crud.save_license_plate(db, payload.root)
    except Exception as exc:  # pragma: no cover - simple safety
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "license plate processed"}


@api_router.get("/availability", response_model=List[GarageOut])
def get_availability(db: Session = Depends(get_db)):
    return crud.get_availability(db)


@api_router.get("/find-car/{plate}", response_model=ParkingTransactionOut)
def find_car(plate: str, db: Session = Depends(get_db)):
    tx = crud.find_car(db, plate)
    if not tx:
        raise HTTPException(status_code=404, detail="car not found")
    return tx

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    garages = db.query(models.Garage).all()

    data = []
    for g in garages:
        garage_total_bays = 0
        garage_available_bays = 0
        level_data = []

        for level in g.levels:
            level_total_bays = 0
            level_available_bays = 0
            zone_data = []

            for zone in level.zones:
                zone_total_bays = len(zone.bays)
                zone_available_bays = sum(1 for bay in zone.bays if bay.status == "available")

                level_total_bays += zone_total_bays
                level_available_bays += zone_available_bays

                zone_data.append({
                    "zone_name": zone.name,
                    "total_bays": zone_total_bays,
                    "available_bays": zone_available_bays,
                    "percent_available": (zone_available_bays / zone_total_bays * 100) if zone_total_bays else 0
                })

            garage_total_bays += level_total_bays
            garage_available_bays += level_available_bays

            level_data.append({
                "level_name": level.name,
                "total_bays": level_total_bays,
                "available_bays": level_available_bays,
                "percent_available": (level_available_bays / level_total_bays * 100) if level_total_bays else 0,
                "zones": zone_data
            })

        data.append({
            "garage_name": g.name,
            "total_bays": garage_total_bays,
            "available_bays": garage_available_bays,
            "percent_available": (garage_available_bays / garage_total_bays * 100) if garage_total_bays else 0,
            "levels": level_data
        })

    return templates.TemplateResponse("dashboard.html.j2", {
        "request": request,
        "data": data
    })


app.include_router(api_router)
