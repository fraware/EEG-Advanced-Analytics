"""Sampling and trial alignment for paired group comparisons."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sample_data(
    stimulus: str,
    eeg_data: pd.DataFrame,
    rng: np.random.Generator,
    *,
    random_index: int | None = None,
) -> pd.DataFrame:
    """Select one alcoholic and one control subject for *stimulus*; align to min trial per subject.

    Subject choice is reproducible: names are sorted, then indexed by *random_index* modulo
    available counts (or drawn uniformly if *random_index* is None).
    """
    if not isinstance(eeg_data, pd.DataFrame):
        raise TypeError("eeg_data must be a pandas DataFrame.")

    mask_stim = eeg_data["matching condition"] == stimulus
    a_mask = mask_stim & (eeg_data["subject identifier"] == "a")
    c_mask = mask_stim & (eeg_data["subject identifier"] == "c")
    a_names = np.sort(eeg_data.loc[a_mask, "name"].unique())
    c_names = np.sort(eeg_data.loc[c_mask, "name"].unique())

    if a_names.size < 1 or c_names.size < 1:
        msg = "Not enough subjects (need at least one 'a' and one 'c') for the stimulus."
        raise ValueError(msg)

    if random_index is None:
        ia = int(rng.integers(0, a_names.size))
        ic = int(rng.integers(0, c_names.size))
    else:
        ia = int(random_index) % a_names.size
        ic = int(random_index) % c_names.size

    alcoholic_id = a_names[ia]
    control_id = c_names[ic]

    stim_match = eeg_data["matching condition"] == stimulus
    filter_alcoholic = (eeg_data["name"] == alcoholic_id) & stim_match
    filter_control = (eeg_data["name"] == control_id) & stim_match

    min_trial_alcoholic = eeg_data.loc[filter_alcoholic, "trial number"].min()
    min_trial_control = eeg_data.loc[filter_control, "trial number"].min()

    alcoholic_df = eeg_data[filter_alcoholic & (eeg_data["trial number"] == min_trial_alcoholic)]
    control_df = eeg_data[filter_control & (eeg_data["trial number"] == min_trial_control)]

    out: pd.DataFrame = pd.concat([alcoholic_df, control_df])
    return out
