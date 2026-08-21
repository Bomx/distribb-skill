---
name: distribb
description: Distribb is an SEO platform that handles keyword research, original data research, content publishing to WordPress/Webflow/Shopify, high-DR backlink exchange network, link building outreach playbooks, internal linking, social media repurposing and posting, Google Business Profile management (live reviews, public review replies, Google posts), and Microworkers campaign management. Use this skill when the user wants to create SEO-optimized articles, find keywords, get real backlinks from other businesses, run link building or backlink outreach campaigns, publish to their CMS, manage their content calendar, manage their Google Business Profile and its reviews, post to their connected social accounts, or manage Microworkers campaigns.
homepage: https://distribb.io
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["DISTRIBB_API_KEY"]}}}
---

## FIRST TIME READING THIS SKILL? STOP. WALK THE USER THROUGH THIS BEFORE ANYTHING ELSE.

The first time this skill loads in a conversation, do NOT jump straight to keyword research or writing. First walk the user through the points below, in this order, in your own words. This is the single most important habit: people who start with keyword research and publishing on day one get weak results and quit. People who follow the process get results.

### A. What Distribb is, in one breath

Distribb is your SEO platform. You (the AI agent) do the thinking and the writing. Distribb provides the infrastructure: real keyword data, a backlink exchange network of real businesses, Google Search Console analysis, CMS publishing (WordPress, Webflow, Shopify, Ghost, Wix, Notion, GoHighLevel, Framer, or any API webhook), a content calendar, social repurposing, and done-for-you distribution on the Accelerator plan. You bring your own AI model. Distribb does everything around the writing.

### B. The proper SEO process (show this list to the user every first run)

Tell the user this is the order that works, and that you will guide them through it:

1. **Create your account and go through onboarding** at https://distribb.io . Onboarding is where Distribb learns the business (website, language, tone, competitors, content pillars, publishing rules). Do not skip it. Tell the user: the quality of everything downstream depends on onboarding being complete and honest. See `references/onboarding-guide.md` for exactly what onboarding asks and why.
2. **Connect the two things that matter most: the website (CMS) and Google Search Console.** The CMS connection lets Distribb publish. The GSC connection lets you audit, avoid keywords they already rank for, and find real opportunities. Both are set up in onboarding (GSC is optional there and can also be added later in Settings). See `references/onboarding-guide.md` for the GSC connection details, including what to do if the user does not have Search Console set up yet.
3. **Make sure there is a blog to publish to.** Many sites have no blog or no blog index page. Without one, articles have nowhere to live. Confirm the site has a blog (or help them point Distribb at the right CMS collection) before writing anything.
4. **Audit the site BEFORE writing a single article.** This is step one of real SEO, not keyword research. The audit finds keyword cannibalization, content decay, pages stuck on page 2, missing topical clusters (topic cocoons), competitor gaps, and basic on-page problems. Run `/gsc-audit <domain>` or follow `references/audit-playbook.md`. The audit is available on every plan.
5. **Plan topical clusters, then do keyword research.** Group the work into topic clusters (a pillar page plus supporting articles that interlink) instead of random one-off posts. Then use keyword research to fill each cluster. See `references/audit-playbook.md` (topical authority section).
6. **Write and publish, always feeding the backlink exchange.** Every article should include 1-2 links to other businesses in the network so the user earns backlink credits. Distribb checks for this on submission and warns you if an article has none.
7. **Optimize what already ranks.** Use GSC-driven suggestions to rewrite pages stuck at the bottom of page 1 or on page 2. This is the fastest win because the page already has authority. Run `/optimize`.

This whole skill exists to run that loop for the user. When in doubt, point them back to it.

### C. The Backlink Exchange (explain this clearly, it is the differentiator)

Distribb runs a network of real businesses that exchange backlinks. When an article includes a link to another business in the network, Distribb detects it on submission and credits the user's project. The more links the user gives, the more they receive. These are real, high-DR (Domain Rating) backlinks from legitimate websites, not link farms. **Every current plan gets unlimited exchange access. Legacy Free Agentic accounts receive 1 backlink per month.** Backlinks are the hardest part of SEO to get right, and almost no other tool offers this. See `references/plans-and-backlinks.md`.

### D. Slash commands

This skill ships ready-to-use slash commands so the user can drive the whole workflow with `/`:

| Command | What it does |
|---|---|
| `/distribb` | Overview, account status, and the proper SEO process above |
| `/distribb-setup` | Check the API key, confirm website + GSC are connected, and enable the other slash commands |
| `/gsc-audit <domain>` | Full SEO audit from Search Console + on-page + competitor + cannibalization + topic clusters |
| `/keyword-research <seed>` | Keyword ideas with volume and difficulty |
| `/write-article <keyword>` | Research, write, add internal links + backlinks, and publish one article |
| `/optimize` | Find and rewrite pages stuck on page 2+ using GSC data |
| `/backlinks` | Check backlink credits, see targets, and explain how the exchange works |
| `/content-calendar` | List, schedule, and manage planned/draft/published articles |
| `/ai-visibility` | Find where the user should be recommended by ChatGPT/Perplexity/Gemini and which listicles to pitch |
| `/news-writer <site-url-or-niche>` | Newsjack: find fresh news in the niche, write grounded news drafts, and queue them in Distribb |
| `/statistics-page-writer <topic>` | Deep-research and publish a sourced statistics page journalists cite for months |
| `/youtube-motion-video <topic>` | Make a faceless motion-collage explainer video ("In a Nutshell" docu style), optimize it for YouTube SEO, and publish it to the connected YouTube channel |
| `/instagram-carousel <article-id-or-keyword>` | Turn one article/keyword into a viral, save-driven Instagram carousel (cover hook, one idea per slide, comment-for-link play), publish it, and close the loop with a companion article |
| `/review-video <competitor>` | Compile REAL, verified reviews of a competitor into a faceless "<competitor> reviews" video, position the connected project's own business as the alternative, append the project's own testimonials, and publish to YouTube + a companion article |
| `/gbp` | Google Business Profile manager: live review triage, draft + post public review replies, queue Google Business posts, post analytics |
| `/link-outreach` | Work your backlink outreach replies: see which listicle authors replied (and their asking price), draft and send in-thread replies from Distribb's inbox (Accelerator) |
| `/gov-backlinks` | Register the business in free government directories (SAM.gov, the SBA small business listing, state vendor portals) by driving the user's browser, for real .gov profile backlinks |

If these commands are not yet available when the user types them, run `/distribb-setup` (or copy this skill's `commands/*.md` into the project's `.claude/commands/` folder) to register them. See the **Slash Commands** section below.

### E. Getting an account

If the user has no Distribb account yet, send them to **https://distribb.io** to sign up and go through onboarding. Their Distribb API key appears in Settings afterward. Plans at a glance (full detail in `references/plans-and-backlinks.md`):

- **Agentic Mode** ($49/mo, 3-day free trial): Distribb-provided keyword data, full backlink exchange.
- **Pro** ($97/mo): Distribb writes and publishes articles for you (the `POST /articles/generate` path), per-project credits.
- **Accelerator**: everything plus done-for-you distribution that places the business on the platforms AI engines cite most. See section below and `references/plans-and-backlinks.md`.

The free Agentic plan ($0/mo) is deprecated and no longer offered to new users. Current plans are Agentic Mode at $49/month and Pro at $97/month.

**Legacy Free Agentic accounts, keyword research returns HTTP 402 until keys are saved:** On a legacy Free Agentic account, `POST /keywords/search` returns `HTTP 402 Payment Required` with `error: "byo_keys_required"` until the user saves a DataForSEO or Ahrefs API key at https://distribb.io/settings#seo-keys. The 402 body includes an `instructions_for_agent` string. Surface it verbatim to the user, do not retry. See the **Keyword Research, BYO Keys** section below for the full contract.

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
| **allowed-tools** | Bash(curl:*), Bash(jq:*), Bash(cat:*), WebFetch, WebSearch, Read, Write |

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
| **Keyword Research** | Search volume, difficulty scores, keyword ideas. Current plans use Distribb data; legacy Free Agentic accounts use the user's own DataForSEO or Ahrefs key (returns HTTP 402 if not set) | `POST /keywords/search` (alias: `POST /keywords/research`) |
| **Backlink Exchange** | Get real backlinks from other businesses in the network | `GET /backlink-targets` |
| **Backlink Ledger** | Full link-level detail behind the aggregate status: earned + scheduled links (source domain, DR, business, target URL, status, date) plus a velocity/gap summary | `GET /backlinks` |
| **CMS Publishing** | Publish to WordPress, Webflow, Shopify, Ghost, custom API | `POST /articles/:id/publish` |
| **Content Calendar** | Schedule articles, track status, manage your pipeline | `GET /articles`, `POST /articles`, `PUT /articles/:id`, `DELETE /articles/:id` |
| **Feature Image** | Attach a hero image URL to an article (cannot generate one; supply the URL) | `POST /articles`, `PUT /articles/:id` with `feature_image` |
| **Project Settings** | Read & edit the FULL settings surface (~30 fields): instructions, sitemap/blog URLs, content pillars, tone, writing profile, positioning, images/brand, competitors, toggles, publish time/timezone | `GET /projects/:id`, `PUT /projects/:id` |
| **Create + Onboard Project** | Create a new project (gated to paid slots; returns a buy-a-slot link if over) and optionally start keyword research + first articles. Ask the user before running research. Connect WordPress via API too | `POST /projects`, `POST /projects/:id/onboarding`, `POST /projects/:id/wordpress` |
| **Internal Linking** | Get your published article URLs to cross-link in new content | `GET /internal-links` |
| **Business Context** | Get brand voice, competitors, custom instructions | `GET /business-context` |
| **Integrations** | See connected CMS platforms | `GET /integrations` |
| **Google Search Console** | Pull the user's real GSC performance, top queries, top pages, clicks, impressions, CTR, position (if they've connected GSC). Aliased as `GET /rankings` and `GET /analytics` (search performance, NOT web-session analytics) | `GET /search-console` |
| **Google Business Profile** | Live Google reviews (reviewer, rating, text, reply status), post/delete the business's PUBLIC review replies, queue Google Business posts, post-level analytics (if they've connected Google Business) | `GET /gbp/status`, `GET /gbp/reviews`, `POST\|DELETE /gbp/reviews/reply`, `POST /gbp/posts`, `GET /gbp/analytics` |
| **Link Outreach** | Listicle authors who replied to the user's managed backlink outreach (their message + any asking price), and sending an in-thread reply from Distribb's warmed inbox on the user's behalf (Accelerator only) | `GET /link-outreach/prospects`, `POST /link-outreach/prospects/:id/reply` |
| **AI Visibility (AEO)** | Distribb's already-tracked AI-search visibility: visibility score, share-of-voice, per-engine citation status (ChatGPT, Perplexity, Gemini, AI Overviews, AI Mode), cited pages, on-demand scans. Track your **own buyer-query prompts** (up to 25/project, scanned first) and scan AI Overview / AI Mode / ChatGPT / Gemini from the client's **own city** via `primary_location` | `GET /ai-visibility`, `POST /ai-visibility/scan`, `POST\|DELETE /ai-visibility/prompts` |
| **Content Optimizations** | Find pages worth rewriting (mostly from GSC), review the AI's before/after diff, then approve and publish the rewrite to the CMS. Filter by opportunity with `?type=` (cannibalisation, declining_page, striking_distance, ctr_underperform, ...) | `GET /suggestions`, `POST /suggestions/run`, `POST /suggestions/:id/approve\|publish\|regenerate\|reject` |
| **Social Media Repurposing** | Auto-generates social posts (X, LinkedIn, Reddit, etc.) when an article is published | Automatic (no endpoint needed) |
| **Social Media Posting** | Write a post and send it to the user's connected accounts, now or scheduled | `GET /social/accounts`, `POST /social/publish` |
| **Microworkers Campaign Management** | Create/register campaigns, list submissions, and rate worker slots for Reddit, Quora, YouTube, or generic proof tasks | `GET/POST /microworkers/campaigns`, `GET /microworkers/campaigns/:id/slots`, `POST /microworkers/slots/:slot_id/rate` |

