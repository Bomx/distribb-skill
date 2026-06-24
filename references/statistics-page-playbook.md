# Statistics Page Playbook

The deep methodology behind `/statistics-page-writer`. Read this when you (the agent) are about to build a research-backed statistics page for the user and publish it through Distribb.

The goal is a **linkable asset**: one URL the user can point dozens of journalists at over months, that AI engines quote, and that keeps earning backlinks long after it goes live. This is not a one-off article. It is the single best on-domain asset the user can own for both classic backlinks and AI-search visibility.

A statistics page is published through Distribb like any other article (`POST /api/v1/articles`), so it lands in the connected CMS and shows up on the content calendar. The one thing that makes it special: it deliberately breaks Distribb's usual backlink-exchange rule. See "Hoard the juice" below.

---

## Why a statistics page works

1. **It earns recurring backlinks, not one-time ones.** Reporters are paid to cite numbers, not opinions. A page that hands them pre-vetted, sourced stats is the easiest possible thing to cite, screenshot, or link to. Once it ranks for `"<topic> statistics 2026"`, journalists find it on their own and link to it without any outreach. One page can accumulate dozens of backlinks over its life.

2. **It is a prime AI-search asset.** ChatGPT, Perplexity, Gemini, and Google AI Overviews preferentially cite pages with structured, entity-driven, numbered facts. A statistics page is exactly that shape: discrete, self-contained, sourced claims an AI engine can lift verbatim into an answer and attribute to the user's domain. If the user runs `/ai-visibility`, this is one of the highest-leverage pages you can build to start showing up.

3. **It is the perfect outreach hook.** When the user pitches journalists, HARO, or Qwoted requests, a comprehensive stats roundup converts far better than a naked opinion pitch. The page does the credibility work before the conversation starts.

4. **It compounds with the rest of the SEO program.** Internal links from the user's blog feed it authority, the backlink exchange and AI-visibility outreach drive external links to it, and it ranks for a query journalists actively search.

---

## When to build one (and when not to)

Build a statistics page when **at least one** of these is true:

- The topic is broad enough that a roundup is genuinely useful (e.g. "marketing automation trends", "ecommerce conversion benchmarks") rather than a narrow anecdote ask.
- The user wants a flagship asset for journalist / HARO / Qwoted outreach.
- The user wants to win AI-search citations on a topic and `/ai-visibility` shows they are invisible there.
- There are several pieces of outreach planned on the same topic. Build the page once, point everything at it.
- The user already has one or two stats pages and you want to cluster more around a pillar.

Skip it (write a normal article instead) when:

- The topic is genuinely qualitative with little public data. Stats pages need stats. An opinion piece needs a different format.
- The deadline is under 24 hours. There is not enough time to research and verify properly.
- The angle calls for personal anecdotes or case studies, not numbers.

If you skip it, fall back to `/write-article <keyword>`.

---

## Step 0: Scope the project in Distribb

Before researching, pull the same context every Distribb workflow starts from.

1. `GET /api/v1/projects` to resolve `project_id` and the project's domain.
2. `GET /api/v1/business-context?project_id=...` for:
   - **Author identity** for the byline and author bio (business name, positioning, brand voice). This replaces any external profile lookup. Use the business name and the user's role for `AUTHOR_NAME` / `AUTHOR_TITLE`, the brand description for `AUTHOR_BIO`, and the project domain for `AUTHOR_URL`.
   - **Competitors** (never name them as the recommended option, never link to them, mention factually only if a stat genuinely requires it).
   - **Language** and any custom `ai_instructions` (e.g. "keep it short", regional spelling). Honor them.
3. `GET /api/v1/internal-links?project_id=...&keyword=<topic> statistics` for on-domain pages to cross-link from inside the page. Internal links are encouraged here. Only the outbound links are forbidden.

Tell the user the planned **title** and **section list** before you research, so they can redirect if the angle is off.

---

## Step 1: Identify the angle

Lock these in before any research:

