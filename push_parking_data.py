import os
import random
from typing import Dict

import requests

BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://pgabackend-udmn.onrender.com/api/indect/occupancy",
)

session = requests.Session()

def generate_bays(num_bays=10):
    bays = {}
    for i in range(1, num_bays + 1):
        status = random.choice(["available", "occupied"])
        bays[str(i)] = f"{i};{status}"
    return bays

def generate_zone(name_prefix, zone_num):
    return {
        "Name": f"{name_prefix}{zone_num}",
        "Bays": generate_bays(),
        "Zones": []  # Add nested sub-zones if you'd like
    }

def generate_level(level_num):
    return {
        "Name": f"Level {level_num}",
        "Zones": [generate_zone(f"Zone L{level_num}-", i+1) for i in range(2)]  # 2 zones per level
    }

def generate_garage(garage_name):
    return {
        "Name": garage_name,
        "Zones": [generate_level(i+1) for i in range(2)]  # 2 levels per garage
    }

def push_data(garage_payload: Dict[str, object]) -> None:
    """Send a single garage payload to the API with error handling."""

    try:
        response = session.post(BASE_URL, json=garage_payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f"❌ Error pushing data for {garage_payload['Name']}: {exc}")
        return

    print(f"✅ Successfully pushed data for {garage_payload['Name']}")

if __name__ == "__main__":
    # Define garages
    garage_names = ["Garage A", "Garage B", "Garage C", "Garage D"]

    for name in garage_names:
        garage_data = generate_garage(name)
        push_data(garage_data)
