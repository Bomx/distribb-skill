# Instagram Carousels for SEO Playbook

How `/instagram-carousel` turns one Distribb article (or one keyword) into a viral,
save-driven Instagram carousel that ranks, gets indexed and cited, and feeds branded
search. This is the deep reference. The command file (`commands/instagram-carousel.md`) is
the thin entry point. Every rule here is numeric and portable so any agentic framework can
run it. This is the same playbook Distribb's own done-for-you carousel engine runs, distilled
for you to run by hand with your own AI.

> **PINNED DEFAULTS (one source of truth):** default carousel = **8 slides**, range **6 to 10**
> (cover + 4 to 8 value + 1 CTA). Never pad to a number, never go under 6. Canvas
> **1080 x 1350 (4:5)**. **Max 10 slides via the Graph API.** Hashtags **0 to 5** (or none).
> One soft brand mention, on the CTA slide only. Alt text on every slide.

---

## 1. Why carousels are an SEO tactic (not "just social")

Treat a carousel as the visual distribution layer of the blog's authority engine, not a
social channel. Three reasons it is an SEO move:

- **They are indexed and cited.** Since mid-2025, public posts from professional Instagram
  accounts are indexable by Google and Bing and are eligible to be cited by LLMs. On-slide
  text (via alt text) and the caption are the indexable surfaces. A carousel is a page that
  ranks, so it belongs in the SEO plan.
- **They manufacture branded search, the strongest AI-citation predictor.** Brand search
  volume correlates with LLM citations far more than backlinks do. ChatGPT mentions brands
  more often than it links them, and brands present on 4+ platforms are meaningfully more
  likely to appear in AI answers. Carousels create saves, recall, and branded search, plus
  a recent, stat-rich, cross-platform brand footprint, all direct AI-visibility inputs.
- **They win on saves.** Carousels carry the highest engagement and roughly 9x the saves of
  a single image (Metricool 2026, a 24.3M-post study). A save is a private "I want this
  later" signal, hard to fake, and the dominant ranking input for educational content. The
  mechanism is the multi-slide re-serve: a non-swiped carousel is re-served on slide 2 or 3,
  so one post earns 2 to 3 impressions per user.

The real KPI is **branded search and organic authority, not likes**. Optimize for saves,
sends, and branded search. Do not report on follower count.

---

## 2. The workflow at a glance

1. Preflight: API key, project, brand context (language, voice, competitors), primary goal.
2. Source the topic: repurpose one Distribb article, or pick one winnable keyword.
3. Architect: run the Carousel Maker to produce the strict JSON (slides + caption + alt + keyword trigger).
4. Build: render each idea to a 1080x1350 designed slide.
5. Wire the comment-for-link play (if the goal is DM leads).
6. Publish to the connected Instagram, with alt text on every slide.
7. Close the loop: publish/refresh a companion Distribb article on the same keyword.

---

## 3. Source the topic (repurpose, do not compress)

You are re-architecting an article's load-bearing ideas into a swipe arc and discarding
everything that does not earn a swipe. You are not summarizing it.

1. **Extract the 3 to 6 load-bearing ideas**: the section headings, stats, numbers, named
   steps, and the single transformation the article promises. Drop intros and SEO padding.
2. **Pick a mode**: *whole-post summary* (H1 -> hook cover, each H2 -> one value slide) or
   *single-section deep-dive* (expand one H2/H3 into step slides).
3. **One idea maps to exactly one value slide.** Condense each to ~30 to 50 words.
4. **Reuse the article's own images, screenshots, and charts** as slide visuals.

**Which article types convert best** (ranked by save-worthiness):
1. "X mistakes / X signs you are doing Y wrong" (highest save lift)
2. Frameworks, step-by-steps, checklists, audits
3. How-tos
4. Listicles ("5 ways / 10 tips")
5. Data and stat posts, myth-vs-fact (shareable AND AI-citation bait)

Pure product-feature posts convert worst. A single ~2,000-word article yields **3 to 5
distinct carousels**.

---

## 4. The Carousel Maker (the JSON contract)

Run your own AI as CAROUSEL MAKER: a fused short-form strategist, viral copywriter, and art
director. Give it the brand context + the article/keyword and have it return **STRICT JSON
only** in the schema below. Force JSON mode or re-prompt on any schema failure. Run at
temperature ~0.6 to 0.8 so hooks stay fresh while the JSON stays disciplined.

