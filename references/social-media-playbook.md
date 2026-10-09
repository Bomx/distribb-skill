# Social media playbook

How to grow a Distribb user's social accounts: what to post where, how often, how to turn articles and videos into posts, how to run comment-to-DM, the inbox and Reddit, and how to measure what works. For the exact publishing calls (reels, media upload, comment-for-guide settings) read `social-publishing.md`.

## Principles

1. **Native beats cross-posted.** The same idea, rewritten for each platform, beats one caption pasted everywhere. Change the hook, length, format and call to action per platform.
2. **Consistency beats volume.** Three good posts a week for six months beats thirty posts in one week and silence after. Pick a cadence the user can sustain.
3. **The first line or first second decides everything.** Write the hook first, the rest after. If the hook would not stop the user's own thumb, rewrite it.
4. **Saves, shares and comments are the signal.** Likes are cheap. A post people save or send to a friend gets shown to more people on every platform.
5. **One post, one idea, one call to action.**
6. **The business's own voice.** Read the project's business context (brand voice, audience, competitors) before writing. Never copy another account's words; borrow the format and angle only.

## Platform guide

| Platform | What works | Cadence that works for most businesses |
|---|---|---|
| Instagram | Reels (hook in the first second, 7 to 30 seconds, captions on screen), carousels for saves (cover hook, one idea per slide, last slide with the call to action), comment-a-keyword-to-get-the-guide | 3 to 5 Reels or carousels a week, Stories daily if possible |
| TikTok | Talking to camera, demos, behind the scenes, trends adapted to the niche; native text and sound | 3 to 7 a week |
| YouTube | Shorts for reach; long-form for search and trust (titles that match what people search, a chaptered description) | 2 to 4 Shorts a week, 1 long video a week or fortnight |
| LinkedIn | Text-first posts from a person's profile (personal profiles reach far more than Company Pages), document carousels, opinions backed by numbers, short stories with a lesson | 3 to 5 a week from the founder or team |
| X | Short takes, threads that teach, replies to bigger accounts in the niche | Daily, replies count |
| Facebook | Community, local offers, events, video; groups for niches | 3 to 5 a week |
| Pinterest | Evergreen how-to and product pins, vertical 2:3 images, keyword-rich titles; links to articles | 5 to 15 pins a week, scheduled |
| Threads, Bluesky | Conversational posts and replies; repurpose X and LinkedIn ideas | A few a week |
| Reddit | Genuine help in relevant threads, no links, no pitching; an account with history | A few helpful replies a week (see Reddit below) |
| Google Business Profile | Weekly posts: offers, updates, events, new articles; photos | 1 a week minimum |
| Telegram, Discord, Slack, WhatsApp | Announcements and community for existing customers or fans | When there is news; do not spam |

## Turning one article into a week of posts

Every published article can feed social:

1. **LinkedIn:** the article's sharpest finding as a 150 to 250 word post, a personal angle in the first line, the link in the first comment or at the end.
2. **Instagram carousel:** the article's steps or list as slides (see `instagram-carousel-playbook.md`), with comment-to-DM delivering the full guide.
3. **Short video (Reel, TikTok, Short):** one tip from the article in 20 to 40 seconds, said to camera or as a captioned screen recording.
4. **X thread:** the article's argument in 5 to 8 posts.
5. **Pinterest pin:** the article title as a keyword-rich pin linking to the article.
6. **Google Business post:** when the article is relevant to local customers.

Distribb can also auto-post new articles to a social account: `manage_integration` with `set_repurposing` on that account.

## Hooks that work

- A specific number or result: "We cut our clinic's no-shows by 38% with one text message."
- A mistake: "Stop posting at 9am. Here is when our customers actually read."
- A question the audience is already asking: "Is a heat pump worth it in a cold climate?"
- A contrarian line backed by experience: "Our best-performing post took ten minutes to make."
- A before and after the business can prove.

Avoid vague openers ("In today's fast-paced world"), stacked emojis, and hashtags as a strategy. Three to five relevant hashtags on Instagram is plenty; most other platforms need none.