---

## Start Here: Onboarding and the Two Connections

Before any keyword research or writing, the user must have completed onboarding at https://distribb.io and connected two things. Everything downstream depends on this.

**What onboarding collects** (so you know what Distribb already knows, and what to fill if it is thin): the website URL, then an AI pass that auto-populates business details. It captures language, tone (Informative / Conversational / Persuasive), writing profile (Experienced practitioner / Simple educational / Balanced SEO), product positioning, sitemap + blog root URL, content pillar URLs, internal-link count, keyword region, publishing time + timezone, blog publishing preference (publish live / save as draft in Distribb / send as draft to the CMS), image hosting + style, YouTube-videos toggle, brand intelligence, duplicate-content protection, custom AI instructions, 3-7 competitors, and the Google Search Console connection. Full field-by-field detail and how to read or change each via the API is in `references/onboarding-guide.md`.

**The two connections that matter most:**
1. **Website / CMS** (WordPress, Webflow, Shopify, Ghost, Wix, Notion, GoHighLevel, Framer, or API webhook). This is how Distribb publishes. Check it with `GET /integrations`.
2. **Google Search Console.** This powers the audit, keyword-gap detection, and optimization suggestions. Check it with `GET /search-console` (returns `connected: true/false`). If the user has GSC access but has not connected it to Distribb, send them to https://distribb.io/integrations . **If the user does not have Search Console set up at all yet**, point them to Google's guide first: https://support.google.com/webmasters/answer/10267942?hl=en , then have them connect it in Distribb.

Also confirm the site actually has a **blog** to publish to. A site with no blog index has nowhere for articles to live, and this is a common reason new users see no results.

---

## The SEO Audit (Run This First)

Real SEO starts with an audit, not with publishing. Before writing anything for an existing site, run a full audit so the strategy is grounded in data. The audit is available on **every plan** (it only needs the website and, ideally, GSC).

A Distribb audit covers:
- **Keyword cannibalization** (multiple pages competing for the same query)
- **Content decay** (pages losing traffic vs the previous period)
- **Quick wins / striking distance** (queries at positions 11-20 and pages stuck on page 2+)
- **CTR optimization** (pages that rank but get fewer clicks than expected)
- **Dead pages** (pages that dropped to zero traffic)
- **Brand vs non-brand health**
- **Topical authority clusters (topic cocoons)** (which pillars and supporting clusters to build)
- **Competitor analysis** (gaps vs the competitors captured in onboarding)
- **Basic on-page checks** (titles, meta descriptions, headings, internal linking, indexability)

Run it with `/gsc-audit <domain>` or follow the full playbook in **`references/audit-playbook.md`**. The audit pulls real data from `GET /search-console`, `GET /suggestions`, and `GET /business-context`, crawls the live site for on-page checks, and ends with a prioritized action list wired to Distribb (new articles for gaps, optimization suggestions for page-2 pages). For very large GSC datasets, run each analysis in its own sub-agent so context stays manageable.

---

## Platform Tour: Where Things Live

Users often ask "where do I see X?" Here is the map (full detail in `references/platform-guide.md`):

| Page | What the user does there | API equivalent you can use |
|---|---|---|
| **Dashboard** | Overview of projects and recent activity | `GET /projects` |
| **Content Calendar** | See and manage planned / draft / published articles and their schedule | `GET /articles`, `POST /articles`, `PUT /articles/:id`, `DELETE /articles/:id` |
| **Settings** | Business description, custom AI instructions, publish time, timezone, backlink-network toggle, SEO data keys | `GET /projects/:id`, `PUT /projects/:id` |
| **Integrations** | Connect CMS, social accounts, Google Search Console, and Google Business Profile | `GET /integrations`, `GET /search-console`, `GET /gbp/status`, `GET /social/accounts` |
| **Backlinks** | See backlinks earned and given, and credits (aggregate) or the full link-by-link ledger | `GET /backlinks/status`, `GET /backlinks`, `GET /backlink-targets` |
| **Optimizations / Suggestions** | Review and approve GSC-driven rewrites of underperforming pages | `GET /suggestions`, `POST /suggestions/run`, approve/publish |

**Yes, you (the agent) can check backlinks for the user.** Use `GET /backlinks/status?project_id=...` for credits and counts, `GET /backlinks?project_id=...` for the full link-by-link ledger (every earned and scheduled link), and `GET /backlink-targets` for who they can link to next. The dashboard Backlinks page shows the same data visually.

---

## Plans, Backlink Exchange, and the Accelerator

Quick reference (full detail in `references/plans-and-backlinks.md`):

- **Backlink exchange:** Every current plan gets **unlimited** exchange access. Legacy Free Agentic accounts receive **1 backlink per month**. Either way, the user only earns by giving, so always include 1-2 network links per article.
- **Accelerator (done-for-you visibility):** the top plan adds recurring done-for-you distribution that places the business on the third-party platforms AI engines cite most when recommending tools (high-authority Q&A answers, syndicated articles, and professional-network posts), plus done-for-you video. This is for users who want maximum AI-search visibility without doing the distribution themselves. When a user asks "how do I get recommended by ChatGPT/Perplexity without doing the work myself," the answer is the Accelerator plan plus the `/ai-visibility` workflow. Direct them to https://distribb.io to upgrade.

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
# Output an article HTML FRAGMENT that follows the mandatory contract below.
# You MUST include 1-2 URLs from the backlink-targets response as natural references.

# 7. SUBMIT: Save to Distribb's content calendar
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "keyword": "best crm for small business",
    "title": "Best CRM for Small Business: 2026 Guide",
    "content": "<nav class=\"table-of-contents\" aria-label=\"Table of contents\"><h3>Table of Contents</h3><ul><li><a href=\"#introduction\">Introduction</a></li></ul></nav><h2 id=\"introduction\">Introduction</h2><p>Your full HTML article here...</p>",
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

## Mandatory Article HTML Contract and Safe Edit Protocol

These rules apply to every article-producing command, helper, and sub-skill. They are a publishing contract, not optional style advice.

- `content` is inserted inside Distribb's existing `.blog-content` element. Submit an HTML **fragment**, never a complete document.
- Never include `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, a page `<h1>`, document metadata/schema, page-level `<style>`, or executable `<script>`. Distribb owns the document shell, H1, metadata, schema, author block, sidebar, and CSS.
- Give every H2 a unique, stable, URL-safe `id`. When there are two or more H2s, include exactly one `<nav class="table-of-contents">` whose anchors resolve to the current IDs.
- Preserve existing wrappers, classes, IDs, `data-*` attributes, tables, links, and embeds during edits.
- Wrap every YouTube iframe in `<div class="youtube-embed">`; include a descriptive `title`, `loading="lazy"`, `allowfullscreen`, and no fixed dimensions.

For every edit: GET and save the article as a rollback copy; patch its fetched `Content`; diff and validate the fragment/IDs/TOC/embeds; PUT only changed fields; GET and verify readback. Published articles keep their slug and status: the API freezes the slug and rejects a move back to Draft/Planned. Distribb-hosted posts are live from the database; when a PUT returns `sync_required: true`, call `POST /api/v1/articles/:id/sync` (or resend the PUT with `"sync": true`; the CLI flag is `--sync`). Never republish or create a replacement for an existing live article.

Before publishing, and again on the live URL, inspect desktop and mobile widths. Confirm the sidebar/TOC matches the real headings and every video fills the article column at 16:9. A non-2xx response or failed readback is failure.

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

### Project Settings (Read & Edit): the FULL settings surface

`GET` returns a `settings` object; `PUT` accepts that **same shape**. So the loop is: GET, change the keys you want, PUT them back (read-modify-write). The PUT exposes the *entire* Settings UI, ~30 fields, not just a handful, so you can configure a project end-to-end without the dashboard. This is what makes agency-scale onboarding possible.

```bash
# Read current settings  (returns { "project": {...}, "settings": {...} })
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects/42 | jq .settings

# Edit settings (send ONLY the keys you want to change, partial updates are safe)
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sitemap_url": "https://acme.com/sitemap.xml",
    "blog_root_url": "https://acme.com/blog",
    "content_pillars": ["https://acme.com/crm", "https://acme.com/pricing"],
    "internal_links_per_article": 3,
    "tone": "Conversational",
    "writing_profile": "Balanced SEO",
    "product_positioning": "Soft mention",
    "image_hosting": "CMS",
    "brand_color": "#1d4ed8",
    "cta_intensity": "Soft",
    "competitors": ["https://competitor1.com", "https://competitor2.com"],
    "brand_intelligence": true,
    "duplicate_content_protection": true,
    "timezone": "America/New_York"
  }' \
  https://distribb.io/api/v1/projects/42 | jq .
