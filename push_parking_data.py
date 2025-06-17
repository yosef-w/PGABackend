import requests
import random

# Your Render URL
BASE_URL = "https://pgabackend-udmn.onrender.com/api/indect/occupancy"

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

def push_data(garage_payload):
    response = requests.post(BASE_URL, json=garage_payload)
    if response.ok:
        print(f"✅ Successfully pushed data for {garage_payload['Name']}")
    else:
        print(f"❌ Failed to push data for {garage_payload['Name']}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Define garages
    garage_names = ["Garage A", "Garage B", "Garage C", "Garage D"]

    for name in garage_names:
        garage_data = generate_garage(name)
        push_data(garage_data)
