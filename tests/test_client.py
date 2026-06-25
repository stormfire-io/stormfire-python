"""Unit tests for the Stormfire Python SDK.

These tests assert client construction behavior without making any network
calls (we never instantiate a real upstream connection here). The Stormfire
class is a thin subclass of openai.OpenAI; verifying base_url and api_key
resolution is enough to lock in the public contract.
"""


import pytest
from openai import AsyncOpenAI, OpenAI

from stormfire import (
    DEFAULT_BASE_URL,
    AsyncStormfire,
    Stormfire,
    __version__,
)


def test_version_present():
    assert isinstance(__version__, str)
    assert __version__.count(".") == 2


def test_default_base_url():
    assert DEFAULT_BASE_URL == "https://api.stormfire.io/v1"


def test_sync_client_uses_stormfire_base_url():
    client = Stormfire(api_key="sk-test")
    assert isinstance(client, OpenAI)
    assert str(client.base_url).rstrip("/") == DEFAULT_BASE_URL


def test_async_client_uses_stormfire_base_url():
    client = AsyncStormfire(api_key="sk-test")
    assert isinstance(client, AsyncOpenAI)
    assert str(client.base_url).rstrip("/") == DEFAULT_BASE_URL


def test_base_url_override(monkeypatch):
    custom = "https://api.example.com/v1"
    client = Stormfire(api_key="sk-test", base_url=custom)
    assert str(client.base_url).rstrip("/") == custom


def test_env_base_url(monkeypatch):
    custom = "https://api-staging.stormfire.io/v1"
    monkeypatch.setenv("STORMFIRE_BASE_URL", custom)
    client = Stormfire(api_key="sk-test")
    assert str(client.base_url).rstrip("/") == custom


def test_api_key_from_env(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("STORMFIRE_API_KEY", "sk-from-env")
    client = Stormfire()
    assert client.api_key == "sk-from-env"


def test_api_key_falls_back_to_openai_env(monkeypatch):
    monkeypatch.delenv("STORMFIRE_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fallback")
    client = Stormfire()
    assert client.api_key == "sk-fallback"


def test_api_key_explicit_beats_env(monkeypatch):
    monkeypatch.setenv("STORMFIRE_API_KEY", "sk-from-env")
    client = Stormfire(api_key="sk-explicit")
    assert client.api_key == "sk-explicit"


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("STORMFIRE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="No API key found"):
        Stormfire()


def test_user_agent_header_set():
    client = Stormfire(api_key="sk-test")
    assert client.default_headers.get("User-Agent", "").startswith("stormfire-python/")
    assert client.default_headers.get("X-Stormfire-Client") == "python"


def test_custom_headers_merge():
    client = Stormfire(
        api_key="sk-test",
        default_headers={"X-App": "demo"},
    )
    assert client.default_headers.get("X-App") == "demo"
    assert client.default_headers.get("X-Stormfire-Client") == "python"
