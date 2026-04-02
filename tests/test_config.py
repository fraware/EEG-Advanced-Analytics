from __future__ import annotations

from pathlib import Path

from eeg_advanced_analytics.config import resolve_data_dir, validate_data_dir


def test_resolve_data_dir_explicit(tmp_path: Path) -> None:
    d = tmp_path / "d"
    d.mkdir()
    assert resolve_data_dir(d) == d.resolve()


def test_resolve_data_dir_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EEG_DATA_DIR", str(tmp_path))
    assert resolve_data_dir() == tmp_path.resolve()


def test_resolve_data_dir_default_no_env(monkeypatch) -> None:
    monkeypatch.delenv("EEG_DATA_DIR", raising=False)
    cwd = Path.cwd()
    assert resolve_data_dir() == (cwd / "data" / "train").resolve()


def test_validate_data_dir_missing(tmp_path: Path) -> None:
    missing = tmp_path / "nope"
    try:
        validate_data_dir(missing)
    except FileNotFoundError as e:
        assert "does not exist" in str(e)
    else:
        raise AssertionError


def test_validate_data_dir_no_csvs(tmp_path: Path) -> None:
    try:
        validate_data_dir(tmp_path)
    except FileNotFoundError as e:
        assert "No CSV" in str(e)
    else:
        raise AssertionError
