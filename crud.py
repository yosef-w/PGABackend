from sqlalchemy.orm import Session
import models
from datetime import datetime

def update_occupancy(db: Session, data: dict):
    garage_name = data.get("Name")
    garage = db.query(models.Garage).filter_by(name=garage_name).first()
    if not garage:
        garage = models.Garage(name=garage_name)
        db.add(garage)
        db.commit()

    for level_data in data.get("Zones", []):
        level_name = level_data.get("Name")
        level = db.query(models.Level).filter_by(name=level_name, garage_id=garage.id).first()
        if not level:
            level = models.Level(name=level_name, garage=garage)
            db.add(level)
            db.commit()

        for zone_data in level_data.get("Zones", []):
            process_zone(db, zone_data, level)

def process_zone(db: Session, zone_data: dict, level):
    zone_name = zone_data.get("Name")
    zone = db.query(models.Zone).filter_by(name=zone_name, level_id=level.id).first()
    if not zone:
        zone = models.Zone(name=zone_name, level=level)
        db.add(zone)
        db.commit()

    for bay_id, bay_str in zone_data.get("Bays", {}).items():
        parts = bay_str.split(";")
        bay_number, status = parts[0], parts[1]
        bay = db.query(models.Bay).filter_by(bay_number=bay_number, zone_id=zone.id).first()
        if not bay:
            bay = models.Bay(bay_number=bay_number, status=status, zone=zone)
            db.add(bay)
        else:
            bay.status = status
    db.commit()

    for subzone_data in zone_data.get("Zones", []):
        process_zone(db, subzone_data, level)

def save_license_plate(db: Session, data: dict):
    tx = models.ParkingTransaction(
        license_plate=data.get("numberPlate"),
        spot_id=data.get("spotId"),
        garage_id=data.get("garageId"),
        level_id=None,
        zone_id=None,
        timestamp_entry=datetime.utcnow(),
        photo_base64=data.get("carPhotoData")
    )
    db.add(tx)
    db.commit()

def get_availability(db: Session):
    garages = db.query(models.Garage).all()
    result = []

    for garage in garages:
        garage_dict = {
            "id": garage.id,
            "name": garage.name,
            "available_spots": 0,
            "levels": []
        }

        for level in garage.levels:
            level_dict = {
                "id": level.id,
                "name": level.name,
                "available_spots": 0,
                "zones": []
            }

            for zone in level.zones:
                zone_dict = {
                    "id": zone.id,
                    "name": zone.name,
                    "bays": []
                }

                for bay in zone.bays:
                    bay_info = {
                        "id": bay.id,
                        "bay_number": bay.bay_number,
                        "status": bay.status,
                        "reservation_status": bay.reservation_status,
                        "overstayer_status": bay.overstayer_status,
                        "license_plate": bay.license_plate
                    }

                    if bay.status == "available":
                        level_dict["available_spots"] += 1

                    zone_dict["bays"].append(bay_info)

                level_dict["zones"].append(zone_dict)

            garage_dict["levels"].append(level_dict)
            garage_dict["available_spots"] += level_dict["available_spots"]

        result.append(garage_dict)

    return result

def find_car(db: Session, plate: str):
    return db.query(models.ParkingTransaction).filter_by(license_plate=plate, timestamp_exit=None).first()
