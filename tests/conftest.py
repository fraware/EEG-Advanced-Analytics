"""Shared pytest fixtures."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def tiny_eeg_frame() -> pd.DataFrame:
    """Minimal tabular EEG-like rows for two subjects, one stimulus, two sensors."""
    rows: list[dict[str, object]] = []
    for _sid, name, grp in (
        ("s1", "n1", "a"),
        ("s1", "n2", "c"),
    ):
        for trial in (1,):
            for sample in range(4):
                for ch, pos in enumerate(("FZ", "CZ")):
                    rows.append(
                        {
                            "name": name,
                            "subject identifier": grp,
                            "matching condition": "S1 obj",
                            "trial number": trial,
                            "sample num": sample,
                            "sensor position": pos,
                            "channel": ch,
                            "sensor value": float(sample + ch + (0.5 if grp == "a" else 0.0)),
                        }
                    )
    return pd.DataFrame(rows)


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(42)
