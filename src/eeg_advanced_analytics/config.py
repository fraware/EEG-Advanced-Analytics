"""Resolve data directory from CLI or environment."""

from __future__ import annotations

import os
from pathlib import Path


def resolve_data_dir(explicit: str | Path | None = None) -> Path:
    """Return absolute data directory path.

    Precedence: explicit argument, then ``EEG_DATA_DIR``, then ``data/train`` (relative to CWD).
    """
    if explicit is not None:
        p = Path(explicit)
    else:
        env = os.environ.get("EEG_DATA_DIR")
        p = Path(env) if env else Path("data") / "train"
    return p.expanduser().resolve()


def validate_data_dir(path: Path) -> None:
    """Ensure directory exists and contains at least one CSV file."""
    if not path.is_dir():
        msg = f"Data directory does not exist or is not a directory: {path}"
        raise FileNotFoundError(msg)
    csvs = list(path.glob("*.csv"))
    if not csvs:
        msg = (
            f"No CSV files found under {path}. "
            "Place UCI EEG training CSVs here or set EEG_DATA_DIR."
        )
        raise FileNotFoundError(msg)
