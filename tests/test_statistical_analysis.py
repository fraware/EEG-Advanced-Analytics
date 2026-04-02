from __future__ import annotations

import numpy as np
import pandas as pd

from eeg_advanced_analytics import statistical_analysis


def test_mann_whitney_nan_when_empty() -> None:
    df = pd.DataFrame(
        {
            "subject identifier": ["a"],
            "matching condition": ["S1"],
            "sensor position": ["FZ"],
            "sensor value": [1.0],
        }
    )
    p, r = statistical_analysis.mann_whitney_alcoholic_vs_control("S1", "FZ", df)
    assert np.isnan(p) and np.isnan(r)


def test_mann_whitney_returns_finite(tiny_eeg_frame: pd.DataFrame) -> None:
    p, r = statistical_analysis.mann_whitney_alcoholic_vs_control("S1 obj", "FZ", tiny_eeg_frame)
    assert np.isfinite(p) and np.isfinite(r)


def test_mann_whitney_grid_fdr_columns(tiny_eeg_frame: pd.DataFrame) -> None:
    out = statistical_analysis.mann_whitney_grid_fdr(tiny_eeg_frame, alpha=0.05)
    for col in ("p_value", "rank_biserial", "p_value_fdr_bh", "reject_null_fdr"):
        assert col in out.columns


def test_correlated_pairs_both_groups(tiny_eeg_frame: pd.DataFrame) -> None:
    out = statistical_analysis.correlated_pairs_both_groups("S1 obj", 0.0, tiny_eeg_frame)
    assert set(out["group"].unique()) >= {"a", "c"}
