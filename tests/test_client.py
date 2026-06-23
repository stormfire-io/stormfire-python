"""Smoke tests for stormfire SDK."""

import os
import pytest

from stormfire import Stormfire, AsyncStormfire, DEFAULT_BASE_URL, __version__


def test_version():
    assert __version__ == "0.1.0"


def test_default_base_url():
    assert DEFAULT_BASE_URL == "https://api.stormfire.io/v1"


def test_client_uses_stormfire_base_url():
    client = Stormfire(api_key="sk-test")
    assert str(client.base_url).rstrip("/") == DEFAULT_BASE_URL


def test_client_custom_base_url():
    client = Stormfire(api_key="sk-test", base_url="https://staging.stormfire.io/v1")
    assert "staging" in str(client.base_url)


def test_client_reads_env_var(monkeypatch):
    monkeypatch.setenv("STORMFIRE_API_KEY", "sk-from-env")
    client = Stormfire()
    assert client.api_key == "sk-from-env"


def test_client_falls_back_to_openai_env(monkeypatch):
    monkeypatch.delenv("STORMFIRE_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-env")
    client = Stormfire()
    assert client.api_key == "sk-openai-env"


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("STORMFIRE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="No API key"):
        Stormfire()


def test_async_client_creates():
    client = AsyncStormfire(api_key="sk-test")
    assert str(client.base_url).rstrip("/") == DEFAULT_BASE_URL