## Using Distribb's social tools

| Task | Tools |
|---|---|
| See connected accounts | `list_social_accounts` (pick the exact handle the user named) |
| Publish or schedule now | `publish_social_post` (MCP), with media from `upload_social_media`; check with `get_social_post` |
| Save a draft for the user to review | `create_social_post` |
| Edit or remove saved posts | `update_social_post`, `delete_social_post` |
| Best posts so far | `get_top_social_posts` (ranked by views, likes, saves, shares; last 365 days by default) |
| Ideas from the niche | `get_inspiration_setup`, `track_inspiration_targets`, `scan_social_inspiration` (can take minutes), `list_social_inspiration` |
| DMs, comments, mentions, reviews, analytics, best times to post, broadcasts, automations | `zernio_project_accounts`, then `zernio_find_operations` and `zernio_call` |
| Organic video for Reels, TikTok or Shorts | `create_social_video` (lands as a draft) |
| Reddit | `get_reddit_opportunities`, `manage_reddit_radar` |
| The distribution network (Medium, LinkedIn articles, Quora) | `get_distribution_network`, `manage_network_post` |

Inbox and community calls that send, reply, delete or cost money return a preview first and only run with `confirm: true` after the user approves.

## Comment-to-DM (comment a keyword, get the guide)

This is the strongest growth loop on Instagram right now: the post promises a resource, people comment a keyword, an automatic DM sends the link.

- Promise something specific and useful: a checklist, a template, the full article, a price list.
- One keyword, short and unambiguous ("GUIDE", "PRICES"). Put it in the caption's first lines and on the last slide or end of the video.
- The DM message contains the link and one friendly line, nothing salesy.
- Set it when publishing (`is_comment_for_guide` with the configuration in `social-publishing.md`), verify the rule with `get_social_post`, and fix a failed rule with `configure_social_post_auto_reply` on the same post. Never republish to retry.
- Only DM people who commented the keyword. Never message people who did not ask.

## Community management

- Reply to comments in the first hour after posting when possible; early replies lift reach.
- Answer DMs within a day. Hide spam and abuse; never argue in public.
- Draft replies for the user to approve, unless they asked you to handle replies of a given kind on their own. Public replies and DMs speak for the business.
- Reviews on Google: reply to all of them, see the Google Business notes in `integrations-playbook.md`.

## Reddit

Reddit rewards help and punishes promotion.

- Reply only where the user genuinely knows the answer. Lead with the answer, add first-hand detail, no links and no product names unless someone asks.
- New or low-karma accounts start in warm-up mode (hobby subreddits, no business topics) until they have history.
- The account owner accepts the risk notice on the Reddit Radar page themselves before anything is posted from their account. Publishing is capped per day; scheduled replies spread out.

## Inspiration without copying

Use the inspiration scan to find what is working in the niche: the most engaged recent posts from competitors and keywords, news, rising searches and trending sounds. Take the format, the hook structure and the angle. Write it fresh for the user's brand, with their facts. Never reuse another account's wording, images or video.

## Measuring

- Read results weekly with `get_top_social_posts` and the analytics tools: saves, shares, comments, watch time and profile visits beat likes.
- For video, the first three seconds and the share of people who watch to the end matter most. Fix hooks before anything else.
- Put UTM parameters on links so website visits from social show in Google Analytics and the Analytics page.
- Double down on formats that work: when a post beats the account's median by two or three times, make three more on the same idea in different formats. The best ones are also the best candidates for paid ads (see `paid-ads-playbook.md`).

## Guardrails

- Never post publicly, send a DM or reply to a review without the user's approval of the exact text, unless they set a standing rule for that kind of post.
- Never say a post is live without its live URL or a published status from `get_social_post`.
- Respect each platform's rules: no buying followers or engagement, no mass identical DMs, no automation that impersonates a person.
- Health, finance and legal topics need care: no promises of results, no personal medical advice in replies.
