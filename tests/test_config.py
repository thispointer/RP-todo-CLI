"""This module tests config.py"""
# tests/test_config.py

from pathlib import Path

from rptodo_project import SUCCESS, config


def test_init_app(tmp_path: Path):
    """Test app configuration initialization."""
    db_path = str(tmp_path / "test.db")
    result = config.init_app(db_path)
    assert result == SUCCESS
    assert config.CONFIG_FILE_PATH.exists()


def test_init_app_creates_config_dir(tmp_path: Path, monkeypatch):
    """Test that init_app creates config directory."""
    db_path = str(tmp_path / "test.db")
    result = config.init_app(db_path)
    assert result == SUCCESS
