from __future__ import annotations

import pandas as pd

from eeg_advanced_analytics.data_loading import load_and_preprocess_data


def test_load_maps_and_excludes(tmp_path) -> None:
    df1 = pd.DataFrame(
        {
            "name": ["a", "a"],
            "subject identifier": ["a", "a"],
            "matching condition": ["S1 obj", "S1 obj"],
            "trial number": [1, 1],
            "sample num": [0, 0],
            "sensor position": ["AF1", "X"],
            "channel": [0, 1],
            "sensor value": [1.0, 2.0],
        }
    )
    df1.to_csv(tmp_path / "f1.csv", index=False)
    df2 = pd.DataFrame(
        {
            "Unnamed: 0": [0],
            "name": ["b"],
            "subject identifier": ["c"],
            "matching condition": ["S1 obj"],
            "trial number": [1],
            "sample num": [0],
            "sensor position": ["FZ"],
            "channel": [0],
            "sensor value": [3.0],
        }
    )
    df2.to_csv(tmp_path / "f2.csv", index=False)

    out = load_and_preprocess_data(tmp_path)
    assert "AF3" in out["sensor position"].values
    assert "AF1" not in out["sensor position"].values
    assert "X" not in out["sensor position"].values
    assert len(out) == 2
