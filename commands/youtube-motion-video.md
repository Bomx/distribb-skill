---
description: Make a faceless motion-collage explainer video ("In a Nutshell" docu style), optimize it for YouTube SEO with Distribb data, and publish it to the connected YouTube channel
argument-hint: <topic-or-keyword>
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Produce and publish a YouTube-SEO motion video for: `$ARGUMENTS`

This is the "YouTube SEO With Motion Videos" workflow. You turn a keyword/concept
into a short, faceless **motion-collage explainer** (bold screen-print cutout collage
visuals + a calm "In a Nutshell" documentary voice), optimize it for YouTube SEO with
Distribb's real keyword and Search Console data, and publish it to the user's
connected YouTube channel through Distribb, then publish a companion article that
embeds it.

Load the Distribb skill, then READ `references/youtube-motion-video-playbook.md` for
the full method (preflight, the collage look, the Seedance motion rules, the docu
voice, the SEO packaging, the publish path). Then run this workflow against
`$ARGUMENTS`:

1. **Preflight.** Confirm `DISTRIBB_API_KEY` works (`GET /api/v1/projects`) and pick
   the `project_id`. Ensure the production skill is installed:
   `npx skills add Bomx/super-video-maker-skill` (or clone
   `https://github.com/Bomx/super-video-maker-skill`). Confirm the production keys the
   video skill needs exist: `OPENAI_API_KEY` (images), `FALAI_API_KEY` (Seedance via
   fal.ai), `ELEVENLABS_API_KEY` (voice). Confirm the user's YouTube channel is
   connected in Distribb: `GET /api/v1/integrations?project_id=<id>`; if not, send them
   to https://distribb.io/integrations ("Connect via Google") and stop.

2. **Project + voice.** `GET /api/v1/business-context?project_id=<id>` for brand voice,
   language, audience, and competitors. The narration matches the project's language
   and voice; never mention or link to a competitor.

3. **Pick the target keyword (the SEO step).** `POST /api/v1/keywords/search` on the
   concept and `GET /api/v1/search-console` for striking-distance queries. Choose ONE
   winnable, on-brand primary keyword. It becomes the concept, the title spine, and the
   companion article's keyword. On a legacy Free Agentic account, if `keywords/search` returns HTTP 402
   `byo_keys_required`, surface the message verbatim and use GSC + the concept instead.

4. **Script the docu VO.** Write the "In a Nutshell" narration (open on a question,
   name the concept, one analogy, takeaway, soft CTA). Calm and curious, one idea,
   second person, no invented stats, **no em dashes**. Split into 3 to 6 beats. Show
   the user the concept + script before spending on generation.

5. **Produce the video** with super-video-maker's `motion-collage-explainer` recipe
   (see its `MOTION_COLLAGE_STYLE.md`): build one collage poster per beat with
   `image_provider.py generate` / `openai_image_tool.py` (`gpt-image-2`, `1024x1536`
   for 9:16), animate each still with `fal_seedance_video.py --mode image` (Seedance 2.0
   via fal.ai, the generated image as reference), then add ElevenLabs VO, beat-locked
   karaoke captions, and export the `9:16` master (and `16:9` if requested). QC that
   every frame still reads as a flat printed collage.

6. **Package for YouTube SEO.** Keyword-led title (under ~70 chars), a description whose
   first line restates the keyword + payoff, chapter timestamps, a link to the companion
   article + site, a soft CTA, tags = primary keyword + 5 to 12 related terms from the
   keyword response, and a collage thumbnail (reuse the hero poster or a 16:9 variant).

7. **Publish to YouTube via Distribb.** With the channel connected (step 1), publish the
   finished MP4 to the connected YouTube channel through Distribb's Social publishing,
   applying the step-6 title, description, and tags. Record the resulting YouTube URL.

8. **Close the SEO loop.** Publish a companion Distribb article that embeds the YouTube
   video and targets the same keyword: `GET /api/v1/internal-links` and (if the project
   is in the exchange) `GET /api/v1/backlink-targets`, weave both in, then
   `POST /api/v1/articles`. If the response has a `backlinks_warning`, add network links
   and `PUT` the revised content.

9. **Summarize.** Print: concept + primary keyword, the video path(s), the YouTube URL,
   the title/description/tags, and where the companion article landed (draft/scheduled).

Default to one video per run unless the user asks for a batch.

## Rules
- Install and drive super-video-maker; do not reimplement image/video generation here.
- Topic and title come from real keyword/GSC data, not vibes.
- Match the project's language and brand voice. Never link to competitors.
- Docu voice, one idea, calm and curious. No invented stats. No em dashes.
- Keep it a living collage; never ship a Seedance frame that realified the paper collage.
- Confirm the YouTube connection before any paid generation.