1. **Topic** extracted from the user's request or the project's niche. e.g. "AI in marketing", "SaaS pricing trends", "remote work productivity".
2. **Slug**: `<topic-words>-statistics-2026`. Used as the CMS slug. Keep it literal.
3. **Title**: `<TOPIC> Statistics You Need to Know in 2026`. Boring on purpose. This is the exact phrase journalists and AI engines search for. Do not get clever. "The Ultimate Guide to..." ranks worse.
4. **Sections**: 6 to 12 themed buckets you will fill. Common patterns:
   - Key Statistics (the headline set, first)
   - Market Size and Growth
   - User / Buyer Behavior
   - Adoption and Usage
   - Technology / Platform Trends
   - ROI and Performance
   - Investment and Spending
   - Industry / Regional Benchmarks
   - Future Projections
   - FAQ (last, optional but recommended for AI Overviews)
   - Sources (deduped, plain text)

---

## Step 2: Research (the bar is high)

### Sources to PREFER, in priority order

1. **Primary research from analyst firms**: Gartner, Forrester, McKinsey, Deloitte, Accenture, IDC, IBM Institute, BCG.
2. **Vendor "State of X" reports with stated methodology**: HubSpot State of Marketing, Salesforce State of Sales/Service/Marketing, Semrush, Ahrefs, Buffer, Notion, Stripe, Slack, Zapier State of X.
3. **Industry trade publications with original reporting**: Search Engine Land, Marketing Brew, Inc., HBR, MIT Sloan Review, TechCrunch (when they cite a primary report).
4. **Government / inter-governmental data**: US BLS, US Census, Eurostat, WIPO, OECD, UN.
5. **Academic / peer-reviewed**: Google Scholar, arxiv.org for technical topics.
6. **Reputable market-sizing reports**: IMARC, Grand View Research, Mordor Intelligence, Statista (often paywalled, cite via vendor blogs that summarize).
7. **Reputable surveys**: Pew Research, Edelman Trust Barometer, Gallup, Morning Consult, YouGov.

### Sources to AVOID

- Listicle blogs that just cite each other. Always trace to the primary source. If you cannot find one, drop the stat.
- Press releases without underlying data.
- Affiliate or vendor-promotional content posing as research.
- AI-generated stats roundups. These are the source of most hallucinated numbers polluting the web. Do not propagate them.
- Stats older than 3 years, unless they are the only authoritative number (label the year clearly).
- Wikipedia as a primary source. Cite the source Wikipedia itself is citing.
- Competitors of the user (from `business-context`). Do not platform them as the source if a comparable independent number exists.

### Quality bar: every single stat must pass ALL six

| # | Criterion | Why |
|---|-----------|-----|
| 1 | Has a **named source** (an organization or publication, not "experts say") | Anonymous stats are worthless to a journalist. |
| 2 | Has a **year** (this year, last year, or clearly labelled) | Reporters and AI engines need recency context. |
| 3 | Is **specific** (a number, percentage, or ratio, not a vague modifier) | "Many companies" is not a stat. |
| 4 | Has a **real URL you actually fetched** | Proof the stat exists. This URL is for YOUR verification only. It is stored in the audit trail. It is NOT rendered as a clickable link. See "Hoard the juice". |
| 5 | Is **quoted faithfully** (no rounding, no extrapolation) | Misquoting one number kills the page's credibility. |
| 6 | The source URL **works at the time of writing** | So a spot-checker finds the original. Still not rendered as a link. |

### Research workflow

For each planned section:

```
1. Run 2 to 4 web searches using these query patterns:
   - "{topic} statistics {YEAR}"
   - "{topic} market size {YEAR}"
   - "{topic} survey results {YEAR}"
   - "state of {topic} report {YEAR}"
   - "{topic} ROI" OR "{topic} effectiveness"
   - "{topic}" research site:gartner.com OR site:forrester.com OR site:mckinsey.com
   - "{topic}" filetype:pdf {YEAR}

2. For each promising hit, FETCH the page. Do not trust search snippets.

3. Extract candidate stats. Record each one as:
   {
     "stat": "94% of marketers plan to use AI in content creation in 2026",
     "source_name": "HubSpot",
     "source_url": "https://www.hubspot.com/state-of-marketing/...",
     "year": 2026,
     "section": "Technology and Tools",
     "fetched_on": "2026-06-24"
   }

4. Discard any stat that fails any of the six quality criteria.

5. Stop when you have 5 to 12 verified stats for that section.
   If after 4 searches you still have under 3 stats, drop the section.
```

### Stat-count targets

- **Total**: 40 to 80 stats across the whole page.
- **Per section**: 5 to 12. Fewer feels thin, more than 12 reads like scannable spam.
- **Unique source domains**: at least 8.
- **Recency**: 60 percent or more of stats from the current or previous year.

