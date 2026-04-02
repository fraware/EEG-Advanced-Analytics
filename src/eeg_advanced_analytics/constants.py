"""Non-path configuration shared across the package."""

# Default random seed (numpy Generator uses this when constructed from int)
RANDOM_SEED = 123

SENSOR_POSITION_MAPPINGS: dict[str, str] = {
    "AF1": "AF3",
    "AF2": "AF4",
    "PO1": "PO3",
    "PO2": "PO4",
}

EXCLUDED_SENSOR_POSITIONS: frozenset[str] = frozenset({"X", "Y", "nd"})
