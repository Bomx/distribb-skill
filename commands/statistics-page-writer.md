---
description: Deep-research and publish a sourced statistics page journalists cite for months
argument-hint: <industry-or-topic>
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Build and publish a research-backed statistics page on: `$ARGUMENTS`

This is not a normal article. A statistics page is a linkable asset: one URL journalists, bloggers, and other stat roundups cite for months, and one of the pages AI engines preferentially quote because the facts are structured and numbered. The work is the research. Every number must trace to a real primary source you actually fetched, because one fabricated stat caught by a reporter torpedoes the user's credibility for good.

Load the Distribb skill, then READ `references/statistics-page-playbook.md` for the full method (source tiers, the 6-point per-stat quality bar, the zero-outbound hoard-the-juice rule, stat-count targets, section patterns, and anti-patterns). Then run this Distribb-specific workflow:

1. Pick the project and pull voice. `GET /api/v1/projects` to choose `project_id`, then `GET /api/v1/business-context` for brand voice, competitors (never quote a competitor as your data source, never link to one), and language. If no topic was given in `$ARGUMENTS`, derive a strong one from the business (for example "<industry> statistics 2026").

2. Lock the angle and show it first. Set a boring-on-purpose title, "<TOPIC> Statistics You Need to Know in 2026", the exact phrase journalists type into Google. Do not try to be clever ("The Ultimate Guide" ranks worse). Set the slug and 6-12 themed sections (Market Size and Growth, Adoption and Usage, ROI and Performance, Investment and Spending, Regional Breakdown, Future Projections, and so on). Show the user the title plus the section list BEFORE you research, so they can redirect the angle.

3. Deep research, section by section. Run 2-4 web searches per section using the playbook query patterns ("{topic} statistics {year}", "{topic} market size {year}", "state of {topic} report {year}", analyst-firm site: searches). FETCH every promising source, never trust a search snippet. Keep a stat only if it passes ALL six criteria: named source, a year, a specific number, a real URL you fetched, a faithful quote (no rounding or extrapolation), and a working URL. Targets: 40-80 stats total, 5-12 per section, at least 8 unique source domains, at least 60% from the current or previous year. If two reputable sources disagree on the same figure, include BOTH with their attributions; reporters love the spread. Drop any section that cannot reach 3 verified stats.

4. Build the page as valid HTML. Short intro, an anchor-only table of contents, one section per theme with a headline-stat callout plus a numbered and sourced stat list, 1-3 tables for ranking or comparison data, optional 1-3 Chart.js charts only when a real data story justifies one (never force a chart on 2-3 numbers), and Article plus FAQPage JSON-LD schema, then an author and CTA footer. KEY RULE inherited from the playbook: the rendered HTML must contain ZERO outbound `<a>` tags to any other domain. Every source is PLAIN TEXT, like "(Source: HubSpot State of Marketing, 2026)". This is a deliberate exception to the normal /write-article backlink-exchange rule: a stats page is a link MAGNET, so it hoards authority instead of distributing it. Say this explicitly to the user so they do not think backlinks were forgotten. Internal links to the user's own pages are fine and encouraged: `GET /api/v1/internal-links?project_id=...&keyword=<topic>+statistics+2026` and weave a few in.

5. Leave an audit trail. At the very bottom of the HTML, add an HTML comment listing each stat with its source_name, source_url, and year. It is invisible to readers and not a crawlable link, and it lets a human spot-check every number.

6. Publish through Distribb. `POST /api/v1/articles` with `project_id`, `keyword` (the "<topic> statistics 2026" phrase), `title`, `content` (the HTML), `meta_description`, and `status` Draft to review or Planned plus `scheduled_date` so Distribb auto-publishes it to the connected CMS on the content calendar. For long HTML, write it to a file and pass it with `jq -n --arg content "$(cat stats-page.html)"`. The canonical version must live on the user's own domain first, never republish it to Medium or LinkedIn before the user's site. Distribb handles the last-mile publishing, then confirm where it landed and offer `POST /api/v1/articles/:id/publish` to push it live now.

7. Close on the distribution payoff. This page is the asset to point journalists, HARO, and Qwoted pitches at: pitch it once and it keeps earning backlinks as it ranks, turning one outreach email into many cumulative links. It also feeds AI-search visibility, since structured, entity-rich stat pages are the kind AI engines cite. Offer next steps: run `/ai-visibility` to find where the page should be cited, or pitch it to reporters covering the topic.

RULES:
- Never invent a stat. If you cannot find and fetch it, leave it out. One fabricated number ends the page's credibility.
- Trace every stat to a real primary source: analyst firms (Gartner, Forrester, McKinsey), "State of X" vendor reports with stated methodology, government or academic data, reputable surveys (Pew, Gallup). Avoid AI-generated stat roundups and listicle blogs that cite each other, always trace through to the original.
- Stats pages are scanned, not read. Aim 1500-3500 words, not a 10,000-word "ultimate guide".
- Do not force charts where there is no data story.
- Keep the canonical copy on the user's own domain. Zero outbound links in the rendered HTML; sources stay plain text plus the audit-trail comment.
