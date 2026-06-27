# Distribb Platform Tour

Where things live in the Distribb app, what the user does on each page, and the API call you (the agent) can use to do the same thing for them. Use this when a user asks "where do I see X?" or "can you check Y for me?"

The app is at https://distribb.io . Everything below is per-project; resolve `project_id` from `GET /projects` first.

---

## Dashboard
The landing page after login. Shows the user's projects and recent activity (articles generated, published, backlinks). New users may see "preparing" loaders while their first content and welcome assets are generated.
- Agent equivalent: `GET /projects` for the project list and high-level fields (status, backlink credits, articles per day, backlink-network participation).

## Content Calendar
Where the user sees and manages every article: Planned, Draft, and Published, plus the schedule. This is the heart of day-to-day use. Planned articles with a scheduled date auto-publish at that time; Drafts wait for review.
- See articles: `GET /articles?project_id=...` (filter by `status=Planned|Draft|Published`).
- Create/schedule: `POST /articles` (set `status` and `scheduled_date`).
- Edit: `PUT /articles/:id`. Unschedule: `PUT` with `scheduled_date: null`.
- Delete a Draft/Planned article: `DELETE /articles/:id` (published articles cannot be deleted).

## Settings
Where the user edits the project: business description, custom AI instructions, daily publish time, timezone, the backlink-network toggle, and their SEO data API keys (DataForSEO / Ahrefs for the Free Agentic plan, saved at https://distribb.io/settings#seo-keys).
- Read: `GET /projects/:id` (its `settings` object lists every writable key), `GET /business-context`.
- Change: `PUT /projects/:id` — the full Settings UI (~30 fields: instructions, sitemap/blog URLs, content pillars, tone, writing profile, positioning, internal links, region, language, images/brand, banned phrases, competitors, toggles, publish time/timezone). Send only the keys you want; partial updates are safe. See SKILL.md "Project Settings" for the table.
- Create + onboard a project: `POST /projects` (gated to paid slots), `POST /projects/:id/wordpress` (connect CMS), `POST /projects/:id/onboarding` (start keyword research — ask the user first).

## Integrations
Where the user connects their CMS (WordPress, Webflow, Shopify, Ghost, Wix, Notion, GoHighLevel, Framer, API webhook), social accounts, and **Google Search Console**.
- Connected platforms: `GET /integrations?project_id=...`.
- GSC status: `GET /search-console?project_id=...` (`connected: true/false`). Connect at https://distribb.io/integrations .

## Backlinks
Where the user sees the backlink exchange: links earned, links given, and remaining credits. **You can check all of this for the user, they do not have to open the dashboard.**
- Credits + status: `GET /backlinks/status?project_id=...`.
- Who they can link to next: `GET /backlink-targets?project_id=...&keyword=...`.
- Free plans receive 1 backlink/month; paid plans get unlimited exchange access. The user earns by giving, so every article should include 1-2 network links. See `plans-and-backlinks.md`.
- Note: links the user *receives* currently surface mainly on the dashboard Backlinks page; `GET /backlinks/status` is the most reliable programmatic read for credits and counts.

## Optimizations / Suggestions
Where Distribb proposes rewrites of underperforming pages, mostly from Google Search Console data (queries with impressions but low CTR, pages stuck at the bottom of page 1 or on page 2). Each suggestion stages a before/after diff. This is the highest-leverage ongoing loop because it improves pages that already rank.
- Generate a fresh batch: `POST /suggestions/run`.
- List + inspect: `GET /suggestions`, `GET /suggestions/:id`, `GET /suggestions/:id/diff`.
- Act: approve (`/approve`, triggers the rewrite), then publish (`/publish`). Regenerate with feedback or reject as needed.
- Command: `/optimize`.

## AI Visibility
Distribb's focus is not only Google rankings but being recommended by AI engines (ChatGPT, Perplexity, Gemini, Google AI Overviews). The `/ai-visibility` workflow finds the buyer prompts where the business should appear, checks where it currently does, and builds an outreach list of third-party listicles to get added to. The Accelerator plan automates much of this distribution as done-for-you work (see `plans-and-backlinks.md`).

---

## Quick "can you check this for me?" answers
- "How many backlinks do I have / how many credits?" -> `GET /backlinks/status`.
- "What's on my calendar?" -> `GET /articles`.
- "Is my Search Console connected?" -> `GET /search-console`.
- "What does Distribb think my competitors are?" -> `GET /business-context`.
- "What should I optimize next?" -> `POST /suggestions/run` then `GET /suggestions`.
- "Which CMS am I connected to?" -> `GET /integrations`.
