from __future__ import annotations

import re

# Stable IDs and ranges copied from the approved Indicator Catalogue's catalogue-at-a-glance table.
MODULE_RANGES = {
    "ISS": 12, "FIN": 22, "CON": 12, "GOV": 14, "VAL": 12,
    "DEM": 14, "GMP": 6, "NEWS": 12, "ATT": 6, "PEER": 10,
    "RISK": 12, "XCHK": 18, "DATA": 10,
}
_CODE_PATTERN = re.compile(r"^([A-Z]+)-(\\d{2})$")


def is_registered_indicator(code: str) -> bool:
    match = _CODE_PATTERN.fullmatch(code.strip().upper())
    if match is None:
        return False
    module, number = match.groups()
    return module in MODULE_RANGES and 1 <= int(number) <= MODULE_RANGES[module]