```json
{
  "carousel_title": "string, internal label, not shown on slides",
  "slide_count": 8,
  "slides": [
    {
      "index": 1,
      "role": "cover | value | cta",
      "headline": "string, on-screen headline, respects the word limits",
      "subtext": "string, supporting on-screen lines, or empty for a text-free cover",
      "design_note": "string, layout/focal/contrast/swipe-cue direction for the renderer",
      "page_label": "string, e.g. 1/8 (cover may use empty string)"
    }
  ],
  "caption": {
    "first_line_hook": "string, <=125 chars, extends the cover, contains the keyword if natural",
    "body": "string, short value lines separated by \n, exactly one soft brand mention",
    "cta": "string, one action matching the primary goal, mirrors the CTA slide",
    "keyword_dm_trigger": "string, the ALL-CAPS comment keyword, or empty if not a DM-lead goal",
    "keyword_variants": ["2 to 3 ALL-CAPS misspellings of the trigger, or empty array"]
  },
  "hashtags": ["0 to 5 strings, no # needed, tightly relevant or empty"],
  "alt_text": ["one keyword-rich alt string per slide, same length as slides"],
  "suggested_post_time_note": "string, audience-data-first note"
}
```

**Word and copy limits** the Maker must respect:
- Cover headline: 6 to 10 words ideal, **12 hard max**, one idea, one sentence.
- Value mini-headline: 3 to 7 words.
- Subtext per slide: **~30 words max**, 1 to 3 short lines, one thought per line.
- Recap: a tight checklist / one-liner, screenshot-worthy, under 40 words.

**Validate before you render (hard-reject and re-prompt on any fail):**
1. Valid JSON, matches the schema, no markdown fences, no trailing commas.
2. `slide_count == slides.length`, between 6 and 10, arc is cover -> value... -> cta.
3. `alt_text.length == slides.length`.
4. **Zero em dashes** anywhere. Zero banned buzzwords (leverage, delve, unlock, elevate,
   seamless, synergy, robust, transformative, "in today's fast-paced world", "the power of").
5. Cover headline <=12 words, uses a hook formula, has a swipe cue in its `design_note`.
6. One idea per value slide; each value slide ends on a forward micro-hook.
7. Brand mentioned exactly once in the slides and once in the caption, soft framing.
8. Caption first line <=125 chars, extends (does not repeat) the cover, contains the keyword if natural.
9. CTA slide and caption CTA are the same single action, aligned to the primary goal.
10. `hashtags.length` is 0 to 5. If `keyword_dm_trigger` is set, `keyword_variants` has 2 to 3 entries.
11. Output language matches the project's language.

---

## 5. The cover / hook system (this carries ~80% of the outcome)

The cover is a standalone ad for the swipe, not slide 1 of your content. In-feed it is the
only thing shown, and swipe-through and completion are the #1 and #2 carousel ranking
signals, so the cover is literally the reach lever. Its one job is to win the swipe-or-scroll
decision in under ~50ms. **Tease, never teach**: the payoff lives behind the swipe. If the
cover explains, there is no open loop left to pull the reader into slide 2.

**Six hook formulas (pick one, fill the blanks):**
1. **Curiosity / question**: "Is your X costing you Y? The signs most people miss"
2. **Shock-stat**: "87% of X fail in year one. Here is what the 13% do differently"
3. **Promise**: "How to [result] without [the painful thing]"
4. **List / number**: "5 [things] that [outcome] (swipe for all of them)"
5. **Mistake / myth**: "You have been doing [X] wrong this whole time"
6. **Contrarian / relatable-enemy**: "Stop doing [common thing] if you want [result]"

Numbers and specificity ("13%", "100k in 6 months") signal a concrete payoff. Mistake and
contrarian hooks trigger loss-aversion the brain resolves by swiping.

**Cover specs (hard rules):**
- Headline 6 to 10 words (12 max). One idea, one sentence. Readable in under ~0.7s (squint test).
- Hook is the largest text on the slide. Hooks run 60 to 100pt on a 1080-wide canvas.
- Exactly one dominant high-contrast focal point. A face is an optional pattern-interrupt, not required. Two competing ideas is a fail.
- Contrast >=4.5:1. Keep faces, logos, and key text inside the center 70%.
- Add an explicit `Swipe ->` cue. Only ~5% of carousels have one and it lifts swipe-through.
- Make the visual feel incomplete (a cropped diagram, a split-screen, a number that promises more). An unfinished visual is an open loop.

Targets (industry heuristics, medium confidence): swipe-through 65%+, completion 55%+.
Reaching slide 3+ above your account average triggers re-serve to non-followers.

---

