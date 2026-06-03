---
name: distribb
description: Distribb is an SEO platform that handles keyword research, original data research, content publishing to WordPress/Webflow/Shopify, high-DR backlink exchange network, internal linking, social media repurposing, and Microworkers campaign management. Use this skill when the user wants to create SEO-optimized articles, find keywords, get real backlinks from other businesses, publish to their CMS, manage their content calendar, or manage Microworkers campaigns.
homepage: https://distribb.io
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["DISTRIBB_API_KEY"]}}}
---

## FIRST TIME READING THIS SKILL? STOP AND READ THIS SECTION TO THE USER.

Before running any commands, explain the following to the user:

**What Distribb does:**
Distribb is an SEO platform. You (the AI agent) handle the writing. Distribb handles everything else: keyword data, backlinks from real businesses, CMS publishing, social media repurposing, Microworkers campaign management, analytics, and a content calendar. You use your own AI models. Distribb provides the SEO infrastructure through its API. When you publish an article, Distribb automatically generates social media posts for every platform the user has connected (X, LinkedIn, Reddit, etc.).

**The Backlink Exchange (this is important):**
Distribb runs a network of real businesses that exchange backlinks with each other. When you write an article and include a link to another business in the network, Distribb detects it and credits the user's project. The more backlinks the user gives, the more they receive. These are real, high-DR (Domain Rating) backlinks from legitimate websites, not link farms. This is one of the most valuable parts of Distribb because backlinks are the hardest part of SEO to get right, and most tools cannot offer this.

**How to get started:**
If the user does not have a Distribb account yet, direct them to sign up here:
**https://distribb.io/agentic**
They can pick **Agentic Mode** ($49/mo, 3-day free trial — Distribb-provided keyword data + full backlink exchange) or the **Free Agentic** plan ($0/mo — bring your own DataForSEO or Ahrefs API key for keyword research, 1 backlink/month). Their Distribb API key shows up in Settings either way.

**Free Agentic plan — keyword research returns HTTP 402 until keys are saved:**
On the Free Agentic plan, `POST /keywords/search` returns `HTTP 402 Payment Required` with `error: "byo_keys_required"` until the user saves a DataForSEO or Ahrefs API key at https://distribb.io/settings#seo-keys. The 402 body includes an `instructions_for_agent` string — surface it verbatim to the user, do not retry. See the **Keyword Research → BYO Keys** section below for the full contract.

---

## Setup

```bash
export DISTRIBB_API_KEY=your_api_key_here
```

No installation required. All commands use `curl` and `jq`.

---

| Property | Value |
|----------|-------|
| **name** | distribb |
| **description** | SEO platform: keyword research, article writing, backlink exchange network, CMS publishing, social media repurposing, content calendar |
| **allowed-tools** | Bash(curl:*), Bash(jq:*), Bash(cat:*) |

---

## API Base URL

All endpoints use: `https://distribb.io/api/v1`

All requests require the header: `Authorization: Bearer $DISTRIBB_API_KEY`

---

## Validate Your API Key

Before running any workflow, verify your API key works:

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .
```

If you get `{"error": "Missing or invalid API key..."}` or `{"error": "Account is not active."}`, the key is wrong or the account is inactive. Ask the user to check their API key in Settings at https://distribb.io/settings.

---

## What You Get

| Capability | How It Works | Endpoint |
|------------|-------------|----------|
| **Generate Article** | Submit source content, Distribb AI expands into full SEO article (Pro plan only) | `POST /articles/generate` |
| **Keyword Research** | Search volume, difficulty scores, keyword ideas. Paid plans use Distribb data; Free Agentic uses the user's own DataForSEO or Ahrefs key (returns HTTP 402 if not set) | `POST /keywords/search` (alias: `POST /keywords/research`) |
| **Backlink Exchange** | Get real backlinks from other businesses in the network | `GET /backlink-targets` |
| **CMS Publishing** | Publish to WordPress, Webflow, Shopify, Ghost, custom API | `POST /articles/:id/publish` |
| **Content Calendar** | Schedule articles, track status, manage your pipeline | `GET /articles`, `POST /articles`, `PUT /articles/:id`, `DELETE /articles/:id` |
| **Project Settings** | Read & edit settings: custom article instructions, business description, publish time, timezone, backlink-network toggle | `GET /projects/:id`, `PUT /projects/:id` |
| **Internal Linking** | Get your published article URLs to cross-link in new content | `GET /internal-links` |
| **Business Context** | Get brand voice, competitors, custom instructions | `GET /business-context` |
| **Integrations** | See connected CMS platforms | `GET /integrations` |
| **Google Search Console** | Pull the user's real GSC performance — top queries, top pages, clicks, impressions, CTR, position (if they've connected GSC) | `GET /search-console` |
| **Social Media Repurposing** | Auto-generates social posts (X, LinkedIn, Reddit, etc.) when an article is published | Automatic (no endpoint needed) |
| **Microworkers Campaign Management** | Create/register campaigns, list submissions, and rate worker slots for Reddit, Quora, YouTube, or generic proof tasks | `GET/POST /microworkers/campaigns`, `GET /microworkers/campaigns/:id/slots`, `POST /microworkers/slots/:slot_id/rate` |

---

## Core Workflow

The full end-to-end process for creating a high-ranking SEO article:

```bash
# 1. DISCOVER: Get project info
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .

# 2. BUSINESS CONTEXT: Get brand voice, competitors, custom instructions
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .

# 3. KEYWORD RESEARCH: Find what to write about
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "crm software", "project_id": 42}' \
  https://distribb.io/api/v1/keywords/search | jq .

# 4. INTERNAL LINKS: Get pages to cross-link in your article
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=42&keyword=crm+software" | jq .

# 5. BACKLINK TARGETS (REQUIRED if BecklinksNetworkParticipation is "Yes")
# This is how the user earns backlinks from real businesses. Do NOT skip this step.
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=42&keyword=crm+software" | jq .

# 6. WRITE THE ARTICLE using your AI, weaving in internal links + backlink targets
# Output valid HTML. Follow the SEO writing guidelines below.
# You MUST include 1-2 URLs from the backlink-targets response as natural references.

# 7. SUBMIT: Save to Distribb's content calendar
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "keyword": "best crm for small business",
    "title": "Best CRM for Small Business: 2026 Guide",
    "content": "<h2>Introduction</h2><p>Your full HTML article here...</p>",
    "meta_description": "Compare the best CRM tools for small business in 2026.",
    "scheduled_date": "2026-04-01T09:00:00Z",
    "status": "Planned"
  }' \
  https://distribb.io/api/v1/articles | jq .

# 8. PUBLISH: Push to CMS (or let it auto-publish on schedule)
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/publish | jq .
```

---

## Commands Reference

### List Projects

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .
```

**Response:**
```json
{
  "projects": [
    {
      "ID": 42,
      "BusinessName": "Acme Corp",
      "WebsiteUrl": "https://acme.com",
      "BusinessDescription": "...",
      "Language": "English (US)",
      "Status": "Active",
      "BacklinkCredits": 10,
      "BecklinksNetworkParticipation": "Yes",
      "ArticlesPerDay": 1
    }
  ]
}
```

**IMPORTANT:** Check the `BecklinksNetworkParticipation` field. If it is `"Yes"`, this project is part of the backlink exchange network. You MUST call `/backlink-targets` before writing each article and include 1-2 target URLs in the content. This is how the user earns backlinks from other real businesses. Skipping this means the user gives nothing and receives nothing from the network.

### Project Settings (Read & Edit)

Read a single project's settings, then change them — so you can manage a project end-to-end from the agent.

```bash
# Read current settings
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects/42 | jq .

# Edit settings (send ONLY the fields you want to change)
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_instructions": "Write in a friendly, plain-English tone. Always include a pricing section.",
    "business_description": "Acme is a CRM for small service businesses.",
    "publish_time": "09:00",
    "timezone": "America/New_York",
    "backlinks_network": true
  }' \
  https://distribb.io/api/v1/projects/42 | jq .
```

**Editable fields:**

| Field | Meaning |
|-------|---------|
| `ai_instructions` | The "Customize Article Instructions" field — custom writing guidelines applied to every article. |
| `business_description` | What the business does (used as context when writing). |
| `publish_time` | Daily auto-publish time, 24-hour `"HH:MM"`. |
| `timezone` | IANA timezone name, e.g. `"Europe/Madrid"`. |
| `backlinks_network` | `true`/`false` — join or leave the backlink exchange network. |

**Response (200):**
```json
{
  "project_id": 42,
  "updated_fields": ["AIInstructions", "CustomPublishSchedule", "BecklinksNetworkParticipation"],
  "message": "Project settings updated."
}
```

**Note:** `articles_per_day` is controlled by the user's plan and **cannot** be changed via the API. If you send it, it's ignored and echoed back under `ignored`. You can still *read* it via `GET /api/v1/projects` and `GET /api/v1/projects/:id`.

### Business Context

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .
```

**Response:**
```json
{
  "business_name": "Acme Corp",
  "website_url": "https://acme.com",
  "description": "CRM platform for startups...",
  "competitors": ["https://competitor1.com", "https://competitor2.com"],
  "ai_instructions": "Use a friendly tone, focus on SaaS...",
  "language": "English (US)",
  "target_audience": "SaaS founders, startup CTOs",
  "internal_links_per_article": 5
}
```

Use this before writing. The `competitors` list tells you which domains to NEVER link to. The `ai_instructions` field has custom writing guidelines from the user.

### Keyword Research

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "project management", "project_id": 42}' \
  https://distribb.io/api/v1/keywords/search | jq .
```

