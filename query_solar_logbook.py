#!/usr/bin/env python3
# ---------------------------------------------
# query_solar_logbook.py
# Version      : 1.5.4
# Last updated : 2025-08-07
# Description  : Query solar_log_v2 sorted by timestamp
#                and optionally interpolate and compute watt/klux
# ---------------------------------------------

import sqlite3
import argparse
from tabulate import tabulate
import os
import csv
from datetime import datetime, timedelta
import configparser
from interpolation_utils import interpolate_timeseries, add_watt_per_klux

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "solar_logbook.conf"))

# ---------------------------------------------
# Argument parser
# ---------------------------------------------
parser = argparse.ArgumentParser(description="Query or clean the solar_log_v2 table.")
parser.add_argument(
    '--db-path',
    default=config.get("paths", "logbook_db_path", fallback="/config/solar_logbook.db"),
    help='Path to the SQLite database'
)
parser.add_argument('--limit', type=int, default=10, help='Limit number of rows to display')
parser.add_argument('--remove-duplicates', action='store_true', help='Remove duplicate entries by timestamp')
parser.add_argument('--format', action='store_true', help='Pretty-print the result in table format')
parser.add_argument('--day', help='Show only rows for a specific date (YYYY-MM-DD)')
parser.add_argument('--to-day', help='End date (inclusive) in format YYYY-MM-DD')
parser.add_argument('--from-day', help='Start date (inclusive) in format YYYY-MM-DD')
parser.add_argument('--time', nargs='+', help='Time of day filter: HH:MM [duration_hours]')
parser.add_argument('--auto-limit', action='store_true', help='Automatically set limit based on time range')
parser.add_argument('--filter-nonzero', action='store_true', help='Only show rows with power1 or power2 > 0')
parser.add_argument('--export', help='Export results to a CSV file')
parser.add_argument('--interpolate', action='store_true', help='Interpolate missing numeric values')
args = parser.parse_args()

# ---------------------------------------------
# Connect to SQLite database
# ---------------------------------------------
if not os.path.exists(args.db_path):
    print(f"❌ Database not found at {args.db_path}")
    exit(1)

conn = sqlite3.connect(args.db_path)
cursor = conn.cursor()

# ---------------------------------------------
# Optional: Remove duplicates by timestamp
# ---------------------------------------------
if args.remove_duplicates:
    print("🔧 Removing duplicates based on timestamp...")
    cursor.execute("SELECT COUNT(*) FROM solar_log_v2")
    before = cursor.fetchone()[0]

    cursor.execute("""
        DELETE FROM solar_log_v2
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM solar_log_v2
            GROUP BY timestamp
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM solar_log_v2")
    after = cursor.fetchone()[0]
    deleted = before - after
    print(f"✅ Removed {deleted} duplicate rows.")

# ---------------------------------------------
# Optional time-of-day filter (in SQL)
# ---------------------------------------------
time_clause = ""
if args.time:
    try:
        start_time = datetime.strptime(args.time[0], "%H:%M").time()
        duration_hours = int(args.time[1]) if len(args.time) > 1 else 1
        start_str = start_time.strftime("%H:%M:%S")
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=duration_hours)).time()
        end_str = end_time.strftime("%H:%M:%S")
        time_clause = f"AND TIME(timestamp) BETWEEN '{start_str}' AND '{end_str}'"
    except ValueError:
        print("❌ Invalid --time format. Use --time HH:MM [duration_hours]")
        exit(1)

# ---------------------------------------------
# Auto-limit based on --time and date range
# ---------------------------------------------
if args.auto_limit and args.time:
    duration_hours = int(args.time[1]) if len(args.time) > 1 else 1
    if args.from_day and args.to_day:
        start_date = datetime.strptime(args.from_day, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.to_day, "%Y-%m-%d").date()
        day_count = (end_date - start_date).days + 1
    elif args.day:
        day_count = 1
    else:
        day_count = 1  # fallback
    args.limit = duration_hours * 60 * day_count

# ---------------------------------------------
# Build WHERE clause
# ---------------------------------------------
where_clauses = []
params = []

if args.day:
    where_clauses.append("DATE(timestamp) = ?")
    params.append(args.day)

if args.to_day:
    where_clauses.append("DATE(timestamp) <= ?")
    params.append(args.to_day)

if args.from_day:
    where_clauses.append("DATE(timestamp) >= ?")
    params.append(args.from_day)

if args.filter_nonzero:
    where_clauses.append("(power1 > 0 OR power2 > 0)")

where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
if time_clause:
    where_sql += f" {time_clause}" if where_sql else f"WHERE {time_clause[4:]}"

# ---------------------------------------------
# Query data sorted by timestamp
# ---------------------------------------------
query = f"""
    SELECT timestamp, lux, power1, power2,
           modules1, azimuth1, tilt1,
           modules2, azimuth2, tilt2,
           batteries, battery_cap,
           power_load, battery_load
    FROM solar_log_v2
    {where_sql}
    ORDER BY timestamp ASC
    LIMIT ?
"""
params.append(args.limit)
cursor.execute(query, params)
rows = cursor.fetchall()

# ---------------------------------------------
# Column headers
# ---------------------------------------------
headers = ["timestamp", "lux", "power1", "power2",
           "modules1", "azimuth1", "tilt1",
           "modules2", "azimuth2", "tilt2",
           "batteries", "battery_cap",
           "power_load", "battery_load",
           "watt_per_klux"]

# ---------------------------------------------
# Output: print or export
# ---------------------------------------------
if rows:
    base_headers = headers[:-1]  # all except watt_per_klux
    records = [
        {base_headers[i]: row[i] if base_headers[i] != "timestamp" else datetime.fromisoformat(row[0])
         for i in range(len(base_headers))}
        for row in rows
    ]

    if args.interpolate:
        records = interpolate_timeseries(records)
        records = add_watt_per_klux(records)
    else:
        records = add_watt_per_klux(records)

    if args.format:
        print(tabulate([[r.get(h, "") for h in headers] for r in records], headers=headers, tablefmt="grid"))
    else:
        for r in records:
            print("\t".join(str(r.get(h, "")) for h in headers))
else:
    print("ℹ️ No data found.")

conn.close()

