---
description: Turn one Distribb article or keyword into a viral, save-driven Instagram carousel, build the slides with our 2026 best practices (cover hook, one idea per slide, comment-keyword-to-DM), publish it, and close the SEO loop with a companion article
argument-hint: <article-id-or-keyword>
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Turn this into a ranking Instagram carousel: `$ARGUMENTS`

This is the **"Instagram Carousels for SEO"** workflow. Instagram carousels rank on
Google, get indexed by Google/Bing and cited by LLMs (public professional-account posts
have been indexable since mid-2025), and manufacture the one signal that actually predicts
AI-engine citations for a brand: **branded search**. You re-architect one Distribb article
(or one target keyword) into a swipe-optimized carousel, build the slides with our best
practices for virality, wire the **comment-a-keyword-to-DM** link playbook, publish it, and
close the loop with a companion Distribb article so the carousel feeds organic + AI
visibility, not just likes.

Load the Distribb skill, then **READ `references/instagram-carousel-playbook.md`** for the
full method (the strategy, the Carousel Maker JSON contract, the cover/hook system, the
design specs, the comment-for-link playbook, how to render the slides, and the publish
paths). Then run this workflow against `$ARGUMENTS`:

1. **Preflight.** Confirm `DISTRIBB_API_KEY` works (`GET /api/v1/projects`) and pick the
   `project_id`. Pull brand context: `GET /api/v1/business-context?project_id=<id>` for
   brand name, URL, one-liner, language, audience, and competitors. The carousel is written
   in the project's language and voice, and **never** mentions or links a competitor.
   Decide the ONE primary goal now: `saves` (authority / long-tail), `sends` (cold reach),
   `follows` (audience), or `comment-keyword leads` (the link play). This single choice
   drives the CTA slide and the caption.

2. **Source the topic.** `$ARGUMENTS` is either a Distribb article or a keyword.
   - **Article** (`GET /api/v1/articles/<id>` or pick a strong published one from
     `GET /api/v1/articles?project_id=<id>`): use it as the source. Prefer save-worthy
     article types (mistakes / signs, frameworks / checklists, how-tos, data/stat posts).
   - **Keyword**: `POST /api/v1/keywords/search` on the concept and
     `GET /api/v1/search-console?project_id=<id>` for striking-distance queries; pick ONE
     winnable, on-brand keyword. On a legacy Free Agentic account, if `keywords/search` returns HTTP 402
     `byo_keys_required`, surface the message verbatim and use GSC + the concept instead.
   The chosen keyword becomes the caption keyword and the companion article's keyword.

3. **Architect the carousel (the Carousel Maker).** Extract the 3 to 6 load-bearing ideas
   from the source (headings, stats, named steps, the one transformation) and re-architect
   them into the swipe arc. Produce the strict JSON in the playbook's schema:
   `slides[]` (default **8**, range 6 to 10: cover -> promise -> value... -> recap -> CTA),
   a `caption` (first line is a second hook with the keyword in it), `alt_text` (one per
   slide), `hashtags` (**0 to 5**, or none), and, if the goal is DM leads, a
   `keyword_dm_trigger` plus 2 to 3 misspelling `keyword_variants`. **Show the user the
   cover line and the arc before rendering anything.**

4. **Build the slides.** Render each slide to a **1080x1350 (4:5) JPEG**, identical
   dimensions on every slide (slide 1 locks the ratio). Designed text on a brand-color
   template carries the message; any AI image is a backdrop only. Enforce the design system:
   safe zones (sides 60 to 80px, top 120 to 150px, bottom >=150px clear so the IG buttons
   never cover a line), body text >=40px, hook is the largest text, contrast >=4.5:1 in both
   light and dark feed, a consistent template with a `3/8` page label and a visible
   `Swipe ->` cue on every slide except the CTA. See the playbook for the HTML-to-PNG render
   recipe.

5. **Wire the comment-for-link play (if goal = comment-keyword leads).** Set ONE distinctive
   ALL-CAPS keyword tied to the offer (GUIDE, AUDIT, CHECKLIST, TEMPLATE, never a generic
   word like HI or YES) and register 2 to 3 misspelling variants so mobile typos still fire.
   Configure the auto-DM (e.g. ManyChat) to reply with a short, warm, brand-voice message
   that acknowledges the comment and delivers the link plus one button. This keeps the
   action in-app (no reach penalty), spikes comments, and delivers the link where
   click-through is highest.

6. **Publish.** Post the carousel to the user's connected Instagram professional account.
   If first-party Graph API credentials exist, use the three-step carousel flow in the
   playbook (create each child container, poll `FINISHED`, create the `CAROUSEL` parent,
   `media_publish`). Otherwise deliver the ready-to-post pack (ordered slide images +
   caption + the per-slide alt text + the comment keyword) for the user to upload or
   schedule in their tool. **Set the per-slide alt text** = the actual slide text so Google,
   Bing, and LLMs can index the graphics.

7. **Close the SEO loop.** Publish (or refresh) a companion Distribb article on the same
   keyword so the carousel drives branded search back to indexable owned content:
   `GET /api/v1/internal-links` and, if the project is in the exchange,
   `GET /api/v1/backlink-targets`, weave both in, then `POST /api/v1/articles`. If the
   response includes a `backlinks_warning`, add network links and `PUT` the revised content.

8. **Summarize.** Print: the source (article/keyword) + primary goal, the cover line + arc,
   the slide image paths, the caption + keyword trigger (+ variants), where it posted (URL
   or ready-to-post pack), and where the companion article landed.

Default to one carousel per run unless the user asks for a batch. A single ~2,000-word
article usually yields 3 to 5 distinct carousels.

## Rules
- Repurpose, do not compress. Never paste article paragraphs onto a slide. One idea per slide.
- The cover teases, never teaches. Under 12 words, readable in under a second, one focal point, a swipe cue.
- Default 8 slides, range 6 to 10. Never pad to a number. Never go under 6.
- Put the target keyword in the caption body (captions are indexed; comments are not).
- Alt text = the slide's real text, one per slide. This is what makes the graphics rankable.
- Hashtags 0 to 5 max, or none. Hashtag dumps measurably cost reach in 2026.
- Match the primary goal to the CTA: SAVE (authority) or SEND (reach) or comment-keyword-to-DM (leads). One action, mirrored on the slide and in the caption.
- ~80 to 90% pure value. Mention the brand exactly once, late, soft ("we built [Brand] to do exactly this"), never a feature pitch.
- Write in the project's language and brand voice. Never mention or link a competitor.
- No em dashes. No emojis in slide headlines. No corporate buzzwords.
