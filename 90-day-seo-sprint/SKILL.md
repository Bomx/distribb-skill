---
name: 90-day-seo-sprint
description: Run the Distribb 90-Day SEO Sprint - a founder-built 13-week playbook for shipping pre-launch SEO, core pages, a content engine, and a backlink starter stack on the way to compounding organic traffic. Use when the user asks for an "SEO sprint", "90-day SEO plan", "SEO tracker", "SEO roadmap", "where do I even start with SEO", "how do I get my first 1,000 organic visitors", or anything similar. This sub-skill opens the Distribb tracker spreadsheet in the user's browser, walks them through each phase, and hands off keyword research / backlink targets / publishing / Microworkers tasks to the parent Distribb skill.
homepage: https://distribb.io/90-day-seo-sprint
metadata: {"clawdbot":{"emoji":"📅","parent":"distribb"}}
---

## What this sub-skill is

A 13-week execution layer on top of the parent Distribb skill. The user gets a tracker spreadsheet with four phases (Pre-launch, Foundation, Content Engine, Authority) and ~31 dated tasks. You (the agent) help them load it, fill it in, and execute each task, using the parent Distribb skill for the actual API calls (keyword research, backlink targets, internal links, article submission, publishing).

This is **not a separate product**. It is the *opinionated way* to use Distribb for the first 90 days of a new (or low-DA) project. Everything in the tracker maps to endpoints already documented in the parent SKILL.md.

## When to invoke this sub-skill

Trigger on phrases like:

- "Where do I start with SEO?"
- "Walk me through a 90-day SEO plan."
- "Give me an SEO roadmap / sprint / tracker."
- "How do I get my first 1,000 organic visitors?"
- "Help me hit DR 10 / get 10 backlinks / rank in 90 days."
- "Open the 90-day SEO sprint tracker."
- "Run the SEO sprint for project [X]."

If the user just wants a single article published or a single keyword researched, **stay in the parent Distribb skill**, do not invoke this sub-skill.

## Required first action: open the tracker in the user's browser

Before discussing the sprint, surface the tracker to the user so they can fill it in as you go. Pick the first option that works in your runtime:

| Runtime / available tools | What to do |
|---|---|
| You have a browser MCP (e.g. `cursor-ide-browser`, `mcp__playwright`, `mcp__chrome-devtools`, `computer-use`) | Call `browser_navigate` (or equivalent) on the canonical Google Sheet URL: `https://docs.google.com/spreadsheets/d/1mBiXCNMymK0OTlptdO9QMa4IQbOHOycSLjt-joCL-wM/edit?usp=sharing`. Then take a `browser_snapshot` so you can reference cells while coaching the user. |
| You're in Claude Code / a CLI agent with shell access on macOS | Run `open "https://docs.google.com/spreadsheets/d/1mBiXCNMymK0OTlptdO9QMa4IQbOHOycSLjt-joCL-wM/edit?usp=sharing"`. Tell the user the sheet just opened in their default browser. |
| Linux / WSL | Run `xdg-open "https://docs.google.com/spreadsheets/d/1mBiXCNMymK0OTlptdO9QMa4IQbOHOycSLjt-joCL-wM/edit?usp=sharing"` (or `wslview` on WSL). |
| Windows shell | `start https://docs.google.com/spreadsheets/d/1mBiXCNMymK0OTlptdO9QMa4IQbOHOycSLjt-joCL-wM/edit?usp=sharing` |
| No browser, no `open`-style command available | Print the URL clearly and ask the user to open it themselves. |

The user has read-only access to the master sheet. After opening it, tell them to hit **File -> Make a copy** so they get their own editable copy in their own Drive. They can then work in Google Sheets, or download it as `.xlsx` from Sheets to use offline in Excel or Numbers.

If a browser tool was used, capture a snapshot of the **Cover** tab and confirm the user is looking at the right document before continuing.

## The tracker contains 7 tabs

