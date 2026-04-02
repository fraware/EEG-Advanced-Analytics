"""Statistical tests and correlation summaries for tabular EEG data."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests


def mann_whitney_alcoholic_vs_control(
    stimulus: str,
    sensor: str,
    eeg_data: pd.DataFrame,
) -> tuple[float, float]:
    """Return (p_value, rank_biserial) for Mann–Whitney U (two-sided), alcoholic vs control.

    Rank-biserial correlation: ``r = 1 - 2U / (n_a * n_c)`` where *U* is the scipy U for the
    alcoholic sample. Returns ``(nan, nan)`` if either group has no observations.
    """
    x = eeg_data.loc[
        (eeg_data["subject identifier"] == "a")
        & (eeg_data["matching condition"] == stimulus)
        & (eeg_data["sensor position"] == sensor),
        "sensor value",
    ]
    y = eeg_data.loc[
        (eeg_data["subject identifier"] == "c")
        & (eeg_data["matching condition"] == stimulus)
        & (eeg_data["sensor position"] == sensor),
        "sensor value",
    ]
    na, nc = len(x), len(y)
    if na < 1 or nc < 1:
        return float("nan"), float("nan")

    res = mannwhitneyu(x, y, alternative="two-sided")
    p = float(res.pvalue)
    u = float(res.statistic)
    rank_biserial = 1.0 - (2.0 * u) / (na * nc)
    return p, rank_biserial


def get_p_value(stimulus: str, sensor: str, eeg_data: pd.DataFrame) -> float:
    """Backward-compatible p-value only wrapper."""
    p, _ = mann_whitney_alcoholic_vs_control(stimulus, sensor, eeg_data)
    return p


def mann_whitney_grid_fdr(
    eeg_data: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Run all sensor × stimulus Mann–Whitney tests; add Benjamini–Hochberg FDR (global family).

    The multiple-testing family is **all** sensor–stimulus pairs in *eeg_data* (one global FDR).
    """
    sensors = np.sort(eeg_data["sensor position"].unique())
    stimuli = np.sort(eeg_data["matching condition"].unique())
    rows: list[dict[str, object]] = []
    for sensor in sensors:
        for stimulus in stimuli:
            p, r_rb = mann_whitney_alcoholic_vs_control(stimulus, str(sensor), eeg_data)
            rows.append(
                {
                    "stimulus": stimulus,
                    "sensor": sensor,
                    "p_value": p,
                    "rank_biserial": r_rb,
                }
            )
    out = pd.DataFrame(rows)
    valid = np.isfinite(out["p_value"].to_numpy(dtype=float))
    p_adj = np.full(len(out), np.nan)
    reject = np.zeros(len(out), dtype=bool)
    if valid.any():
        rej, pvals_corrected, _, _ = multipletests(
            out.loc[valid, "p_value"].astype(float),
            alpha=alpha,
            method="fdr_bh",
        )
        p_adj[valid] = pvals_corrected
        reject[valid] = rej
    out["p_value_fdr_bh"] = p_adj
    out["reject_null_fdr"] = reject
    out["reject_null_uncorrected"] = out["p_value"] <= alpha
    return out


def get_correlated_pairs_high_counts(
    stimulus: str,
    threshold: float,
    group: str,
    eeg_data: pd.DataFrame,
) -> pd.DataFrame:
    """Count channel pairs with correlation >= *threshold* across trials (one group)."""
    corr_pairs_dict: dict[str, int] = {}
    id_match = eeg_data["subject identifier"] == group
    trial_mask = id_match & (eeg_data["matching condition"] == stimulus)
    for trial_number in eeg_data.loc[trial_mask, "trial number"].unique():
        sub_df = eeg_data[id_match & (eeg_data["trial number"] == trial_number)]
        pivot_data = sub_df.pivot_table(
            values="sensor value", index="sample num", columns="sensor position"
        ).corr()
        for idx, column in enumerate(pivot_data.columns):
            for j in range(idx + 1, len(pivot_data.columns)):
                col_b = pivot_data.columns[j]
                value = float(pivot_data.at[column, col_b])
                if value >= threshold:
                    pair = f"{column}-{col_b}"
                    corr_pairs_dict[pair] = corr_pairs_dict.get(pair, 0) + 1

    corr_count = pd.DataFrame(list(corr_pairs_dict.items()), columns=["channel_pair", "count"])
    corr_count["group"] = group
    corr_count["stimulus"] = stimulus
    return corr_count


