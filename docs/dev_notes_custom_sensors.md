# Developer Notes: Adding Custom Sensors

## How to Add

1. Add a `SolaXModbusSensorEntityDescription` to the plugin's `SENSOR_TYPES_MAIN` list.
2. Make sure the `allowedtypes` match your inverter's type.
3. If the register is not contiguous, add `newblock=True`.

## Example

```python
SolaXModbusSensorEntityDescription(
    name="Custom Sensor",
    key="custom_sensor",
    register=0x42D,
    register_type=REG_INPUT,
    unit=REGISTER_U16,
    allowedtypes=X1 | MIC,
    scale=0.1,
    rounding=1
)
```

## Tips

- Use `scale` and `rounding` for formatting.
- Use `ignore_readerror=True` for sensors that may not always be available.
- Use debug logs to trace entity registration.