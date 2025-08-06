# 🌓 Solar Logbook for Home Assistant

Export and log your PV & Lux data for technical and legal analysis.

## 📦 Features

- Minute-level export of solar production and illuminance
- Automatic calculation of high-noon solar window (with solar correction)
- DB insert to a local SQLite logbook with smart overwrite
- Lux-to-Power correlation with interpolation & metrics
- Integration with Home Assistant (automation + shell_command)
- Future-proof: supports hybrid inverter & battery expansion

## 🗂 Structure

| File                         | Description                                 |
|------------------------------|---------------------------------------------|
| `export_solar_logbook.py`    | Exports solar data and inserts to DB        |
| `query_solar_logbook.py`     | Query & filter solar logbook data           |
| `interpolation_utils.py`     | Interpolation + derived metrics             |
| `ha_location.py`             | Reads location info from HA `core.config`   |
| `homeassistant/automation.yaml` | Scheduled export automation               |
| `homeassistant/shell_command.yaml` | Shell command for HA                   |

## 💻 CLI Usage

```bash
./export_solar_logbook.py --day 2025-08-01 --insert-db
./query_solar_logbook.py --from 2025-08-01 --l 1500 --int
```
## # Solar Log Export Tool

This script exports solar production data from the Home Assistant SQLite database.
It generates a CSV file and optionally inserts the data into a local solar logbook database.

## Usage

```bash
python3 export_solar_logbook.py --day YYYY-MM-DD [--insert-db] [--modules1 N] [--azimuth1 DEG] [--tilt1 DEG]
                                [--modules2 N] [--azimuth2 DEG] [--tilt2 DEG] [--batteries N] [--battery_cap kWh]
                                [--delta-hours N]
```

### Examples

```bash
python3 export_solar_logbook.py --day 2025-07-31 --insert-db --modules1 2 --azimuth1 190 --tilt1 15
```

## Output

- CSV file at `/share/data/solar_log_YYYY-MM-DD.csv`
- Optional database entries into `/config/solar_logbook.db`

## CSV Fields

- timestamp
- lux
- power1
- power2
- modules1, azimuth1, tilt1
- modules2, azimuth2, tilt2
- batteries, battery_cap
- power_load, battery_load
## 🏡 Home Assistant Integration

See `homeassistant/automation.yaml`

---

## 📚 Documentation

- [RJ45 Modbus Resistor Installation Guide](docs/rj45_resistor_installation_en.md)
- [Custom Sensor: Inverter Temperature Alt](docs/inverter_temperature_alt.md)

## 📚 Documentation SolaX Mini

- [Debugging custom sensor entities](docs/debugging_entities.md)
- [Developer notes: custom sensors for SolaX Mini](docs/dev_notes_custom_sensors.md)
- [Register map: SolaX X1 Mini inverter](docs/register_map_x1mini.md)