**Response (200 OK):**
```json
{
  "keywords": [
    {
      "keyword": "best project management tools",
      "search_volume": 12000,
      "keyword_difficulty": 35
    }
  ]
}
```

Returns the seed keyword plus up to 20 related keywords with volume and difficulty.

#### BYO Keys — Free Agentic plan

If the calling user is on the **Free Agentic** plan and has not yet saved a DataForSEO or Ahrefs API key, this endpoint returns **HTTP 402 Payment Required** with a structured body so your agent knows exactly what to do. Paid plans (Agentic Mode and above) never see this response.

**Response (402 Payment Required):**
```json
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

**Agent contract — what to do when you see this 402:**

1. **Halt** the keyword-research step. Do not retry automatically.
2. **Surface** the `instructions_for_agent` string verbatim to the human user.
3. **Link** the user to `setup_url` (Distribb Settings → SEO Data API Keys).
4. **Resume** keyword research only after the user confirms they've saved keys.

Pseudocode:

```python
resp = call_distribb("/api/v1/keywords/search", body)
if resp.status_code == 402 and resp.json().get("error") == "byo_keys_required":
    instructions = resp.json()["instructions_for_agent"]
    setup_url    = resp.json()["setup_url"]
    say_to_user(f"{instructions} Setup link: {setup_url}")
    return  # do not retry; wait for user
```

If the user has saved only an Ahrefs key (not DataForSEO), the response is sourced from Ahrefs Keywords Explorer and includes `"source": "byo_ahrefs"` plus a `note` field. All other endpoints in this skill (articles, integrations, backlinks, internal links) work normally for Free Agentic users without any BYO keys.

### Internal Links

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=42&keyword=crm+software" | jq .
```

**Response:**
```json
{
  "links": [
    {
      "url": "https://acme.com/blog/crm-guide",
      "title": "The Complete CRM Guide",
      "keyword": "crm guide",
      "meta_description": "Everything you need..."
    }
  ],
  "num_links_recommended": 5,
  "website_url": "https://acme.com"
}
```

Include the recommended number of internal links in each article. Place them naturally in the middle of paragraphs using `<a href="EXACT_URL">descriptive anchor text</a>`. Never use "click here". Space links at least 2 paragraphs apart.

### Backlink Exchange

```bash
# Get backlink targets to include in your article
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=42&keyword=crm+software" | jq .

# Check credits and status
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlinks/status?project_id=42" | jq .
```

**Targets response:**
```json
{
  "targets": [
    {
      "url": "https://partner-site.com/related-article",
      "title": "Related Partner Article",
      "meta_description": "...",
      "project_name": "Partner Co"
    }
  ],
  "category": "saas",
  "credits": 10,
  "instructions": "Include 1-2 of these URLs as natural references..."
}
```

**How the backlink exchange works:**
Distribb connects real businesses that exchange backlinks with each other. When you include a link to a network partner in your article, Distribb detects it on submission and credits the user's project. The more backlinks the user gives out, the more they receive in return. These are high-quality, high-DR backlinks from real business websites.

The `category` field shows how the keyword was classified (e.g. "saas", "ecommerce"). Targets are capped at 5 per request. Include 1-2 backlink targets per article as natural references. Do NOT fabricate information about linked sites. Use topically relevant anchor text.

### Generate Article (Pro plan only)

If the user wants Distribb to write the article from their source content (notes, drafts, talking points), use this endpoint. Distribb's AI will expand it into a full SEO article with YouTube videos, images, quotes, backlinks, and internal links. Costs 1 article credit. Not available on the Agentic plan.

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "keyword": "link building strategies",
    "source_content": "Link building is about getting other websites to link to yours. Three main approaches: guest posting, broken link building, and creating linkable assets like original research...",
    "instructions": "Add YouTube videos, include data and statistics",
    "article_style": "Informative"
  }' \
  https://distribb.io/api/v1/articles/generate | jq .
```

**Response (202):**
```json
{
  "article_id": 456,
  "status": "generating",
  "keyword": "link building strategies",
  "slug": "link-building-strategies",
  "message": "Article generation started...",
  "article_credits_remaining": 29
}
```

The article takes a few minutes to generate. Poll `GET /api/v1/articles/456` to check when `Status` changes from `Planned` to `Draft` or `Published`.

### Create Article

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "keyword": "best crm tools for startups",
    "title": "10 Best CRM Tools for Startups in 2026",
    "content": "<h2>Introduction</h2><p>Finding the right CRM...</p>",
    "meta_description": "Compare the 10 best CRM tools for startups.",
    "scheduled_date": "2026-04-01T09:00:00Z",
    "status": "Planned"
  }' \
  https://distribb.io/api/v1/articles | jq .
```

