from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from eeg_advanced_analytics.data_processing import sample_data


def test_sample_data_requires_both_groups(
    tiny_eeg_frame: pd.DataFrame,
    rng: np.random.Generator,
) -> None:
    only_a = tiny_eeg_frame[tiny_eeg_frame["subject identifier"] == "a"]
    with pytest.raises(ValueError, match="Not enough subjects"):
        sample_data("S1 obj", only_a, rng)


def test_sample_data_returns_concat(
    tiny_eeg_frame: pd.DataFrame,
    rng: np.random.Generator,
) -> None:
    out = sample_data("S1 obj", tiny_eeg_frame, rng, random_index=0)
    assert set(out["subject identifier"].unique()) == {"a", "c"}
