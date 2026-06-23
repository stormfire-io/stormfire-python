"""
Stormfire Python SDK
====================

Drop-in replacement for the OpenAI Python SDK pointed at Stormfire's gateway.

Quickstart::

    from stormfire import Stormfire

    client = Stormfire(api_key="sk-...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response.choices[0].message.content)

That's it. Same interface as ``openai.OpenAI``, paid in USDT.
"""

from __future__ import annotations

import os
from typing import Any

try:
    from openai import OpenAI as _OpenAI  # type: ignore
    from openai import AsyncOpenAI as _AsyncOpenAI  # type: ignore
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "The 'openai' package is required. Install it with:\n"
        "    pip install openai>=1.50.0"
    ) from e


__version__ = "0.1.0"

DEFAULT_BASE_URL = "https://api.stormfire.io/v1"


class Stormfire(_OpenAI):  # type: ignore[misc]
    """Synchronous Stormfire client.

    Subclass of :class:`openai.OpenAI` with a Stormfire base URL and helpful defaults.

    Parameters
    ----------
    api_key:
        Your Stormfire API key (``sk-...``). Falls back to the
        ``STORMFIRE_API_KEY`` environment variable, then ``OPENAI_API_KEY``.
    base_url:
        Override the gateway URL. Default: ``https://api.stormfire.io/v1``.
    **kwargs:
        Forwarded to :class:`openai.OpenAI`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        **kwargs: Any,
    ) -> None:
        resolved_key = (
            api_key
            or os.environ.get("STORMFIRE_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        if not resolved_key:
            raise ValueError(
                "No API key provided. Set STORMFIRE_API_KEY or pass api_key=..."
            )
        super().__init__(
            api_key=resolved_key,
            base_url=base_url or DEFAULT_BASE_URL,
            **kwargs,
        )


class AsyncStormfire(_AsyncOpenAI):  # type: ignore[misc]
    """Asynchronous Stormfire client. See :class:`Stormfire`."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        **kwargs: Any,
    ) -> None:
        resolved_key = (
            api_key
            or os.environ.get("STORMFIRE_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        if not resolved_key:
            raise ValueError(
                "No API key provided. Set STORMFIRE_API_KEY or pass api_key=..."
            )
        super().__init__(
            api_key=resolved_key,
            base_url=base_url or DEFAULT_BASE_URL,
            **kwargs,
        )


__all__ = [
    "Stormfire",
    "AsyncStormfire",
    "DEFAULT_BASE_URL",
    "__version__",
]
