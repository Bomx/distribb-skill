# YouTube SEO With Motion Videos (Playbook)

Turn a keyword or concept into a short, faceless **motion-collage explainer video**
(bold screen-print cutout collage visuals, calm "In a Nutshell" documentary voice),
optimize it for **YouTube SEO** with Distribb's real keyword + Search Console data,
and publish it to the user's connected **YouTube** channel through Distribb.

This playbook pairs the **Distribb SEO brain** (keyword data, GSC, internal links,
backlinks, publishing, a companion article) with the **`super-video-maker` skill**
(image + Seedance video production). It is driven by the `/youtube-motion-video`
slash command.

The look and the production method are defined in the super-video-maker skill's
`MOTION_COLLAGE_STYLE.md` and its `motion-collage-explainer` recipe. This playbook
is the SEO-and-publish wrapper around that recipe.

---

## What you produce

A 20 to 45 second vertical (`9:16`, plus `16:9` if the user wants a standard upload)
explainer short:
- one concept, idiom, or "simple question" made concrete,
- **visuals:** a black-and-white halftone **cutout collage** on a single bold flat
  background, torn-paper caption label, flat geometric accents, that **comes to life**
  with subtle Seedance motion (a living collage, not a re-imagined scene),
- **voice:** a calm, curious documentary narration in the spirit of Kurzgesagt
  ("In a Nutshell"): open on a question, name the concept, one analogy, a takeaway,
- **SEO:** a keyword-led title, a structured description, tags, and a companion
  Distribb article that embeds the video and cross-links it.

---

## Preflight (do this once)

1. **Distribb.** Confirm `DISTRIBB_API_KEY` is set and the account is active
   (`GET /api/v1/projects`). Pick the `project_id` this video is for.
2. **Install the video skill.** The production runs on the super-video-maker skill:
   ```bash
   npx skills add Bomx/super-video-maker-skill
   ```
   If `npx skills` is not available, clone it and point the agent at the folder:
   `git clone https://github.com/Bomx/super-video-maker-skill`.
3. **Production API keys** (used by super-video-maker, not by Distribb):
   - `OPENAI_API_KEY` for the collage stills (`gpt-image-2`),
   - `FALAI_API_KEY` for Seedance 2.0 through fal.ai,
   - `ELEVENLABS_API_KEY` for the narration voice.
4. **YouTube connection.** The user connects their own YouTube channel in Distribb at
   **https://distribb.io/integrations** ("Connect via Google"). Confirm it with
   `GET /api/v1/integrations?project_id=<id>` and look for a connected YouTube account.
   If it is not connected, stop and send the user to the Integrations page first;
   there is nowhere to publish until the channel is connected.

---

## The loop

### 1. Project + voice

```bash
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/business-context?project_id=42" | jq .
```

Pull brand voice, language, target audience, and competitors. The narration must
match the project's language and voice. Never mention or link to a competitor in
the description or the companion article.

### 2. Choose the target keyword (this is the SEO)

The video's topic and title are chosen from **real data**, not vibes. Two sources:

```bash
# Search-intent keywords with volume + difficulty
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "<concept or seed>", "project_id": 42}' \
  https://distribb.io/api/v1/keywords/search | jq .

# What the site already gets impressions for (find a phrase the channel can win)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/search-console?project_id=42&days=90&limit=100" | jq .
```

Pick ONE primary keyword that is:
- a real question or concept people search ("what is bikeshedding", "why do meetings run long"),
- winnable (lower difficulty, or an existing striking-distance query from GSC),
- on-brand (ties back to what the business does).

That keyword becomes the video's concept, its title spine, and the companion
article's keyword. On the **Free Agentic** plan, `keywords/search` returns HTTP 402
(`byo_keys_required`) until the user saves a DataForSEO or Ahrefs key; surface that
message verbatim and use GSC + the concept directly instead.

### 3. Script the docu narration

Write the VO in the "In a Nutshell" documentary voice (full rules in
`MOTION_COLLAGE_STYLE.md`, section 5):