### When stats conflict

If two reputable sources give different numbers for the same fact (e.g. global market size), include **both** with their attributions. Do not pick one. Reporters love seeing the spread, and showing the range signals you did real research.

### Never fabricate

If you cannot find and verify a stat, leave it out. One invented number caught by a journalist torpedoes the user's reputation permanently. This is the same hard rule that governs every Distribb article: ground everything in real, fetched sources, never invent stats, quotes, dates, names, or URLs.

---

## Hoard the juice: ZERO outbound links in the rendered page

This is the one place the statistics page deliberately departs from Distribb's normal rules.

Distribb's usual posture is the **backlink exchange**: most articles include 1 to 2 links to network partners, because giving links is how the user earns links back (see `references/plans-and-backlinks.md`). The statistics page is the deliberate exception. Its entire job is to ATTRACT inbound links, not to GIVE them. It is a link magnet, not a link giver. So you do NOT call `GET /backlink-targets` for this page, and you do NOT add network or any other off-domain links.

**Hard rule: the rendered HTML must contain ZERO `<a>` tags pointing to any domain other than the page's own domain.** No exceptions. No `nofollow` workaround (in 2026 `nofollow` is still only a hint and Google may crawl through it anyway).

### What this means in practice

| Pattern | Allowed? | Example |
|---|---|---|
| Source attribution as **plain text** | REQUIRED | `(Source: HubSpot State of Marketing, 2026)` |
| Source attribution as a clickable link | FORBIDDEN | `(Source: <a href="https://hubspot.com/...">HubSpot</a>, 2026)` |
| Internal TOC anchor link | Fine | `<a href="#market-size">Market Size</a>` |
| Internal link to the user's OWN content (from `/internal-links`) | Encouraged | `<a href="https://acme.com/blog/related-guide">descriptive anchor</a>` (same domain) |
| `<link rel="canonical">` in `<head>` | Fine | self-referential, no leak |
| Author-bio CTA to the user's business URL (SAME domain as the page) | Fine | `<a href="https://acme.com">Visit acme.com</a>` when the page lives at `acme.com/blog/...` |
| Link to an analyst firm methodology page | FORBIDDEN | strip it |
| Link to a quoted analyst's social profile | FORBIDDEN | strip it |
| Link to the publisher homepage or another off-domain article | FORBIDDEN | strip it |

Internal links to the user's own pages stay encouraged. The ban is on outbound links only. If the author-bio CTA points at a DIFFERENT domain than where the page is hosted, drop the `<a>` wrapper and render it as plain text instead.

### Rendering source attribution

Every stat is attributed inline as plain text, with a consistent "Source:" prefix and a year:

```html
<li><strong>42% of B2B marketers say AI is their number one priority</strong>.
    <span class="source">(Source: HubSpot State of Marketing, 2026)</span></li>
```

Never:

```html
<!-- WRONG: leaks juice -->
<li><strong>42% of B2B marketers...</strong>
    <span class="source">(Source: <a href="https://hubspot.com/...">HubSpot</a>, 2026)</span></li>
```

### Where the source URLs live

- In your research records (the audit trail) so you can prove no stat was hallucinated.
- In an HTML comment at the bottom of the page (see the skeleton), so a human reviewer can open view-source and spot-check. HTML comments are invisible to readers and not followed by crawlers.

### Why zero `<a>` tags rather than `nofollow`

1. Google has treated `nofollow` as a "hint" since 2020 and may still crawl through it.
2. Some PageRank leakage through `nofollow` is still debated.
3. Zero `<a>` tags is the only provably leak-free posture.
4. It is trivial to audit: a `grep 'href="http'` on the rendered HTML should return only the canonical link and same-domain internal links.

### The one trade-off

Well-placed outbound links to authoritative sources are a mild positive ranking signal. On a brand-new domain with zero authority, a zero-outbound stats page may rank slightly slower at first. Mitigations already baked in: rich on-page schema (Article + FAQPage), a named author, date stamps, plain-text named sources, strong internal links from the user's blog, and the inbound links the outreach earns over time. For a domain that already has authority, the no-outbound posture is a pure win. Accept the small cold-start cost on new domains.

---

## Step 3: Build the HTML page

