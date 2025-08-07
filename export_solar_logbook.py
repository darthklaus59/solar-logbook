#!/usr/bin/env python3
# ---------------------------------------------
# export_solar_logbook.py
# Version       : 1.4.4
# Last updated  : 2025-08-07
# Author        : KlausiPapa & ChatGPT
# Description   : Solar data export from Home Assistant with optional DB insert
# ---------------------------------------------

import sqlite3
import csv
import os
import argparse
from datetime import timezone, datetime, timedelta
import pytz
from ha_location import read_ha_location_from_storage
from configparser import ConfigParser

# ---------------------------------------------
# Load config values
# ---------------------------------------------
config = ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solar_logbook.conf")
if not config.read(config_path):
    raise FileNotFoundError(f"❌ Config file not found: {config_path}")

def get_optional_int(section, key):
    val = config.get(section, key, fallback=None)
    return int(val) if val else None

def get_optional_float(section, key):
    val = config.get(section, key, fallback=None)
    return float(val) if val else None

default_delta_hours = config.getint("time", "delta_hours", fallback=7)

# ---------------------------------------------
# Argument parser
# ---------------------------------------------
parser = argparse.ArgumentParser(
    description="Export solar data for a given day from Home Assistant DB into CSV and optionally into a local logbook DB."
)
parser.add_argument('--day', help="Target date in format YYYY-MM-DD. Default is today.", default=datetime.now().date().isoformat())
parser.add_argument('--insert-db', action='store_true', help="Insert result into local SQLite database 'solar_log_v2'.")
parser.add_argument('--overwrite', action='store_true', help="Overwrite existing rows with the same timestamp in the DB.")
parser.add_argument('--verbose', action='store_true', help="Enable verbose debug output.")
parser.add_argument('--test', action='store_true', help="Only show last timestamp in DB for the selected day.")

# System config overrides
parser.add_argument('--modules1', type=int, default=None, help="Wp of modules (string 1).")
parser.add_argument('--azimuth1', type=int, default=None, help="Azimuth angle (deg) of modules string 1.")
parser.add_argument('--tilt1', type=int, default=None, help="Tilt angle (deg) of modules string 1.")
parser.add_argument('--modules2', type=int, default=None, help="Wp of modules (string 2).")
parser.add_argument('--azimuth2', type=int, default=None, help="Azimuth angle (deg) of modules string 2.")
parser.add_argument('--tilt2', type=int, default=None, help="Tilt angle (deg) of modules string 2.")
parser.add_argument('--batteries', type=int, default=None, help="Number of batteries.")
parser.add_argument('--battery_cap', type=float, default=None, help="Total battery capacity in kWh.")

parser.add_argument(
    '--delta-hours',
    type=int,
    default=None,
    help=f"Half-width of window around high noon in hours (default from conf: {default_delta_hours})"
)
parser.add_argument('--solar-offset', nargs='?', const="", help=(
    "Solar correction in hours. If omitted, offset = 0. "
    "If passed without value, the value from Home Assistant location will be used. "
    "If passed with value, that will be used."
))

args = parser.parse_args()

# ---------------------------------------------
# Fill missing args with conf values
# ---------------------------------------------
args.modules1 = args.modules1 if args.modules1 is not None else get_optional_int("system", "modules1")
args.azimuth1 = args.azimuth1 if args.azimuth1 is not None else get_optional_int("system", "azimuth1")
args.tilt1 = args.tilt1 if args.tilt1 is not None else get_optional_int("system", "tilt1")
args.modules2 = args.modules2 if args.modules2 is not None else get_optional_int("system", "modules2")
args.azimuth2 = args.azimuth2 if args.azimuth2 is not None else get_optional_int("system", "azimuth2")
args.tilt2 = args.tilt2 if args.tilt2 is not None else get_optional_int("system", "tilt2")
args.batteries = args.batteries if args.batteries is not None else get_optional_int("system", "batteries")
args.battery_cap = args.battery_cap if args.battery_cap is not None else get_optional_float("system", "battery_cap")
args.delta_hours = args.delta_hours if args.delta_hours is not None else default_delta_hours

# ---------------------------------------------
# Paths
# ---------------------------------------------
DB_PATH = config["paths"]["ha_db_path"]
LOGBOOK_DB_PATH = config["paths"]["logbook_db_path"]
OUTPUT_CSV = os.path.join(config["paths"]["output_dir"], f"solar_log_{args.day}.csv")

# ---------------------------------------------
# Time range: High Noon local ± delta-hours
# ---------------------------------------------
location = read_ha_location_from_storage()
if location:
    print("🔎 Location info:")
    print("  Timezone        :", location['time_zone'])
    print("  Solar offset    :", location['offset_hours'], "hours")

# Base offset
day_dt = datetime.strptime(args.day, "%Y-%m-%d")
ntz_date = datetime(day_dt.year, 1, 1, 12, 0)
local_tz = pytz.timezone(location['time_zone'])
base_offset = local_tz.utcoffset(ntz_date).total_seconds() / 3600
NTZ = timezone(timedelta(hours=base_offset))

# Solar offset calculation
if args.solar_offset is None:
    solar_offset = 0
elif args.solar_offset == "":
    solar_offset = float(location['offset_hours'])
else:
    try:
        solar_offset = float(args.solar_offset)
    except ValueError:
        print("⚠️ Invalid --solar-offset, fallback to 0")
        solar_offset = 0

# Compute high noon in UTC
local_noon = datetime(day_dt.year, day_dt.month, day_dt.day, 12, 0, tzinfo=NTZ)
corrected_local_noon = local_noon - timedelta(hours=solar_offset)
high_noon_utc = corrected_local_noon.astimezone(pytz.utc)