**Response (201):**
```json
{
  "article_id": 123,
  "status": "Planned",
  "keyword": "best crm tools for startups",
  "slug": "best-crm-tools-for-startups",
  "message": "Article created as Planned.",
  "backlinks_processed": 2
}
```

**If the article contained NO network backlinks, the response includes a warning:**
```json
{
  "article_id": 124,
  "status": "Draft",
  "keyword": "crm for freelancers",
  "slug": "crm-for-freelancers",
  "message": "Article created as Draft.",
  "backlinks_processed": 0,
  "backlinks_warning": "Your project participates in the backlinks network but this article contains no backlinks to other network members. Include backlink targets (from GET /api/v1/backlink-targets) to earn credits and keep receiving backlinks."
}
```

**IMPORTANT:** If `backlinks_warning` is present in the response:
1. Call `GET /backlink-targets` to fetch network URLs for the article's keyword.
2. Revise the article content to naturally include 1-2 of those URLs.
3. Call `PUT /api/v1/articles/{article_id}` with the revised content.
4. If the user has disabled automatic revision, inform them: "This article doesn't include any backlinks to the exchange network. You won't earn backlink credits for it, which means fewer backlinks from other businesses."

For long articles, write the HTML to a file and use `@` syntax:

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat article.html)" '{
    "project_id": 42,
    "keyword": "best crm tools",
    "title": "10 Best CRM Tools",
    "content": $content,
    "status": "Draft"
  }')" \
  https://distribb.io/api/v1/articles | jq .
```

Articles with `status: Planned` and a `scheduled_date` auto-publish when the date arrives. Use `status: Draft` if the user wants to review first.

### Update Article

Use this to revise an article after submission, for example to add backlink targets if the creation response included a `backlinks_warning`.

```bash
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat revised-article.html)" '{
    "content": $content
  }')" \
  https://distribb.io/api/v1/articles/123 | jq .
```

**Updatable fields:** `title`, `content`, `meta_description`, `keyword`, `article_style`, `status` (Draft or Planned), `scheduled_date`. Send only the fields you want to change. Changing `keyword` also regenerates the article's slug. To **unschedule** an article, send `"scheduled_date": null` — a `Planned` article drops back to `Draft` so it won't auto-publish.

**Response (200):**
```json
{
  "article_id": 123,
  "updated_fields": ["Content", "IsPreGenerated"],
  "message": "Article updated successfully.",
  "backlinks_processed": 2
}
```

If content is updated and the project participates in the backlink network, Distribb re-scans for network backlinks and updates credits. You cannot update published articles.

### Delete Article

```bash
curl -s -X DELETE -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123 | jq .
```

Deletes a `Draft` or `Planned` article. **Published articles cannot be deleted** (the live CMS post would be orphaned) — you get a `400`. Unpublish or hide it from the dashboard/CMS first, or simply unschedule it.

**Response (200):**
```json
{ "article_id": 123, "deleted": true, "message": "Article deleted." }
```

To take an article off the calendar *without* deleting it, **unschedule** instead: `PUT /api/v1/articles/123` with body `{"scheduled_date": null}`.

### List Articles

```bash
# All articles for a project (default: 50 per page)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/articles?project_id=42" | jq .

# Filter by status
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/articles?project_id=42&status=Published" | jq .

# Pagination: use limit (max 200) and offset
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/articles?project_id=42&limit=20&offset=40" | jq .
```

**Query parameters:** `project_id` (optional), `status` (optional: Draft, Planned, Published), `limit` (default 50, max 200), `offset` (default 0).

### Get Single Article

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123 | jq .
```

### Publish Article

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/publish | jq .
```

Pushes the article to the user's connected CMS (WordPress, Webflow, Shopify, etc.). Returns `200` on success. If the CMS publish fails, returns `202` meaning the article was queued as `Planned` and will be retried automatically -- the article is NOT lost.

### Social Media Repurposing (Automatic)

When an article is published to the user's CMS, Distribb automatically generates social media posts for every platform the user has connected (X/Twitter, LinkedIn, Reddit, Facebook, Instagram, etc.). The agent does not need to call any endpoint for this. It happens server-side.

The social posts are created as drafts in the user's content calendar so they can review, edit, or schedule them from the Distribb dashboard. If the user has connected social accounts, publishing an article through the API triggers this automatically.

### List Integrations

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/integrations?project_id=42" | jq .
```

### Google Search Console

