# Distribb Onboarding Guide

What Distribb learns about a business during onboarding, why it matters, and how you (the agent) can read or change each setting later through the API. When a user has just signed up, walk them through onboarding. When a user is already set up, use this to understand what Distribb already knows and to spot thin or missing settings.

Onboarding lives at https://distribb.io and runs once per project. The first thing it asks for is the website URL, then an AI pass analyzes the site in the background and auto-populates most of the fields below. The user can review and adjust them under an "Advanced: Customize AI settings" section, and can change everything later in Settings.

---

## Step 1: Website URL
The single required field. Distribb analyzes the site to auto-fill business details, language, competitors, and SEO settings. Tell the user to use their real primary domain. Read later via `GET /projects` (`WebsiteUrl`).

## Step 2: Connect your platform (CMS)
The user connects the blog/CMS Distribb will publish to. Options: **WordPress, Notion, Webflow, Shopify, Wix, Ghost, GoHighLevel, Framer, or a generic API webhook.** Distribb tries to auto-detect the platform (e.g. it will spot Shopify). Until publishing preferences are changed, articles are saved as drafts. Read connected integrations via `GET /integrations?project_id=...`.

If the user has a webhook-based or custom CMS, the API Webhook option lets them point Distribb at any endpoint. For WordPress, they need the site URL, username, and an **Application Password** (not their login password).

## The business profile (auto-filled, user-adjustable)

### Content
- **Language** (e.g. English US/UK, Spanish, French, German, and ~35 more). Drives the language all content is written in. `GET /projects` -> `Language`.
- **Tone and Style:** Informative / Conversational / Persuasive.
- **Writing Profile:** Experienced practitioner (sounds specific, operational, less AI-written) / Simple educational / Balanced SEO.
- **Product Positioning:** Neutral operational (useful, not salesy) / Soft mention / Promotional. Controls how hard the user's own product is pushed in articles.

### Blog information
- **Sitemap URL** and **Blog Root URL:** where the blog lives, used for internal linking and on-page analysis.
- **Content Pillars URLs:** the main pages or topic hubs the business wants to build authority around. These seed the topic-cluster (topic cocoon) strategy, so they matter a lot for the audit. Comma- or newline-separated.

### SEO
- **Internal Links:** target number of internal links per article (1-5). Distribb only inserts links to relevant live pages, so new sites get fewer until they have published content. Mirrors `internal_links_per_article` in `GET /business-context`.
- **Keyword Region:** the geographic market for search-volume data (Worldwide or a specific country).
- **Ideal Publishing Time** + **Timezone:** when scheduled articles auto-publish, in the user's local time. Editable via `PUT /projects/:id` (`publish_time`, `timezone`).
- **Blog Publishing Preference:** Publish Immediately / Save as Drafts in Distribb (review in the Distribb editor first) / Send as Draft to the website (creates CMS drafts instead of going live).
- **Image Hosting:** Distribb (hosted on Distribb's servers) or My CMS (uploaded to the user's own site).

### Overall AI instructions
A free-text field for custom rules applied to all content and keyword research (e.g. "friendly tone, focus on SaaS, avoid jargon, prefer long-tail, never mention competitor X"). This is the most powerful single field. It maps to `ai_instructions` and is editable via `PUT /projects/:id`. Always read it (`GET /business-context`) before writing and respect it exactly.

### Enhancements
- **Image Style:** Realism / Watercolor / Cinematic / Illustration / Sketch / Doodle / Papercraft / Neon Noir / Claymation / Stained Glass / Custom.
- **Include YouTube Videos in Articles:** on/off.
- **Brand Intelligence:** when on, Distribb analyzes the site's visual identity and uses it for images and copy.
- **Duplicate Content Protection:** when on, Distribb avoids planning or finalizing articles too similar to existing content.

### Competitors
The user adds **3 to 7 competitors**. Distribb uses these for keyword discovery, content-gap analysis, and to tune content to challenge them. These feed the audit's competitor analysis. Read them via `GET /business-context` (`competitors`). Never link to a competitor in the user's content; the writer positions the client above them in any "best X" list.

---

## The two connections that matter most

Everything downstream depends on these two. Confirm both before running keyword research or writing.

### 1. Website / CMS
How Distribb publishes. Set in Step 2 above. Verify with `GET /integrations`. If nothing is connected, the user can publish nowhere, so fix this first. Also confirm the site has a real **blog** (a blog index page or CMS collection). A surprising number of new users have no blog, so their articles have nowhere to live and they see "no results."

### 2. Google Search Console
How you audit, avoid keywords they already rank for, find opportunities, and run optimization suggestions. It is offered during onboarding (optional) and can be added anytime in Settings / Integrations.

- Connect it inside Distribb at https://distribb.io/integrations . It only links if the site is already added and verified in the user's Search Console account.
- Verify the connection with `GET /search-console?project_id=...` (returns `connected: true/false`).
- **If the user does not have Google Search Console set up at all yet**, send them to Google's official guide first: https://support.google.com/webmasters/answer/10267942?hl=en . Once their site is verified in Search Console, they connect it to Distribb as above.

Strongly encourage connecting GSC. Without it the audit and the optimization loop run in a much weaker, blind mode.

---

## Reading and changing settings via the API
- Read everything: `GET /projects`, `GET /projects/:id` (returns a `settings` object with every writable key), `GET /business-context?project_id=...`.
- Change settings: `PUT /projects/:id` with only the keys to change. The PUT now exposes the **FULL Settings UI (~30 fields)** — sitemap/blog URLs, content pillars, tone, writing profile, product positioning, internal links, keyword region, language, images/brand color, banned phrases, competitors, CTA intensity, brand intelligence, duplicate-content protection, publish time/timezone, and more. Partial updates are safe (quality/image prefs are merged, not reset). See SKILL.md "Project Settings" for the full field table. Note: `articles_per_day` is plan-controlled and optimization thresholds aren't persisted, both are echoed under `ignored`.

## Onboarding a NEW project via the API (agency scale)
You can run the whole client setup without the dashboard:
1. **Create the project:** `POST /projects` with `website_url` (required) plus any settings fields to configure it in one call. Project creation is gated by the account's paid slots: if it returns **HTTP 402 `project_limit_reached`**, show the user the `purchase_url` (one click buys a slot), then retry the same call. Never bypass the limit.
2. **Connect the CMS:** `POST /projects/:id/wordpress` with `wordpress_url` + the Distribb plugin `integration_key` (or have the user connect Webflow/Shopify/etc. in the dashboard).
3. **Tune settings:** `PUT /projects/:id` for any remaining fields.
4. **Start keyword research + first articles:** `POST /projects/:id/onboarding`. **ASK THE USER FIRST** — it spends keyword/LLM credits. It returns `202`; poll `GET /articles?project_id=...` to watch planned articles appear. (Free/Agentic plans bring their own keywords, so it returns `skipped_byok`.)

When onboarding fields are thin (e.g. no content pillars, only one competitor, empty AI instructions), proactively offer to improve them. Better inputs here lift the quality of every article and the accuracy of the audit.
