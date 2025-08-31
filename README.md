# Solar Logbook Tools

Scripts to export, migrate, and query solar production and consumption data from a Home Assistant database into a local SQLite logbook. Provides CSV export, database storage, and advanced query functionality.

---

## Features

### Export Script (`export_solar_logbook.py`)
- Extracts configured sensors from Home Assistant DB.
- Aggregates data to **1-minute resolution**.
- Writes results to:
  - CSV file (`/share/data/solar_log_<date>.csv`)
  - SQLite DB (`solar_log_v2`, optional `--insert-db`)
- Handles:
  - System metadata (modules, tilt, azimuth, batteries)
  - Power & load sensors
  - Integrated energy values
- Configurable via `solar_logbook.conf`.

### Query Script (`query_solar_logbook.py`)
- Query stored data from `solar_log_v2`.
- Options:
  - Filter by date, range, or time-of-day.
  - Interpolate missing values (`--interpolate`).
  - Compute derived metrics (e.g. Watt/klux).
  - Export results to CSV.
  - Pretty table output with `--format`.
- Ensures rows are sorted by timestamp.

### Migration Script (`migrate_solar_logbook.py`)
- Updates `solar_log_v2` schema based on `solar_logbook.conf`.
- Adds missing columns for newly configured sensors.
- Ensures compatibility after config updates.

---

## Configuration (`solar_logbook.conf`)

```ini
[paths]
ha_db_path = /config/home-assistant_v2.db
logbook_db_path = /config/solar_logbook.db
output_dir = /share/data

[time]
delta_hours = 7

[logging]
log_level = INFO

[system]
modules1 = 760
azimuth1 = 190
tilt1 = 15
modules2 = 0
azimuth2 = 280
tilt2 = 60
batteries = 0
battery_cap = 2.4

[ha_sensors]
# Grid & Consumption
grid_power = sensor.smart_meter_sum_active_instantaneous_power
grid_export = sensor.smart_meter_active_power_export
grid_fossil_share = sensor.grid_fossil_fuel_percentage
total_power = sensor.sum_elec_power

# Solar Production
inverter_power_solax = sensor.solax_inverter_power
inverter_power_mini = sensor.solax_ac_power
inverter_power_hybrid = sensor.hybrid_inverter_power

# Environmental
illuminance = sensor.esp8266_relay04_bh1750_illuminance

# Load & Battery
power_load = sensor.power_load
battery_load = sensor.battery_load

# Integrated Energy Sensors (kWh)
solar_energy1 = sensor.280_60_solar_energy
solar_energy2 = sensor.280_15_solar_energy
```

---

## CSV & Database Columns

Each row contains:

```
timestamp, lux, power1, power2,
modules1, azimuth1, tilt1,
modules2, azimuth2, tilt2,
batteries, battery_cap,
power_load, battery_load,
grid_power, grid_export, grid_fossil_share, total_power,
solar_energy1, solar_energy2
```

- **timestamp** → 1-minute resolution
- **lux** → Illumination (klux)
- **power1/power2** → Inverter power (main + hybrid)
- **solar_energy1/2** → Integrated kWh values from string-specific sensors

---

## Usage

### Export daily data
```bash
./export_solar_logbook.py --day 2025-08-30 --insert-db --overwrite
```

### Query with interpolation
```bash
./query_solar_logbook.py --from-day 2025-08-01 --to-day 2025-08-31 --interpolate --format
```

### Remove duplicate rows
```bash
./query_solar_logbook.py --remove-duplicates
```

### Migrate DB schema after config change
```bash
./migrate_solar_logbook.py
```

---

## Notes
- All scripts require **Python 3.9+**.
- DB schema evolves with config – run migration after changing sensors.
- Export and query scripts are versioned (`v1.5.x`).
- Data stays accessible for **long-term comparisons** (e.g., monthly/annual production).