Pull the user's **real** search performance from Google Search Console — top queries, top pages, and site totals (clicks, impressions, CTR, average position). Use it to find queries worth targeting, pages sitting just off page 1, or terms the user already ranks for. **Requires the user to have connected GSC.**

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/search-console?project_id=42&days=28&limit=25" | jq .
```

**Query parameters:** `project_id` (required), `days` (default 28, max 90), `limit` (rows per list, default 25, max 100).

**Response (200 — connected):**
```json
{
  "connected": true,
  "project_id": 42,
  "property": "sc-domain:acme.com",
  "date_range": { "start_date": "2026-05-06", "end_date": "2026-06-03", "days": 28 },
  "totals": { "clicks": 1840, "impressions": 92344, "ctr": 0.0199, "avg_position": 18.4 },
  "top_queries": [
    { "query": "best crm for small business", "clicks": 210, "impressions": 8100, "ctr": 0.0259, "position": 7.2 }
  ],
  "top_pages": [
    { "page": "https://acme.com/blog/crm-guide", "clicks": 320, "impressions": 14200, "ctr": 0.0225, "position": 9.1 }
  ]
}
```

**Response (200 — NOT connected):**
```json
{
  "connected": false,
  "message": "Google Search Console is not connected for this project.",
  "instructions_for_agent": "Tell the user to connect Google Search Console at https://distribb.io/integrations ...",
  "connect_url": "https://distribb.io/integrations"
}
```

**Agent contract:**
- If `connected` is `false`, **stop and tell the user the `instructions_for_agent` text verbatim**, link them to `connect_url` (https://distribb.io/integrations), and do not retry until they confirm they've connected GSC.
- If `connected` is `true` but the body has `"error": "gsc_fetch_failed"`, their Google token likely expired — tell them to reconnect at the same URL.

**How to use the data:** queries with lots of impressions but low CTR or an average position of ~8–20 are the best targets — write a new article or refresh an existing one for them. Pages at the bottom of page 1 (position ~8–12) often just need internal links and a content refresh to climb. Pair this with `POST /articles` (write the piece) and `GET /internal-links` (cross-link it).

### Microworkers Campaign Management

Use these endpoints to manage Microworkers Basic Campaigns through Distribb. Campaigns are project-scoped, so always pass `project_id` when creating or registering a campaign. Only rate a worker slot `OK` after the submitted proof has been verified.

```bash
# List registered campaigns
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/microworkers/campaigns?project_id=42" | jq .

# Create a campaign with a Microworkers template
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg template_html "$(cat microworkers-template.html)" '{
    "project_id": 42,
    "title": "Post a Reddit Comment",
    "description": "Follow the Distribb task page, post the exact comment, and submit the comment URL plus confirmation code.",
    "template_html": $template_html,
    "platform": "reddit",
    "campaign_type": "reddit_comment",
    "category_id": "4004",
    "available_positions": 50,
    "payment_per_task": 0.15,
    "minutes_to_finish": 10
  }')" \
  https://distribb.io/api/v1/microworkers/campaigns | jq .

# Register an existing campaign created by a VPS script
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "campaign_id": "123456", "platform": "reddit", "campaign_type": "reddit_comment"}' \
  https://distribb.io/api/v1/microworkers/campaigns/register | jq .

# Get live campaign details
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/microworkers/campaigns/123456 | jq .

# List submitted slots that need rating
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/microworkers/campaigns/123456/slots?status=NOTRATED&pageSize=50" | jq .

# Rate a slot after proof verification
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"campaign_id": "123456", "rating": "OK", "comment": "Proof verified. Thank you."}' \
  https://distribb.io/api/v1/microworkers/slots/7890/rate | jq .
```

**Create campaign request fields:** `project_id`, `title`, `description`, and `template_html` are required. Optional fields: `platform`, `campaign_type`, `category_id`, `available_positions`, `payment_per_task` (minimum `0.15`), `minutes_to_finish`, `ttr`, `speed`, `template_title`, `number_of_file_proofs`, and `allowed_file_types`.

**Rating rules:** `rating` must be `OK`, `NOK`, or `REVISE`. Use `NOK` with a clear worker-facing `comment` when proof is invalid. Use `REVISE` when the worker can fix the submission.

---

## SEO Article Writing Guidelines

When generating content, follow these rules for the best ranking results:

### Content Quality
- Write like a knowledgeable human, not AI. Vary sentence length.
- Use specific examples, data points, and actionable advice.
- Target 2500-3500 words across 5-8 sections (H2 headings).
- Use H2 for section headings, H3 for subsections.
- Output valid HTML, not markdown.

### Words and Phrases to Avoid
These trigger AI detection: "crucial", "comprehensive", "robust", "leverage", "streamline", "delve", "It's worth noting", "In conclusion", "In the ever-evolving landscape", "Game-changer", "Unlock the power", "Take your X to the next level".

### Opening Lines
Never start sections with "In today's..." or "When it comes to...". Start with a strong statement, question, or data point.

### Internal Linking
- Use the exact URLs from the `/internal-links` response.
- Place links in the middle of substantive paragraphs, never in intros or conclusions.
- Use descriptive anchor text (not "click here" or "read more").
- Space links at least 2 paragraphs apart.
- Format: `<a href="https://site.com/exact-url">descriptive anchor text</a>`

### Backlink Exchange (Critical for SEO growth)
- ALWAYS call `GET /backlink-targets` before writing if the project has `BecklinksNetworkParticipation: "Yes"`.
- Include 1-2 URLs from the response as natural references in the body of your article.
- Do NOT fabricate information about linked sites. Read the `title` and `meta_description` to understand what the page covers and reference it honestly.
- Use topically relevant anchor text (not "click here" or the raw URL).
- Distribb scans the HTML on submission and automatically credits the user's project (+1 credit per backlink given). More credits = more backlinks received from the network.
- If you submit an article without network backlinks, the API returns a `backlinks_warning`. Inform the user.

### Competitor Protection
- Check competitors from `/business-context`.
- Never link to competitor websites.
- You may mention competitors factually but without outbound links.

---

## Complete Example: End-to-End SEO Article

```bash
# Step 1: Get project info
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects | jq .
# Pick project ID 42