```

**Writable fields** (every key the `settings` object returns is writable; aliases in parentheses):

| Field | Meaning / allowed values |
|-------|--------------------------|
| `ai_instructions` | Custom writing guidelines applied to every article. |
| `business_name`, `business_description` | Brand name + what the business does (writing context). |
| `target_audience` | List of audience strings, e.g. `["SaaS founders"]`. |
| `sitemap_url` | Sitemap URL (used to build the internal-link index). |
| `blog_root_url` | Blog root URL. |
| `content_pillars` | **List of URLs** (drives topic clusters + internal links). Each must be a valid URL, no spaces. |
| `internal_links_per_article` (`internal_links`) | Integer `1` to `5`. |
| `tone` | `Informative` \| `Conversational` \| `Persuasive`. |
| `language` | UI label or code, e.g. `English (US)`, `French`, `en-gb`. |
| `keyword_region` | e.g. `United States`, `United Kingdom`, `Worldwide`. |
| `writing_profile` | `Experienced practitioner` \| `Simple educational` \| `Balanced SEO`. |
| `product_positioning` | `Neutral operational` \| `Soft mention` \| `Promotional`. |
| `custom_author_name` | Byline author name. |
| `social_media_ai_instructions` | Custom instructions for repurposed social posts. |
| `publish_time` | Daily auto-publish time, 24-hour `"HH:MM"`. |
| `timezone` | IANA name, e.g. `"Europe/Madrid"`. |
| `publishing_status` | `Publish Immediately` \| `Save as Drafts` \| `Send as Drafts`. |
| `social_media_publishing_status` | `Save as Drafts` \| `Publish Immediately`. |
| `image_hosting` | `Distribb` \| `CMS`. |
| `image_style` | Free text (e.g. `Realism`, or a custom description). |
| `brand_color` | Hex string like `"#e11d2a"`. |
| `image_prompt_instructions` | Extra guidance for image generation. |
| `title_based_featured_image` | `true`/`false`, title-card featured image. |
| `cta_intensity` | `None` \| `Soft` \| `Direct`. |
| `first_person_writing` | `true`/`false`. |
| `table_of_contents` | `true`/`false`, auto table of contents. |
| `avoid_formulaic_section_endings` | `true`/`false`. |
| `require_operational_examples` | `true`/`false`. |
| `strict_banned_phrase_guard` | `true`/`false`. |
| `banned_phrases` (`extra_banned_phrases`) | List of phrases to never use. |
| `brand_intelligence` | `true`/`false`. |
| `duplicate_content_protection` (`duplicate_content_guard_enabled`) | `true`/`false`. |
| `videos_enabled` | `true`/`false`. |
| `backlinks_network` | `true`/`false`, join/leave the backlink exchange. |
| `competitors` (`competitor_websites`) | **List of competitor domains** (read AND write). |

**Partial updates are safe.** The article-quality and image preferences are stored as merged JSON, so sending just `{"cta_intensity": "Soft"}` changes ONLY that, the other quality flags keep their current values. Invalid enum values return `400` with a message naming the allowed values.

**Response (200):**
```json
{
  "project_id": 42,
  "updated_fields": ["tone", "cta_intensity", "competitors"],
  "updated_columns": ["ContentStyle", "ArticleQualitySettings", "CompetitorWebsites"],
  "message": "Project settings updated."
}
```

**Not settable via API:**
- `articles_per_day` is plan-controlled. If sent, it's echoed back under `ignored`. Read it via `GET /api/v1/projects` or the `settings` block.
- **Optimization thresholds** (`min_position`, `max_position`, `min_impressions_per_week`, `min_article_age_days`, `excluded_article_ids`) are applied at scan time by `POST /api/v1/suggestions/run`, not yet persisted per project. Sent values are echoed under `ignored`.

### Create a Project (agency-scale onboarding)

Spin up a brand-new project for a client and configure it in ONE call. You can pass any writable settings field from the table above alongside the basics.

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "website_url": "https://client.com",
    "business_name": "Client Co",
    "business_description": "Bookkeeping for trades businesses.",
    "target_audience": ["plumbers", "electricians"],
    "tone": "Conversational",
    "content_pillars": ["https://client.com/bookkeeping", "https://client.com/payroll"],
    "competitors": ["https://rival.com"]
  }' \
  https://distribb.io/api/v1/projects | jq .
```

**Response (201):** `{ "project_id": 77, "project_slots": {"used": 3, "total": 5}, "next_step": "...", ... }`

**Project slots are gated by the paid quantity.** If the account is already at its limit, you get **HTTP 402**:
```json
{
  "error": "project_limit_reached",
  "active_projects": 5,
  "project_quantity": 5,
  "purchase_url": "https://distribb.io/dashboard?add_project=1",
  "instructions_for_agent": "Tell the user they've hit their project limit and share purchase_url ..."
}
```
When you see this: **show the user `purchase_url`** (one click opens the "Buy More Seats" dialog in their dashboard). Once they confirm they bought a slot, **retry the same POST**. Never try to bypass the limit.

Creating a project **does NOT start keyword research** (that spends credits). After it's created, **ASK the user** whether they want to kick off keyword research + the first articles now. If yes, call the onboarding endpoint below.

### Run Onboarding (keyword research + first articles)

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/projects/77/onboarding | jq .
```

Starts the same pipeline the dashboard runs when onboarding finishes: GSC-aware keyword discovery -> a planned content calendar -> the first articles begin generating. Returns **202**; poll `GET /api/v1/articles?project_id=77` to watch planned articles appear.

- **Always ask the user first**, this spends keyword/LLM credits.
- If the project already has articles, it returns `already_onboarded` and does nothing.
- On Agentic plans and on legacy Free Agentic accounts this returns `skipped_byok` (those plans bring their own keywords, use `POST /api/v1/keywords/search` then `POST /api/v1/articles`).

### Connect WordPress

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "wordpress_url": "https://client.com", "integration_key": "<plugin Integration Key>" }' \
  https://distribb.io/api/v1/projects/77/wordpress | jq .
```

Install the Distribb WordPress plugin on the site, copy its **Integration Key**, and send it here. Credentials are validated (format check + live probe) before saving, the same checks the dashboard runs. Returns `{ "status": "connected" }`; if live validation is inconclusive (WAF/network) it still saves and returns a `warning`.

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

#### BYO Keys, legacy Free Agentic accounts

The free Agentic plan is deprecated and no longer offered to new users, but existing accounts still run. If the calling user is on one of those legacy **Free Agentic** accounts and has not yet saved a DataForSEO or Ahrefs API key, this endpoint returns **HTTP 402 Payment Required** with a structured body so your agent knows exactly what to do. Current plans (Agentic Mode at $49/month, Pro at $97/month, and Accelerator) never see this response.

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

**Agent contract, what to do when you see this 402:**

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

If the user has saved only an Ahrefs key (not DataForSEO), the response is sourced from Ahrefs Keywords Explorer and includes `"source": "byo_ahrefs"` plus a `note` field. All other endpoints in this skill (articles, integrations, backlinks, internal links) work normally on legacy Free Agentic accounts without any BYO keys.

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

### Backlink Ledger (full link-level detail)

`GET /backlinks/status` gives the aggregate (credits + counts). `GET /backlinks` gives the **link-by-link ledger** behind it: every earned (verified) link and every scheduled/upcoming link, with the source domain, source Domain Rating, source business name, the target URL on the user's own site, status, and date, plus a velocity + competitor-gap summary. Use it to answer "which sites actually link to me, and how strong are they?"

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlinks?project_id=42" | jq .
```

**Query parameters:** `project_id` (required), `earned_limit` (default 100, max 500), `scheduled_limit` (default 50, max 200).

**Response (200):**
```json
{
  "project_id": 42,
  "earned": [
    {
      "id": 55123,
      "source_domain": "partner-site.com",
      "source_business": "Partner Co",
      "source_dr": 61,
      "source_url": "https://partner-site.com/related-article",
      "target_url": "https://acme.com/blog/crm-guide",
      "status": "Verified",
      "date": "2026-06-14"
    }
  ],
  "earned_count": 1,
  "scheduled": [
    {
      "id": 55130,
      "source_domain": "another-partner.com",
      "source_business": "Another Partner",
      "source_dr": 48,
      "target_url": "https://acme.com/blog/pricing",
      "status": "Scheduled",
      "scheduled_since": "2026-06-30"
    }
  ],
  "scheduled_count": 1,
  "velocity": {
    "velocity_cap": 8,
    "velocity_used": 3,
    "competitor_gap_percent": 42,
    "competitor_gap_target": 120
  },
  "note": "Per-link anchor text is not captured yet; anchor-mix distribution is not included."
}
```

Scheduled links usually have no `source_url` yet (the linking article is still being written), so only `source_domain`/`source_business`/`source_dr` are populated for them. **Per-link anchor text is not tracked yet**, so this endpoint intentionally does NOT return an anchor-text-mix breakdown. Do not infer or fabricate one.

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
    "content": "<nav class=\"table-of-contents\" aria-label=\"Table of contents\"><h3>Table of Contents</h3><ul><li><a href=\"#introduction\">Introduction</a></li></ul></nav><h2 id=\"introduction\">Introduction</h2><p>Finding the right CRM...</p>",
    "meta_description": "Compare the 10 best CRM tools for startups.",
    "feature_image": "https://cdn.example.com/crm-comparison-hero.png",
    "alt_text": "Comparison chart of the 10 best CRM tools for startups",
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

### Feature image

`feature_image` is an absolute `http(s)` URL, stored as the article's hero. Send
`alt_text` with it; if you omit it, the title is used. Both fields also work on
`PUT /api/v1/articles/{id}`, where `"feature_image": ""` clears the hero.

**Distribb cannot generate an image for you through this API.** The writer pipeline
that normally produces a hero does not run on content you submit yourself, so an
article you create here has no feature image unless you supply one. Generating a new
image is a dashboard action.

**IMPORTANT:** If `image_warning` is present in the response, the article has no hero:

1. If `image_candidates` is also present, those are absolute image URLs already
   embedded in the article body. Promote the best one:
   `PUT /api/v1/articles/{article_id}` with `{"feature_image": "<url>"}`.
2. **Do not blindly take the first candidate.** In a listicle the early images are
   usually screenshots of the competitors being reviewed, and a competitor's product
   shot makes a poor hero for the user's own article. Pick one that represents the
   user's brand, or a neutral/illustrative one.
3. If there are no candidates, ask the user for an image URL rather than leaving it
   blank silently.

Without a hero the article loses its `og:image` (no preview card when the link is
shared), its schema.org `image`, its on-page hero, and its thumbnail on the blog
index. Medium and LinkedIn syndication read the same field.

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

Setting a `scheduled_date` schedules the article: submit it as a `Draft` with a date and Distribb auto-promotes it to `Planned` (passing `status: Planned` yourself is still fine). Omit the date and it stays a `Draft` for review. What happens ON the date depends on the project's `PublishingStatus` (read it from `GET /api/v1/projects`): `Publish Immediately` goes live; `Save as Drafts` keeps it as a draft inside Distribb for manual review; `Send as Drafts` pushes it to the CMS as a draft. So a correctly-scheduled article on a `Save as Drafts` project will NOT auto-publish to the live site, that is by design, not a bug.

### Update Article

Use this to revise an article after submission, including a Published article. Follow the mandatory fetch-patch-verify protocol above: GET and preserve the current article, patch its fetched `Content`, and send only changed fields.

```bash
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat revised-article.html)" '{
    "content": $content
  }')" \
  https://distribb.io/api/v1/articles/123 | jq .
```

**Updatable fields:** `title`, `content`, `meta_description`, `keyword`, `article_style`, `status` (Draft or Planned), `scheduled_date`, `category`, `published_at`, `sync`. Send only the fields you want to change. On a Published article the slug is frozen (changing `keyword` updates the keyword but no longer moves the URL) and `status` cannot go back to Draft/Planned, so the live URL and publication state cannot drift.

- `category`: the CMS category NAME to assign (e.g. `"Accessibility Guides"`). It must ALREADY exist on the destination CMS (WordPress or GoHighLevel); Distribb resolves the name to that platform's category at publish time and cannot create new categories. Send `""` to clear it. Detection ships for WordPress and GoHighLevel; other CMSs ignore it for now.
- `published_at`: a PAST ISO 8601 timestamp used to BACKDATE the post on the CMS (e.g. `"2024-02-05T09:00:00Z"`). This changes only the date the CMS records, NOT when Distribb publishes and NOT the article's position on the content calendar (that is `scheduled_date`). Send `""`/`null` to clear it. Backdating is applied on GoHighLevel today.

**Response (200):**
```json
{
  "article_id": 123,
  "updated_fields": ["Content", "IsPreGenerated"],
  "message": "Article updated successfully.",
  "backlinks_processed": 2,
  "sync_required": false
}
```

If content is updated and the project participates in the backlink network, Distribb re-scans for network backlinks and updates credits. GET and validate readback after the PUT. If the response says `sync_required: true`, call `POST /api/v1/articles/:id/sync`; this overwrites the existing CMS post and never creates a replacement. Distribb-hosted posts return `sync_required: false` and are live immediately.

### Update a Published Article (edit content that is already live)

Published articles ARE editable. The edit lands inside Distribb first; the live post on the site changes only when you **sync** it. That two-step split means a typo can never go live by accident.

```bash
# 1. Edit the stored article
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat corrected-article.html)" '{"content": $content}')" \
  https://distribb.io/api/v1/articles/123 | jq .

