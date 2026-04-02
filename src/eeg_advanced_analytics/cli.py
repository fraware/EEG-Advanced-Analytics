"""Command-line interface."""

from __future__ import annotations

from pathlib import Path

import typer

from eeg_advanced_analytics.constants import RANDOM_SEED
from eeg_advanced_analytics.pipeline import run_pipeline

_DEFAULT_OUTPUT = Path("outputs")


def main(
    data_dir: str | None = typer.Option(
        None,
        "--data-dir",
        help="Directory containing EEG CSV files. Overrides EEG_DATA_DIR.",
        envvar="EEG_DATA_DIR",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        help="Artifacts directory (default: ./outputs).",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        help="Open Plotly figures in the browser in addition to writing HTML.",
    ),
    seed: int = typer.Option(RANDOM_SEED, "--seed", help="RNG seed for subject sampling."),
) -> None:
    """Load data, run visualizations, correlations, and Mann–Whitney + FDR."""
    run_pipeline(
        data_dir=data_dir,
        output_dir=output_dir if output_dir is not None else _DEFAULT_OUTPUT,
        interactive=interactive,
        seed=seed,
    )


def cli_entry() -> None:
    typer.run(main)


if __name__ == "__main__":
    cli_entry()
