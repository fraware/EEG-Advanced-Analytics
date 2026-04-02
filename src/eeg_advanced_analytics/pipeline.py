"""End-to-end orchestration for the UCI-style EEG analysis pipeline."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from eeg_advanced_analytics import (
    data_loading,
    data_processing,
    statistical_analysis,
    visualization,
)
from eeg_advanced_analytics.config import resolve_data_dir, validate_data_dir
from eeg_advanced_analytics.constants import RANDOM_SEED


def channel_sensor_lists(eeg_data: pd.DataFrame) -> tuple[list, list]:
    """Unique sensor order with channel indices for Plotly y-axis labels."""
    dup = eeg_data[["sensor position", "channel"]].drop_duplicates().reset_index(drop=True)
    dup = dup.drop(columns=["channel"]).reset_index(drop=False).rename(columns={"index": "channel"})
    channels = dup["channel"].tolist()
    sensor_positions = dup["sensor position"].tolist()
    return channels, sensor_positions


def run_pipeline(
    *,
    data_dir: str | Path | None = None,
    output_dir: Path | None = None,
    interactive: bool = False,
    seed: int = RANDOM_SEED,
    stimuli_list: list[str] | None = None,
) -> None:
    load_dotenv()
    root = Path(output_dir) if output_dir is not None else Path("outputs")
    figures = root / "figures"
    tables = root / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    path = resolve_data_dir(data_dir)
    validate_data_dir(path)

    rng = np.random.default_rng(seed)
    eeg_data = data_loading.load_and_preprocess_data(path)

    stimuli = stimuli_list if stimuli_list is not None else ["S1 obj", "S2 match"]
    channels, sensor_positions = channel_sensor_lists(eeg_data)

    for stimulus in tqdm(stimuli, desc="Processing stimuli"):
        stim_slug = visualization.slugify(stimulus)
        try:
            sampled = data_processing.sample_data(stimulus, eeg_data, rng)

            for group in ("a", "c"):
                visualization.plot_3d_surface_and_heatmap(
                    stimulus,
                    group,
                    sampled,
                    channels,
                    sensor_positions,
                    output_path=figures / f"surface_{stim_slug}_{group}.html",
                    interactive=interactive,
                )

            corr_pairs_df = statistical_analysis.correlated_pairs_both_groups(
                stimulus,
                0.9,
                eeg_data,
            )
            statistical_analysis.compare_corr_pairs(
                stimulus,
                corr_pairs_df,
                output_path=figures / f"corr_pairs_{stim_slug}.html",
                interactive=interactive,
            )

            statistical_analysis.plot_sensors_correlation(
                sampled,
                0.97,
                output_dir=figures,
                stimulus_slug=stim_slug,
            )
        except (ValueError, FileNotFoundError) as e:
            print(f"Skipping {stimulus} due to error: {e}")

    stat_test_results = statistical_analysis.mann_whitney_grid_fdr(eeg_data, alpha=0.05)
    stat_test_results.to_csv(tables / "mann_whitney_fdr.csv", index=False)

    visualization.visualize_significant_differences(
        stat_test_results,
        output_path=figures / "significant_differences.html",
        interactive=interactive,
    )
