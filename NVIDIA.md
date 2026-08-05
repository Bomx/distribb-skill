# Using NVIDIA NIM (free OpenAI-compatible API)

Base URL: `https://integrate.api.nvidia.com/v1`

API key: free `nvapi-...` from [build.nvidia.com](https://build.nvidia.com) → Settings → API Keys  
(requires a free NVIDIA Developer Program account; no credit card).

## Env preset

```bash
export OPENAI_API_KEY=nvapi-...            # NVIDIA key goes in the OPENAI_API_KEY slot
export AI_BASE_URL=https://integrate.api.nvidia.com/v1
export AI_MODEL=meta/llama-3.3-70b-instruct
export RESEARCH_MODEL=deepseek-ai/deepseek-r1
export AI_MAX_TOKENS=4000
export AI_RESEARCH_MAX_TOKENS=4000
export AI_MAX_RETRIES=5
```

`AI_MAX_TOKENS` / `AI_RESEARCH_MAX_TOKENS` must be set for NVIDIA — many NIM models cap output far below OpenAI’s 12k article path, and truncated JSON is unrecoverable (the scripts now fail loud on `finish_reason=length`).

## Caveats

- **JSON mode has no schema guarantee.** NVIDIA accepts `response_format={"type":"json_object"}` but docs state it does **not** enforce a schema. NVIDIA’s recommended alternative is `extra_body={"nvext":{"guided_json": <schema>}}`. This skill uses prompt-instructed JSON + parser fallbacks, and now raises `ValueError` on total parse failure instead of silently returning `{}`.
- **Free-tier throttle ~40 req/min per account** (not per key); NVIDIA does not grant increases. *[community-reported, not an official published SLA]*
- **Some models from `GET /v1/models` still 404** on `chat/completions` due to account entitlement.
- **Free-tier credit amounts and expiry** are community-reported and not authoritatively documented.
- **Do not send `presence_penalty` / `frequency_penalty`** — 422 on some NIM backends. (This skill does not send them.)
- **Use the `system` role, never `developer`** — the latter can 500.
