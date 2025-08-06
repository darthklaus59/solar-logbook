# Solax X1 Mini Register Map (Observed)

## Commonly Used Registers

| Register | Name                      | Description                |
|----------|---------------------------|----------------------------|
| 0x400    | inverter_voltage          | AC voltage                 |
| 0x40D    | inverter_temperature      | Outside temperature (!)    |
| 0x42C    | inverter_temperature_alt  | Real inverter temperature  |
| 0x423    | total_yield               | Total energy yield (kWh)   |
| 0x425    | today_s_yield             | Today's yield (kWh)        |

## Notes

- Use `REGISTER_S16` for signed values like temperature.
- Use `mbpoll` to test registers manually.
- The sensor at `0x42C` is not included by default. A custom sensor must be defined.