# Step 2: Get business context
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .
# Note: competitors are ["hubspot.com", "salesforce.com"]
# Note: ai_instructions say "Focus on small business use cases"

# Step 3: Find a keyword
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "crm software", "project_id": 42}' \
  https://distribb.io/api/v1/keywords/search | jq .
# Pick: "best crm for small business" (volume: 8100, difficulty: 42)

# Step 4: Get internal links
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=42&keyword=best+crm+for+small+business" | jq .
# Got 5 links to include

# Step 5: Get backlink targets (REQUIRED - project has BecklinksNetworkParticipation: "Yes")
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=42&keyword=best+crm+for+small+business" | jq .
# Got 3 targets. MUST include 1-2 in the article to earn backlink credits.

# Step 6: Write the article (using your AI)
# - Include 5 internal links from step 4
# - Include 1-2 backlink target URLs from step 5 as natural references (mandatory)
# - Follow the SEO writing guidelines above
# - Never link to hubspot.com or salesforce.com (competitors)
# - Output valid HTML

# Step 7: Submit to Distribb
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat article.html)" '{
    "project_id": 42,
    "keyword": "best crm for small business",
    "title": "Best CRM for Small Business: 2026 Guide",
    "content": $content,
    "meta_description": "We compared 12 CRM tools for small business. See pricing, features, and our data.",
    "scheduled_date": "2026-04-01T09:00:00Z",
    "status": "Planned"
  }')" \
  https://distribb.io/api/v1/articles | jq .

