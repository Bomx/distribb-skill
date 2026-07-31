---
description: List, schedule, and manage planned, draft, and published articles
argument-hint: (optional - e.g. "show drafts", "schedule next week")
allowed-tools: Bash, Read, Glob, Grep
---

Manage the content calendar. Intent: `$ARGUMENTS`

Load the Distribb skill and:

1. Resolve `project_id` (`GET /api/v1/projects`). **Read the project's `PublishingStatus`** from that response, it decides what "scheduled" actually does (see the publishing-preference note at the bottom). If a user is confused about why a scheduled article "won't publish", this field is almost always the answer.
2. Show the calendar: `GET /api/v1/articles?project_id=...` (filter with `status=Planned|Draft|Published`; paginate with `limit`/`offset`). Summarize what is published, what is drafted, and what is scheduled and when. When you summarize, state the project's publishing preference in plain words so the user knows whether scheduled items go live or wait as drafts.
3. Act on the user's request:
   - Schedule a draft: `PUT /api/v1/articles/:id` with `status: Planned` + `scheduled_date` (ISO 8601, respects the project timezone).
   - Unschedule: `PUT` with `scheduled_date: null` (drops back to Draft).
   - Edit title/content/meta/keyword: `PUT /api/v1/articles/:id`.
   - Edit an article that is ALREADY PUBLISHED: same `PUT`, then `POST /api/v1/articles/:id/sync` to update the live post in place (or send `"sync": true` in the PUT to do both). Two fields are frozen once live: changing `keyword` no longer moves the slug (it is the public URL), and `status` cannot go back to Draft/Planned (`400 cannot_unpublish`). In-place updates work on WordPress, Webhook, Shopify, Webflow, Wix, Ghost, GoHighLevel, Framer and Notion; anything else returns `unsupported_for_sync` and has to be edited on the platform.
   - Publish now: `POST /api/v1/articles/:id/publish`. This goes LIVE immediately even on a `Save as Drafts`/`Send as Drafts` project (a deliberate publish overrides the auto-publish preference). It needs a connected website/CMS, if there is none you get `400 no_cms_integration`; relay it and point the user to https://distribb.io/integrations. Confirm a CMS is connected (`GET /api/v1/integrations`) before promising a user their article will publish; a Search Console (analytics) link does not count.
   - Delete a Draft/Planned article: `DELETE /api/v1/articles/:id` (published articles cannot be deleted; unschedule or unpublish instead).
4. If the calendar is empty or thin, recommend running `/gsc-audit` to build a topic-cluster plan, then `/write-article` to fill it.

**Status vs publishing preference (this is the thing people get wrong):**

- A `Planned` article with a `scheduled_date` enters the pipeline for that date; a `Draft` waits for review. Setting a `scheduled_date` on a Draft now auto-promotes it to `Planned` (you no longer have to send `status:Planned` separately, though doing so is still fine).
- What happens ON the scheduled date depends on the **project's `PublishingStatus`**, not just the article status:
  - **`Publish Immediately`** -> the article goes **live** on your site on its scheduled date.
  - **`Save as Drafts`** -> Distribb keeps it as a **draft inside Distribb** for you to review and publish manually. It will NOT auto-publish to your site. This is the usual reason a perfectly-scheduled article "won't publish" on its own.
  - **`Send as Drafts`** -> the article is pushed to your CMS as a **draft** (e.g. a WordPress draft) on its date, still not live, you publish from the CMS.
- So if a user asks "why won't my scheduled article publish?", first check `PublishingStatus`. If it is `Save as Drafts`/`Send as Drafts`, explain that the article is ready and waiting as a draft by design, and that switching the project to `Publish Immediately` (Settings, or `PUT /api/v1/projects/:id` with `{"publishing_status":"Publish Immediately"}`) is what makes scheduled articles go live automatically.
