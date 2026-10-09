# SEO playbook

How to run SEO for a Distribb user so it ranks on Google and gets the business recommended in AI answers (ChatGPT, Gemini, Perplexity, Google AI Overviews). Distribb's own agent is built around this process; this is the version for agents working from outside. The full skill (`SKILL.md`) has every endpoint; `audit-playbook.md` has the audit in depth.

## The process that works, in order

People who start with keyword research and publishing on day one get weak results and quit. Walk the user through this order:

1. **Onboarding complete and honest.** Website, language, tone, competitors, content pillars (the pages articles should send readers to), publishing rules. Everything downstream depends on it. `get_project` shows what is filled in; `update_project` fixes gaps.
2. **Connect the website and Google Search Console.** The CMS lets Distribb publish; Search Console makes every decision data-led. Use `integrations_catalog` and send the connect links (see `integrations-playbook.md`).
3. **Make sure there is a blog.** Articles need a home with an index page that links to them.
4. **Audit before writing.** Cannibalization, decaying pages, pages stuck on page 2, missing topic clusters, competitor gaps, on-page problems. `search_console_performance` and `list_optimizations` are the starting points.
5. **Plan topic clusters, then keywords.** A pillar page plus supporting articles that link to each other, around the services the business sells.
6. **Write and publish, feeding the backlink exchange.** Each article carries one or two links to partner businesses in the network, which earns the project links back.
7. **Optimize what already ranks.** Pages at positions 5 to 20 are the fastest wins.

## Choosing keywords

- **Buying intent first.** Comparisons ("x vs y", "alternatives to x"), "best x for y", pricing, "x near me", service and problem pages bring customers. Pure "what is" topics are a small minority of the plan, only when they support a cluster.
- **Named products and brands in a keyword mean a listicle or comparison format**, not a how-to.
- **Let the search results decide the format.** If the top results are lists, write a list; if they are tools, a guide will not rank.
- **Check before planning:** has the site already got a page for this (cannibalization), and does Search Console show it already ranking?
- Volume is a guide, not a goal. A 50-searches-a-month keyword that sells is better than 5,000 visitors who never buy.
- Tools: `keyword_research` for ideas with volume and difficulty, Search Console queries for what the site already almost ranks for.

## Writing articles that rank and get cited

- **Answer first.** The first paragraph answers the query in two or three sentences.
- **Information gain.** Add something the top results lack: first-hand experience, original numbers, a worked example, real photos or screenshots, a clear recommendation. AI assistants cite pages that state specific, checkable facts.
- **Be specific.** Prices, timelines, quantities, named tools, locations. Vague advice is what AI writing is known for.
- **Structure for scanning:** descriptive H2s that match sub-questions, short paragraphs, tables for comparisons, a short FAQ when people ask follow-ups.
- **Internal links:** link to the pillar page and two to four related articles with descriptive anchors. Each article links to at least one content pillar (a money page).
- **Exchange links:** the article brief (`get_article_brief`) lists the partner links the article is committed to carry and partner pages it can link to. Place them where they genuinely help the reader.
- **Images:** a relevant hero image and screenshots for listicles (`screenshot_page` captures a product's homepage; `upload_image` hosts your own). Never charts drawn as images.
- **Claims:** never invent statistics, quotes, reviews or prices. If a number cannot be sourced, leave it out. Never claim a competitor lacks a feature without evidence.

When you write an article yourself, save it with `create_article` or `update_article` with the full HTML. Content of 2,000 characters or more is published exactly as sent: Distribb adds no images or links to it, so include them.

## Listicles and AI visibility

- AI assistants recommend businesses that appear on the lists they read. `ai_visibility_report` shows where the brand is cited, for which buyer prompts and on which engines.
- Get onto third-party "best x" lists through link outreach (see `outreach-playbook.md`), and publish the business's own honest roundups. Ranking the business first in its own roundup is fine; be fair to the others listed.
- Consistent facts everywhere (name, what it does, prices, locations) help AI engines describe the business correctly.

## Optimizing existing pages

- **Striking distance:** queries at positions 5 to 20 with impressions. Improve the page that ranks: answer the query better, add missing sub-topics, tighten the title and meta description, add internal links to it.
- **Low CTR:** a page with impressions but few clicks at a good position needs a better title and description, not new content.
- **Decay:** pages losing clicks month over month need refreshed facts, dates and examples.
- **Cannibalization:** two pages competing for one query: merge them or make their intents clearly different.
- Distribb finds these from Search Console: `list_optimizations` lists suggestions, `get_optimization` shows the diagnosis and the before and after, `review_optimization` approves or rejects, `publish_optimization` pushes the approved rewrite to the live page.

## Technical basics worth checking

- Pages are indexable (no stray noindex, in the sitemap, linked from somewhere).
- Fast enough on mobile; images compressed.
- One clear H1, a unique title and meta description per page.
- IndexNow on (`manage_integration` with `set_indexnow`) so Bing and partner engines pick up new pages quickly.
- Bing Webmaster Tools connected when available: several AI search engines lean on Bing's index.

## Local SEO

For businesses that serve an area: Google Business Profile complete and active (categories, services, hours, photos), a weekly Google post, every review answered, a page per service and per main location, and the same name, address and phone everywhere. See the Google Business notes in `integrations-playbook.md`.

## Cadence and measurement

- Publishing: steady beats bursts. The article plan (`set_article_plan`) sets how many a month; quality and buying intent matter more than count.
- Monthly: Search Console clicks and impressions by page and query, AI visibility, new backlinks (`backlinks_status`, `list_backlinks`), leads or sales from organic traffic when analytics are connected.
- SEO compounds over months. Report trends against the previous period and name the next action, rather than celebrating or worrying about one week.