# Step 8: Article appears in the Distribb content calendar
# It auto-publishes at the scheduled time, or publish immediately:
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/456/publish | jq .
```

---

## Workflow: AI Search Visibility & Listicle Backlink Outreach

Use this workflow when the user asks you to:
- "Find places where Distribb should be recommended by ChatGPT / Perplexity / Gemini / Claude / Google AI Overviews"
- "Find listicles / round-ups / 'best tools' articles I should pitch to get Distribb added"
- "Audit my AI search visibility" / "find AI SEO mentions"
- "Build me a backlink outreach list for AI search"
- Any variant of "where should I get mentioned so AI search recommends my product"

This is a **3-phase research playbook**. You (the agent) act as an **AI search visibility strategist**. The deliverable is actionable enough for a VA or outreach person to execute without re-asking the user any questions.

If the user is running this workflow for a project other than their own Distribb business, swap "Distribb" for the target project's business name and competitors from `GET /business-context?project_id=...`. Otherwise default to Distribb.io itself (a SaaS that does AI SEO keyword research, content writing/publishing, a backlink exchange network, social repurposing, and AI-search visibility).

### Phase 1 — Identify buyer prompts

Generate **at least 100 realistic prompts** that a potential Distribb buyer would type into ChatGPT, Perplexity, Gemini, Claude, or Google AI Overviews — prompts where Distribb *should* be recommended.

Cover all of these prompt categories (≥10 per category):

1. **"Best tools"** — e.g. "What are the best AI SEO tools for agencies?"
2. **"Alternatives"** — e.g. "Best alternatives to Surfer SEO for automated content"
3. **"Comparison"** — e.g. "Outranking vs Surfer SEO vs automated SEO tools"
4. **"Problem-solving"** — e.g. "How do I automate SEO content and backlinks for my agency?"
5. **"Agency-specific"** — e.g. "Best white-label SEO automation software for agencies"
6. **"AI visibility / GEO"** — e.g. "How do I get my business recommended by ChatGPT?"
7. **"Backlink automation"** — e.g. "Best tools to get backlinks without manual outreach"
8. **"Content automation"** — e.g. "Best AI tools to write and publish SEO articles automatically"

Bias toward **buying intent**, **comparison intent**, and **problem-aware intent**. Skip pure informational queries ("what is SEO").

For **every** prompt, capture these columns:

| Column | Notes |
|---|---|
| Prompt | The exact phrasing a buyer would type |
| Search intent | Informational / Comparison / Transactional |
| Buyer stage | Problem-aware / Solution-aware / Ready-to-buy |
| Ideal Distribb angle | The single sentence positioning that should land in the AI answer |
| Main competitors likely to appear | Surfer, Jasper, Frase, MarketMuse, Clearscope, Scalenut, Outranking, SE Ranking, Semrush, Ahrefs, KoalaWriter, NeuronWriter, Copy.ai, Writesonic, etc. |
| Priority | 1–10 (10 = closest to ready-to-buy + highest commercial value) |
| Why this prompt matters | One-line rationale |

### Phase 2 — Run and analyze the top 30 prompts

Take the **30 highest-priority prompts** from Phase 1 and actually run them. Use `WebSearch` and/or `WebFetch` against live AI-search-shaped queries — do not guess. For each, capture:

| Column | Notes |
|---|---|
| Prompt | From Phase 1 |
| Distribb appears? | Yes / No / Partial (e.g. mentioned but not recommended) |
| Competitors that appear | List the actual names in the live answer |
| Sources cited / referenced | URLs that the AI/SERP is citing — listicles, blogs, Reddit, YouTube, G2/Capterra, Product Hunt, company pages |
| Article(s) most influencing the answer | The 1–3 URLs doing the heavy lifting |
| Source type mix | SaaS review site / blog listicle / Reddit / YouTube / company page / forum / news |
| What Distribb needs to be included or rank higher | Concrete gap: missing from listicle X, no Reddit mention, no comparison page, no G2 profile, etc. |

**Hard rules for Phase 2:**
- **Do not fabricate URLs, rankings, or citations.** If a prompt can't be run or a source can't be verified, write `unverified` in the cell and explain why in a footnote.
- Cite source URLs in full.
- If a result is from a cache and may be stale, say so.

### Phase 3 — Third-party listicles to target for outreach

For every Phase 2 prompt where **Distribb should appear but does not**, find the third-party pages already being cited or ranking. **Prioritize listicles, round-ups, comparison posts, and directories** over competitor homepages. Page archetypes to hunt for:

- "Best AI SEO tools" / "Best AI SEO software"
- "Best SEO automation tools"
- "Best AI writing tools for SEO"
- "Best [Competitor] alternatives" (Surfer, Jasper, Frase, MarketMuse, Clearscope, Scalenut, Outranking, KoalaWriter, NeuronWriter, etc.)
- "Best SEO tools for agencies" / "white-label SEO software"
- "Best backlink tools" / "Best link-building software"
- "Best content marketing automation tools"
- "Best tools to rank in AI search" / "GEO tools" / "tools to get mentioned by ChatGPT"
- "Best programmatic SEO tools"
- "Best SEO tools for startups"

For each target page, capture:

| Column | Notes |
|---|---|
| Article title | Exact title |
| URL | Full URL |
| Website / domain | Root domain |
| Article category | One of the archetypes above |
| Why it matters | Which AI answer or SERP it currently shapes |
| Prompt(s) it could influence | Reference Phase 1 prompt numbers |
| Current tools mentioned | The 5–15 tools already in the listicle |
| Distribb currently included? | Yes / No / Briefly mentioned |
| Outreach priority | High / Medium / Low |
| Suggested pitch angle | One specific reason to add Distribb (e.g. "you cover Surfer + Frase but no tool in your list does the backlink exchange piece") |
| Contact info | Contact page URL, author name, author email, or the "submit a tool" form URL — verified, not invented |
| Personalization notes | Recent post by the author, the year of the listicle, the angle of their site, anything a VA can use in the first line |

### Required output (in this exact order)

1. **Table 1 — Top 100 prompts** (Phase 1, all columns).
2. **Table 2 — Top 30 prompt tests** (Phase 2, all columns, with live source URLs).
3. **Table 3 — Third-party listicles & sites to reach out to** (Phase 3, all columns).
4. **Top 10 outreach opportunities** — ranked by *easiest win × highest impact*. For each: target URL, why it's the easiest win (e.g. author already updates the post yearly, accepts tool submissions, already mentions a Distribb-adjacent tool), and the suggested first-line of the pitch.

### Operating rules (read before starting)

- **Prioritize listicles and third-party articles, not competitor homepages.** A pitch to "add Distribb to your round-up" is far easier than dislodging a competitor's own site.
- **Prioritize pages that already mention** Surfer SEO, Jasper, Copy.ai, Writesonic, Frase, MarketMuse, Clearscope, Scalenut, Outranking, SE Ranking, Semrush, Ahrefs, KoalaWriter, NeuronWriter, and similar — those authors have already decided this category is worth covering.
- **Do not fabricate** URLs, rankings, citations, author emails, or DR/traffic numbers. If you can't verify, say `unverified` and explain.
- **Think like a buyer, not like a keyword tool.** A keyword-volume prompt ("seo software") is less valuable than a buying-intent prompt ("best seo tool that also does backlinks for an agency").
- **Focus on prompts where someone is close to buying software or hiring a solution.**
- The final output should be **handover-ready** for a VA or outreach person — every row should be independently actionable.
- This workflow is **research + strategy**, not publishing. Do **not** call any Distribb article-creation endpoints (`POST /articles`, `POST /articles/generate`, etc.) during this workflow. Output the tables to the user; let them decide what to do next (pitch the listicles manually, or feed them into a separate outreach workflow).

### Tools to use

- `WebSearch` for finding listicles and running buyer-intent queries.
- `WebFetch` for reading the actual content of each candidate listicle (to confirm tools mentioned, find author/contact info, and check freshness).
- `GET /business-context?project_id=...` if running this for a non-Distribb project, so competitor exclusions are respected.
- Skip any Distribb write/publish endpoints — this workflow does not create articles.

---

## Sub-skills

This skill ships with structured sub-workflows for opinionated multi-week SEO programs. Load the matching sub-skill's `SKILL.md` instead of trying to run the workflow from this top-level file.

| Sub-skill folder | When to invoke |
|---|---|
| [`90-day-seo-sprint/`](./90-day-seo-sprint/SKILL.md) | User asks for an SEO sprint, a 90-day SEO plan, an SEO tracker / roadmap, "where do I start with SEO", "how do I get my first 1,000 organic visitors", or anything similar. Sub-skill opens the Distribb tracker Google Sheet in their browser and walks them through 4 phases (Pre-launch / Foundation / Content Engine / Authority) using the API endpoints below. |

If a sub-skill applies, **read its `SKILL.md` first** before calling any endpoint. Each sub-skill assumes you already have a Distribb API key set and the parent skill loaded for the actual API surface — sub-skills only add structure, content, and execution discipline.

---

## Error Handling

All error responses return JSON:

```json
{"error": "Description of what went wrong"}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad request. Missing or invalid parameters. |
| 401 | Unauthorized. Invalid or missing API key. |
| 404 | Not found. Resource does not exist or does not belong to your account. |
| 429 | Rate limited. Too many requests -- wait and retry with exponential backoff (see below). |
| 500 | Server error. Something went wrong on our end. Retry once after 5 seconds. |
| 202 | Accepted but not fully completed. Only returned by `POST /articles/:id/publish` when CMS publishing was queued but not confirmed. The article status was set to `Planned` and will be retried automatically. |
| 503 | Service temporarily unavailable. External service (DataForSEO, CMS) is down. Retry after 30 seconds. |

