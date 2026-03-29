import os
import pytest
from app import get_config

def test_get_config_missing_env(monkeypatch):
    """Pipeline should fail loudly if secrets are missing."""
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("DB_URL", raising=False)
    with pytest.raises(EnvironmentError):
        get_config()

def test_get_config_present(monkeypatch):
    """Pipeline should succeed when secrets are injected."""
    monkeypatch.setenv("API_KEY", "fake-key-for-test")
    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")
    config = get_config()
    assert config["api_key"] == "fake-key-for-test"
    assert config["db_url"] == "sqlite:///:memory:"

def test_api_key_not_empty(monkeypatch):
    """Empty string secrets should also be rejected."""
    monkeypatch.setenv("API_KEY", "")
    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")
    with pytest.raises(EnvironmentError):
        get_config()
