# Distribb SEO Audit Playbook

A full SEO audit, run from Distribb's own data and a live crawl. This is step one of real SEO. Run it before writing any article for an existing site. It works on **every plan, including Free** (it needs the website, and ideally a connected Google Search Console).

**Command:** `/gsc-audit <domain>` (or just say "audit my site").

The audit ends with a prioritized action list wired straight into Distribb: new articles for gaps, optimization suggestions for page-2 pages, internal-link fixes, and on-page fixes.

---

## What this audit covers

| # | Analysis | What it finds | Why it matters |
|---|----------|---------------|----------------|
| 1 | CTR optimization | Pages that rank well but get fewer clicks than expected | Fast wins from better titles/meta |
| 2 | Content decay | Pages losing traffic vs the prior period | Refresh before they fall further |
| 3 | Quick wins (striking distance) | Queries at positions 11-20 and pages stuck on page 2+ | Small pushes to page 1 |
| 4 | Keyword cannibalization | Multiple pages competing for the same query | Consolidate or differentiate |
| 5 | Dead pages | Pages that dropped to zero traffic | Catch deindexing / accidental removal |
| 6 | Brand vs non-brand health | How dependent traffic is on the brand name | Measure real organic visibility |
| 7 | Topical authority clusters (topic cocoons) | Which pillars and supporting clusters to build | Authority comes from clusters, not one-offs |
| 8 | Competitor analysis | Gaps vs the competitors captured in onboarding | Take topics they rank for and you do not |
| 9 | On-page checks | Title/meta/heading/internal-link/indexability problems | Foundation issues that cap every page |

---

## Data sources (all Distribb-native)

You do not need any extra setup beyond what onboarding connects. Pull from:

- `GET /search-console?project_id=...&days=90&limit=100` -> totals, `top_queries` (with position, impressions, ctr, clicks), `top_pages`. This is the audit's spine. If it returns `connected: false`, surface `instructions_for_agent` and send the user to https://distribb.io/integrations . If they do not have Search Console at all yet, point them to https://support.google.com/webmasters/answer/10267942?hl=en first.
- `GET /suggestions?project_id=...` and `POST /suggestions/run` -> Distribb's suggestion engine scores pages with impressions but low CTR and pages stuck at the bottom of page 1 / page 2, straight from GSC. Treat these as pre-computed striking-distance findings (analysis 3) and refresh candidates (analysis 2). Derive cannibalization (analysis 4) yourself from the content, as described below.
- `GET /business-context?project_id=...` -> competitors, target audience, brand voice, custom instructions.
- `GET /articles?project_id=...&limit=200` -> the user's existing content, used for cannibalization-by-keyword and cluster mapping.
- `GET /internal-links?project_id=...&keyword=...` -> existing linkable pages, used for internal-link gap checks.
- A **live crawl** of the site (`WebFetch` the homepage, blog index, sitemap, and key pages) for on-page checks and topic mapping.
- Keyword research (`POST /keywords/search`) to size cluster gaps and competitor gaps.

**Optional deep mode:** if the user has a raw Google Search Console MCP connected in their environment, you can pull row-level `query x page`, `device`, and period-comparison data for the fuller versions of analyses 2, 4, 5, and a mobile/desktop gap check. This is optional. The Distribb-native path above already produces a strong, actionable audit without it.

**Handling large datasets:** GSC data can be huge. Run each analysis in its own sub-agent (one sub-agent per numbered analysis), have each return only its findings table, then assemble the report. This keeps context manageable and lets analyses run in parallel.

---

## Phase 0: Scope

1. Confirm the project and resolve `project_id` from `GET /projects`.
2. Read `GET /business-context` for competitors and brand terms. Derive brand terms from the business name and domain if not explicit (used to exclude brand queries from cannibalization and to compute brand vs non-brand).
3. Check GSC with `GET /search-console`. If not connected, run the on-GSC-less subset (analyses 7, 8, 9 plus whatever `/suggestions` already holds) and tell the user the audit is stronger once GSC is connected.
4. Ask the user (with sensible defaults): analysis period (default 90 days, the API max), which analyses to run (default all), and any high-value URL patterns where clicks matter most (e.g. `/pricing`, `/demo`, `/contact`).

