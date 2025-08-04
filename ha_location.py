# ha_location.py
# Function to read Home Assistant location info from .storage/core.config

import json

def read_ha_location_from_storage(path="/config/.storage/core.config"):
    """
    Load HA location from /config/.storage/core.config

    Returns:
        dict with latitude, longitude, elevation, time_zone, correction_minutes, offset_hours
        or None on failure
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or "data" not in data:
                return None

            location = data["data"]
            lat = location.get("latitude")
            lon = location.get("longitude")
            elev = location.get("elevation")
            tz = location.get("time_zone")

            if lat is None or lon is None:
                return None

            correction_minutes = (lon - 15) * 4
            offset_hours = correction_minutes / 60

            return {
                "latitude": lat,
                "longitude": lon,
                "elevation": elev,
                "time_zone": tz,
                "correction_minutes": correction_minutes,
                "offset_hours": offset_hours
            }

    except Exception as e:
        print(f"Error reading location: {e}")
        return None

