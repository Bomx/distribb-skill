---
description: Turn fresh news in the site's niche into grounded news-article drafts and queue them in Distribb to autopublish
argument-hint: <site-url-or-niche>
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Turn fresh news into publish-ready news drafts for: `$ARGUMENTS`

This is the newsjacking counterpart to `/write-article`. Instead of an evergreen keyword, you find FRESH stories in the site's niche, write grounded news drafts in news voice, then submit them to Distribb. You draft. Distribb does the last-mile publishing on the content calendar.

Load the Distribb skill and follow the **SEO Article Writing System** in `SKILL.md` (but in NEWS voice), running against `$ARGUMENTS`:

1. **Resolve the project and brand voice.** `GET /api/v1/projects` to pick the `project_id`. If `$ARGUMENTS` is a URL, match it to a project; if it is a niche phrase, ask which project (or infer the obvious one); if empty, use the user's default project. Then `GET /api/v1/business-context?project_id=...` for brand voice, language, competitors (never link to them), and AI instructions. If there is no matching Distribb project, `WebFetch` the URL or homepage to profile the niche, audience, and voice instead.

2. **Derive 3-5 specific news queries** for the niche. Be specific: two-to-four-word phrases tied to the topic (good: `"google ai overviews ranking"`, `"shopify checkout update"`). Avoid bare words like `"seo"` or `"news"`, they pull off-topic noise. Match the angles this audience cares about right now.

3. **Find fresh topics.** Run the bundled helper at the skill root (same folder as `distribb_cli.py`):
   `python3 "<skill-dir>/news_topics.py" "<query1>" "<query2>" "<query3>" ...`
   Substitute the real absolute skill path. It pulls Google News RSS (no API key) and writes `news_topics_export.csv` next to itself. Add `--days 7` to tighten recency for fast-moving niches. If it errors, show the exact error and stop. Do not retry blindly.

4. **Shortlist the best 3.** Read `news_topics_export.csv` from the skill directory (columns: `Date`, `Title`, `Source`, `Query`, `URL`). Cluster near-duplicate headlines (same story, many outlets) into single topics, then pick the best 3 on: timely (last few days, drop anything stale or off-topic), relevant to THIS audience, and a clear on-brand angle that ties the story back to what the business does ("what this means for <audience>"). A story you cannot connect to the business is noise, skip it. Present headline, date, source, and one line on the angle.

5. **Ground each story, then write it.** Before writing, `WebFetch` 1-2 real source URLs (the `URL` column) per story to get the actual who/what/when, real numbers, and real quotes. Never write from a headline alone. Then write in news voice: lede-first (who/what/when/why-it-matters in the first 2-3 sentences), then what happened (attributed), why it matters, and the on-brand pivot tying the story to what the business does. Timely, factual, attributed. Not an evergreen "ultimate guide." Write quotable, self-contained claims AI engines lift as answers ("X did Y on <date>, according to <source>"). Match brand voice and language. Valid HTML. Never bold the keyword.

6. **Add links per project.** `GET /api/v1/internal-links?project_id=...&keyword=<news angle>` and place the recommended count in substantive paragraphs. If the project has `BecklinksNetworkParticipation: "Yes"`, `GET /api/v1/backlink-targets?project_id=...&keyword=<news angle>` and include 1-2 of those URLs as natural references (mandatory, this is how the user earns backlinks). Never link to competitors.

7. **Submit each draft to Distribb.** One `POST /api/v1/articles` per story with `project_id`, `keyword` (the news angle), `title`, `content` (valid HTML), `meta_description`, and `status`: `Draft` to review, or `Planned` + `scheduled_date` so Distribb autopublishes it on the calendar. For long HTML, write each to a file and pass it with `jq -n --arg content "$(cat article.html)"`. If a response has a `backlinks_warning`, add network links and `PUT` the revised content.

8. **Summarize and close.** Print a SUMMARY table: file or title, headline, angle, approximate word count, sources, where it landed (draft or scheduled). Then one line: the drafts are written and queued in Distribb, and Distribb autopublishes them on the calendar. Offer to publish any one now with `POST /api/v1/articles/:id/publish`.

Default 3 articles per run unless the user asks for more or fewer.

## Rules
- Ground every claim in fetched sources. Cite them. No invented stats, quotes, dates, names, or URLs. If a fact is unconfirmed, attribute it to the source and keep it general.
- News voice, not SEO filler. Lede-first, timely, factual. Not an evergreen guide.
- Match the project's brand voice and language from `business-context`.
- Never fabricate. Never link to competitors.
- Do not modify the CSV. Do not re-run the script on failure. Show the error and stop.