Embed the page as the article `content` you will POST. Below is the skeleton to fill, distilled from the proven template. It is a single self-contained file: responsive layout, sticky TOC, headline-stat callouts, stat lists with plain-text sources, tables, Chart.js from CDN (degrades gracefully), Article + FAQPage JSON-LD, and an audit-trail comment. No separate template file is required.

Replace every `{{...}}` placeholder. Duplicate `<section class="stat-section">` blocks as needed. Delete the FAQ schema block if you have no FAQ data.

```html
<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{TITLE}}</title>
  <meta name="description" content="The most-cited {{TOPIC_LOWER}} statistics for {{YEAR}}, organized by topic and sourced from analyst firms, vendor research, and primary surveys." />
  <meta name="author" content="{{AUTHOR_NAME}}" />
  <link rel="canonical" href="{{CANONICAL_URL}}" />

  <meta property="og:title" content="{{TITLE}}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{{CANONICAL_URL}}" />
  <meta name="twitter:card" content="summary_large_image" />

  <!-- Article schema: gets you into rich results and AI Overviews. Keep it. -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{{TITLE}}",
    "author": { "@type": "Person", "name": "{{AUTHOR_NAME}}", "jobTitle": "{{AUTHOR_TITLE}}", "url": "{{AUTHOR_URL}}" },
    "datePublished": "{{ISO_DATE}}",
    "dateModified": "{{ISO_DATE}}",
    "publisher": { "@type": "Organization", "name": "{{PUBLISHER_NAME}}", "url": "{{AUTHOR_URL}}" },
    "mainEntityOfPage": "{{CANONICAL_URL}}"
  }
  </script>

  <!-- FAQPage schema: fill in 4 to 6 pairs, or delete this block if no FAQ. -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": "{{FAQ_Q_1}}", "acceptedAnswer": { "@type": "Answer", "text": "{{FAQ_A_1}}" } },
      { "@type": "Question", "name": "{{FAQ_Q_2}}", "acceptedAnswer": { "@type": "Answer", "text": "{{FAQ_A_2}}" } }
    ]
  }
  </script>

  <style>
    :root { --accent: {{ACCENT_COLOR}}; --ink: #15171a; --ink-soft: #4a5057; --ink-faded: #7a8089;
            --line: #e6e8ec; --bg: #fff; --bg-soft: #f6f7f9; --radius: 14px; --maxw: 1100px; --content: 760px; }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--ink); font-size: 17px; line-height: 1.65;
           font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }
    h1 { font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; margin: 0 0 .5rem; }
    h2 { font-size: 1.7rem; font-weight: 700; margin: 3rem 0 1rem; padding-bottom: .5rem; border-bottom: 2px solid var(--accent); }
    p { color: var(--ink-soft); }
    .hero { padding: 4rem 1.5rem 3rem; border-bottom: 1px solid var(--line); }
    .hero-inner, .layout { max-width: var(--maxw); margin: 0 auto; }
    .byline { color: var(--ink-soft); font-size: .95rem; }
    .layout { display: grid; gap: 2rem; padding: 2rem 1.5rem 4rem; grid-template-columns: minmax(0,1fr); }
    @media (min-width: 860px) { .layout { grid-template-columns: 200px minmax(0,var(--content)); } }
    .toc { background: var(--bg-soft); border-radius: var(--radius); padding: 1.25rem 1.5rem; font-size: .92rem; }
    @media (min-width: 860px) { .toc { position: sticky; top: 1.5rem; align-self: start; } }
    .toc ol { list-style: none; margin: 0; padding: 0; } .toc li { margin-bottom: .5rem; }
    .toc a { color: var(--ink-soft); text-decoration: none; } .toc a:hover { color: var(--accent); }
    .stat-section { scroll-margin-top: 1.5rem; }
    .headline-stat { background: var(--bg-soft); border-left: 4px solid var(--accent); padding: 1.25rem 1.5rem;
                     border-radius: 0 var(--radius) var(--radius) 0; margin: 1.5rem 0; font-size: 1.15rem; font-weight: 500; color: var(--ink); }
    .headline-stat .source { display: block; margin-top: .5rem; font-size: .85rem; font-weight: 400; color: var(--ink-soft); }
    .stats-list { list-style: none; counter-reset: stat; padding: 0; margin: 1.5rem 0; }
    .stats-list li { counter-increment: stat; padding: .85rem 0 .85rem 2.75rem; border-bottom: 1px solid var(--line); position: relative; color: var(--ink); }
    .stats-list li::before { content: counter(stat); position: absolute; left: 0; top: .95rem; width: 1.9rem; height: 1.9rem;
                             border-radius: 50%; background: var(--bg-soft); color: var(--ink-soft); font-size: .82rem; font-weight: 700;
                             display: flex; align-items: center; justify-content: center; }
    .stats-list .source { color: var(--ink-faded); font-size: .92rem; }
    .stat-table-wrap { overflow-x: auto; margin: 1.5rem 0; }
    table.stat-table { width: 100%; border-collapse: collapse; font-size: .95rem; }
    .stat-table th, .stat-table td { padding: .85rem 1rem; text-align: left; border-bottom: 1px solid var(--line); }
    .stat-table th { background: var(--bg-soft); font-weight: 700; font-size: .82rem; text-transform: uppercase; }
    .chart-card { border: 1px solid var(--line); border-radius: var(--radius); padding: 1.5rem; margin: 1.5rem 0; }
    .chart-card .chart-source { font-size: .82rem; color: var(--ink-faded); margin-bottom: 1rem; }
    .chart-canvas-wrap { position: relative; height: 320px; }
    .faq details { border-bottom: 1px solid var(--line); padding: 1rem 0; }
    .faq summary { cursor: pointer; font-weight: 600; }
    .sources-list { column-count: 2; column-gap: 2rem; font-size: .92rem; color: var(--ink-soft); }
    .author-card { margin-top: 4rem; padding: 2rem; background: var(--bg-soft); border-radius: var(--radius); }
    .author-card .name { font-size: 1.2rem; font-weight: 700; margin: 0 0 .25rem; }
    .author-card .website { display: inline-block; padding: .5rem 1rem; background: var(--accent); color: #fff;
                            text-decoration: none; border-radius: 999px; font-weight: 600; font-size: .9rem; }
  </style>
</head>
<body>

  <header class="hero">
    <div class="hero-inner">
      <h1>{{TITLE}}</h1>
      <p class="byline">By <strong>{{AUTHOR_NAME}}</strong> &middot; {{AUTHOR_TITLE}} &middot; Last updated: {{LAST_UPDATED}}</p>
    </div>
  </header>

  <div class="layout">

    <aside class="toc" aria-label="Table of contents">
      <strong>Contents</strong>
      <ol>
        <li><a href="#key-stats">Key {{TOPIC}} Statistics</a></li>
        <li><a href="#market-size">Market Size and Growth</a></li>
        <li><a href="#user-behavior">User Behavior</a></li>
        <li><a href="#technology">Technology and Tools</a></li>
        <li><a href="#roi">ROI and Performance</a></li>
        <li><a href="#future">Future Projections</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sources">Sources</a></li>
      </ol>
    </aside>

    <main class="article">

      <p>{{INTRO_PARAGRAPH}}</p>

      <!-- Key stats: the headline set, 6 to 10 of the strongest numbers. -->
      <section id="key-stats" class="stat-section">
        <h2>Key {{TOPIC}} Statistics</h2>
        <ol class="stats-list">
          <li><strong>{{KEY_STAT_1}}</strong>. <span class="source">(Source: {{SOURCE_NAME_1}}, {{YEAR_1}})</span></li>
          <li><strong>{{KEY_STAT_2}}</strong>. <span class="source">(Source: {{SOURCE_NAME_2}}, {{YEAR_2}})</span></li>
          <!-- ...6 to 10 total -->
        </ol>
      </section>

      <!-- Themed section with a headline-stat callout, a stat list, an optional chart, an optional table. -->
      <section id="market-size" class="stat-section">
        <h2>Market Size and Growth</h2>
        <div class="headline-stat">
          {{MARKET_SIZE_HEADLINE}}
          <span class="source">(Source: {{HEADLINE_SOURCE}}, {{HEADLINE_YEAR}})</span>
        </div>
        <ol class="stats-list">
          <li><strong>{{STAT}}</strong>. <span class="source">(Source: {{NAME}}, {{YEAR}})</span></li>
          <!-- 5 to 12 stats -->
        </ol>
        <div class="chart-card">
          <h4>{{CHART_1_TITLE}}</h4>
          <p class="chart-source">{{CHART_1_SOURCE}}</p>
          <div class="chart-canvas-wrap"><canvas id="chart-market-size"></canvas></div>
        </div>
        <div class="stat-table-wrap">
          <table class="stat-table">
            <thead><tr><th>{{COL_A}}</th><th>{{COL_B}}</th></tr></thead>
            <tbody>
              <tr><td>{{ROW_A_1}}</td><td>{{ROW_B_1}}</td></tr>
              <tr><td>{{ROW_A_2}}</td><td>{{ROW_B_2}}</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Duplicate the themed section for: user-behavior, technology, roi, future, etc. -->

      <section id="faq" class="stat-section faq">
        <h2>Frequently Asked Questions</h2>
        <details><summary>{{FAQ_Q_1}}</summary><p>{{FAQ_A_1}}</p></details>
        <details><summary>{{FAQ_Q_2}}</summary><p>{{FAQ_A_2}}</p></details>
        <!-- 4 to 6 total -->
      </section>

      <section id="sources" class="stat-section">
        <h2>Sources</h2>
        <p>Every stat above is drawn from one of the following organizations or publications.</p>
        <ol class="sources-list">
          <li>{{SOURCE_NAME}}</li>
          <!-- deduped, plain text, no links -->
        </ol>
      </section>

      <aside class="author-card">
        <p style="font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faded);margin:0 0 .5rem;">About the author</p>
        <p class="name">{{AUTHOR_NAME}}</p>
        <p style="color:var(--ink-soft);margin:0 0 .75rem;">{{AUTHOR_TITLE}}</p>
        <p style="color:var(--ink-soft);">{{AUTHOR_BIO}}</p>
        <!-- SAME-DOMAIN ONLY. If {{AUTHOR_URL}} is a different domain than the page, render as plain text instead. -->
        <a class="website" href="{{AUTHOR_URL}}">Visit {{AUTHOR_DOMAIN}}</a>
      </aside>

    </main>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
  <script defer>
    window.addEventListener('load', () => {
      if (typeof Chart === 'undefined') return; // CDN blocked: stats still readable in the list, nothing lost.
      const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#3a86ff';
      const c1 = document.getElementById('chart-market-size');
      if (c1) new Chart(c1, {
        type: 'bar',
        data: { labels: ['{{X1}}','{{X2}}','{{X3}}','{{X4}}'],
                datasets: [{ label: '{{CHART_1_LABEL}}', data: [{{Y1}},{{Y2}},{{Y3}},{{Y4}}], backgroundColor: accent, borderRadius: 6 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
                   scales: { y: { beginAtZero: true } } }
      });
    });
  </script>

  <!--
    audit_trail (not rendered, not crawled): one entry per stat, mirrors your research records.
    - stat: "{{STAT_TEXT}}"
      source_name: "{{SOURCE_NAME}}"
      source_url:  "{{SOURCE_URL}}"   # audit only, NEVER rendered as a link
      year: {{YEAR}}
      fetched_on: "{{YYYY-MM-DD}}"
    - ...
  -->
</body>
</html>
```

