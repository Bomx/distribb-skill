---
description: List, schedule, and manage planned, draft, and published articles
argument-hint: (optional - e.g. "show drafts", "schedule next week")
allowed-tools: Bash, Read, Glob, Grep
---

Manage the content calendar. Intent: `$ARGUMENTS`

Load the Distribb skill and:

1. Resolve `project_id` (`GET /api/v1/projects`).
2. Show the calendar: `GET /api/v1/articles?project_id=...` (filter with `status=Planned|Draft|Published`; paginate with `limit`/`offset`). Summarize what is published, what is drafted, and what is scheduled and when.
3. Act on the user's request:
   - Schedule a draft: `PUT /api/v1/articles/:id` with `status: Planned` + `scheduled_date` (ISO 8601, respects the project timezone).
   - Unschedule: `PUT` with `scheduled_date: null` (drops back to Draft).
   - Edit title/content/meta/keyword: `PUT /api/v1/articles/:id`.
   - Publish now: `POST /api/v1/articles/:id/publish`.
   - Delete a Draft/Planned article: `DELETE /api/v1/articles/:id` (published articles cannot be deleted; unschedule or unpublish instead).
4. If the calendar is empty or thin, recommend running `/gsc-audit` to build a topic-cluster plan, then `/write-article` to fill it.

Planned articles with a `scheduled_date` auto-publish at that time. Drafts wait for review.