# 2. Push it to the live post (updates in place, never creates a duplicate)
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123/sync | jq .
```

**`sync_required` tells you whether a push is even needed.** Every PUT response carries it:

- `false` on an unpublished article (nothing is live yet).
- `false` on a Distribb-hosted post (distribb.io serves `/blog/<slug>` straight from the database, so the edit is live the moment it saves).
- `true` when a live post exists on an external CMS. That is the only case that needs a sync.

Or do both in one call with `"sync": true`:

```bash
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Corrected Title", "sync": true}' \
  https://distribb.io/api/v1/articles/123 | jq .
```

**Two fields are frozen once an article is live:**

- `keyword` still updates the main keyword, but it no longer regenerates the slug. The slug IS the public URL and the key Distribb matches the remote post on, so changing it would 404 the live page and make the next sync create a second post.
- `status` cannot go back to `Draft` or `Planned` (returns `400 cannot_unpublish`). That would orphan the live post and let the scheduler publish a duplicate over the top of it. To take a post down, unpublish it from the Distribb dashboard or delete it in the CMS.

**Sync outcomes:**

| Response | What it means |
|---|---|
| `200 {"status":"synced","url":...}` | The live post now carries your edit. |
| `400 {"error":"not_published"}` | Nothing live to update yet. Use `POST /api/v1/articles/<id>/publish` first. |
| `400 {"error":"no_cms_integration"}` | The site is disconnected. Reconnect it at https://distribb.io/integrations . |
| `400 {"error":"unsupported_for_sync"}` | That platform has no update path yet. Edit the post directly on the platform. |
| `400 {"error":"sync_failed"}` | The CMS rejected the update; `message` carries the platform's reason. The Distribb-side edit is still saved, so fix the cause and retry the sync. |

**In-place updates are supported on:** WordPress, API Webhook, Shopify, Webflow, Wix, Ghost, GoHighLevel, Framer, Notion. Anything else returns `unsupported_for_sync`.

Syncing is safe to repeat. Distribb finds the remote post by its stored ID, then slug, then title, and fails closed rather than risk publishing a duplicate.

**CLI:**

```bash
python distribb_cli.py articles:update --article-id 123 --content-file corrected.html --sync
python distribb_cli.py articles:sync --article-id 123
```

### Delete Article

```bash
curl -s -X DELETE -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/123 | jq .
```

Deletes a `Draft` or `Planned` article. **Published articles cannot be deleted** (the live CMS post would be orphaned), you get a `400`. Unpublish or hide it from the dashboard/CMS first, or simply unschedule it.

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

Pushes the article to the user's connected CMS (WordPress, Webflow, Shopify, etc.). A manual publish like this **always goes live**, even if the project is set to `Save as Drafts` / `Send as Drafts`, that preference only controls AUTOMATIC scheduled publishing, not a deliberate "publish now". Returns `200` with `{"status":"published","url":...}` once the CMS confirms a live URL; `202` with `{"status":"pending"}` if the CMS hasn't confirmed yet (it will retry, the article is NOT lost).

Use this only for Draft/Planned articles without a live post. For a Published article, PUT and then use the update-only `/sync` endpoint when requested; never publish it again.

**The project must have a website/CMS connected.** If none is, this returns **`400` with `{"error":"no_cms_integration"}`** and a `connect_url`. Surface that to the user verbatim, there is nowhere to publish until they connect their site at https://distribb.io/integrations . This is the single most common reason a scheduled article never publishes: a Google Search Console (analytics) connection is NOT a publishing destination. Before you tell a user an article will publish, confirm a CMS is connected with `GET /api/v1/integrations`.

### Social Media Repurposing (Automatic)

When an article is published to the user's CMS, Distribb automatically generates social media posts for every platform the user has connected (X/Twitter, LinkedIn, Reddit, Facebook, Instagram, etc.). The agent does not need to call any endpoint for this. It happens server-side.

The social posts are created as drafts in the user's content calendar so they can review, edit, or schedule them from the Distribb dashboard. If the user has connected social accounts, publishing an article through the API triggers this automatically.

### Posting to Social Media Yourself

Repurposing is automatic, but you can also write a post and send it to the user's connected accounts. This is the same publisher behind the dashboard's Social Composer, so anything you send lands in their calendar next to everything else.

**1. See what is connected.**

```bash
curl -s "https://distribb.io/api/v1/social/accounts?project_id=42" \
  -H "Authorization: Bearer $DISTRIBB_API_KEY" | jq
```

Returns `{connected, accounts: [{platform, account_id, account_name}], instructions_for_agent}`. A project with nothing connected is not an error: it returns `200` with `connected: false`. Connecting an account is a browser OAuth step at https://distribb.io/integrations, so you cannot do it for the user.

**2. Post.**

```bash
curl -s -X POST https://distribb.io/api/v1/social/publish \
  -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "content": "The three keyword mistakes that cost us six months.",
    "platforms": ["linkedin", "x"],
    "link": "https://example.com/blog/keyword-mistakes"
  }' | jq
```

| Field | Notes |
|---|---|
| `project_id` | Required. Must be a project the API key's account owns or is a team member of. |
| `content` | Required. The post text. |
| `platforms` | Required. `["linkedin", "x"]`, or `[{"platform": "x", "account_id": "..."}]` when one platform has several connected accounts. |
| `link` | Optional. Stored with the post. On LinkedIn and Facebook it is appended to the text so the preview card renders. |
| `media_files` | Optional. `[{"type": "image", "s3_url": "..."}]`. |
| `platform_overrides` | Optional. Per-platform copy and per-network options, keyed by platform. |
| `scheduled_for` | Optional ISO8601 UTC. Schedules the post instead of sending it now. |

The CLI wraps both:

```bash
python distribb_cli.py social:accounts --project-id 42
python distribb_cli.py social:publish --project-id 42 --platforms linkedin,x \
  --content "The three keyword mistakes that cost us six months." \
  --link https://example.com/blog/keyword-mistakes
```

Supported platforms: `x` (or `twitter`), `linkedin`, `facebook`, `instagram`, `threads`, `bluesky`, `reddit`, `tiktok`, `youtube`, `pinterest`, `telegram`, `snapchat`, `googlebusiness`.

**Per-platform copy beats one shared post.** Use `platform_overrides` to rewrite for each network and to reach the options only that network has:

```json
{
  "platform_overrides": {
    "x": {"threadSteps": ["Second tweet.", "Third tweet."]},
    "linkedin": {"text": "A longer, first-person version.", "firstComment": "Full breakdown: https://example.com/blog/keyword-mistakes"},
    "reddit": {"subredditName": "SEO", "title": "What six months of keyword mistakes taught us"}
  }
}
```

**Scheduling.** With `scheduled_for` the post is saved as scheduled and goes out within five minutes of that time, and the user can still edit or delete it in the dashboard until then. The response is a `201` with `scheduled: true`. Without it the post publishes immediately and the response carries the live URLs.

**Character limits are enforced server-side**: X 280, Bluesky 300, Threads 500, Pinterest 500, Google Business 1500, Instagram and TikTok 2200, LinkedIn 3000, YouTube 5000. Going over is a `400` naming the platform and the count, so write to the limit rather than fixing it after a rejection.

**Confirm the copy before you send it.** A published post is public and immediate, and deleting it later does not undo who saw it. Show the user the exact text per platform and wait for a yes, unless they have already told you to post without checking.

### YouTube SEO With Motion Videos (`/youtube-motion-video`)

Turn a keyword or concept into a short, faceless **motion-collage explainer video**
(bold screen-print cutout collage visuals, a calm "In a Nutshell" documentary voice),
optimize it for **YouTube SEO** with Distribb's real keyword + Search Console data, and
publish it to the user's connected **YouTube** channel through Distribb, then close the
loop with a companion article that embeds it.

This is a hybrid workflow: Distribb is the SEO brain (keyword data, GSC, internal links,
backlinks, the companion article) and the **`super-video-maker`** skill is the production
engine (OpenAI `gpt-image-2` collage stills → Seedance 2.0 via fal.ai motion → ElevenLabs
narration → captions). Install it once with `npx skills add Bomx/super-video-maker-skill`.

Run it with `/youtube-motion-video <topic>` and follow **`references/youtube-motion-video-playbook.md`**
for the full method (preflight, the collage look, the Seedance motion rules, the docu
voice, the SEO packaging, and the connect-and-publish path). The user connects their own
YouTube channel first at https://distribb.io/integrations ("Connect via Google").

### Instagram Carousels for SEO (`/instagram-carousel`)

Instagram carousels are an **SEO tactic**, not just social. Since mid-2025 public posts from
professional accounts are indexed by Google/Bing and cited by LLMs, and carousels manufacture
the strongest predictor of AI-engine citations for a brand: **branded search**. They also
carry the highest saves of any IG format (~9x a single image), and a save is the dominant
ranking signal for educational content.

This workflow re-architects **one Distribb article** (or one target keyword) into a viral,
save-driven carousel using our 2026 best practices: a cover that teases (it carries ~80% of
the outcome), an 8-slide swipe arc (cover -> promise -> one-idea-per-slide value -> recap ->
CTA), the exact design system (1080x1350, safe zones, >=4.5:1 contrast, consistent template),
keyword-rich captions + per-slide **alt text** (the indexable surfaces, since hashtags no
longer drive reach), and the **comment-a-keyword-to-DM** link play (one ALL-CAPS keyword +
misspelling variants + an auto-DM, which beats link-in-bio). It then closes the SEO loop with
a companion Distribb article on the same keyword so the attention becomes indexable owned
authority.

Run it with `/instagram-carousel <article-id-or-keyword>` and follow
**`references/instagram-carousel-playbook.md`** for the full method (the Carousel Maker JSON
contract, the cover/hook formulas, the design specs, how to render the slides, the
comment-for-link playbook, and the publish paths: Graph API, a scheduler, or a ready-to-post
hand-off). The user connects their Instagram professional account first at
https://distribb.io/integrations .

### List Integrations

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/integrations?project_id=42" | jq .
```

### Google Search Console

