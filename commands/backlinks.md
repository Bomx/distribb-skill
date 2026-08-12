---
description: Check backlink credits and targets, and explain how the exchange works
argument-hint: (optional keyword)
allowed-tools: Bash, Read, Glob, Grep
---

Load the Distribb skill and report on the backlink exchange:

1. Resolve `project_id` (`GET /api/v1/projects`) and check standing: `GET /api/v1/backlinks/status?project_id=...` (credits + counts).
2. Show available targets: `GET /api/v1/backlink-targets?project_id=...&keyword=$ARGUMENTS` (or a relevant keyword if none given).
3. Explain the exchange clearly (see `references/plans-and-backlinks.md`):
   - Distribb is a network of real businesses that link to each other; links are detected on article submission and credited (+1 per link given).
   - The user only receives by giving, so every article should include 1-2 network links.
   - **Every current plan gets unlimited exchange access; legacy Free Agentic accounts receive 1 backlink/month.**
   - These are real, high-DR links from legitimate sites, not link farms.
4. If they want more received links, the levers are: publish more articles that include network links, and stay opted in (`backlinks_network` toggle in Settings). On a legacy Free Agentic account, mention that every current plan unlocks unlimited exchange.

Yes, you can check all of this for the user; they do not need to open the dashboard.