## 6. Slide arc and welding rules

A carousel is a single curiosity engine engineered to be swiped to the end, not a slide deck
of facts.

| Slide | Role | Job |
|-------|------|-----|
| 1 | **Cover / Hook** | Stop the scroll, open one curiosity gap. Tease, do not teach. |
| 2 | **Promise / Credibility** | Reduce skepticism, preview the payoff. Must stand alone (IG often serves slide 2 first). Punch with value immediately. |
| 3 to N-2 | **Value** | Exactly one idea per slide. Put your strongest insight by slide 3. |
| N-1 | **Recap / screenshot moment** | A condensed checklist that looks good standalone, because it will be screenshotted and shared. |
| N | **CTA** | One clear action (save / send / comment keyword). |

**Welding rules (this is the craft):**
- **One idea per slide.** Flashcard, not paragraph. Each value slide stands alone if screenshotted.
- **Open loops + bottom-of-slide micro-hooks.** Never close every loop within a slide. Plant a transition at the bottom of body slides: "But that is not the biggest mistake...", "The next tip is the one most people skip...", "Swipe to see the fix."
- **Slide 1 -> 2 is the make-or-break friction point.** If the cover does not force an immediate swipe, the algorithm reads disinterest no matter how good slides 3-N are.
- **Anti-padding rule.** Never pad to hit a count. Filler slides tank completion, which is a negative signal. If content drags, drop to 6 or 7 slides to protect swipe velocity.

---

## 7. Visual design system (exact specs)

**Canvas:**
- Default **1080 x 1350 px (4:5)** for maximum feed real estate. Taller option 1080 x 1440 (3:4).
- Always design at exactly **1080px wide** (never lower, avoids upscaling blur).
- **Slide 1's aspect ratio locks all slides.** You cannot mix ratios. Pre-normalize every slide to identical dimensions.

**Safe zones (hard rule):**
- Sides: 60 to 80px clear. Top: 120 to 150px clear (username bar + menu). Bottom: keep **~150px** absolutely clear or your CTA / bottom micro-hook gets covered by the save ribbon and action buttons.
- Resulting safe content box: ~1000 x 1200px.
- Profile-grid crop is separate: keep faces/text/logos in the center 3:4 window so the cover survives both feed and grid.

**Typography:**
- Body minimum ~40px (the practical no-zoom phone floor). Hook is always the largest text.
- 2 to 3 fonts max: one bold display for the hook + one clean sans (Inter, Open Sans, SF Pro). Keep sizes identical slide-to-slide.
- Per slide: under ~40 words, ~6 to 8 words per line, one idea.

**Contrast (WCAG AA, both modes):** 4.5:1 normal text, 3:1 large text and page dots. It must
pass in both light AND dark feed. If a background could blend, add a defined card or solid fill.

**Template rules:**
- Same headline position, margins, color tokens, logo/handle lockup, and slide-number placement on every frame. Consistent formatting is cited at ~3x the engagement of mixed.
- 1 to 2 brand colors + neutrals. Whitespace is a feature.
- A `3/8` page label and a visible `Swipe ->` cue on slides 1 through N-1.
- **Designed text-on-brand slides carry the message. AI imagery is a backdrop only** (it cannot guarantee 4.5:1 contrast or safe-zone discipline). Set all critical text as real designed type on top.

---

## 8. Building the slides (render recipe)

Designed text on a brand template is the default because for save-driven info carousels you
control contrast, legibility, type scale, and the safe zone, none of which AI imagery
guarantees. Two portable ways to render, pick what your environment supports:

**A. HTML/CSS to PNG (recommended, highest fidelity).** Write one HTML template with the
brand tokens (accent hex, two fonts, handle lockup, page-label + swipe-cue slots), fill it
per slide from the Carousel Maker JSON, and screenshot each at exactly 1080x1350 with a
headless browser. This gives you exact web typography, flexbox layout, and easy contrast/
safe-zone control.

```bash
# one 1080x1350 PNG per slide with Playwright/Chromium (pseudo-recipe)
#  - render slide_1.html ... slide_N.html from the JSON + a shared brand.css
#  - page.set_viewport_size({"width":1080,"height":1350})
#  - page.screenshot(path="slide_1.png", clip={x:0,y:0,width:1080,height:1350})
#  - then convert to JPEG (<5MB) so it is Graph/scheduler-safe
```

**B. Image library (Pillow / sharp / canvas).** Draw text-on-color frames directly: shared
1080x1350 canvas, accent background, wrapped hook + body inside the safe box, a page label
and swipe cue in a fixed corner. This is exactly how Distribb's own engine renders (a Pillow
text-on-brand stack), and it is cheap and reliable.