Pull the user's **real** search performance from Google Search Console, top queries, top pages, and site totals (clicks, impressions, CTR, average position). Use it to find queries worth targeting, pages sitting just off page 1, or terms the user already ranks for. **Requires the user to have connected GSC.**

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/search-console?project_id=42&days=28&limit=25" | jq .
```

**Query parameters:** `project_id` (required), `days` (default 28, max 90), `limit` (rows per list, default 25, max 1000), `start_row` (pagination offset, default 0), `compare` (`true` to add period-over-period deltas vs the immediately preceding window of equal length).

**Aliases:** `GET /rankings` and `GET /analytics` are documented aliases of this endpoint (same handler, same parameters and response). They serve Search-Console **search performance** (clicks, impressions, CTR, position by query and by page), NOT web-session analytics. If a user asks for "analytics" expecting sessions/bounce-rate/traffic-source data, clarify that Distribb exposes Search-Console performance, not a web-analytics product.

**Pagination:** page through large result sets with `start_row`. The response includes a `pagination` block with the current `limit`, `start_row`, and a `next_start_row` (null when there are no more rows). Fetch the next page by passing `start_row=next_start_row`.

**Compare (`compare=true`):** adds a `comparison` block with `previous_date_range`, `previous_totals`, and `delta_totals`, and adds `delta_clicks`, `delta_impressions`, `delta_position`, and `is_new` to each query/page row. Use it to spot rising or decaying queries and pages at a glance.

**Response (200, connected):**
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

**Response (200, NOT connected):**
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
- If `connected` is `true` but the body has `"error": "gsc_fetch_failed"`, their Google token likely expired, tell them to reconnect at the same URL.

**How to use the data:** queries with lots of impressions but low CTR or an average position of ~8-20 are the best targets, write a new article or refresh an existing one for them. Pages at the bottom of page 1 (position ~8-12) often just need internal links and a content refresh to climb. Pair this with `POST /articles` (write the piece) and `GET /internal-links` (cross-link it).

### Google Business Profile (reviews, replies, posts, analytics)

Act on the user's **connected Google Business Profile**: read their Google reviews live, post or delete the business's public review replies, queue Google Business posts, and pull post analytics. Local-SEO leverage in one surface: reviews with owner replies convert better and fresher profiles rank better in the map pack. **Requires the Google Business integration** (Integrations page -> 'Add Integration' -> 'Google Business', signed in with the Google account that manages the profile).

```bash
# Connection + live review summary (business name, address, totals, unreplied count)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/status?project_id=42" | jq .
```

**Response (200, connected):**
```json
{
  "connected": true,
  "business_name": "Fusion Electrical & Carpentry Projects",
  "location_address": "11/23 Lake Road, Tuggerah, NSW",
  "connected_at": "2026-07-10T01:46:44",
  "review_notifications_subscribed": true,
  "total_reviews": 96,
  "average_rating": 5,
  "unreplied_count": 50,
  "unreplied_count_is_partial": true,
  "capabilities": ["list Google reviews (live)", "reply to reviews / delete a reply", "publish Google Business posts (via the social pipeline)", "post-level analytics for posts published through Distribb"],
  "not_available": "Location performance insights (calls, direction requests, website clicks, search keywords), Q&A, photo uploads, and business-info edits are not available through this connection."
}
```

When `connected` is `false` the body carries `instructions_for_agent`, so relay it verbatim and stop until the user connects.

**List reviews (live from Google):**

```bash
# Needs-reply triage: unreplied reviews first
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/reviews?project_id=42&has_reply=false&limit=25" | jq .

# Negative/neutral reviews only
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/reviews?project_id=42&max_rating=3" | jq .
```

**Query parameters:** `project_id` (required), `has_reply` (`false` = needs-reply triage), `min_rating`/`max_rating` (1-5), `sort_by` (`date`|`rating`), `sort_order` (`asc`|`desc`), `limit` (1-50, default 25), `cursor` (pass a previous response's `next_cursor` while `has_more` is true).

Each review: `review_id`, `reviewer_name`, `rating`, `text`, `created`, `has_reply`, `reply_text`, `reply_created`, `review_url`. The response's `total_reviews` / `average_rating` reflect the **current filter** (with `has_reply=false`, `total_reviews` is the unreplied total).

**Reply to a review (PUBLIC, confirm wording with the user first):**

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" -H "Content-Type: application/json" \
  -d '{"project_id": 42, "review_id": "accounts/.../locations/.../reviews/AbFvOq...", "message": "Thanks Sarah, glad the switchboard upgrade went smoothly. See you on the next project!"}' \
  https://distribb.io/api/v1/gbp/reviews/reply | jq .

# Remove a posted reply (the review itself cannot be deleted)
curl -s -X DELETE -H "Authorization: Bearer $DISTRIBB_API_KEY" -H "Content-Type: application/json" \
  -d '{"project_id": 42, "review_id": "accounts/.../locations/.../reviews/AbFvOq..."}' \
  https://distribb.io/api/v1/gbp/reviews/reply | jq .
```

Reply etiquette the agent should follow: write in the project's brand voice, thank the reviewer by name, reference something specific from their review, keep it short (2-4 sentences, max 4000 chars). For negative reviews: stay professional, own what's ownable, move resolution offline ("call us at ..."). Never argue. To EDIT a live reply, just reply again with the new text (Google keeps one owner reply per review); to remove it, use DELETE.

**Create a Google Business post:**

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" -H "Content-Type: application/json" \
  -d '{"project_id": 42, "text": "Spring switchboard-safety checks are now booking...", "link": "https://acme.com/switchboard-checks", "scheduled_date": "2026-07-15 09:00"}' \
  https://distribb.io/api/v1/gbp/posts | jq .
```

Body: `text` (required, max 1500 chars), `link` (optional, becomes the post's **Learn More** button), `image_url` (optional, public http(s) image), `scheduled_date` (optional, `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` UTC). With `scheduled_date` the post is `scheduled` and auto-publishes at that time; without it the post is saved as a `draft` for review in the Social Composer. Returns **201** with `post_id` + `status`. Articles published through Distribb also auto-repurpose to Google Business when the integration is connected, so use this endpoint for standalone posts (offers, updates, seasonal pushes).

**Post analytics:**

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/gbp/analytics?project_id=42" | jq .
```

Covers Google Business posts published through Distribb (post counts + per-post engagement where Google provides it).

**Agent contract:**
- Review counts, ratings, and review text must come **only** from these payloads, never estimate or invent them.
- Replies are **public on Google immediately** under the business name. Unless the user already supplied or approved the exact wording, show the draft and get a go-ahead before `POST /gbp/reviews/reply`. Bulk-replying is fine once the user approves the approach and tone (e.g. "reply to all unreplied 5-star reviews, one line each, varied wording").
- This connection **cannot** read location insights (calls, direction requests, website clicks, search keywords), Q&A, photos, or edit business info. Say so when asked instead of promising them.
- A `404` with `instructions_for_agent` on the write endpoints means Google Business is not connected, so relay the instructions.

**Good `/gbp` workflow:** `GET /gbp/status` -> if `unreplied_count > 0`, pull `has_reply=false` reviews -> draft replies in the brand voice (get approval) -> post them -> finish with a queued Google Business post pointing at the latest published article.

### Link Outreach (listicle backlink replies)

Link Outreach is Distribb's managed service that emails "best of" / "top tools" listicle authors, from Distribb's warmed inboxes, asking to add the user's business to lists that already rank their competitors. Discovery, sending, and follow-ups are automatic. This surface is for the **replies**: seeing which authors answered (and what they want) and responding to them **in-thread**, without the user leaving Distribb.

- `GET /link-outreach/prospects?project_id=...&status=replied,offer&limit=50` lists the authors who replied. Each row: `prospect_id`, `host`, `author_name`, `author_email`, `status` (`replied` or `offer`), the author's `reply` (their actual message), and `offer_amount` / `offer_currency` when they named an asking price. Omit `project_id` to span every project the key owns; `status=all` returns the whole pipeline. Read-only, 30 req/min.
- `POST /link-outreach/prospects/:id/reply` with `{ "body": "<the reply>" }` sends the user's reply **in-thread from the Distribb inbox that ran the original outreach**, so it stays connected and lands in the author's inbox. **Accelerator only** (other plans reply from their own inbox). 10 req/min.

**Agent contract (this SENDS a real email on the user's behalf):**
- Always `GET` the replies first and summarize them. Quote the `reply` text and any `offer_amount` exactly. Never invent a price, terms, or intent the author did not state.
- Most listicle placements are paid; that is the industry norm. Whether to accept, negotiate, or pass is ALWAYS the user's call, never yours. Distribb never agrees to or pays for a placement on their behalf.
- Draft the reply, show the user the exact wording, and get a clear go-ahead BEFORE calling `POST .../reply`. It is not reversible. Never send a reply the user has not seen and approved.

**Good `/link-outreach` workflow:** `GET /link-outreach/prospects` -> summarize who replied + any asking price -> draft a short reply in the user's voice -> get explicit approval of the wording -> `POST /link-outreach/prospects/:id/reply`.

### AI Visibility (AEO)

Read Distribb's **already-tracked** AI-search visibility for a project: how often AI engines cite the site, the share-of-voice vs competitors, per-engine citation status, the tracked prompts, and the exact pages engines cited. This is the API-key mirror of the dashboard AI-visibility pane (same `ai_citation_tracker` backend), so an agent can pull it directly instead of re-deriving everything with live `WebSearch`. The five tracked engines are ChatGPT, Perplexity, Gemini, Google AI Overviews, and Google AI Mode.

```bash
# Summary: visibility score, share-of-voice, per-engine cited/not, scan state
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/ai-visibility?project_id=42&view=summary" | jq .

# Other views: prompts (paged), competitors (share-of-voice), cited_pages (your cited URLs)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/ai-visibility?project_id=42&view=prompts&page=1&per_page=10" | jq .
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/ai-visibility?project_id=42&view=competitors" | jq .
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/ai-visibility?project_id=42&view=cited_pages" | jq .
```

**Query parameters:** `project_id` (required), `view` (`summary` default, or `prompts` | `competitors` | `cited_pages`). For `view=prompts`: `page` (default 1), `per_page` (default 10).

**Summary response (200):**
```json
{
  "has_data": true,
  "scanning": false,
  "score": 38,
  "engines_citing": 2,
  "engines_total": 5,
  "share_of_voice": 12,
  "prompts_tracked": 18,
  "scan_location": "Sydney,New South Wales,Australia",
  "engines": [
    { "key": "chatgpt", "label": "ChatGPT", "state": "cited" },
    { "key": "perplexity", "label": "Perplexity", "state": "mentioned" },
    { "key": "gemini", "label": "Gemini", "state": "not_cited" }
  ],
  "last_scan": "2026-07-01 06:00:00",
  "manual_scans_used": 0,
  "manual_scans_limit": 2,
  "can_scan": true
}
```

Per-engine `state` is one of `cited` (your page was cited), `mentioned` (brand named but not cited), `not_cited` (the engine answered but did not cite you), or `no_data`. If `has_data` is `false`, no scan has run yet (or one is `scanning`), trigger one with the scan endpoint below. The `competitors` view returns `you` (your citation count), `rows` (each stored competitor with citation counts), and `other_cited` (most-cited domains that are neither you nor a competitor). The `cited_pages` view returns your own URLs that engines cited, with per-URL citation counts and which engines cited them.

#### Trigger a scan

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42}' \
  https://distribb.io/api/v1/ai-visibility/scan | jq .
