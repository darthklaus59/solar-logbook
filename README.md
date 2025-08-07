# 🌓 Solar Logbook for Home Assistant

Export and log your PV & Lux data for technical and legal analysis.

## 📦 Features

-   Minute-level export of solar production and illuminance
-   Automatic calculation of high-noon solar window (with solar
    correction)
-   DB insert to a local SQLite logbook with smart overwrite
-   Lux-to-Power correlation with interpolation & metrics
-   Integration with Home Assistant (automation + shell_command)
-   Future-proof: supports hybrid inverter & battery expansion

## 🗂 Structure

  -------------------------------------------------------------------------------
  File                                 Description
  ------------------------------------ ------------------------------------------
  `export_solar_logbook.py`            Exports solar data and inserts to DB

  `query_solar_logbook.py`             Query & filter solar logbook data

  `interpolation_utils.py`             Interpolation + derived metrics

  `ha_location.py`                     Reads location info from HA `core.config`

  `homeassistant/automation.yaml`      Scheduled export automation

  `homeassistant/shell_command.yaml`   Shell command for HA

  `solar_logbook.conf`                 Config paths and parameters
  -------------------------------------------------------------------------------

## 🔧 Configuration File: `solar_logbook.conf`

As of version 1.5.x, the `solar_logbook.conf` file allows you to
centrally configure important paths and parameters used by the
`export_solar_logbook.py` and `query_solar_logbook.py` scripts.

This file must be placed in the root directory of the project (alongside
the Python scripts).

### 📄 Example: `solar_logbook.conf`

``` ini
[paths]
ha_db_path = /config/home-assistant_v2.db
logbook_db_path = /config/solar_logbook.db
output_dir = /share/data

[time]
delta_hours = 7

[logging]
log_level = INFO
```

### 📌 Sections and Parameters

  -----------------------------------------------------------------------------
  Section              Key                           Description
  -------------------- ----------------------------- --------------------------
  `paths`              `ha_db_path`                  Path to the Home Assistant
                                                     SQLite database
                                                     (`home-assistant_v2.db`)

                       `logbook_db_path`             Path to the local solar
                                                     logbook database
                                                     (`solar_logbook.db`)

                       `output_dir`                  Folder where export CSV
                                                     files will be stored

  `time`               `delta_hours`                 Width of the time window
                                                     (in hours) around local
                                                     noon for data
                                                     export/interpolation

  `logging`            `log_level`                   Optional logging level
                                                     (e.g., `INFO`, `DEBUG`,
                                                     etc.)
  -----------------------------------------------------------------------------

### 🤔 Behavior

-   If a script argument like `--db-path` or `--delta-hours` is **not
    provided**, the value from `solar_logbook.conf` will be used as
    default.
-   Command-line arguments always **override** the configuration file.
-   If `solar_logbook.conf` is missing or incomplete, **hardcoded
    fallback values** will be used.

### 📂 File location

Make sure `solar_logbook.conf` is located in the same directory as the
main scripts:

    solar-logbook/
    ├── export_solar_logbook.py
    ├── query_solar_logbook.py
    ├── solar_logbook.conf       ← here
    ...

## 💻 CLI Usage

``` bash
./export_solar_logbook.py --day 2025-08-01 --insert-db
./query_solar_logbook.py --from 2025-08-01 --l 1500 --int
```

## \# Solar Log Export Tool

This script exports solar production data from the Home Assistant SQLite
database. It generates a CSV file and optionally inserts the data into a
local solar logbook database.

## Usage

``` bash
python3 export_solar_logbook.py --day YYYY-MM-DD [--insert-db] [--modules1 N] [--azimuth1 DEG] [--tilt1 DEG]
                                 [--modules2 N] [--azimuth2 DEG] [--tilt2 DEG] [--batteries N] [--battery_cap kWh]
                                 [--delta-hours N]
```

### Examples

``` bash
python3 export_solar_logbook.py --day 2025-07-31 --insert-db --modules1 2 --azimuth1 190 --tilt1 15
```

## Output

-   CSV file at `/share/data/solar_log_YYYY-MM-DD.csv`
-   Optional database entries into `/config/solar_logbook.db`

## CSV Fields

-   timestamp
-   lux
-   power1
-   power2
-   modules1, azimuth1, tilt1
-   modules2, azimuth2, tilt2
-   batteries, battery_cap
-   power_load, battery_load

## 🏡 Home Assistant Integration

See `homeassistant/automation.yaml`

------------------------------------------------------------------------

## 📚 Documentation

-   [RJ45 Modbus Resistor Installation
    Guide](docs/rj45_resistor_installation_en.md)
-   [Custom Sensor: Inverter Temperature
    Alt](docs/inverter_temperature_alt.md)

## 📚 Documentation SolaX Mini

-   [Debugging custom sensor entities](docs/debugging_entities.md)
-   [Developer notes: custom sensors for SolaX
    Mini](docs/dev_notes_custom_sensors.md)
-   [Register map: SolaX X1 Mini inverter](docs/register_map_x1mini.md)
