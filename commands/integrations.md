---
description: See every integration the account can connect, get the user connected, and use any connected integration (ad accounts, social inboxes, analytics, banks, outreach tools, databases, new integrations)
argument-hint: (optional: an integration or a goal, e.g. "meta ads", "hunter", "analytics", "paid ads")
allowed-tools: Bash, Read, Glob, Grep
---

Load the Distribb skill (Integrations section) and read `references/integrations-playbook.md`. `$ARGUMENTS` may name an integration or a goal; with none, run the full loop.

1. Resolve `project_id` (`GET /api/v1/projects`). If there are several projects, use the one the user is working on.
2. Read the catalog: `GET /api/v1/integrations/catalog?project_id=...` (CLI `integrations:catalog`). Summarize in a short table: connected (with account names), available to connect, and anything unavailable on this account. The catalog is the source of truth; never promise an integration it does not list as available.
3. Recommend, do not quiz. From the user's goal (or `$ARGUMENTS`), pick the two or three connections that matter most (the playbook's "What to connect first" table), one line each on why.
4. To connect one: `GET /api/v1/integrations/connect?project_id=...&integration=<key or name>` (CLI `integrations:connect`). Send the user the `connect_url` and the steps. They sign in or paste their key on Distribb's own card. **Never ask for passwords or API keys in the chat.** When they say it is done, read the catalog again and confirm `connected: true` before saying so.
5. To use a connected integration:
   - Find the tools: `GET /api/v1/agent-tools?area=<area>` or `?integration=<name>` (CLI `tools:list`); pass `names=` to get each tool's `input_schema`.
   - Reads and previews: `POST /api/v1/agent-tools/call` with `"mode": "read"` (CLI `tools:call --mode read`).
   - Changes: preview first, show the user the exact change, then after a clear yes run it with `"mode": "action"` and `"confirm": true` for preview_safe tools.
   - A result with `status: running` has a `job_id`: read it with `GET /api/v1/agent-tools/jobs/<job_id>` (CLI `tools:job`) about 30 seconds later. Never start the same call twice.
6. For the work itself, read the matching playbook: `references/paid-ads-playbook.md`, `references/social-media-playbook.md`, `references/outreach-playbook.md`, `references/seo-playbook.md` (or `GET /api/v1/playbooks/<topic>`).

Report what is connected, what you did with each integration (with ids, live URLs or statuses as proof), and the next connection or action worth doing.