| Tab | Purpose | Agent interactions |
|---|---|---|
| **Cover** | Distribb-branded intro: phases overview, KPIs (`10+`, `100K+`, `90`), tab-by-tab usage guide. | Read-only orientation. Use it to anchor the conversation. |
| **Dashboard** | Single input cell: `B4` (start date, `YYYY-MM-DD`). Auto-calculates current day / week / phase. KPI table. Pulls task counts from other tabs via `=COUNTIF(...)`. | Always ask the user for their `start_date` first and fill `B4`. Everything else flows from there. |
| **Task Tracker** | 31 pre-filled tasks across the 4 phases. Columns: `Week`, `Phase`, `Focus`, `Task`, `Owner`, `Done?`, `Notes`. | The Done column (F) is the user's checklist. The agent's job each session is to find the next 1-3 unchecked tasks and execute them through the parent Distribb skill. |
| **Keywords** | 30 numbered rows. Columns: `#`, `Keyword`, `Intent`, `Search volume`, `KD`, `Target page (URL)`, `Wk 4 pos`, `Wk 8 pos`, `Wk 13 pos`. | Fill via `POST /keywords/search` from the parent skill. Tag intent as Problem / Solution / Brand. Skip any keyword whose top 3 ranking domains all have DR > 50. |
| **Backlinks** | 15 starter directories pre-filled (Product Hunt, G2, Capterra, SaaSHub, AlternativeTo, BetaList, IndieHackers, Hacker News, Reddit, StackShare, …) + 15 blank rows. Columns: `#`, `Source / Site`, `Type`, `URL`, `Live?`, `DR`, `Notes`. | Combine with `GET /backlink-targets` from the parent skill to get *additional* exchange-network backlinks per article keyword. Tick `Live?` only when the link is verified live. |
| **Content Calendar** | 18 suggested entries by week (comparison pages → use-case pages → blog posts → pillar + cluster → updates). Columns: `Wk`, `Type`, `Target keyword`, `Title`, `Status`, `Published?`, `URL`, `Repurposed?`. | One row per planned article. Tick `Published?` after `POST /articles/:id/publish`. Tick `Repurposed?` after the auto-generated LinkedIn / X / Reddit posts are reviewed. |
| **Day 90 Audit** | 16 items grouped by Traffic / Technical / Content / Authority. Two columns: `Day 0 baseline`, `Day 90 result`. | Help the user fill the `Day 0 baseline` column on the very first session. At Day 90 (week 13), help them screenshot GSC and fill `Day 90 result`. |

## The 4 phases

Each phase has a clear deliverable, a set of tasks in the tracker, and a matching set of Distribb API calls.

### Phase 0: Pre-launch (Day 0)

Run these the day before or the day of launch.

- Unique title tag + meta description on every page (not just the home).
- `SoftwareApplication` (or `Article`) schema markup.
- Verify Google Search Console + submit the sitemap.
- Verify Bing Webmaster Tools (import GSC).
- Manually request indexing for the 5 most important URLs.
- Cross-link from an existing property you own (or drop a strong post on X / LinkedIn).

**Distribb calls in this phase:** none yet. This is pure hygiene.

**Agent action:** confirm each task is done with the user. Tick the boxes in column F of Task Tracker. If the user has not launched yet, hold here.

### Phase 1: Foundation (Days 1-30)

Goal: clean site, real keyword list, three core pages live.

- Lighthouse / PageSpeed on home + 3 core pages.
- robots.txt, sitemap, canonical tags, Core Web Vitals.
- Pick 20-30 winnable keywords (DR < 50 in top 3).
- Tag each keyword by intent: Problem / Solution / Brand.
- Rewrite homepage H1 with the primary keyword.
- Publish the highest-intent use-case page.
- Publish the first "you-vs-category-leader" comparison page.

**Distribb calls in this phase:**

```bash
# Keyword universe
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "<seed>", "project_id": <id>}' \
  https://distribb.io/api/v1/keywords/search | jq .

# Business context (brand voice, competitors, custom instructions)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=<id>" | jq .

# Internal links you can weave into the core pages
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=<id>&keyword=<kw>" | jq .

# Backlink targets, REQUIRED if BecklinksNetworkParticipation is "Yes"
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=<id>&keyword=<kw>" | jq .

# Submit the core pages as articles in the Distribb content calendar
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "project_id": <id>, "keyword": "<kw>", "title": "<title>", "content": "<HTML>", "status": "Draft" }' \
  https://distribb.io/api/v1/articles | jq .
```

**Agent action:** for each keyword the agent surfaces from `/keywords/search`, drop it into a new row on the **Keywords** tab. Fill `Intent`, `Search volume`, `KD`. Tick the Phase 1 tasks in the Task Tracker as you ship each core page.

### Phase 2: Content Engine (Days 31-60)

Goal: 2-3 articles/week and 10 referring domains.

- Publish comparison and alternative pages **first** (highest conversion intent).
- Then use-case pages.
- Then problem-aware blog posts.
- Then thought leadership.
- Ship a pillar post + first programmatic template.
- Internal-link a cluster of 5-7 supporting posts back to the pillar.
- Submit to the 15 starter directories on the **Backlinks** tab.
- Ship 1 strong guest post on a DR 40+ blog.
- DM 3 founders with complementary products and trade one relevant link each.

**Distribb calls in this phase:**

For **every article** you create:

