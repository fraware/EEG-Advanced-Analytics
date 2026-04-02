"""Optional MNE-Python integration (montages, standard EEG I/O).

Install with: ``pip install 'eeg-advanced-analytics[mne]'``.

This module is a thin hook for future work: the current pipeline uses UCI tabular CSVs.
Use MNE when you need ``Raw``/``Epochs``, standard montages, or BDF/EDF ingestion.
"""


def mne_available() -> bool:
    """Return True if ``mne`` can be imported."""
    try:
        import mne  # noqa: F401
    except ImportError:
        return False
    return True
