"""
Stormfire — Pay AI APIs in USDT. OpenAI SDK drop-in replacement.

Quick start:

    from stormfire import Stormfire

    client = Stormfire(api_key="sk-...")
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(resp.choices[0].message.content)

Homepage: https://stormfire.io
Repository: https://github.com/stormfire-io/stormfire-python
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

import httpx
from openai import AsyncOpenAI, OpenAI

__version__ = "0.1.0"

DEFAULT_BASE_URL = "https://api.stormfire.io/v1"
"""Default API base URL. Override via base_url=... when constructing the client
or via the ``STORMFIRE_BASE_URL`` environment variable."""

_USER_AGENT = f"stormfire-python/{__version__}"


def _resolve_api_key(api_key: str | None) -> str:
    """Pick API key from explicit arg → STORMFIRE_API_KEY → OPENAI_API_KEY.

    Raises ``ValueError`` if none of the sources provide a usable key. We do
    not raise on construction time when the user is going to override later
    via the underlying client; callers should still set a key.
    """
    if api_key:
        return api_key
    for env in ("STORMFIRE_API_KEY", "OPENAI_API_KEY"):
        value = os.environ.get(env)
        if value:
            return value
    raise ValueError(
        "No API key found. Set STORMFIRE_API_KEY (or OPENAI_API_KEY) "
        "or pass api_key=... when constructing the client. "
        "Get a key at https://stormfire.io"
    )


def _resolve_base_url(base_url: str | None) -> str:
    if base_url:
        return base_url
    return os.environ.get("STORMFIRE_BASE_URL", DEFAULT_BASE_URL)


def _merged_default_headers(
    extra: Mapping[str, str] | None,
) -> dict[str, str]:
    headers: dict[str, str] = {"User-Agent": _USER_AGENT, "X-Stormfire-Client": "python"}
    if extra:
        headers.update(extra)
    return headers


class Stormfire(OpenAI):
    """Synchronous Stormfire client.

    A thin subclass of :class:`openai.OpenAI` that defaults ``base_url`` to
    ``https://api.stormfire.io/v1`` and picks the API key from
    ``STORMFIRE_API_KEY`` (falling back to ``OPENAI_API_KEY``).

    All keyword arguments accepted by :class:`openai.OpenAI` are forwarded
    unchanged, so this is a literal drop-in replacement.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            api_key=_resolve_api_key(api_key),
            base_url=_resolve_base_url(base_url),
            organization=organization,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=_merged_default_headers(default_headers),
            default_query=default_query,
            http_client=http_client,
            **kwargs,
        )


class AsyncStormfire(AsyncOpenAI):
    """Asynchronous Stormfire client.

    Async equivalent of :class:`Stormfire`. Use this from inside ``async``
    functions or anywhere you would normally reach for
    :class:`openai.AsyncOpenAI`.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            api_key=_resolve_api_key(api_key),
            base_url=_resolve_base_url(base_url),
            organization=organization,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=_merged_default_headers(default_headers),
            default_query=default_query,
            http_client=http_client,
            **kwargs,
        )


__all__ = [
    "Stormfire",
    "AsyncStormfire",
    "DEFAULT_BASE_URL",
    "__version__",
]
