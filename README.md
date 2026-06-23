# Stormfire — Python SDK

[![PyPI](https://img.shields.io/pypi/v/stormfire?color=ff6b35)](https://pypi.org/project/stormfire/)
[![Python](https://img.shields.io/pypi/pyversions/stormfire)](https://pypi.org/project/stormfire/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stormfire](https://img.shields.io/badge/Stormfire-AI%20Gateway-ff6b35)](https://stormfire.io)

Drop-in replacement for the OpenAI Python SDK that routes your API calls through [Stormfire](https://stormfire.io) — pay AI APIs in USDT, no Stripe, no KYC.

## Install

```bash
pip install stormfire
```

## Quick start

```python
from stormfire import Stormfire

client = Stormfire(api_key="sk-...")  # get yours at https://stormfire.io

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

That's it. Same interface as `openai.OpenAI`, paid in USDT.

## Why?

Stormfire is an AI API gateway. You pay us in USDT, we pay OpenAI / Anthropic / Google / DeepSeek on your behalf. No Stripe in the loop, no KYC, works in 30+ countries that traditional billing rejects.

This package is a 30-line wrapper around the official `openai` SDK that:
- Sets the base URL to `https://api.stormfire.io/v1`
- Reads `STORMFIRE_API_KEY` (falls back to `OPENAI_API_KEY`)
- Exports both sync (`Stormfire`) and async (`AsyncStormfire`) clients

Everything else is identical. All `openai` features work — streaming, function calling, vision, structured outputs, the whole surface area.

## Migrate an existing project

If you already have OpenAI SDK code, you have two options:

### Option 1 — Use this package (recommended)

```python
# before
from openai import OpenAI
client = OpenAI()

# after
from stormfire import Stormfire
client = Stormfire()  # picks up STORMFIRE_API_KEY or OPENAI_API_KEY
```

### Option 2 — Just change the base URL on the official SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",
    base_url="https://api.stormfire.io/v1",
)
```

Both work. Option 1 is shorter and survives upstream renames better.

## Async usage

```python
import asyncio
from stormfire import AsyncStormfire

async def main():
    client = AsyncStormfire()
    response = await client.chat.completions.create(
        model="claude-3-5-sonnet",
        messages=[{"role": "user", "content": "Write a haiku"}],
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## Models

Stormfire supports 30+ models including:

- **OpenAI**: `gpt-4o`, `gpt-5`, `gpt-4o-mini`
- **Anthropic**: `claude-3-5-sonnet`, `claude-3-7-sonnet`, `claude-3-5-haiku`
- **Google**: `gemini-2.0-pro`, `gemini-2.0-flash`
- **DeepSeek**: `deepseek-v3`, `deepseek-v4`
- **Mistral**: `mistral-large`, `mistral-small`
- **Open source**: `llama-3.1-405b`, `qwen-2.5-72b`

Full list and current pricing: <https://stormfire.io/pricing>.

## LangChain / LlamaIndex / etc.

Anything that accepts a `base_url` works. Example with LangChain:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="sk-stormfire-key",
    base_url="https://api.stormfire.io/v1",
    model="gpt-4o",
)
```

## Development

```bash
git clone https://github.com/stormfire-io/stormfire-python
cd stormfire-python
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