start_utc = (high_noon_utc - timedelta(hours=args.delta_hours)).timestamp()
end_utc = (high_noon_utc + timedelta(hours=args.delta_hours)).timestamp()

if args.verbose:
    print("delta", args.delta_hours, "NTZ", NTZ, "local_tz", local_tz, "pytz.utc", pytz.utc)
    print("high_noon_utc", high_noon_utc)
    print("start_utc", start_utc, "end_utc", end_utc)

# ---------------------------------------------
# Test mode: show last entry in DB
# ---------------------------------------------
if args.test:
    print(f"🔎 Test mode for UTC window: {datetime.fromtimestamp(start_utc)} → {datetime.fromtimestamp(end_utc)}")
    conn = sqlite3.connect(LOGBOOK_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(timestamp) FROM solar_log_v2
        WHERE timestamp BETWEEN ? AND ?
    """, (datetime.utcfromtimestamp(start_utc).strftime("%Y-%m-%d %H:%M"),
          datetime.utcfromtimestamp(end_utc).strftime("%Y-%m-%d %H:%M")))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
        print(f"✅ Last entry on {args.day}: {result[0]}")
    else:
        print("⚠️ No entry found for selected day")
    exit(0)

# ---------------------------------------------
# Entity definitions
# ---------------------------------------------
ENTITY_IDS = [
    "sensor.esp8266_relay04_bh1750_illuminance",
    "sensor.solaxmini_inverter_power",
    "sensor.solax_ac_power",
    "sensor.hybrid_inverter_power",
    "sensor.power_load",
    "sensor.battery_load"
]

# ---------------------------------------------
# Read from Home Assistant database
# ---------------------------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

entity_id_map = {}
for eid in ENTITY_IDS:
    cursor.execute("SELECT metadata_id FROM states_meta WHERE entity_id = ?", (eid,))
    result = cursor.fetchone()
    if result:
        entity_id_map[result[0]] = eid

metadata_ids = tuple(entity_id_map.keys())
query = f"""
SELECT metadata_id, state, last_updated_ts
FROM states
WHERE metadata_id IN ({','.join(['?'] * len(metadata_ids))})
  AND last_updated_ts BETWEEN ? AND ?
"""
cursor.execute(query, (*metadata_ids, start_utc, end_utc))
data = cursor.fetchall()
conn.close()

# ---------------------------------------------
# Aggregate by minute
# ---------------------------------------------
temp_data = {}
for meta_id, state, ts in data:
    try:
        val = float(state)
    except (ValueError, TypeError):
        continue
    dt = datetime.fromtimestamp(ts, tz=timezone.utc).replace(second=0, microsecond=0)
    minute = dt.strftime("%Y-%m-%d %H:%M")
    entity = entity_id_map.get(meta_id)
    if not entity:
        continue
    if minute not in temp_data:
        temp_data[minute] = {}
    temp_data[minute][entity] = val

# ---------------------------------------------
# Build rows
# ---------------------------------------------
rows = []
for minute in sorted(temp_data.keys()):
    entry = temp_data[minute]
    lux = entry.get("sensor.esp8266_relay04_bh1750_illuminance")
    power1 = entry.get("sensor.solaxmini_inverter_power") or entry.get("sensor.solax_ac_power")
    power2 = entry.get("sensor.hybrid_inverter_power")
    power_load = entry.get("sensor.power_load")
    battery_load = entry.get("sensor.battery_load")
    rows.append([
        minute, lux, power1, power2,
        args.modules1, args.azimuth1, args.tilt1,
        args.modules2, args.azimuth2, args.tilt2,
        args.batteries, args.battery_cap,
        power_load, battery_load
    ])

# ---------------------------------------------
# Write CSV
# ---------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
with open(OUTPUT_CSV, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "timestamp", "lux", "power1", "power2",
        "modules1", "azimuth1", "tilt1",
        "modules2", "azimuth2", "tilt2",
        "batteries", "battery_cap",
        "power_load", "battery_load"
    ])
    writer.writerows(rows)

# ---------------------------------------------
# Optional insert into logbook DB
# ---------------------------------------------
if args.insert_db:
    conn = sqlite3.connect(LOGBOOK_DB_PATH)
    cursor = conn.cursor()
    last_timestamp = None
    if not args.overwrite:
        try:
            cursor.execute("SELECT MAX(timestamp) FROM solar_log_v2")
            result = cursor.fetchone()
            if result and result[0]:
                last_timestamp = result[0]
                print(f"ℹ️ Last DB timestamp: {last_timestamp}")
        except sqlite3.Error as e:
            print(f"❌ SQLite error while checking last timestamp: {e}")

    insert_count = 0
    skip_count = 0

    for row in rows:
        timestamp = row[0]
        if last_timestamp and timestamp <= last_timestamp:
            skip_count += 1
            continue
        if args.overwrite:
            cursor.execute("DELETE FROM solar_log_v2 WHERE timestamp = ?", (timestamp,))
        cursor.execute(f"""
        INSERT INTO solar_log_v2 (
            timestamp, lux, power1, power2,
            modules1, azimuth1, tilt1,
            modules2, azimuth2, tilt2,
            batteries, battery_cap,
            power_load, battery_load
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
        insert_count += 1

    conn.commit()
    conn.close()

    print(f"✅ Data inserted into solar_log_v2: {insert_count} new row(s), {skip_count} skipped.")

print(f"✅ Export complete: {len(rows)} rows to {OUTPUT_CSV}")

