#!/usr/bin/env python3
# ---------------------------------------------
# interpolation_utils.py
# Version      : 1.2.0
# Last updated : 2025-08-02
# Description  : Interpolate selected numeric fields in solar log data
# ---------------------------------------------

import numpy as np
from copy import deepcopy

def interpolate_timeseries(rows):
    """
    Interpolates numeric values (lux, power1, power2) in a list of dicts
    Assumes each dict contains a timestamp and possibly missing numeric values
    """
    if not rows:
        return []

    interpolated_rows = deepcopy(rows)
    numeric_fields = ["lux", "power1", "power2"]

    for field in numeric_fields:
        values = [row.get(field) for row in interpolated_rows]
        numeric = np.array([float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else np.nan for v in values])

        if np.all(np.isnan(numeric)):
            continue  # skip interpolation if all values are missing

        # Perform linear interpolation over index positions
        interpolated = np.interp(
            x=np.arange(len(numeric)),
            xp=np.flatnonzero(~np.isnan(numeric)),
            fp=numeric[~np.isnan(numeric)]
        )

        # Assign interpolated values back
        for i, val in enumerate(interpolated):
            interpolated_rows[i][field] = round(val, 2)

    return interpolated_rows

def add_watt_per_klux(rows):
    """
    Add 'watt_per_klux' field, calculated as (power1 / lux) * 1000
    """
    for row in rows:
        try:
            lux = float(row.get("lux", 0))
            power = float(row.get("power1", 0))
            if lux > 0:
                row["watt_per_klux"] = round((power / lux) * 1000, 1)
            else:
                row["watt_per_klux"] = None
        except (ValueError, TypeError):
            row["watt_per_klux"] = None

    return rows

