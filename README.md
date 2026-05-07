## Install as a skill

```bash
npx skills add Bomx/distribb-skill
```

# Distribb SEO Skill

SEO automation for AI agents. Use any AI model you want. Distribb provides the infrastructure: keyword data, backlinks from real businesses, CMS publishing, and analytics.

## Quick Start

```bash
export DISTRIBB_API_KEY=your_key_here
```

No installation required. The skill uses `curl` and `jq` to interact with the Distribb API.

## Plans

| Plan | Keyword data | Backlinks | Notes |
|------|---|---|---|
| **Agentic Mode** ($49/mo) | Distribb-provided | Full exchange access | The default paid Agentic plan. |
| **Free Agentic** ($0/mo) | **Bring your own** DataForSEO **or** Ahrefs API key | 1 backlink/month | Save your keys at [distribb.io/settings#seo-keys](https://distribb.io/settings#seo-keys). |

## Commands

```bash
# Projects
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .

# Business context (brand voice, competitors, custom instructions)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .

# Keyword research
# Free Agentic plan: returns HTTP 402 with `error: "byo_keys_required"` until
# the user saves their own DataForSEO or Ahrefs API key in Settings. Read
# `instructions_for_agent` from the body and surface it to the user verbatim.
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "crm software", "project_id": 42}' \
  https://distribb.io/api/v1/keywords/search | jq .

# Internal links
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=42&keyword=crm+software" | jq .

# Backlink targets
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=42&keyword=crm+software" | jq .

# Create article
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "keyword": "best crm", "title": "Best CRM", "content": "<h2>...</h2>", "status": "Draft"}' \
  https://distribb.io/api/v1/articles | jq .

# Update article (e.g. add backlink targets after submission)
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "<h2>Revised...</h2>"}' \
  https://distribb.io/api/v1/articles/123 | jq .

# List articles
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/articles?project_id=42" | jq .

# Publish to CMS
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/publish | jq .

# Integrations
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/integrations?project_id=42" | jq .
```

## Backlink Exchange

Distribb connects real businesses that exchange backlinks. When your article includes a link to a network partner, Distribb detects it on submission and credits your project. More backlinks given = more received. These are high-DR backlinks from legitimate business websites.

## Bring-Your-Own-Keys (Free Agentic plan)

The Free Agentic plan does not bundle keyword data. Users save their own **DataForSEO** or **Ahrefs** API keys at [distribb.io/settings#seo-keys](https://distribb.io/settings#seo-keys). All other endpoints (articles, integrations, backlinks) work normally without any keys.

When `/api/v1/keywords/search` is called by a Free Agentic user with no keys saved, the response is:

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "error": "byo_keys_required",
  "message": "Keyword research requires your own DataForSEO or Ahrefs API key.",
  "plan": "Agentic Free",
  "required": { "any_of": ["dataforseo", "ahrefs"] },
  "setup_url": "https://distribb.io/settings#seo-keys",
  "docs_url": "https://distribb.io/api-docs#byo-keys",
  "instructions_for_agent": "Tell the user to add their DataForSEO Login + API Key (or Ahrefs API Key) at distribb.io/settings, then re-run keyword research."
}
```

**Agent contract:** when you receive HTTP 402 with `"error": "byo_keys_required"`, halt the keyword-research step and surface `instructions_for_agent` to the human user verbatim. Do not retry until they have visited `setup_url` and saved credentials. Other endpoints in this skill remain unaffected.

If the user has saved only an Ahrefs key, responses include `"source": "byo_ahrefs"` and a `note` field explaining that DataForSEO would unlock fuller keyword expansion.

## MCP Server (Cursor / Claude Desktop)

The MCP server exposes every Distribb endpoint as a native tool that Claude, Cursor, and other MCP clients can call directly.

See the [API docs](https://distribb.io/api-docs#ep-mcp) for MCP setup instructions.

## Get an API Key

Sign up at [distribb.io](https://distribb.io). Your API key is in Settings after signup.
