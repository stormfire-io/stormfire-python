"""Stream a chat completion through Stormfire.

This example mirrors the official OpenAI streaming example at
https://github.com/openai/openai-python so existing OpenAI users can compare
side by side.

Run::

    pip install stormfire
    export STORMFIRE_API_KEY="sk-..."
    python examples/streaming.py
"""

from __future__ import annotations

from stormfire import Stormfire


def main() -> None:
    client = Stormfire()  # picks STORMFIRE_API_KEY from env

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "Explain TLS handshake in 3 short sentences."},
        ],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
