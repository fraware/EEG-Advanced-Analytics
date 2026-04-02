"""Load and preprocess tabular EEG data from a directory of CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from eeg_advanced_analytics.constants import (
    EXCLUDED_SENSOR_POSITIONS,
    SENSOR_POSITION_MAPPINGS,
)


def load_and_preprocess_data(directory: str | Path) -> pd.DataFrame:
    """Load all ``*.csv`` files from *directory* and apply column/sensor cleanup."""
    path = Path(directory)
    data_frames: list[pd.DataFrame] = []
    for file_path in sorted(path.glob("*.csv")):
        data_frames.append(pd.read_csv(file_path))

    if not data_frames:
        msg = f"No CSV files found in {path}"
        raise FileNotFoundError(msg)

    eeg_data = pd.concat(data_frames, ignore_index=True)
    unnamed = [c for c in eeg_data.columns if str(c).startswith("Unnamed")]
    if unnamed:
        eeg_data = eeg_data.drop(columns=unnamed)

    for original, updated in SENSOR_POSITION_MAPPINGS.items():
        eeg_data.loc[eeg_data["sensor position"] == original, "sensor position"] = updated
    eeg_data = eeg_data[~eeg_data["sensor position"].isin(EXCLUDED_SENSOR_POSITIONS)]

    return eeg_data