```

Queues an on-demand scan and returns **202** `{"status":"queued", ...}`. Poll `GET /ai-visibility?view=summary` until it completes. The **per-project daily manual-scan cap is SHARED** with the dashboard "Scan now" button and the Distribb Agent, so heavy API scanning draws from the same budget. When the cap is hit you get **429** `{"status":"rate_limited", "manual_scans_used": N, "manual_scans_limit": M}` (resets at midnight UTC). `project_id` may be sent in the body or as a query param.

#### Add or remove a tracked prompt

```bash
# Add a prompt to track
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "prompt": "best crm for small business"}' \
  https://distribb.io/api/v1/ai-visibility/prompts | jq .

# Remove a tracked prompt (soft-delete; past results are kept)
curl -s -X DELETE -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42, "prompt": "best crm for small business"}' \
  https://distribb.io/api/v1/ai-visibility/prompts | jq .
```

Body: `{"project_id": <id>, "prompt": "..."}`. Added prompts are picked up on the next scan. `POST` returns `{"status":"added"|"duplicate"|"limit"|"invalid"}` (a `limit` status means the tracked-prompt cap is reached, remove one first). `DELETE` returns `{"status":"removed"}` or `404` `{"status":"not_found"}`.

**Bring your own prompts (the ones that matter).** Every project seeds with about 10 auto-generated prompts that skew brand-y ("Is [brand] a good tool?"). Those are just a starting point. Add the real buyer queries your clients care about ("best pickleball paddle australia", "best crm for real estate") with the add endpoint, they are your highest-signal prompts and are scanned first. A project tracks up to **25** prompts total (your own prompts take priority over the auto ones); remove the auto prompts you do not want so your buyer queries fill the set. To lift the ceiling above 25 across the whole workspace, ask Distribb to raise `AI_CITATION_MAX_TRACKED` (it is cost-bounded: each prompt is scanned across 5 engines per scan).

#### Set the scan location (local businesses)

For local businesses, proximity decides the AI answer, so the scan should run from the client's own market, not a default country. Distribb scans **Google AI Overview, Google AI Mode, ChatGPT, and Gemini from the project's `primary_location`** (a `"City, Region, Country"` string) when it is set, and falls back to the country otherwise. **Perplexity is always country-level** (its API accepts only a country code). The location the scan actually used is echoed back as `scan_location` on the summary response, so you can prove localization in a report.

`primary_location` is captured at onboarding, and you can set or override it per client via the projects API (or the CLI):

```bash
# Set the client's market so AI Visibility scans from their city
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"primary_location": "Sydney, New South Wales, Australia"}' \
  https://distribb.io/api/v1/projects/42 | jq .
```

If DataForSEO does not recognize the city, the scan quietly falls back to the country for that run (no error), so a rough or misspelled market never breaks a scan. Changing the location shifts where future scans measure from, so trend lines compare like-for-like only after the first scan at the new location.

#### CLI

The same surface is wrapped in `distribb_cli.py` so you do not have to hand-write curl:

```bash
python distribb_cli.py ai-visibility:get --project-id 42 --view summary
python distribb_cli.py ai-visibility:get --project-id 42 --view prompts --page 1 --per-page 25
python distribb_cli.py ai-visibility:get --project-id 42 --view competitors
python distribb_cli.py ai-visibility:get --project-id 42 --view cited_pages
python distribb_cli.py ai-visibility:scan --project-id 42
# Bulk-add a client's buyer queries in one call (repeat --prompt)
python distribb_cli.py ai-visibility:prompts:add --project-id 42 \
  --prompt "best pickleball paddle australia" \
  --prompt "best pickleball paddle for beginners"
python distribb_cli.py ai-visibility:prompts:remove --project-id 42 --prompt "Is Acme a good tool?"
# Localize the scan to the client's market
python distribb_cli.py projects:update --project-id 42 --primary-location "Sydney, New South Wales, Australia"
```

### Content Optimizations (Suggestions)

Distribb continuously finds pages where a rewrite could win more traffic, mostly from the user's **Google Search Console** data (queries with impressions but low CTR, pages stuck at the bottom of page 1). Each one is a **suggestion**: Distribb scrapes the live page, has its AI draft an improved version, and stages a before/after **diff** for review. You (the agent) list them, inspect the diff, approve (which triggers the rewrite), then publish the approved rewrite straight to the user's CMS. This is the highest-leverage ongoing SEO loop, it acts on pages that *already* rank, so wins come faster than net-new articles.

**Lifecycle:** `pending` → (approve) → `rewriting` → `ready` → (publish) → `published`. A suggestion can also be `rejected`, `failed`, or `superseded` (the article changed after the suggestion was created, so the staged rewrite is stale).

```bash
# Generate a fresh batch now (pulls GSC + scores articles). Mirrors the weekly cron.
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": 42}' \
  https://distribb.io/api/v1/suggestions/run | jq .

# List suggestions (optionally filter by status: pending, ready, published, ...)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/suggestions?project_id=42&status=pending" | jq .

# Filter by opportunity type instead (cannibalisation, content decay, audit findings, ...)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/suggestions?project_id=42&type=cannibalisation" | jq .

# Inspect a single suggestion, then its before/after rewrite
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/suggestions/123 | jq .
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/suggestions/123/diff | jq .

# Approve -> starts a background rewrite. Poll the suggestion until status is "ready".
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/suggestions/123/approve | jq .

# Once "ready", publish the rewrite to the connected CMS
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/suggestions/123/publish | jq .

# Not happy with the rewrite? Regenerate with feedback (only valid while "ready")
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"feedback": "Keep the pricing table, tighten the intro, add a FAQ."}' \
  https://distribb.io/api/v1/suggestions/123/regenerate | jq .

# Or dismiss it
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Page is being deprecated."}' \
  https://distribb.io/api/v1/suggestions/123/reject | jq .
```

**List response (200):**
```json
{
  "project_id": 42,
  "gsc_connected": true,
  "counts": { "pending": 4, "ready": 1, "published": 9, "rejected": 2 },
  "settings": { "enabled": true },
  "suggestions": [
    {
      "id": 123,
      "project_id": 42,
      "article_id": 8801,
      "status": "pending",
      "suggestion_type": "content_rewrite",
      "source_type": "distribb",
      "article_title": "Best CRM for Small Business",
      "article_url": "https://acme.com/blog/crm-guide",
      "trigger_snapshot": { "query": "best crm for small business", "impressions": 8100, "ctr": 0.012, "position": 11.4 },
      "created_at": "2026-06-16T06:00:00"
    }
  ]
}
```

**Agent contract:**
- **Approve and publish are real, billable actions.** `publish` pushes the rewrite live to the user's CMS. Show the user the diff (`GET /suggestions/:id/diff`) and get a clear go-ahead before approving/publishing, unless they've explicitly told you to run optimizations autonomously.
- **Approve and regenerate are asynchronous.** They return immediately with status `rewriting`. Poll `GET /api/v1/suggestions/:id` every ~15-30s until status is `ready` (rewrite staged) or `failed`. Do **not** publish until `ready`.
- **A `409` on approve or publish is a conflict**, the article changed since the suggestion was created (status flips to `superseded`). Run `POST /suggestions/run` to regenerate fresh suggestions against the current article, then start over.
- If `gsc_connected` is `false` and the list is empty, follow the `instructions_for_agent` string: tell the user to connect GSC at https://distribb.io/integrations, then `POST /suggestions/run`.

**Parameters:**
- `GET /suggestions`, `project_id` (required), `status` (optional), `type` (optional), `limit` (default 100, max 500).
- `POST /suggestions/run`, `project_id` (required).

**Filter by opportunity type (`?type=`):** narrow the list to a single opportunity type (`opportunity_type`) so cannibalisation, content-decay, and audit findings are consumable as data. Common values: `cannibalisation`, `declining_page`, `striking_distance`, `ctr_underperform` (and others as the engine adds them). It filters the returned `suggestions` list only, the per-status `counts` still reflect the whole project. Combine with `status` to, for example, list `pending` `cannibalisation` items.
- `POST /suggestions/:id/reject`, optional `reason`. `POST /suggestions/:id/regenerate`, optional `feedback`.

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

## SEO Article Writing System

Follow this for EVERY article. The goal: content a human wants to read AND that AI search engines (ChatGPT, Perplexity, Gemini, Google AI Overviews) quote and recommend.

### 1. Format first
Pick the format from search intent, then follow its spine:
- **Listicle** ("best X", "top X", "X tools/agencies/alternatives") -> short intro -> `## 1. [Named option]` ... `## N. [Named option]` -> optional ONE "how to choose" checklist near the end -> FAQ -> short conclusion
- **Comparison** ("X vs Y") -> short intro -> quick context -> one section per option on the SAME criteria -> verdict -> FAQ
- **Review** -> short intro -> one section per aspect (features, pricing reality, support) -> verdict -> FAQ
- **How-to** ("how to X", literal procedures) -> short intro -> `## Step 1: [Action]` ... (sequential) -> FAQ -> conclusion
- **Explainer** ("what is X") -> short intro that answers the question in 2 sentences -> definition -> how it works -> pitfalls -> FAQ
- **Resources** ("X templates/examples/statistics") -> short intro -> the curated collection -> FAQ

The worst mistake is writing a "best X" listicle as a how-to ("Step 1: define your goals"). Name the actual options. That IS the article.

### 2. Go straight to the point
- Intro is SHORT: 2-4 sentences, under ~80 words. A hook, one line of stakes, then straight to the payoff.
- In a listicle/comparison/review, NEVER add a "Why X matters", "What is X", or "Benefits of X" preamble section. Fold a one-line definition into the intro at most, then go straight to the items.
- Never start a section with "In today's...", "When it comes to...", or "Whether you're X or Y."