### Headline-stat callouts

Each themed section leads with one `.headline-stat` callout: the single most striking number in that section, with its plain-text source. This is the stat a journalist screenshots and an AI engine lifts first.

### Charts

Add 1 to 3 Chart.js charts, and only where there is a real quantitative story:

- **Bar / line** for a metric over time (e.g. market size by year).
- **Doughnut / pie** for a share-of-X breakdown (e.g. click share by SERP position).
- **Stacked bar** for composition over time.

Do not force a chart for a single number (use a callout), for two data points (use a sentence), or across radically different scales (charts mislead there). The chart degrades gracefully: if the CDN is blocked, the underlying numbers are still readable in the stat list.

### Tables

Use HTML tables for ranking or comparison data with 4 or more rows and 2 or more columns: CTR by SERP position, market size by year (actual plus projected), adoption rate by region, and similar.

### Schema markup

Keep both JSON-LD blocks. The Article schema and the FAQPage schema are a large part of what wins AI Overview and ChatGPT citations. Fill the FAQPage block if you have FAQ data, otherwise delete that one block.

---

## Step 4: Self-check before publishing

Scan the assembled HTML for:

- **Zero outbound links.** Conceptually run `grep 'href="http'`: the only hits allowed are the canonical link and same-domain internal links. Any off-domain `<a>` is a bug. Strip it.
- **Every stat has a plain-text source and a year.** No naked numbers.
- **No implausible numbers** (extra zero, wrong percent, impossible ratio).
- **Author bio and URL correct**, and the author CTA is same-domain or plain text.
- **Schema present and valid** (Article always, FAQPage if there is FAQ data).
- **Internal links** from `/internal-links` use exact URLs and descriptive anchor text, placed inside body paragraphs.
- **Audit-trail comment** filled, one entry per stat, matching your research.
- **Honor `ai_instructions`** from business-context (length, spelling, tone).

