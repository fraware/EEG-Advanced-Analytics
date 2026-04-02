from __future__ import annotations

from eeg_advanced_analytics.mne_spike import mne_available


def test_mne_available_boolean() -> None:
    assert isinstance(mne_available(), bool)