**AI-image backdrop (optional enhancement).** If you want a photographic backdrop, generate
it (any image model), place it as a full-bleed background, then lay a dark scrim + your
designed type on top so contrast still passes. Never let an AI image be the text carrier.

**Always:** output JPEG, normalize EVERY slide to identical 1080x1350 (so the first-slide
ratio lock never crops a later slide), and aim under ~5MB per image.

---

## 9. Caption, SEO, and the comment-for-link playbook

The CTA is a layered system, not one "FOLLOW FOR MORE" slide.

**Caption structure (this is the indexable surface):**
- **Line 1 is the SECOND hook.** Only ~125 characters show before "more". Make it a 5 to 10 word hook. Do NOT repeat the cover verbatim, extend it.
- **Put the buyer-search keyword in the first 1 to 2 sentences.** Captions are indexed for IG search and Google; comments are not. This is where your SEO term must live.
- Body: 2 to 3 line paragraphs, ~150 to 300 words. A blank line immediately before the CTA to isolate it.
- **Alt text on every slide = the actual slide text.** This is what makes the graphics indexable by Google, Bing, and LLMs. Do not skip it.
- Hashtags: 0 to 5 relevant tags, or none. Hashtag dumps measure lower reach (~-32% views). Replace hashtags with keyword SEO in the caption, on-slide text, and alt text.

**Match the CTA to the goal (pick ONE, mirror it on the slide and in the caption):**
- Reach -> **SEND**: "Send this to the [persona] who owns your content calendar."
- Authority / long-tail -> **SAVE**: "Save this for the next time your post ranks on page 2."
- Leads -> **comment keyword** (below). Do not conflate saves and sends.

**The comment-a-keyword-for-the-link play (the highest-converting click path):**
Link-in-bio is not the primary path. A comment-keyword-to-DM trigger (a) keeps the action
in-app so it is not reach-penalized, (b) spikes comment count (a confirmed signal), and (c)
delivers the link by DM, where click-through is far higher.

- **Engineer the keyword:** ONE distinctive ALL-CAPS word tied to the offer (GUIDE, AUDIT,
  CHECKLIST, TEMPLATE). Avoid generic short words (HI, YES) that mis-trigger.
- **Register 2 to 3 misspelling variants** (AUDT, CHECLIST) so mobile typos still fire.
- **Auto-DM** (ManyChat or similar): short, warm, brand-voice. Acknowledge their comment,
  deliver the link + one button. Rotate a few unique public replies and space them ~3s to
  avoid spam flags.
- **CTA slide copy example:** "Comment AUDIT and I will DM you the checklist."
- **Caption CTA must mirror it exactly.** One action, no split asks.

**Follow ask:** a bare "FOLLOW FOR MORE" converts poorly. Reframe as a cadence payoff tied
to a series: "I post one of these every Tuesday. Follow if you want next week's."

**SaaS brand rule:** ~80 to 90% of slides are pure value with zero ask. Mention the brand
exactly ONCE, late (last 1 to 2 slides), framed as "we built [Brand] to automate exactly
this", never a feature pitch. Hard-sell suppresses the saves and sends you need.

---

## 10. Publishing

Post the finished carousel to the user's connected Instagram **professional** account
(personal accounts cannot use the API or alt text at scale). Order matters: slide 1 first.

**Path A: Instagram Graph API (programmatic, needs a first-party IG token + IG user id).**
Three steps:

```
1. Each image: POST /<IG_USER_ID>/media  image_url=<public https>, is_carousel_item=true
   (do NOT pass media_type on children) -> child container id; poll status_code=FINISHED
2. POST /<IG_USER_ID>/media  media_type=CAROUSEL, children=<comma-joined ids>, caption=...
   -> parent container id; poll FINISHED
3. POST /<IG_USER_ID>/media_publish  creation_id=<parent> -> ig_media_id
```

Hard platform limits: **min 2 / max 10 items via the API** (the app allows 20, the API does
not), JPEG, aspect 4:5 to 1.91:1, first image locks the ratio, ~8MB max (aim <5MB),
`image_url` must be a PUBLIC unauthenticated HTTPS URL that stays live through processing (no
localhost, no short-TTL signed URLs), containers expire ~24h, and there is a 50-published-
containers / rolling-24h quota (a carousel counts as 1). Use the IG professional account id,
not the Facebook Page id.

