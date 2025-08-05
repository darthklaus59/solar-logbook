# Custom Sensor: Inverter Temperature Alt (0x42C)

This document describes the purpose and usage of the custom sensor **"Inverter Temperature Alt"** in the `solax_modbus` Home Assistant integration.

## 📌 Purpose

The built-in sensor:

- `Inverter Temperature` (register `0x40D`)

does **not** measure the internal inverter temperature, as the name suggests. It rather corresponds to the **outside/ambient temperature** near the inverter enclosure.

## ✅ Solution

The actual internal inverter temperature is provided by:

- `Inverter Temperature Alt` (register `0x42C`)

### Sensor Definition (plugin)

This sensor can be added to your custom plugin by extending `SENSOR_TYPES_MAIN` in your `plugin_solax.py` file:

```python
SolaXModbusSensorEntityDescription(
    name="Inverter Temperature Alt",
    key="inverter_temperature_alt",
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    device_class=SensorDeviceClass.TEMPERATURE,
    state_class=SensorStateClass.MEASUREMENT,
    register=0x42C,
    register_type=REG_INPUT,
    unit=REGISTER_S16,
    allowedtypes=MIC | GEN4 | X1,  # or 0x2102 if you're sure
    entity_category=EntityCategory.DIAGNOSTIC,
),