def correlated_pairs_both_groups(
    stimulus: str,
    threshold: float,
    eeg_data: pd.DataFrame,
) -> pd.DataFrame:
    """Stack high-correlation pair counts for alcoholic ('a') and control ('c')."""
    a_df = get_correlated_pairs_high_counts(stimulus, threshold, "a", eeg_data)
    c_df = get_correlated_pairs_high_counts(stimulus, threshold, "c", eeg_data)
    return pd.concat([a_df, c_df], ignore_index=True)


def compare_corr_pairs(
    stimulus: str,
    corr_pairs_df: pd.DataFrame,
    *,
    output_path: Path | None = None,
    interactive: bool = False,
) -> go.Figure:
    """Grouped bar chart of top correlated pairs per group."""
    if "group" not in corr_pairs_df.columns:
        raise ValueError("The DataFrame does not contain the 'group' column.")

    parts: list[pd.DataFrame] = []
    for g in ("a", "c"):
        g_df = corr_pairs_df[corr_pairs_df["group"] == g]
        sub = g_df.sort_values("count", ascending=False).head(10)
        parts.append(sub)
    top_pairs = pd.concat(parts, ignore_index=True)

    def create_bar(data: pd.DataFrame, name: str, color: str) -> go.Bar:
        return go.Bar(
            x=data["channel_pair"],
            y=data["count"],
            text=data["count"],
            name=name,
            marker=dict(color=color),
        )

    data_a = top_pairs[top_pairs["group"] == "a"]
    data_c = top_pairs[top_pairs["group"] == "c"]

    fig = go.Figure(
        data=[
            create_bar(data_a, "Alcoholic group", "rgb(20,140,45)"),
            create_bar(data_c, "Control group", "rgb(200,100,45)"),
        ],
        layout=go.Layout(
            title=f"Correlated pairs (top per group): {stimulus}",
            xaxis=dict(title="Channel pairs"),
            yaxis=dict(title="Count"),
            barmode="group",
        ),
    )
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path), include_plotlyjs="cdn")
    if interactive:
        fig.show()
    return fig


def print_high_correlation_pairs(
    correlation_matrix: pd.DataFrame,
    threshold: float,
    group_label: str,
) -> None:
    """Print pairs whose correlation in *correlation_matrix* is >= *threshold*."""
    cols = list(correlation_matrix.columns)
    found: list[str] = []
    for i, col1 in enumerate(cols):
        for col2 in cols[i + 1 :]:
            v = float(cast(float, correlation_matrix.at[col1, col2]))
            if v >= threshold:
                found.append(f"{col1}-{col2}")
    print(f"Channel pairs with correlation >= {threshold} ({group_label}): {found}")


def plot_sensors_correlation(
    df: pd.DataFrame,
    threshold_value: float,
    *,
    output_dir: Path | None = None,
    stimulus_slug: str = "stimulus",
) -> None:
    """Heatmaps per group; print high-correlation pairs from each group's correlation matrix."""

    def corr_pivot(sub_df: pd.DataFrame) -> pd.DataFrame:
        return sub_df.pivot_table(
            values="sensor value", index="sample num", columns="sensor position"
        ).corr()

    def generate_heatmap(sub_df: pd.DataFrame, title: str, ax: plt.Axes) -> None:
        pivot_data = corr_pivot(sub_df)
        mask = np.triu(np.ones_like(pivot_data, dtype=bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(
            pivot_data,
            mask=mask,
            cmap=cmap,
            vmin=-1,
            vmax=1,
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.5},
            ax=ax,
        )
        ax.set_title(title)

    alcoholic_df = df[df["subject identifier"] == "a"]
    control_df = df[df["subject identifier"] == "c"]
    stim = df["matching condition"].unique()[0]

    fig, axes = plt.subplots(1, 2, figsize=(17, 10))
    generate_heatmap(alcoholic_df, "Alcoholic group", axes[0])
    generate_heatmap(control_df, "Control group", axes[1])
    fig.suptitle(
        f"Correlation between sensor positions: {stim}",
        fontsize=16,
    )
    fig.tight_layout()
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_png = output_dir / f"sensor_correlation_heatmap_{stimulus_slug}.png"
        fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)

    corr_a = corr_pivot(alcoholic_df)
    corr_c = corr_pivot(control_df)
    print_high_correlation_pairs(corr_a, threshold_value, "Alcoholic")
    print_high_correlation_pairs(corr_c, threshold_value, "Control")