### 3. Section anatomy
- **Listicle item** (`## N. [Name]`): one line of what it is (plain "is/has") -> who it's best for -> 2-4 sentences of concrete, sourced reasons it earns the spot -> an honest caveat/limitation -> vary the closer (don't end every item with "Bottom line:").
- **How-to step** (`## Step N: [Action]`): goal -> exact imperative instructions -> a milestone ("By now you should have...").
- **FAQ** (last before conclusion): 4-6 questions as people actually type them; 40-80 word answers; direct answer in the FIRST sentence (that's what AI engines lift).
- **Conclusion**: short -- one recommendation + one next action. No keyword-stuffed recap.

### 4. Humanize before you ship
Write the draft, cut these AI tells, then ask "what still reads like AI?" and fix it:
- Significance inflation ("a testament to", "plays a pivotal role", "stands as"); promotional fluff ("vibrant", "robust", "seamless", "boasts"); vague attribution ("experts believe" with no source).
- "-ing" tails that fake depth ("..., highlighting its value"); "not just X, it's Y"; forced rule-of-three; "from X to Y" false ranges; synonym cycling (one term, repeated).
- Signposting ("Let's dive in"); persuasive-authority tropes ("at its core", "the real question is"); fake-candor openers ("Honestly?", "Here's the thing").
- Filler ("in order to"->"to", "due to the fact that"->"because"); "**Label:** description" inline-header lists; em dashes; emojis; curly quotes.
- Use plain verbs (is/has, not serves as/boasts). Vary sentence length hard. Take a clear stance. Never bold the keyword.

### 5. Length: match the top results, then build on top (NOT shortness for its own sake)
- Decide length dynamically from the TOP 3 ranking pages for the keyword: check how long they are, match that depth, then build a little on top (skyscraper). They rank for a reason -- emulate them, then go a bit beyond. Cap it around 3,000 words; never runaway-pad.
- Reach that length with REAL substance: examples, sourced facts, specifics, genuine depth per section. Never filler or padding. Don't pad past the depth the topic needs, and DON'T undershoot it by writing thin.
- Structure stays tight even when the article is long: the DEPTH lives in the body sections, not a bloated intro.
- (Some founders prefer short, punchy articles. If the project's `ai_instructions` ask for that, follow them.)

### 6. SEO + AI-recommendation mechanics
- Primary keyword in the first ~100 words once (never bolded), then naturally where it fits. Don't repeat the exact phrase in every heading or stuff a stale year everywhere.
- Write quotable, self-contained claims AI engines lift as answers: "X reduces Y by Z%, according to [source]" beats "X has many benefits."
- Cite 2-3 real authority sources (primary sources, official docs, .gov/.edu, Wikipedia) -- never a competitor's blog ranking for the same keyword.
- Use H2 for sections, H3 for subsections. Output a fragment that follows the mandatory Article HTML Contract: stable unique H2 IDs, one matching TOC, and wrapped responsive videos. Never output markdown or a full HTML document.

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
# - Output a contract-compliant HTML fragment with stable H2 IDs and one matching TOC

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

### Phase 1: Identify buyer prompts

Generate **at least 100 realistic prompts** that a potential Distribb buyer would type into ChatGPT, Perplexity, Gemini, Claude, or Google AI Overviews, prompts where Distribb *should* be recommended.

Cover all of these prompt categories (≥10 per category):

1. **"Best tools"**, e.g. "What are the best AI SEO tools for agencies?"
2. **"Alternatives"**, e.g. "Best alternatives to Surfer SEO for automated content"
3. **"Comparison"**, e.g. "Outranking vs Surfer SEO vs automated SEO tools"
4. **"Problem-solving"**, e.g. "How do I automate SEO content and backlinks for my agency?"
5. **"Agency-specific"**, e.g. "Best white-label SEO automation software for agencies"
6. **"AI visibility / GEO"**, e.g. "How do I get my business recommended by ChatGPT?"
7. **"Backlink automation"**, e.g. "Best tools to get backlinks without manual outreach"
8. **"Content automation"**, e.g. "Best AI tools to write and publish SEO articles automatically"

Bias toward **buying intent**, **comparison intent**, and **problem-aware intent**. Skip pure informational queries ("what is SEO").

For **every** prompt, capture these columns:

| Column | Notes |
|---|---|
| Prompt | The exact phrasing a buyer would type |
| Search intent | Informational / Comparison / Transactional |
| Buyer stage | Problem-aware / Solution-aware / Ready-to-buy |
| Ideal Distribb angle | The single sentence positioning that should land in the AI answer |
| Main competitors likely to appear | Surfer, Jasper, Frase, MarketMuse, Clearscope, Scalenut, Outranking, SE Ranking, Semrush, Ahrefs, KoalaWriter, NeuronWriter, Copy.ai, Writesonic, etc. |
| Priority | 1-10 (10 = closest to ready-to-buy + highest commercial value) |
| Why this prompt matters | One-line rationale |

### Phase 2: Run and analyze the top 30 prompts

Take the **30 highest-priority prompts** from Phase 1 and actually run them. Use `WebSearch` and/or `WebFetch` against live AI-search-shaped queries, do not guess. For each, capture:

| Column | Notes |
|---|---|
| Prompt | From Phase 1 |
| Distribb appears? | Yes / No / Partial (e.g. mentioned but not recommended) |
| Competitors that appear | List the actual names in the live answer |
| Sources cited / referenced | URLs that the AI/SERP is citing, listicles, blogs, Reddit, YouTube, G2/Capterra, Product Hunt, company pages |
| Article(s) most influencing the answer | The 1-3 URLs doing the heavy lifting |
| Source type mix | SaaS review site / blog listicle / Reddit / YouTube / company page / forum / news |
| What Distribb needs to be included or rank higher | Concrete gap: missing from listicle X, no Reddit mention, no comparison page, no G2 profile, etc. |

**Hard rules for Phase 2:**
- **Do not fabricate URLs, rankings, or citations.** If a prompt can't be run or a source can't be verified, write `unverified` in the cell and explain why in a footnote.
- Cite source URLs in full.
- If a result is from a cache and may be stale, say so.

### Phase 3: Third-party listicles to target for outreach

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
| Current tools mentioned | The 5-15 tools already in the listicle |
| Distribb currently included? | Yes / No / Briefly mentioned |
| Outreach priority | High / Medium / Low |
| Suggested pitch angle | One specific reason to add Distribb (e.g. "you cover Surfer + Frase but no tool in your list does the backlink exchange piece") |
| Contact info | Contact page URL, author name, author email, or the "submit a tool" form URL, verified, not invented |
| Personalization notes | Recent post by the author, the year of the listicle, the angle of their site, anything a VA can use in the first line |

### Required output (in this exact order)

1. **Table 1, Top 100 prompts** (Phase 1, all columns).
2. **Table 2, Top 30 prompt tests** (Phase 2, all columns, with live source URLs).
3. **Table 3, Third-party listicles & sites to reach out to** (Phase 3, all columns).
4. **Top 10 outreach opportunities**, ranked by *easiest win x highest impact*. For each: target URL, why it's the easiest win (e.g. author already updates the post yearly, accepts tool submissions, already mentions a Distribb-adjacent tool), and the suggested first-line of the pitch.

### Operating rules (read before starting)

- **Prioritize listicles and third-party articles, not competitor homepages.** A pitch to "add Distribb to your round-up" is far easier than dislodging a competitor's own site.
- **Prioritize pages that already mention** Surfer SEO, Jasper, Copy.ai, Writesonic, Frase, MarketMuse, Clearscope, Scalenut, Outranking, SE Ranking, Semrush, Ahrefs, KoalaWriter, NeuronWriter, and similar, those authors have already decided this category is worth covering.
- **Do not fabricate** URLs, rankings, citations, author emails, or DR/traffic numbers. If you can't verify, say `unverified` and explain.
- **Think like a buyer, not like a keyword tool.** A keyword-volume prompt ("seo software") is less valuable than a buying-intent prompt ("best seo tool that also does backlinks for an agency").
- **Focus on prompts where someone is close to buying software or hiring a solution.**
- The final output should be **handover-ready** for a VA or outreach person, every row should be independently actionable.
- This workflow is **research + strategy**, not publishing. Do **not** call any Distribb article-creation endpoints (`POST /articles`, `POST /articles/generate`, etc.) during this workflow. Output the tables to the user; let them decide what to do next (pitch the listicles manually, or feed them into a separate outreach workflow).

### Tools to use

- `WebSearch` for finding listicles and running buyer-intent queries.
- `WebFetch` for reading the actual content of each candidate listicle (to confirm tools mentioned, find author/contact info, and check freshness).
- `GET /business-context?project_id=...` if running this for a non-Distribb project, so competitor exclusions are respected.
- Skip any Distribb write/publish endpoints, this workflow does not create articles.

**Where this hands off.** This workflow produces the target list. To actually earn the placement, run `/link-building` and read `references/link-building-playbooks.md`, which turns each target into a give-first campaign with an asset attached.

---

## Workflow: Link Building Playbooks (`/link-building`)

Use this when the user asks you to build links, run outreach, get backlinks outside the exchange, or any variant of "how do I get more sites linking to me".

**The full methodology lives in [`references/link-building-playbooks.md`](./references/link-building-playbooks.md). Read it before running any of these.** This section is the map.

Six playbooks, all give-first: you build something the prospect wants and hand it over, and the link is the consequence rather than the ask.

| # | Playbook | What it does | Run it when |
|---|---|---|---|
| 1 | **Invoice Method** | Mines the user's own billing history for vendors who want testimonials and list customers with links | They need links fast, or have none yet. Fastest to a live link, no asset to build |
| 2 | **Source Sniping** | Prospects by which domains AI engines actually cite, using `ai-visibility:get --view competitors` -> `other_cited` | They ask who to pitch, or get no AI mentions. Reorders every other campaign |
| 3 | **Tombstone Method** | Broken link building aimed at dead companies rather than dead URLs, to take listicle slots | Competitors are on every "best of" list and they are not |
| 4 | **Fact Decay Audit** | Audits a target page for claims that stopped being true, delivers a sourced correction sheet | They have outreach capacity but nothing worth sending |
| 5 | **Stale Screenshot** | Re-shoots a publisher's outdated product screenshots with browser control | They want links from pages already ranking for their keywords |
| 6 | **Missing Visual** | Builds a diagram from the prospect's own prose, for pages carrying image debt | They have content but nobody links to it |

### Three rules that override everything else in this section

1. **You do not send the email. The user does.** There is no Distribb endpoint for arbitrary cold outreach. Distribb's managed Link Outreach service is a **different product**: Distribb's own warmed inboxes, only for prospects Distribb generated, and its API surface is replies only (`GET /link-outreach/prospects`, `POST /link-outreach/prospects/:id/reply`, in-thread replying Accelerator-gated). Nothing in the API starts a campaign. These six playbooks end at a finished draft with the asset attached, saved to a file. Never tell the user you sent something you did not send.

2. **Never invent a fact about a prospect's page.** Four of the six work by telling a publisher something about their own content: a decayed fact, an aged screenshot, a dead company, a missing diagram. The publisher checks. If you cannot verify against a primary source, drop the item rather than hedging it.

3. **Prospecting data mostly comes from outside Distribb.** `search-console:get` covers the user's own property only, `keywords:search` returns keyword ideas rather than third-party SERPs, there is no referring-domain lookup for arbitrary URLs, and the saved Ahrefs key covers keyword research only. Use `WebSearch` / `WebFetch` or the user's own SEO tool for "pages ranking for X" and referring-domain counts, and say which. Source Sniping is the exception: Distribb hands you the prospect list.

4. **These are not volume plays.** Ten to thirty sends with a real asset beats five hundred without, and the mechanic stops working at scale precisely because what converts is that it is obviously bespoke. If the user wants volume, point them at Distribb's managed Link Outreach service (enabled inside Distribb, not from the API) and the backlink exchange, which are built for it.

### Where it plugs into the rest of the skill

- `context:get` for brand voice and the competitor list, which drives Tombstone and Source Sniping directly.
- `ai-visibility:prompts:add` + `ai-visibility:scan` + `ai-visibility:get --view competitors` for Source Sniping. `other_cited` is the prospect list.
- `ai-visibility:get --view cited_pages` to decide what the new links should point at, since engines already treat those URLs as quotable.
- `articles:create` + `articles:publish` if the user has no linkable asset yet. If they have nothing at all, run `/statistics-page-writer` first: a statistics page is the best single target for every playbook here.

---

## Workflow: Free .gov Backlinks (`/gov-backlinks`)

Government supplier registries (SAM.gov feeding SBA's public Small Business Search, plus
state vendor portals and international equivalents) give a real business a public profile
page on a .gov domain with a website field. That page is a legitimate, free backlink from
a real directory, and almost no business claims it.

Run it with `/gov-backlinks` and follow **`references/gov-backlinks-playbook.md`**, which
carries the exact SAM.gov wizard answers, the DBA documentation trap, browser automation
notes for SAM's custom form controls, and the hard handoff rules. The agent drives the
browser through navigation and business-fact form fields only. The user always performs
account creation, Terms of Use agreement, EIN entry, every certification, and every final
submit. Registration is free everywhere; anyone charging for it is a middleman.

The listing appears after the registration activates (up to 10 business days) and dies if
the annual renewal lapses, so log the renewal date wherever the user tracks links.

## Slash Commands

This skill ships a set of slash commands in its `commands/` folder so the user can drive the whole workflow with `/`. Each command is a thin entry point that loads this skill and the matching reference, then runs the workflow against `$ARGUMENTS`.

| Command | Argument | Runs |
|---|---|---|
| `/distribb` | (none) | Overview, account status, and the proper SEO process |
| `/distribb-setup` | (none) | Validate the API key, confirm website + GSC are connected, register the other commands |
| `/gsc-audit` | `<domain>` | Full audit (`references/audit-playbook.md`) |
| `/keyword-research` | `<seed keyword>` | Keyword ideas with volume + difficulty |
| `/write-article` | `<keyword>` | Research, write, link, backlink, and publish one article |
| `/optimize` | (none) | GSC-driven rewrites of pages stuck on page 2+ |
| `/backlinks` | (none) | Credits, targets, and how the exchange works |
| `/content-calendar` | (none) | List / schedule / manage articles |
| `/ai-visibility` | (none) | AI-search visibility + listicle outreach research |
| `/news-writer` | `<site-url-or-niche>` | Newsjack: find fresh news, write grounded drafts, queue in Distribb |
| `/statistics-page-writer` | `<industry-or-topic>` | Deep-research and publish a journalist-ready statistics page |
| `/instagram-carousel` | `<article-id-or-keyword>` | Turn one article/keyword into a viral, save-driven Instagram carousel (cover hook, comment-for-link play), publish it, and close the loop with a companion article |
| `/review-video` | `<competitor>` | Compile REAL, verified competitor reviews into a "<competitor> reviews" video, position the connected project as the alternative, append its own testimonials, publish to YouTube + companion article (drives `super-video-maker`) |
| `/gbp` | (optional: `reviews` \| `reply` \| `post` \| `status`) | Google Business Profile manager: review triage, public replies, posts, analytics |
| `/link-outreach` | (optional: `replies` \| `reply`) | Work backlink outreach replies: review who replied + asking price, draft + send in-thread replies from Distribb's inbox (Accelerator) |
| `/link-building` | (optional: `invoice` \| `source-sniping` \| `tombstone` \| `fact-decay` \| `screenshots` \| `visuals`) | Run one of six give-first outreach playbooks end to end, from prospecting to a ready-to-send draft with the asset attached (`references/link-building-playbooks.md`) |
| `/gov-backlinks` | (optional: `sam` \| `state` \| `international` \| `verify`) | Drive the user's browser through the free government registries that give a public .gov profile linking to their site, with hard handoffs at every account, tax, and certification step (`references/gov-backlinks-playbook.md`) |

**Enabling the commands.** Depending on how the skill was installed, the commands may already be live. If a command is not recognized, register them once by copying this skill's command files into the project's command folder:

```bash
# From the project root, with <skill_dir> = where this skill is installed
mkdir -p .claude/commands
cp <skill_dir>/commands/*.md .claude/commands/
```

`/distribb-setup` does this automatically (it locates the skill directory and copies the files for you), then the commands are available after the next message. Power users can also work entirely through the API sections in this file without any slash commands.

---

## Sub-skills

This skill ships with structured sub-workflows for opinionated multi-week SEO programs. Load the matching sub-skill's `SKILL.md` instead of trying to run the workflow from this top-level file.

| Sub-skill folder | When to invoke |
|---|---|
| [`90-day-seo-sprint/`](./90-day-seo-sprint/SKILL.md) | User asks for an SEO sprint, a 90-day SEO plan, an SEO tracker / roadmap, "where do I start with SEO", "how do I get my first 1,000 organic visitors", or anything similar. Sub-skill opens the Distribb tracker Google Sheet in their browser and walks them through 4 phases (Pre-launch / Foundation / Content Engine / Authority) using the API endpoints below. |

If a sub-skill applies, **read its `SKILL.md` first** before calling any endpoint. Each sub-skill assumes you already have a Distribb API key set and the parent skill loaded for the actual API surface, sub-skills only add structure, content, and execution discipline.

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

## Competitor Reviews Video (`/review-video`)

Turn the keyword **"<competitor> reviews"** into a fast, faceless voiceover montage of
**real, verified** competitor reviews that names the recurring complaints and positions
**the connected project's own business** as the alternative that fixes them, then hands off to
the project's own customer testimonials and ends on the project's CTA. It ranks for a
high-intent, mid-decision keyword and converts by pairing the competitor's own customers' words
with a truthful "here is the tool that closes exactly these gaps."

This is a hybrid workflow. **Distribb is the SEO brain** (the keyword, the project's business
context, YouTube publishing, and a companion article + backlinks) and the **`super-video-maker`**
skill is the production engine (review research + verification → real review screenshots →
ElevenLabs voiceover → captions → a three-part edit that appends the project's own testimonial
reel). Install it once, then follow its `REVIEW_VIDEO_PLAYBOOK.md`:

```bash
npx skills add Bomx/super-video-maker-skill
```

### Guardrail (read first)
Only put **real, verified, attributable** reviews on screen. Never invent, embellish,
paraphrase-as-a-quote, or doctor a review. Cherry-picking the honest negatives is legitimate
comparative marketing; fabricating or misrepresenting a competitor is false advertising and
defamation. Be honest about the competitor's overall rating and win on the *pattern* in the
complaints. If the competitor has no genuine critical-review volume, tell the user and stop.
**The alternative is always the connected project's own business, pulled from
`/business-context`, never a hardcoded company.**

### Workflow
1. **Who is the alternative.** Call `/business-context` for the project's name, value props,
   audience, language, and competitors. THIS project's business is what you position at the end.
   If the user did not name a competitor, offer the ones in `competitors`.
   ```bash
   curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
     "https://distribb.io/api/v1/business-context?project_id=42" | jq .
   ```
2. **Pick the keyword.** Search "<competitor> reviews" and "<competitor> alternative"; the
   primary keyword becomes the title spine and the companion article's keyword. (On a legacy
   Free Agentic account this returns HTTP 402 `byo_keys_required` until SEO keys are saved, so surface it
   verbatim and use the concept instead.)
   ```bash
   curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" -H "Content-Type: application/json" \
     -d '{"project_id":42,"keyword":"<competitor> reviews"}' \
     https://distribb.io/api/v1/keywords/search | jq .
   ```
3. **Research + verify + produce** with super-video-maker's `REVIEW_VIDEO_PLAYBOOK.md`: fan out
   across every review surface (Trustpilot, G2/Capterra, app stores, Reddit/forums, review blogs,
   YouTube, social), extract verbatim reviews with exact source URLs, drive a real browser where a
   site 403s automated fetches (Trustpilot), **adversarially verify every critical quote** (default
   to reject if you cannot corroborate it verbatim), then build the faceless voiceover montage. Map
   each recurring gap to a TRUE strength of THIS project's business (real backlinks, internal
   linking, GSC-grounded content, etc.). Append the project's own testimonial reel if the user has
   one; end on the project's site/CTA. Show the user the verified reviews + script before any paid
   generation.