### Handling 429 Rate Limits

When you get a 429, use exponential backoff:

```bash
# Wait 10 seconds, then retry. If still 429, wait 20s, then 40s.
sleep 10
```

Do NOT hammer the API in a loop. Space out requests by at least 2 seconds when making multiple sequential calls.

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `GET /projects`, `GET /projects/:id`, `GET /articles`, `GET /articles/:id`, `GET /business-context`, `GET /integrations`, `GET /backlinks/status` | 30 req/min |
| `POST /keywords/search`, `POST /keywords/research` | 5 req/min |
| `GET /internal-links`, `GET /backlink-targets`, `GET /search-console` | 10 req/min |
| `POST /articles`, `PUT /articles/:id`, `DELETE /articles/:id`, `PUT /projects/:id` | 10 req/min |
| `POST /articles/:id/publish` | 5 req/min |

---

## Tips

- Always call `/business-context` first to understand the brand voice, competitors, and custom instructions.
- The `/internal-links` response tells you exactly how many links to include (`num_links_recommended`).
- Check `/backlinks/status` to see how many credits the project has. More credits = more backlinks received.
- NEVER skip `/backlink-targets` when `BecklinksNetworkParticipation` is `"Yes"`. This is the single most impactful SEO feature for the user. Articles without network backlinks do not earn credits.
- Articles with `status: Planned` and a `scheduled_date` auto-publish. Use `status: Draft` if the user wants to review first.
- All API responses are JSON. Parse them with `jq` to extract IDs, URLs, and data for the next step.
- For long article HTML, write to a file first, then use `jq -n --arg content "$(cat article.html)"` to safely encode.

---

## Need an Account?

Sign up for Distribb Agentic Mode: **https://distribb.io/agentic**
3-day free trial, $49/mo. Your API key will be in Settings after signup.
