---
description: Distribb overview, account status, and the proper SEO process
argument-hint: (optional question)
allowed-tools: Bash, Read, Glob, Grep, WebFetch
---

Load the Distribb skill (its `SKILL.md`, installed under `.claude/skills/distribb/` or `~/.claude/skills/distribb/`) if it is not already active.

Then help the user with: `$ARGUMENTS`

If there is no specific question, do this:
1. Validate the API key with `GET /api/v1/projects` and report the projects, plan signals (backlink credits, articles per day, backlink-network participation), and whether Google Search Console is connected (`GET /api/v1/search-console`).
2. Show the user the **proper SEO process** from the skill's first-run section (account + onboarding -> connect website + GSC -> confirm a blog exists -> audit -> topic clusters -> keyword research -> write + backlink -> optimize).
3. List the available slash commands (`/gsc-audit`, `/keyword-research`, `/write-article`, `/optimize`, `/backlinks`, `/content-calendar`, `/ai-visibility`, `/distribb-setup`) and ask which step they want to start with.

If the API key is missing or invalid, point them to https://distribb.io to sign up / find their key in Settings.
