---

## ⚡️ Energy Efficiency Factor (stabilized)

### 📐 Purpose

The `energy_efactor` sensor calculates a live energy efficiency indicator that reflects how much of your current power usage is covered by renewable energy — based on local solar production and fossil fuel share of the grid.

### 📊 Sensor Logic

This version uses a **smoothed solar value** and accounts for the different update intervals of the involved sensors:

| Sensor | Meaning                              | Update Interval |
|--------|--------------------------------------|-----------------|
| `ae`   | Grid power usage (import)            | ~ every 60 sec  |
| `ie`   | Inverter (solar) power (raw)         | ~ every 15 sec  |
| `se`   | Averaged solar power (1h)            | smoothed        |

Instead of using the raw inverter power (`ie`), we use the **1-hour average** (`se`) to avoid spikes.

### 🧮 Calculation Formula

```jinja2
{% set ee = 1 - states('sensor.grid_fossil_fuel_percentage') | float / 100 %}
{% set ae = states('sensor.smart_meter_sum_active_instantaneous_power') | float %}
{% set se = states('sensor.average_electrical_solar_1h') | float %}
{% set sum = se + ae %}

{% if ae <= 0 %}
  {{ (se / sum) | round(2) }}
{% else %}
  {{ (((ee * ae) + se) / sum) | round(2) }}
{% endif %}
```

### 💡 Behavior

- If there is **no grid import** (`ae <= 0`):  
  → Effizienz = solar / total

- If there **is grid import**:  
  → Fossil-adjusted net import + solar, divided by total

### ✅ Why this approach?

- Avoids flickering values from `ie` (fast-changing solar inverter data)
- Provides a smoother, more stable efficiency factor
- Reflects real-world self-sufficiency and green power usage

You can optionally add a `statistics:` sensor on top to average over 60s or 5min.

---
