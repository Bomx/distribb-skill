---
description: Research, write, link, backlink, and publish one SEO article
argument-hint: <keyword>
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Write and publish one article targeting: `$ARGUMENTS`

Load the Distribb skill and follow the Core Workflow + the **SEO Article Writing System**:

1. `GET /api/v1/business-context` - brand voice, competitors (never link to them), AI instructions, language.
2. `GET /api/v1/internal-links?project_id=...&keyword=$ARGUMENTS` - pages to cross-link (use the recommended count).
3. If the project has `BecklinksNetworkParticipation: "Yes"`, `GET /api/v1/backlink-targets?...&keyword=$ARGUMENTS` and include **1-2** of those URLs as natural references. This is mandatory; it is how the user earns backlinks.
4. Write the article using the **SEO Article Writing System** in `SKILL.md` (format first from search intent, short intro straight to the point, humanizer pass, length matched to the top results, valid HTML). Never bold the keyword. Never link to competitors.
5. Submit: `POST /api/v1/articles` with `project_id`, `keyword`, `title`, `content`, `meta_description`, and `status` (Draft to review, or Planned + `scheduled_date` to auto-publish). Optionally set `category` (a CMS category NAME that already exists on the destination CMS) and `published_at` (a past ISO 8601 timestamp to backdate the CMS post). For long HTML, write it to a file and pass it with `jq -n --arg content "$(cat article.html)"`.
6. If the response has a `backlinks_warning`, add network links and `PUT` the revised content.
7. Confirm where it landed (calendar / draft / scheduled) and offer to publish now with `POST /api/v1/articles/:id/publish`.

If the user wants Distribb to write it from their notes instead (Pro plan), use `POST /api/v1/articles/generate`.
