# Stormfire Python SDK

> ⚠️ **Coming soon (July 2026)** — this is a placeholder repo. The full SDK will land here.

## Why a dedicated SDK?

Stormfire is **OpenAI SDK compatible** today. If you're using the official OpenAI Python SDK, you can use Stormfire right now by changing one line:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-stormfire-...",
    base_url="https://api.stormfire.io/v1"
)
```

That works for 90% of users. **This dedicated SDK** will add:

- Native USDT top-up flow inside Python code (`client.billing.topup(amount=15, chain='trc20')`)
- Built-in retry on chain confirmation delays
- Real-time balance/usage tracking
- First-party support for Stormfire-specific endpoints (model routing hints, batch discounts)

## Roadmap

- [ ] 0.1 — Basic OpenAI-compatible wrapper with Stormfire-aware retries (July 2026)
- [ ] 0.2 — Top-up via NOWPayments integrated (August 2026)
- [ ] 0.3 — Async + streaming + tool use parity (September 2026)
- [ ] 1.0 — PyPI public release (Q4 2026)

## Want to help?

Open an issue with your use case. We design SDK ergonomics around real workflows, not assumptions.

## License

MIT — same as the official OpenAI Python SDK.

---

Made with ❤️ by [Stormfire](https://stormfire.io)
