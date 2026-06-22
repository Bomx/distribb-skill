---
description: Find and rewrite pages stuck on page 2+ using Google Search Console data
argument-hint: (none)
allowed-tools: Bash, Read, Glob, Grep, WebFetch
---

Run the GSC-driven optimization loop. Load the Distribb skill and:

1. Confirm GSC is connected (`GET /api/v1/search-console`). If not, send the user to https://distribb.io/integrations (or https://support.google.com/webmasters/answer/10267942?hl=en if they have no Search Console yet) and stop.
2. Generate a fresh batch: `POST /api/v1/suggestions/run` with `{"project_id": ...}`. This pulls GSC and scores pages with impressions but low CTR or stuck at the bottom of page 1 / on page 2.
3. List them: `GET /api/v1/suggestions?project_id=...&status=pending`. For each, read `GET /api/v1/suggestions/:id/diff` and show the user the before/after.
4. With the user's go-ahead (approve and publish are real, billable actions that push live to their CMS): `POST /api/v1/suggestions/:id/approve`, poll until `status: ready`, then `POST /api/v1/suggestions/:id/publish`. Use `/regenerate` with feedback if the rewrite is not right.
5. A `409` means the article changed since the suggestion was created (`superseded`); run `/suggestions/run` again and restart for that page.

This is the fastest win in SEO because these pages already rank. Prioritize the ones closest to page 1 with the most impressions.