---

## Step 5: Publish through Distribb

The canonical version must live on the user's own domain first. That is the entire point: the backlinks and citations must point at the user's site. Never republish on Medium, LinkedIn, or anywhere else before the user's own domain.

Distribb handles the last-mile publishing to the connected CMS. You create the article via the API; Distribb pushes it to WordPress / Webflow / Shopify and lands it on the content calendar. Do not ask the user to paste HTML into their CMS by hand.

Submit it as an article:

```bash
# Write the full HTML page to a file, then submit it.
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg content "$(cat statistics-page.html)" \
    '{ project_id: 42,
       keyword: "ai in marketing statistics",
       title: "AI in Marketing Statistics You Need to Know in 2026",
       content: $content,
       meta_description: "The most-cited AI in marketing statistics for 2026, sourced and organized.",
       slug: "ai-in-marketing-statistics-2026",
       status: "Draft" }')" \
  https://distribb.io/api/v1/articles | jq .
```

Choose the status:

- `status: "Draft"` to let the user review it in Distribb before it goes live. Recommended for a flagship asset like this.
- `status: "Planned"` with a `scheduled_date` so Distribb auto-publishes it to the connected CMS on the content calendar.

Once the user approves a draft, publish it with:

```bash
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  https://distribb.io/api/v1/articles/<id>/publish | jq .
```

