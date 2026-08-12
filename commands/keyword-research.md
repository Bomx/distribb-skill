---
description: Find keyword ideas with search volume and difficulty
argument-hint: <seed keyword>
allowed-tools: Bash, Read, Glob, Grep
---

Run keyword research for the seed: `$ARGUMENTS`

Load the Distribb skill and:

1. Resolve `project_id` (`GET /api/v1/projects`) and read `GET /api/v1/business-context` so results respect the user's region, audience, and AI instructions.
2. Call `POST /api/v1/keywords/search` with `{"keyword": "$ARGUMENTS", "project_id": ...}`.
   - On **HTTP 402 `byo_keys_required`** (legacy Free Agentic account with no SEO key saved): stop, surface the `instructions_for_agent` text verbatim, link the user to https://distribb.io/settings#seo-keys , and do not retry until they confirm.
3. Present the keywords with volume and difficulty. Group them into **topic clusters** (a pillar plus supporting articles) rather than a flat list, and flag the high-intent, lower-difficulty terms as the best first targets.
4. Offer to turn the best keyword into an article with `/write-article <keyword>`.

Prefer buyer-intent and comparison keywords ("best X", "X vs Y", "X for [use case]") over pure informational terms.
