"""Use Stormfire to call a Claude model through the OpenAI Chat Completions API.

Stormfire bridges all 30+ supported models behind a single OpenAI-compatible
endpoint. This means you can call Claude 3.5 Sonnet, Gemini 2 Pro, or
DeepSeek v4 using the exact same client object.

Run::

    pip install stormfire
    export STORMFIRE_API_KEY="sk-..."
    python examples/multi_model.py
"""

from __future__ import annotations

from stormfire import Stormfire


def main() -> None:
    client = Stormfire()

    prompt = "In one paragraph: how would you compare Rust and Go for a network proxy?"

    for model in ("gpt-4o", "claude-3-5-sonnet-20241022", "gemini-2-pro", "deepseek-chat"):
        print(f"\n=== {model} ===")
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            print(resp.choices[0].message.content)
        except Exception as e:
            print(f"  (skipped: {e})")


if __name__ == "__main__":
    main()
