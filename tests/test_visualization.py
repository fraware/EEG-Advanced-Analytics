from __future__ import annotations

from pathlib import Path

import pandas as pd

from eeg_advanced_analytics import visualization


def test_plot_3d_writes_html(tiny_eeg_frame: pd.DataFrame, tmp_path: Path) -> None:
    sub = tiny_eeg_frame[tiny_eeg_frame["subject identifier"] == "a"]
    channels = sorted(sub["channel"].unique().tolist())
    positions = [sub.loc[sub["channel"] == c, "sensor position"].iloc[0] for c in channels]
    path = tmp_path / "x.html"
    visualization.plot_3d_surface_and_heatmap(
        "S1 obj",
        "a",
        sub,
        channels,
        positions,
        output_path=path,
        interactive=False,
    )
    assert path.is_file()
    assert path.stat().st_size > 100


def test_slugify() -> None:
    assert visualization.slugify("S1 obj") == "S1_obj"
