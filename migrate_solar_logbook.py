#!/usr/bin/env python3
# ---------------------------------------------
# migrate_solar_logbook.py
# Version       : 1.1.0
# Last updated  : 2025-08-31
# Author        : KlausiPapa & ChatGPT
# Description   : Migration script to update solar_log_v2 table columns
# ---------------------------------------------

import sqlite3
import configparser
from pathlib import Path
import sys

# ---------------------------------------------
# Load config
# ---------------------------------------------
conf_path = "/config/shell/solar_logbook.conf"
config = configparser.ConfigParser()
if not Path(conf_path).exists():
    print(f"❌ Config file not found: {conf_path}")
    sys.exit(1)

config.read(conf_path)
db_path = config["paths"]["logbook_db_path"]

# Collect expected columns from config
sensor_columns = list(config["ha_sensors"].keys())

# Collect fixed system columns
system_columns = [
    "modules1", "azimuth1", "tilt1",
    "modules2", "azimuth2", "tilt2",
    "batteries", "battery_cap"
]

expected_columns = ["timestamp"] + sensor_columns + system_columns

# ---------------------------------------------
# Connect DB
# ---------------------------------------------
if not Path(db_path).exists():
    print(f"❌ Database not found: {db_path}")
    sys.exit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()

# Ensure table exists with at least timestamp
cur.execute("CREATE TABLE IF NOT EXISTS solar_log_v2 (timestamp TEXT PRIMARY KEY)")
con.commit()

# Get existing columns
cur.execute("PRAGMA table_info(solar_log_v2)")
existing_cols = [row[1] for row in cur.fetchall()]

# Add missing columns
added = []
for col in expected_columns:
    if col not in existing_cols:
        cur.execute(f"ALTER TABLE solar_log_v2 ADD COLUMN {col} REAL")
        added.append(col)

con.commit()
con.close()

if added:
    print(f"✅ Added new columns: {', '.join(added)}")
else:
    print("ℹ️ No new columns needed. Table already up to date.")