---

## Analysis logic

### 1. CTR optimization
From `top_pages` (and `top_queries`), filter to position < 20 and impressions > 50. Compare actual CTR to a position benchmark (rough expected CTR: pos 1 ~28%, 2 ~15%, 3 ~10%, 4 ~7%, 5 ~5%, 6-7 ~4%, 8-10 ~2.5%, 11-20 ~1%). Flag where `actual_ctr < expected_ctr * 0.7`. Estimate `potential_clicks = impressions * (expected_ctr - actual_ctr)`. Sort by potential clicks. These are title/meta rewrites: action via `/optimize` (suggestions) or a manual `PUT /articles/:id`.

Output: `| Page | Position | Impressions | Actual CTR | Expected CTR | Gap | Potential clicks |`

### 2. Content decay
Distribb's suggestion engine surfaces refresh candidates (pages with impressions but low CTR, and pages stuck on page 2). Run `POST /suggestions/run` then `GET /suggestions`. Each entry's `trigger_snapshot` is a single point-in-time read (`query`, `impressions`, `ctr`, `position`), not a trend, so use the current CTR and position to prioritize which pages to refresh first. To confirm true decay (clicks falling or position rising over time) you need period-over-period data: use the optional raw GSC MCP, or the page-history view in Search Console. Once you know the trend, diagnose: position dropped -> refresh content; position stable but CTR dropped -> rewrite title/meta; both -> full refresh. Action: approve the suggestion (auto-rewrite) or queue a manual refresh.

Output: `| Page | Trigger (query) | Impressions | CTR | Position | Diagnosis | Action |`

(If a raw GSC MCP is connected, compute true period-over-period click change for a fuller decay list.)

### 3. Quick wins (striking distance)
From `top_queries`, filter to position 11-20 with impressions >= 50, plus any `top_pages` at position 8-12. These are one refresh + a few internal links away from page 1. Cross-reference `/suggestions` (Distribb flags many of these automatically). Sort by impressions.

Output: `| Query | Page | Position | Impressions | Clicks | Next move |`

### 4. Keyword cannibalization
Two complementary checks:
- **From content:** `GET /articles` and group by target keyword. Two or more published articles targeting the same or near-identical keyword is cannibalization. Recommend consolidating into one authoritative page (301 the weaker one) or re-pointing one to a distinct long-tail.
- **From GSC:** scan `top_pages` and `top_queries` for the same target term surfacing on more than one URL. A full query-by-page competition matrix needs row-level data, so use the optional raw GSC MCP if connected. Exclude brand queries.

Output (per cannibalized query): the competing pages with position + impressions, and a recommendation (consolidate vs differentiate). The page that already wins keeps the keyword; the others get redirected or repurposed.

### 5. Dead pages
From `/suggestions` and the page list, find pages that previously had traffic and now show zero. Inspect each (crawl the URL): if it 404s or is noindex, that explains it; if it is live and indexable, traffic likely shifted to a competing page (see cannibalization). Exclude pages with trivially low prior traffic. (Full dead-page detection needs period data: use a raw GSC MCP if available, otherwise report the candidates `/suggestions` surfaces.)

Output: `| Page | Prior signal | Index status | Likely cause | Action |`

### 6. Brand vs non-brand health
Classify each query in `top_queries` as brand (contains a brand term) or non-brand. Sum clicks/impressions for each. `non_brand_ratio = non_brand_clicks / total_clicks`. Assessment: >60% healthy, 40-60% moderate, <40% over-dependent on brand. A low ratio means the content engine is the priority.

