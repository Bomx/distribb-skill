---
description: Make a "<competitor> reviews" video: compile REAL, verified reviews of a competitor, name the recurring gaps, position the connected project's own business as the alternative, hand off to the project's own testimonials, then publish it to YouTube and close the loop with a companion article.
argument-hint: <competitor name or review-page URL> (+ optional path to your own testimonial reel)
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Produce and publish a keyword-targeted **"<competitor> reviews"** video for: `$ARGUMENTS`

This is the **Review-Conquest** workflow. You compile REAL, verified reviews of a competitor
(mostly the honest negatives + neutrals, a couple of positives for balance), surface the
recurring gaps, and position **the connected project's own business**, whatever business is
configured in Distribb, not any specific company, as the alternative that closes those gaps,
ending by handing the mic to the project's own customer testimonials. Then you publish it to the
connected YouTube channel and close the SEO loop with a companion article.

Distribb is the SEO brain (the keyword, GSC, the project's business context, publishing, the
companion article + backlinks); the **`super-video-maker`** skill is the production engine.
Install it once with `npx skills add Bomx/super-video-maker-skill` (or clone
`https://github.com/Bomx/super-video-maker-skill`) and follow its **`REVIEW_VIDEO_PLAYBOOK.md`**
for the research, verification, and faceless-VO-montage build.

## Guardrail (read first)
Only put REAL, verified, attributable reviews on screen, never invent, embellish,
paraphrase-as-a-quote, or doctor a review. Cherry-picking honest negatives is legitimate
comparative marketing; fabricating or misrepresenting a competitor is false advertising +
defamation. Be honest about the competitor's overall rating and win on the *pattern* in the
complaints. If the competitor has no genuine critical-review volume, tell the user and stop.
Never push anything but the connected project's own business.

## Workflow
1. **Preflight.** Confirm `DISTRIBB_API_KEY` works (`GET /api/v1/projects`) and pick the
   `project_id`. Ensure super-video-maker is installed and the production keys exist
   (`ELEVENLABS_API_KEY` for VO; `OPENAI_API_KEY` optional for captions/inserts). Confirm the
   YouTube channel is connected (`GET /api/v1/integrations?project_id=<id>`); if not, send the
   user to https://distribb.io/integrations ("Connect via Google") and stop.
2. **Whose business is the alternative.** `GET /api/v1/business-context?project_id=<id>` for the
   project's name, value props, audience, language, and competitors. **THIS project's business is
   the alternative you position at the end, never hardcode a company.** If `$ARGUMENTS` doesn't
   name a competitor, offer the ones in `business_context.competitors`.
3. **Pick the keyword (the SEO step).** `POST /api/v1/keywords/search` on "<competitor> reviews"
   and "<competitor> alternative"; `GET /api/v1/search-console` for related striking-distance
   queries. The primary keyword becomes the title spine + the companion article's keyword. On a
   legacy Free Agentic account, if `keywords/search` returns HTTP 402 `byo_keys_required`, surface it verbatim
   and use the concept + GSC instead.
4. **Research + verify + produce** with super-video-maker's `REVIEW_VIDEO_PLAYBOOK.md`: fan out
   across every review surface (Trustpilot, G2/Capterra, app stores, Reddit/forums, review blogs,
   YouTube, social), extract verbatim reviews with exact source URLs, drive a real browser where
   sites 403 automated fetches (Trustpilot), **adversarially verify every critical quote**, then
   build the faceless VO montage. Map each recurring gap to a TRUE strength of THIS project's
   business (use the business context + `references/plans-and-backlinks.md` etc. for what is
   genuinely differentiated, e.g. real backlinks, internal linking, GSC-grounded content).
   Append the project's own testimonial reel if provided; end on the project's site/CTA. **Show
   the user the verified reviews + script before any paid generation.**
5. **Package for YouTube SEO.** Keyword-led title ("<Competitor> Reviews: …"), a description
   whose first line restates the keyword and states that **every review shown is real and
   sourced**, chapter timestamps (include the "Real <Business> customers" testimonial chapter), a
   link to the companion article + the project's site, tags = primary keyword + related terms, and
   a hook thumbnail.
6. **Publish to YouTube via Distribb.** With the channel connected, publish the finished MP4 to the
   connected channel through Distribb's Social publishing, applying the step-5 packaging. Record
   the YouTube URL.
7. **Close the loop.** Publish a companion Distribb article targeting "<competitor> reviews" /
   "<competitor> alternative" that embeds the video: `GET /api/v1/internal-links` and (if the
   project is in the exchange) `GET /api/v1/backlink-targets`, weave both in, then
   `POST /api/v1/articles`. If the response has a `backlinks_warning`, add network links and `PUT`
   the revised content.
8. **Summarize.** Competitor + primary keyword, the verified-review count + sources, the video
   path, the YouTube URL, the title/description/tags, and where the companion article landed.

## Rules
- Install and drive super-video-maker; do not reimplement research/production here.
- Real, verified, attributable reviews only; the on-screen source stays visible. Be honest about
  the competitor's overall rating.
- **The alternative is the connected project's business, pulled from business context, never
  hardcode a specific company.** Only push that project.
- Keyword and title come from real keyword/GSC data. Real review screenshots, never generated ones.
- Confirm the YouTube connection and show the verified reviews + script before any paid generation.