**Path B: a scheduler (Buffer, Later, getlate/Zernio).** These publish IG image carousels
natively from an ordered list of 2 to 10 image URLs plus a caption. This is the simplest path
when the user already uses one. (Distribb's own engine publishes carousels through getlate.)

**Path C: ready-to-post hand-off.** If no programmatic access exists, deliver the pack:
ordered slide images + the caption + the per-slide alt text + the comment keyword, and have
the user upload it (setting alt text per slide in the composer). Never let alt text get dropped.

> Note: publishing an article through Distribb auto-generates single social posts for every
> connected platform, but a deliberately-crafted carousel is a separate, higher-value asset.
> This workflow builds that asset; Distribb closes the SEO loop in the next step.

---

## 11. Close the SEO loop

A carousel that just gets likes is a dead end. Convert its attention into indexable owned
authority:

1. **Publish or refresh a companion Distribb article on the same keyword.** Get
   `GET /api/v1/internal-links` and (if in the exchange) `GET /api/v1/backlink-targets`,
   weave both in, then `POST /api/v1/articles`. If the response has a `backlinks_warning`,
   add network links and `PUT` the revised content. Now branded search from the carousel
   lands on a page you own and rank.
2. **Set alt text on every slide** (step 9) so the carousel itself is a rankable, citable page.
3. **Report on saves, sends, and branded search**, not follower count. Reaching slide 3+
   above your account average is the signal that the re-serve queue opened to non-followers.

---

## 12. The one-page checklist

**STRUCTURE**
- [ ] Default 8 slides, range 6 to 10. Never pad, never under 6.
- [ ] Arc: Cover -> Promise -> Value (one idea each) -> Recap -> CTA. Strongest insight by slide 3.
- [ ] Slide 2 stands alone (IG may serve it first). Every body slide ends on an open-loop micro-hook.

**COVER**
- [ ] One of the 6 hook formulas. Tease, do not teach. 6 to 10 words (12 max), readable in <0.7s.
- [ ] Hook is the largest text. One focal point. `Swipe ->` cue present. Visual feels incomplete.

**DESIGN**
- [ ] Canvas 1080x1350 (4:5), same ratio every slide (slide 1 locks it), designed at exactly 1080px wide.
- [ ] Safe zones: sides 60 to 80px, top 120 to 150px, bottom >=150px clear. Key text/faces in the center 3:4 window.
- [ ] Body >=40px, hook 60 to 100pt, <=40 words/slide, <=3 colors, 2 to 3 fonts, identical sizes slide-to-slide.
- [ ] Contrast >=4.5:1, passes in light AND dark. Consistent template with `3/8` label. Critical text is designed type, AI imagery backdrop only.

**CAPTION + CTA**
- [ ] Caption line 1 = second hook (<=125 chars), extends the cover. Buyer keyword in the first 1 to 2 sentences.
- [ ] Blank line before the CTA. ONE primary action, mirrored on the final slide AND caption.
- [ ] Comment-keyword-to-DM as the click path: ONE ALL-CAPS keyword + 2 to 3 misspelling variants + a warm auto-DM. Not link-in-bio.
- [ ] Follow ask reframed as a cadence/series payoff. 0 to 5 hashtags max (or none).

**SEO / AUTHORITY**
- [ ] ~80 to 90% pure value, brand mentioned exactly once, late, soft.
- [ ] Alt text = the actual slide text, one per slide (indexable by Google/Bing/LLMs).
- [ ] Companion Distribb article published/refreshed on the same keyword to close the loop.
- [ ] Never mention or link a competitor. Written in the project's language and voice.

**PUBLISH (Graph API hard limits)**
- [ ] Flow: child containers (`is_carousel_item=true`, poll FINISHED) -> `CAROUSEL` parent (poll FINISHED) -> `media_publish`.
- [ ] Min 2 / max 10 items via API. JPEG, public HTTPS `image_url` live through processing, first image locks ratio, <5MB, containers expire ~24h, 50/24h quota. Use the IG professional account id.

**TARGETS** (industry heuristics, medium confidence)
- [ ] Swipe-through 65%+, completion 55%+. Optimize for saves + sends + branded search, not likes or followers.

---

*Sources: Metricool 2026 study, Adam Mosseri (Oct 2024 / Jan-Feb 2025), Buffer, Hootsuite,
Social Insider, Later, plus Distribb's own DFY carousel research. Treat unlabeled percentages
as ranges. This playbook mirrors Distribb's internal carousel strategy, build spec, and the
Carousel Maker prompt.*
