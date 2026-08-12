---
description: Run a full Distribb SEO audit from Search Console + on-page + competitor + cannibalization + topic clusters
argument-hint: <domain or project>
allowed-tools: Bash, Read, Glob, Grep, WebFetch, WebSearch, Task, Write
---

Run a complete SEO audit for: `$ARGUMENTS`

Load the Distribb skill and follow `references/audit-playbook.md` exactly. In short:

1. Resolve the project (`GET /api/v1/projects`) and read `GET /api/v1/business-context` for competitors and brand terms.
2. Pull data: `GET /api/v1/search-console?project_id=...&days=90&limit=100` and `POST /api/v1/suggestions/run` + `GET /api/v1/suggestions`. If GSC is not connected, run the no-GSC subset and tell the user the audit is stronger once connected (point to https://distribb.io/integrations , or https://support.google.com/webmasters/answer/10267942?hl=en if they have no Search Console yet).
3. Run all nine analyses (CTR, decay, striking distance / page-2, cannibalization, dead pages, brand vs non-brand, topical clusters / topic cocoons, competitor gaps, on-page checks). For large GSC datasets, run each analysis in its own sub-agent.
4. Deliver the report: executive summary, the nine sections with tables, and a **prioritized action plan** where every finding maps to a Distribb action (`/optimize` for existing pages, `/write-article` for gaps, internal-link fixes).
5. Offer CSV export and offer to execute the top 3 items now.

The audit works on every plan.
