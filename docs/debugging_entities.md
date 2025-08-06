# Debugging solax_modbus Sensor Entities

## Missing Entity?

Check the logs for:

- `Entity ... not found in state manager, assuming disabled`
- `failed input block read_error`

## Why It Happens

- The sensor may not match the current inverter type (`allowedtypes` mismatch).
- The register may not be readable (e.g., device returns error).
- The register may be beyond the default Modbus block size.

## How to Force Inclusion

You can add a sensor manually in the plugin like this:

```python
SolaXModbusSensorEntityDescription(
    name="Inverter Temperature Alt",
    key="inverter_temperature_alt",
    register=0x42C,
    ...,
    newblock=True
)
```

Set `newblock=True` to force a separate read operation.