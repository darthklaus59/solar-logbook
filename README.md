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

## 🏡 Home Assistant Integration

See `homeassistant/automation.yaml`
