---
description: Manage the Google Business Profile, live review triage, public review replies, Google posts, analytics
argument-hint: (optional: reviews | reply | post | status)
allowed-tools: Bash, Read, Glob, Grep
---

Load the Distribb skill (Google Business Profile section) and manage the user's connected Google Business Profile. `$ARGUMENTS` may name a focus (`reviews`, `reply`, `post`, `status`); with no argument, run the full loop below.

1. Resolve `project_id` (`GET /api/v1/projects`), then check the connection: `GET /api/v1/gbp/status?project_id=...`.
   - If `connected` is `false`, relay `instructions_for_agent` verbatim (connect at https://distribb.io/integrations -> 'Add Integration' -> 'Google Business') and stop.
   - If connected, show the live summary: business name, address, `total_reviews`, `average_rating`, `unreplied_count`.
2. **Review triage**, pull what needs attention:
   - Unreplied: `GET /api/v1/gbp/reviews?project_id=...&has_reply=false&limit=25`
   - Negative/neutral: `GET /api/v1/gbp/reviews?project_id=...&max_rating=3`
   - Page with `cursor=next_cursor` while `has_more` is true. Quote ratings and text exactly as returned, never invent review data.
3. **Draft replies, get approval, post.** Pull the brand voice from `GET /api/v1/business-context?project_id=...` and draft a short reply per review (2-4 sentences: thank the reviewer by name, reference something specific, vary the wording across reviews). For negative reviews: professional, own what's ownable, move resolution offline. **Replies are PUBLIC on Google immediately**, show the drafts and get the user's go-ahead (a one-time approval of tone + approach covers a batch), then for each: `POST /api/v1/gbp/reviews/reply` with `{project_id, review_id, message}`. To edit a live reply, reply again; to remove one, `DELETE /api/v1/gbp/reviews/reply` with `{project_id, review_id}`.
4. **Google Business post** (fresh profiles rank better in the map pack): offer to queue one, `POST /api/v1/gbp/posts` with `{project_id, text (<=1500 chars), link (becomes the Learn More button), scheduled_date? ('YYYY-MM-DD HH:MM' UTC)}`. With a date it auto-publishes then; without, it lands as a draft in the Social Composer. Good default: a post pointing at the latest published article or a current offer.
5. **Analytics**: `GET /api/v1/gbp/analytics?project_id=...` covers posts published through Distribb. Be honest about limits: location insights (calls, direction requests, website clicks, search keywords), Q&A, photos, and business-info edits are NOT available through this connection.

Yes, you can do all of this for the user; they do not need to open Google Business Profile Manager. Suggest a weekly rhythm: triage new reviews (Distribb is subscribed to review notifications), reply to everything, one fresh post.