- **Open on a simple question or vivid scenario.** ("Ever sat in a meeting where
  everyone argues for an hour about the color of a button?")
- **Name the concept.** ("That is bikeshedding.")
- **Explain with one analogy.** Short sentences, one idea each.
- **Land the takeaway.** One sentence the viewer keeps.
- **Soft CTA** to the channel.

Rules: second person, calm and curious (not hype), no invented statistics, and
**no em dashes** (use commas and periods). Split the script into 3 to 6 beats, one
collage poster per beat.

### 4. Produce the video (super-video-maker `motion-collage-explainer`)

Hand the concept, script, brand color, and target aspect ratio to the video skill
and run its `motion-collage-explainer` recipe. The three production steps:

**a. Collage stills with `gpt-image-2`** (one poster per beat, `1024x1536` for 9:16).
Use the super-video-maker image tool (equivalent to the repo-root
`openai_image_tool.py`) with the `MOTION_COLLAGE_STYLE.md` prompt formula:

```bash
python3 <svm>/tools/image_provider.py generate \
  --prompt "Flat screen-print collage poster, single saturated <brand color> background... \
    black-and-white halftone cutout of <subject doing the literal concept>, paper sticker \
    with white die-cut outline and torn edges, flat geometric accents, torn-paper label \
    reading '<CONCEPT>' in bold condensed uppercase. Matte risograph, limited palette. \
    Avoid gradients, glow, neon, 3D, photorealism, extra text." \
  --size 1024x1536 --quality high --output-format png
```

**b. Animate the still with Seedance 2.0 via fal.ai** (image-to-video, the generated
image is the reference). Motion must be a *living collage*, not a new scene:

```bash
python3 <svm>/tools/fal_seedance_video.py generate \
  --mode image \
  --reference-image output_images/collage_beat1.png \
  --prompt "Subtle living-collage motion: the paper cutout bobs with soft parallax, \
    accent shapes drift, <one literal concept motion>, faint halftone shimmer, gentle \
    push-in. Stays a flat printed paper collage. No scene change, no 3D, no morphing." \
  --duration 5 --resolution 1080p --aspect-ratio 9:16
```

Use `--mode reference` (and reuse one `--seed`) when several beats should share the
collage style. If Seedance "realifies" the collage, lower the motion, tighten the
prompt, or fall back to an FFmpeg Ken Burns + shape-parallax pass on the static PNG.

**c. VO + captions + assemble.** ElevenLabs narration, Whisper word-timing, beat-lock
each collage cut to sentence breaks, centered karaoke captions kept clear of the
torn-paper label band, loudness-normalize, export the `9:16` master (and `16:9` if
requested). QC that every frame still reads as a flat printed collage.

`<svm>` = the installed super-video-maker skill path (e.g.
`.agents/skills/super-video-maker` or wherever `npx skills add` placed it).

### 5. Package for YouTube SEO

Build the upload metadata from the Distribb keyword data:

- **Title:** lead with the primary keyword, keep it a real question/claim, under ~70
  chars. ("Bikeshedding: Why Teams Argue About Trivial Things").
- **Description:** first line restates the keyword and the payoff (this is what ranks
  and shows in search). Then 2 to 4 lines of context, chapter timestamps if the video
  has beats, a link to the companion article (step 7) and the site, and a soft CTA.
  No em dashes.
- **Tags / hashtags:** the primary keyword plus 5 to 12 related terms from the
  `keywords/search` response (the related keywords array).
- **Thumbnail:** reuse the hero collage poster (or generate a 16:9 collage variant at
  `1536x1024`) with the concept label large. Faces/text kept out of the corners.

### 6. Connect + publish to YouTube via Distribb

The channel is connected in Distribb (preflight step 4). Publish the finished video
to that connected YouTube channel **through Distribb**, applying the title,
description, and tags from step 5:

- Confirm the connection: `GET /api/v1/integrations?project_id=42` shows the YouTube
  account.
- Publish the MP4 to the connected YouTube channel from Distribb's Social publishing
  (dashboard **Social / Composer**, YouTube destination), with the SEO title,
  description, and tags. Distribb handles the upload to the user's channel.
- Record the resulting YouTube URL; it feeds step 7.

Note: Distribb's documented `/api/v1` surface publishes **articles** to the CMS, not
video files to YouTube, so the video upload runs through Distribb's connected-social
publishing (the Integrations + Social flow), not a `/api/v1/articles/:id/publish`
call. Keep the video's canonical home on the user's own YouTube channel.

### 7. Close the SEO loop with a companion article

This is where "YouTube SEO" compounds. Publish a short Distribb article that
**embeds the YouTube video** and targets the same keyword, so the video earns search
and AI-search visibility and the article drives watch time back to the channel:

```bash
# internal links to weave in
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/internal-links?project_id=42&keyword=<primary keyword>" | jq .

# backlink targets (mandatory if the project participates in the exchange)
curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  "https://distribb.io/api/v1/backlink-targets?project_id=42&keyword=<primary keyword>" | jq .

# publish the companion article (embed the YouTube iframe, target the keyword)
curl -s -X POST -H "Authorization: Bearer $DISTRIBB_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg content "$(cat companion.html)" '{
    "project_id": 42,
    "keyword": "<primary keyword>",
    "title": "<keyword-led title>",
    "content": $content,
    "meta_description": "<one-line summary>",
    "status": "Draft"
  }')" \
  https://distribb.io/api/v1/articles | jq .
```

The article should: embed the YouTube video near the top, expand the concept the
video explains (so it stands alone as a text answer AI engines can quote), weave in
the recommended internal links, and include 1 to 2 backlink-exchange targets as
natural references (this is how the user earns backlinks). If the create response
carries a `backlinks_warning`, add network links and `PUT` the revised content.
Publishing follows the project's `PublishingStatus` (see the main SKILL.md).

---

## Rules

- **Install super-video-maker first.** This playbook does not reimplement image or
  video generation; it drives that skill's `motion-collage-explainer` recipe.
- **Choose the topic from real keyword/GSC data**, not vibes. The keyword is the
  title spine and the companion article's target.
- **Match the project's language and brand voice** from `business-context`.
- **Docu voice, not hype.** Calm, curious, one idea. No invented statistics. No em dashes.
- **Keep it a living collage.** If Seedance turns the paper collage into a realistic
  scene, fix it (lower motion, tighter prompt, or FFmpeg fallback). Do not ship a
  realified frame.
- **Never link to competitors** in the description or the companion article.
- **The video's canonical home is the user's own YouTube channel**; the companion
  article embeds it, it is not re-hosted elsewhere first.
- **Confirm the YouTube connection before producing anything expensive.** No connected
  channel means nowhere to publish.
