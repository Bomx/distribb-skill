## Install as a skill

```bash
npx skills add Bomx/distribb-skill
```

# Distribb SEO Skill

SEO automation for AI agents. Use any AI model you want. Distribb provides the infrastructure: real keyword data, backlinks from real businesses, a Google Search Console audit, CMS publishing, content calendar, social repurposing and direct social posting, Google Business Profile management (live reviews, public replies, Google posts), Microworkers campaign management, and analytics.

## Quick Start

```bash
export DISTRIBB_API_KEY=your_key_here
```

No installation required for the API. The skill uses `curl` and `jq`. The first time it loads, it walks the user through the proper SEO process: account + onboarding, connect website + Google Search Console, audit, topic clusters, write + backlink, optimize.

## The proper SEO process (what this skill runs)

1. Sign up and complete onboarding at [distribb.io](https://distribb.io) (Distribb learns the business).
2. Connect the two things that matter most: the website/CMS and Google Search Console.
3. Confirm the site has a blog to publish to.
4. **Audit the site before writing anything** (`/gsc-audit`). Available on every plan, including Free.
5. Plan topic clusters, then do keyword research to fill them.
6. Write and publish, always including 1-2 backlink-exchange links.
7. Optimize pages stuck on page 2+ using GSC data (`/optimize`).

## Slash Commands

| Command | What it does |
|---|---|
| `/distribb` | Overview, account status, and the proper SEO process |
| `/distribb-setup` | Check the API key, confirm website + GSC are connected, enable the commands |
| `/gsc-audit <domain>` | Full SEO audit (CTR, decay, page-2, cannibalization, topic clusters, competitor, on-page) |
| `/keyword-research <seed>` | Keyword ideas with volume and difficulty |
| `/write-article <keyword>` | Research, write, link, backlink, and publish one article |
| `/optimize` | Rewrite pages stuck on page 2+ from GSC data |
| `/backlinks` | Check credits and targets, explain the exchange |
| `/content-calendar` | List, schedule, and manage articles |
| `/ai-visibility` | Find where AI engines should recommend you, and which listicles to pitch |
| `/news-writer <site-url-or-niche>` | Turn fresh news in your niche into grounded drafts and queue them in Distribb to autopublish |
| `/statistics-page-writer <topic>` | Deep-research and publish a sourced statistics page journalists love to link to |
| `/youtube-motion-video <topic>` | Make a faceless motion-collage explainer video ("In a Nutshell" docu style), YouTube-SEO it, and publish it to the connected YouTube channel |
| `/instagram-carousel <article-id-or-keyword>` | Turn one article or keyword into a viral, save-driven Instagram carousel (cover hook, one idea per slide, comment-for-link play), publish it, and close the SEO loop with a companion article |
| `/review-video <competitor>` | Compile REAL, verified competitor reviews into a "<competitor> reviews" video, position your business as the alternative, and publish to YouTube + a companion article |
| `/gbp` | Google Business Profile manager: live review triage, public review replies, Google posts, post analytics |

Command files live in `commands/`. If they are not auto-registered by your installer, run `/distribb-setup` or copy `commands/*.md` into your project's `.claude/commands/` folder.

## Plans

| Plan | Keyword data | Backlinks | Who writes |
|------|---|---|---|
| **Free Agentic** ($0/mo) | Bring your own DataForSEO **or** Ahrefs key | **1 backlink/month** | You (the agent) |
| **Agentic Mode** ($49/mo, 3-day trial) | Distribb-provided | **Unlimited** exchange | You (the agent) |
| **Pro** | Distribb-provided | Unlimited exchange | Distribb writes + publishes for you |
| **Accelerator** | Distribb-provided | Unlimited exchange | You + done-for-you AI-search distribution |

Every plan, including Free, can run the audit and use the content calendar. See [`references/plans-and-backlinks.md`](./references/plans-and-backlinks.md) for full detail. Current pricing is at [distribb.io](https://distribb.io).

## Commands (raw API)

```bash
# Projects
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .

# Business context (brand voice, competitors, custom instructions)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .

# Google Search Console (powers the audit + optimizations)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/search-console?project_id=42&days=90&limit=100" | jq .

# Keyword research
# Free Agentic plan: returns HTTP 402 with `error: "byo_keys_required"` until
# the user saves their own DataForSEO or Ahrefs API key in Settings.
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

# Optimization suggestions (rewrite page-2 pages)
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42}' \
  https://distribb.io/api/v1/suggestions/run | jq .

# Publish to CMS
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/publish | jq .

# Edit an ALREADY-PUBLISHED article and push the change to the live post.
# The PUT saves inside Distribb; "sync": true (or the /sync call) updates the
# live post in place. Supported on WordPress, Webhook, Shopify, Webflow, Wix,
# Ghost, GoHighLevel, Framer and Notion.
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Corrected Title", "sync": true}' \
  https://distribb.io/api/v1/articles/123 | jq .

curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/sync | jq .

# Integrations
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/integrations?project_id=42" | jq .

# Google Business Profile: status + live reviews + public reply + posts
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/status?project_id=42" | jq .
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/reviews?project_id=42&has_reply=false" | jq .
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "review_id": "<review_id from /gbp/reviews>", "message": "Thanks Sarah!"}' \
  https://distribb.io/api/v1/gbp/reviews/reply | jq .
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "text": "Spring checks now booking", "link": "https://acme.com/offer"}' \
  https://distribb.io/api/v1/gbp/posts | jq .

# Microworkers campaigns
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/microworkers/campaigns?project_id=42" | jq .
```

## The Audit

Real SEO starts with an audit, not with publishing. `/gsc-audit <domain>` (or [`references/audit-playbook.md`](./references/audit-playbook.md)) runs nine analyses from Distribb's own Search Console connection and a live crawl: CTR optimization, content decay, striking-distance / page-2 keywords, keyword cannibalization, dead pages, brand vs non-brand health, topical authority clusters (topic cocoons), competitor gaps, and basic on-page checks. It ends with a prioritized action plan wired into Distribb. Works on every plan.

## Backlink Exchange

Distribb connects real businesses that exchange backlinks. When your article includes a link to a network partner, Distribb detects it on submission and credits your project. More given = more received. Free plans receive 1 backlink/month; paid plans get unlimited exchange access. These are high-DR links from legitimate business websites.

## Bring-Your-Own-Keys (Free Agentic plan)

The Free Agentic plan does not bundle keyword data. Users save their own **DataForSEO** or **Ahrefs** API keys at [distribb.io/settings#seo-keys](https://distribb.io/settings#seo-keys). All other endpoints (articles, integrations, backlinks, audit) work normally without any keys.

When `/api/v1/keywords/search` is called by a Free Agentic user with no keys saved, the response is HTTP 402 with `"error": "byo_keys_required"` and an `instructions_for_agent` string. Surface that string to the user verbatim and do not retry until they have saved credentials.

## Microworkers Campaign Management

Distribb can create/register project-scoped Microworkers Basic Campaigns, list worker slots/submissions, and rate submissions as `OK`, `NOK`, or `REVISE`. Campaign creation requires `project_id`, `title`, `description`, and `template_html`; optional fields include `platform`, `campaign_type`, `category_id`, `available_positions`, `payment_per_task`, proof settings, and timing controls.

## References

| File | What it covers |
|---|---|
| [`references/audit-playbook.md`](./references/audit-playbook.md) | The full SEO audit workflow |
| [`references/onboarding-guide.md`](./references/onboarding-guide.md) | Everything onboarding collects + the website + GSC connections |
| [`references/platform-guide.md`](./references/platform-guide.md) | Where things live in the app (calendar, settings, backlinks, optimizations) |
| [`references/plans-and-backlinks.md`](./references/plans-and-backlinks.md) | Plans, the backlink exchange, and the Accelerator |
| [`references/statistics-page-playbook.md`](./references/statistics-page-playbook.md) | How `/statistics-page-writer` deep-researches and builds a journalist-ready statistics page |
| [`references/youtube-motion-video-playbook.md`](./references/youtube-motion-video-playbook.md) | How `/youtube-motion-video` makes a motion-collage explainer with the super-video-maker skill, YouTube-SEOs it, and publishes it to the connected YouTube channel |
| [`references/instagram-carousel-playbook.md`](./references/instagram-carousel-playbook.md) | How `/instagram-carousel` turns a Distribb article/keyword into a save-driven Instagram carousel for SEO: the Carousel Maker JSON contract, cover/hook system, design specs, the comment-for-link play, rendering, and the publish paths |

## Sub-skills

| Folder | What it does |
|---|---|
| [`90-day-seo-sprint/`](./90-day-seo-sprint/) | Run the Distribb 90-Day SEO Sprint: a phased program (Pre-launch / Foundation / Content Engine / Authority) built on the endpoints in this skill. Use when the user asks for an "SEO sprint", "90-day SEO plan", or "where do I start with SEO". |

## Command-line helpers (optional)

The skill works fully with `curl` + `jq` (no install). These Python helpers ship as optional conveniences:

| File | What it is |
|---|---|
| `distribb_cli.py` | A thin CLI over the same API (`projects:list`, `articles:create`, `keywords:search`, `suggestions:list`, etc.). `pip install requests python-dotenv`, then `export DISTRIBB_API_KEY=...`. |
| `distribb_research.py` | A standalone original-data research pipeline (plan -> scrape -> analyze) that produces a sourced hook + data table to weave into articles. Uses your own AI key; never invents data. |
| `distribb_writer.py` | A reference implementation showing how to write an SEO article locally with your own AI and submit it via the API. Meant to be modified or swapped out. |
| `news_topics.py` | Used by `/news-writer`. A stdlib-only Google News RSS scraper (no API key, no install) that surfaces fresh, recent headlines for a niche and writes `news_topics_export.csv` next to itself. |

## MCP Server (Cursor / Claude Desktop)

The MCP server exposes every Distribb endpoint as a native tool. See the [API docs](https://distribb.io/api-docs#ep-mcp) for setup.

## Get an API Key

Sign up at [distribb.io](https://distribb.io). Your API key is in Settings after you complete onboarding.