Output: a brand vs non-brand table + the top 10 non-brand queries (these are the terms to double down on).

### 7. Topical authority clusters (topic cocoons)
This is what turns scattered posts into authority. Build the cluster map:
1. From `top_queries`, `GET /articles`, the sitemap, and content pillars (from onboarding / `business-context`), group existing content into topic clusters: one **pillar** (broad, high-intent) page plus **supporting** articles that all interlink to the pillar and each other.
2. Identify clusters that are **thin** (pillar with too few supporting articles) or **missing** (a clear topic the business should own but has no content for). Size each gap with `POST /keywords/search`.
3. For each cluster, define: the pillar page, 4-8 supporting article keywords, and the internal-linking plan (supporting -> pillar, pillar -> supporting).

This becomes the content plan. Each missing supporting article is a `POST /articles` job; each existing-but-orphaned page needs internal links added (`GET /internal-links` + `PUT /articles/:id`).

Output: a cluster table `| Cluster / pillar | Existing supporting pages | Missing supporting keywords (with volume) | Internal-link gaps |`

### 8. Competitor analysis
Use the competitors from `GET /business-context`. For each: `WebFetch` their blog/sitemap and run buyer-intent queries to see what they rank for. Find topics and keywords they cover that the user does not (content gaps), and clusters where they have a pillar and the user does not. Prioritize gaps with commercial intent. Never link to competitors in the user's content; you may reference them factually.

Output: `| Competitor | Topic/keyword they own | User has it? | Opportunity (volume, intent) | Priority |`

### 9. On-page checks
Crawl the homepage, blog index, and top pages and check the basics:
- Title tags: present, unique, ~50-60 chars, lead with the primary term.
- Meta descriptions: present, unique, ~150-160 chars, written to earn the click.
- Headings: exactly one H1, logical H2/H3 nesting.
- Internal linking: pages have inbound + outbound internal links; no orphan pages (cross-check `GET /internal-links`).
- Indexability: not blocked by robots.txt or noindex; canonical is sane; in the sitemap.
- Basics: images have alt text, the site is HTTPS, pages are reasonably fast.

Output: `| Page | Issue | Severity | Fix |`

---

## Report format

Assemble the findings into one report:

```markdown
# SEO Audit: [domain]
Generated: [date] | Period: [start] to [end] | Project: [name]

## Executive summary
- [N] CTR opportunities (est. +[X] clicks/mo)
- [N] decaying pages
- [N] striking-distance / page-2 keywords
- [N] cannibalized queries
- [N] dead-page candidates
- Non-brand health: [HEALTHY/MODERATE/NEEDS WORK]
- [N] topic clusters to build or strengthen
- [N] competitor content gaps
- [N] on-page issues
Bottom line: [the single most important thing to do first]

## 1-9. [each analysis with its table]

## Prioritized action plan
1. [highest-impact, lowest-effort first] -> [exact Distribb action]
...
```

**Tie every finding to an action.** A finding without a next step is noise. Map them:
- Striking distance / decay / CTR / cannibalization on an existing page -> `/optimize` (run `POST /suggestions/run`, review the diff, approve, publish).
- Missing cluster article or competitor gap -> `/write-article <keyword>` (`POST /articles` with internal links + backlinks).
- Orphan page -> add internal links (`GET /internal-links` + `PUT /articles/:id`).
- On-page issue on a CMS the user controls -> fix directly or queue it.

## CSV export
If the user asks, output each section as CSV with headers, e.g.:

```csv
page,position,impressions,actual_ctr,expected_ctr,gap,potential_clicks
/blog/crm-guide/,8,1800,1.5%,3.5%,2.0%,36
```

Markdown pastes cleanly into Google Docs; CSV opens in any spreadsheet.

---

## After the audit
Offer to execute the top items immediately: "Want me to start on the top 3? I can queue the cluster articles and run the page-2 optimizations now." The audit is only valuable if it turns into published, optimized pages.
