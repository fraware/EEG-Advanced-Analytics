"""Plotly figures for EEG surfaces and significance summaries."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


def slugify(text: str) -> str:
    """Filesystem-safe token for figure filenames."""
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(text))
    return "_".join(s for s in safe.split("_") if s) or "figure"


def _emit_plotly(fig: go.Figure, output_path: Path | None, interactive: bool) -> None:
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path), include_plotlyjs="cdn")
    if interactive:
        fig.show()


def plot_3d_surface_and_heatmap(
    stimulus: str,
    group: str,
    df: pd.DataFrame,
    channels: list,
    sensor_positions: list,
    *,
    output_path: Path | None = None,
    interactive: bool = False,
) -> go.Figure:
    """3D surface (toggle to heatmap) of sensor values by channel and sample."""
    group_names = {"c": "Control", "a": "Alcoholic"}
    group_name = group_names.get(group, "Unknown")

    pivot_df = pd.pivot_table(
        df[["channel", "sample num", "sensor value"]],
        index="channel",
        columns="sample num",
        values="sensor value",
    )
    if pivot_df.isnull().any().any():
        raise ValueError("Missing values in the data. Pivot table creation failed.")

    fig = go.Figure(
        data=[go.Surface(z=pivot_df.values, colorscale="Bluered")],
        layout=go.Layout(
            title=f"3D surface / heatmap: {stimulus} — {group_name}",
            width=800,
            height=900,
            margin=dict(t=0, b=0, l=0, r=0),
            scene=dict(
                xaxis=dict(
                    title="Time (sample num)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                ),
                yaxis=dict(
                    title="Channel",
                    tickvals=list(range(len(channels))),
                    ticktext=sensor_positions,
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230, 230)",
                ),
                zaxis=dict(
                    title="Sensor value",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                ),
                aspectratio=dict(x=1, y=1, z=0.7),
                aspectmode="manual",
            ),
            updatemenus=[
                dict(
                    buttons=[
                        dict(args=["type", "surface"], label="3D Surface", method="restyle"),
                        dict(args=["type", "heatmap"], label="Heatmap", method="restyle"),
                    ],
                    direction="left",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    type="buttons",
                    x=0.1,
                    xanchor="left",
                    y=1.1,
                    yanchor="top",
                )
            ],
            annotations=[
                dict(
                    text="Trace type:",
                    x=0,
                    y=1.085,
                    yref="paper",
                    align="left",
                    showarrow=False,
                )
            ],
        ),
    )
    _emit_plotly(fig, output_path, interactive)
    return fig


def visualize_significant_differences(
    stat_test_results: pd.DataFrame,
    *,
    output_path: Path | None = None,
    interactive: bool = False,
) -> go.Figure:
    """Bar chart of FDR (or uncorrected) rejections per sensor, grouped by stimulus."""
    if "reject_null_fdr" in stat_test_results.columns:
        y_col = "reject_null_fdr"
        y_title = "Significant (FDR BH)"
    else:
        y_col = "reject_null_uncorrected"
        y_title = "Significant (uncorrected p <= 0.05)"

    traces: list[go.Bar] = []
    for stimulus in stat_test_results["stimulus"].unique():
        filtered_df = stat_test_results[stat_test_results["stimulus"] == stimulus]
        traces.append(
            go.Bar(
                x=filtered_df["sensor"],
                y=filtered_df[y_col].fillna(False).astype(int),
                name=str(stimulus),
            )
        )

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title="Significant differences per sensor by stimulus",
            xaxis=dict(title="Sensor"),
            yaxis=dict(title=y_title),
            barmode="group",
        ),
    )
    _emit_plotly(fig, output_path, interactive)
    return fig


def optional_write_static(fig: go.Figure, path: Path) -> None:
    """Write PNG/SVG if Kaleido is installed; no-op on ImportError."""
    try:
        fig.write_image(str(path))
    except ImportError:
        pass