4. **Publish + close the loop.** Confirm the project's YouTube channel is connected
   (`/integrations`; if not, send the user to https://distribb.io/integrations), then publish the
   MP4 with a keyword-led title, a description that restates the keyword and states every review
   shown is real and sourced, chapters, and tags. Then publish a companion article targeting
   "<competitor> reviews" / "<competitor> alternative" that embeds the video, weaving in
   `/internal-links` and (if in the exchange) `/backlink-targets`.

### Rules
- Real, verified, attributable reviews only; keep the on-screen source visible.
- The alternative is the connected project's business, from `/business-context`, never a
  hardcoded company. Only push that project.
- Real review screenshots, never generated ones. Confirm the YouTube connection and show the
  verified reviews + script before any paid generation.

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `GET /projects`, `GET /projects/:id`, `GET /articles`, `GET /articles/:id`, `GET /business-context`, `GET /integrations`, `GET /backlinks/status`, `GET /backlinks` | 30 req/min |
| `POST /keywords/search`, `POST /keywords/research` | 5 req/min |
| `GET /internal-links`, `GET /backlink-targets`, `GET /search-console` (and its `GET /rankings`, `GET /analytics` aliases) | 10 req/min |
| `GET /ai-visibility` | 30 req/min |
| `POST\|DELETE /ai-visibility/prompts` | 20 req/min |
| `POST /ai-visibility/scan` | 6 req/min |
| `GET /suggestions`, `GET /suggestions/:id`, `GET /suggestions/:id/diff` | 30 req/min |
| `POST /articles`, `PUT /articles/:id`, `DELETE /articles/:id`, `PUT /projects/:id`, `POST /projects`, `POST /projects/:id/wordpress` | 10 req/min |
| `POST /suggestions/:id/approve`, `POST /suggestions/:id/reject`, `POST /suggestions/:id/regenerate` | 10 req/min |
| `POST /articles/:id/publish`, `POST /suggestions/:id/publish`, `POST /projects/:id/onboarding` | 5 req/min |
| `POST /suggestions/run` | 3 req/min |

---

## Tips

- Always call `/business-context` first to understand the brand voice, competitors, and custom instructions.
- The `/internal-links` response tells you exactly how many links to include (`num_links_recommended`).
- Check `/backlinks/status` to see how many credits the project has. More credits = more backlinks received.
- NEVER skip `/backlink-targets` when `BecklinksNetworkParticipation` is `"Yes"`. This is the single most impactful SEO feature for the user. Articles without network backlinks do not earn credits.
- Scheduling: a `scheduled_date` promotes a `Draft` to `Planned` automatically; omit the date to keep it a `Draft` for review. Whether a scheduled article goes live or waits as a draft on its date is set by the project's `PublishingStatus` (`Publish Immediately` vs `Save as Drafts`/`Send as Drafts`), so always check that field before telling a user their article will publish.
- All API responses are JSON. Parse them with `jq` to extract IDs, URLs, and data for the next step.
- For long article HTML, write to a file first, then use `jq -n --arg content "$(cat article.html)"` to safely encode.

---

## Need an Account?

Sign up for Distribb Agentic Mode: **https://distribb.io/agentic**
3-day free trial, $49/mo. Your API key will be in Settings after signup.