1. `POST /keywords/search` if you haven't already added the keyword to the **Keywords** tab.
2. `GET /business-context?project_id=...` (cached fine for the session).
3. `GET /internal-links?project_id=...&keyword=...`.
4. `GET /backlink-targets?project_id=...&keyword=...`, **mandatory** if `BecklinksNetworkParticipation: "Yes"`. Include 1-2 returned URLs as natural references in the article body.
5. Write the article (use the parent SKILL.md's SEO writing guidelines, avoid AI giveaway phrases, vary sentence length, use H2/H3 structure).
6. `POST /articles` with `status: "Draft"` for review or `"Planned" + scheduled_date` for auto-publish.
7. After review, `POST /articles/:id/publish` to push to the user's CMS (or let it auto-publish on schedule).
8. Append the article to the **Content Calendar** tab: fill `URL`, tick `Published?`. Distribb auto-creates social posts for every connected platform, tick `Repurposed?` after the user reviews them in the Distribb dashboard.

For the **backlink starter stack**: rate-limit the agent's directory submissions to ~3 per session so you stay human-paced. After each submission, fill the URL in the **Backlinks** tab and leave `Live?` unchecked until the directory editor approves.

### Phase 3: Authority & Compounding (Days 61-90)

Goal: turn early signals into compounding growth.

- Pull GSC pages currently ranking positions 8-20, rewrite + expand them. (Use `PUT /api/v1/articles/:id` to update existing Distribb-published articles.) Position 14 → 4 can triple traffic on a single page.
- Build the first content cluster (5-7 supporting posts around one pillar).
- Add FAQ schema to every key page.
- Format snippet-eligible answers as clean 40-60 word paragraphs.
- Convert H2s into actual questions so ChatGPT, Perplexity, and Google AI Overviews cite the page.

**Distribb calls in this phase:**

```bash
# Rewrite an existing article (e.g. one ranking position 14 that you want at 4)
curl -s -X PUT -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat revised.html)" '{ "content": $content }')" \
  https://distribb.io/api/v1/articles/<id> | jq .
```

If the user wants to chase AI-search visibility specifically, jump into the **"Workflow: AI Search Visibility & Listicle Backlink Outreach"** section in the parent SKILL.md, that's the right tool for Phase 3 outreach work.

### Day 90 audit (Week 13)

Open GSC, screenshot the impressions chart, and fill the **Day 90 Audit** tab. If GSC impressions grew from day 1 to day 90, the sprint worked. The screenshot is the user's next social post.

## Standard session loop

Every time the user comes back to you with the sprint:

1. Open / refresh the tracker in their browser (if you have a browser tool).
2. Read the **Dashboard** tab's `Current phase` cell to know where they are.
3. On **Task Tracker**, find the next 1-3 tasks with `Done?` unchecked.
4. Execute those tasks using the parent Distribb skill API calls. Update the tracker as you go, either by pasting cells into the user's sheet via the browser MCP, or by giving them the exact values to paste.
5. End the session with a one-line summary: tasks shipped this session, tasks remaining in the current phase, and the very next action they should take.

## Tracker maintenance ground rules

- Do not edit the tracker columns or move tabs. The Dashboard tab's formulas reference exact cell locations (`'Task Tracker'!H2`, `'Backlinks'!F2`, `'Content Calendar'!G2`). Breaking those breaks the at-a-glance view.
- The `Done?` columns are stored as `TRUE` / `FALSE`. In Google Sheets, you can multi-select the column and `Insert → Checkbox` to turn them into clickable boxes. Tell the user once, then move on.
- Never delete the 15 starter directories on the **Backlinks** tab. Append new sources below row 19.
- If the user wants a fresh copy of the tracker (e.g. their first one got messy), regenerate by running `python3 make_seo_sprint_sheet.py` from the parent Distribb project, then drag the resulting `.xlsx` into Google Drive.

## Related Distribb workflows to compose with this sub-skill

- **Keyword research + intent classification** → parent SKILL.md `POST /keywords/search` (Phase 1).
- **Backlink exchange (the most important leverage point)** → parent SKILL.md `GET /backlink-targets` (Phases 2-3, every article).
- **AI search visibility / listicle outreach** → parent SKILL.md `Workflow: AI Search Visibility & Listicle Backlink Outreach` (Phase 3).
- **Microworkers Reddit / Quora / YouTube campaigns** → parent SKILL.md `POST /microworkers/campaigns` (great for Phase 2 distribution).

## Need an account?

The full landing page (long-form playbook + email gate that delivers this tracker) is at **https://distribb.io/90-day-seo-sprint**.

The user signs up for Distribb at **https://distribb.io/agentic**. Current plans are Agentic Mode at $49/month and Pro at $97/month. The free Agentic plan is deprecated and no longer offered to new users.