This is a link MAGNET, so you intentionally did NOT call `/backlink-targets` and the page has no network links. If the create response includes a `backlinks_warning`, that is expected for this asset. Do NOT add outbound links to silence it. Tell the user it is deliberate for the statistics page only, and that their normal `/write-article` runs still include the 1 to 2 exchange links.

---

## Step 6: Put the page to work

Once it is live, this URL is the user's best outreach and AI-visibility asset:

- **Journalist / HARO / Qwoted outreach.** Lead pitches with the live URL and 2 to 3 standout stats with their sources. The page is the credibility hook.
- **AI-search visibility.** Pair with `/ai-visibility`: for any buyer prompt where the business should appear but does not, the statistics page is a strong candidate citation source to build toward.
- **Internal linking.** Link to the page from related blog posts (`GET /internal-links` plus `PUT /articles/:id`) so it accrues on-domain authority.
- **Refresh annually.** Update the stats and the `dateModified` each year so it keeps ranking for the current-year query.

---

## Anti-patterns to avoid

- **Inventing stats.** If you cannot verify it, leave it out. One fabricated number caught by a journalist is permanent reputational damage.
- **Citing AI-generated stat roundups as primary.** Trace every number to a real research source.
- **Adding outbound links.** This is the one asset where outbound links are forbidden, including the usual backlink-exchange links. A `backlinks_warning` here is expected, not a problem.
- **Writing a 10,000-word "ultimate guide".** Stats pages are scanned, not read. Aim for 1,500 to 3,500 words of dense, sourced facts.
- **Hiding sources.** Number every stat, attribute it inline as plain text, and list every unique source in the Sources section.
- **Forcing charts where there is no data story.** A bar chart with three random numbers reads as padding.
- **Building a stats page on a topic with little public data.** Stats pages need stats. If the topic is qualitative, use `/write-article` instead.
- **Republishing off-domain first.** The canonical version lives on the user's domain, full stop. That is what makes the backlinks worth anything.
- **Bolding the keyword or stuffing the year into every heading.** Same Distribb writing rules apply: natural keyword use, no keyword bolding, no stale-year stuffing.

---

## Related references

- `references/audit-playbook.md` for the full SEO audit (run it first to confirm the topic is worth a flagship asset).
- `references/plans-and-backlinks.md` for the normal backlink exchange this page deliberately opts out of, and the Accelerator's done-for-you AI-search distribution.
- The `/write-article` command and the SEO Article Writing System in `SKILL.md` for the writing and humanizing rules that still apply to the prose on this page.
