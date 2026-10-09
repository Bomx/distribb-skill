# Paid ads playbook

How to plan, build, run and scale ads on Meta (Facebook and Instagram), Google, TikTok and LinkedIn for a Distribb user, using the ad accounts they connected. The rules below are what the best-known paid ads practitioners agree on as of late 2026 (Distribb keeps a knowledge base of their teaching, refreshed daily, which you can search with `search_ads_knowledge` when the account has it). Platforms change often: when a rule here and a fresh note from the knowledge base disagree, the fresher note wins.

## Rules before any money moves

1. **The user approves every change that can spend.** Creating, resuming, editing a budget or bid, launching a video ad: preview first, show it, wait for a clear yes, then run it with `confirm: true`. New campaigns are created paused; resuming them is its own approved step.
2. **Tracking comes before traffic.** No conversion tracking, no launch. Smart bidding on every network learns from conversions; without them it optimizes for clicks, and clicks include bots.
3. **Know the target cost before choosing a budget.** Work it out from the value of a customer, not gut feel (see Budget math).
4. **Respect the account's ceilings.** `get_ads_setup` returns the minimum daily budget per ad account and Distribb's own budget ceilings. Stay inside them.
5. **Never write misleading ads.** No fake scarcity, no invented reviews or numbers, no before and after claims the business cannot back up. Meta forbids ad copy that asserts or implies personal attributes ("Struggling with your debt?" aimed at "you"). Housing, employment, credit and political ads need the special ad category. Health and finance claims need care everywhere.

## The Distribb workflow

| Step | Tools |
|---|---|
| Read the setup | `get_ads_setup` (accounts, currency, pixels, Pages, ceilings), `get_ads_overview` |
| Check expert guidance | `search_ads_knowledge` with the situation in a sentence ("local plumber, Google Search, $40/day, no conversions yet") |
| Research competitors | `get_competitor_ads_setup`, `track_competitor_ads_targets`, `scan_competitor_ads` (one target per call; can take minutes), `list_competitor_ads`, `read_meta_ad_library` |
| Audit what exists | `list_ad_campaigns`, `list_my_ads`, `audit_meta_ads`, `audit_marketing` (area `google_ads`, `tracking` and more) |
| Make creative | `create_video_ad` (Distribb renders video ads), `create_ads_from_own_videos` (the business's best organic videos with a call to action card), `revise_video_ad`, `get_top_social_posts` |
| Targeting | `search_ads_targeting` (ids for places, interests, job titles, industries), `estimate_ads_reach` |
| Build | `create_meta_campaign`, `create_google_campaign`, `create_tiktok_campaign`, `create_linkedin_campaign`, `launch_video_ad`. Each first call is a preview |
| Run and change | `set_ad_campaign_status`, `set_ad_status`, `update_ad_campaign_budget`, `update_ads` (edit, pause, resume, duplicate, delete at any level) |
| Everything else | `ads_find_operations` then `ads_call`: audiences, lookalikes, lead forms and leads, pixels and conversion events, Conversions API, Google keywords, search terms and negatives, sitelinks and callouts, catalogs, LinkedIn forecasts |

Run reads and previews with `run_integration_read`, approved changes with `run_integration_action` (see the integrations playbook).

## Choosing the network

| Network | Best for | Watch out for |
|---|---|---|
| Google Search | Capturing people already searching for the service; local services; B2B with search demand | Needs enough budget for data (see below); match types are loose now |
| Google Performance Max | Ecommerce with a product feed; lead gen accounts that already convert steadily | Add it only after Search works; exclude the brand |
| Meta (Facebook, Instagram) | Creating demand: ecommerce, local offers, info products, apps, most B2C | Creative is the targeting now; weak creative cannot be fixed with audiences |
| TikTok | Younger audiences, products that demo well, UGC-style creative | Ads must look native; recycled TV-style ads fail |
| LinkedIn | B2B by job title, seniority, industry and company size | High cost per click; needs a strong offer (guide, demo, event) |
| Pinterest, X, ChatGPT Ads | Niche fits: visual planning (Pinterest), tech audiences (X), high-intent questions (ChatGPT) | Smaller volume; test with a capped budget |

For most small businesses: start with Google Search if people search for what they sell, start with Meta if they do not.

## Budget math

- **Target cost per acquisition** comes from value. A customer worth $2,000 can justify $400 to $500 to acquire. If 1 in 10 leads becomes a customer and the target CPA is $200, a lead is worth up to $20; capping cost per lead below what is still profitable starves growth.
- **ROAS targets:** set the target a little above breakeven (2.2 when breakeven is 2.0) and scale spend at that efficiency. More profit usually comes from multiplying spend at a thin margin than from chasing a high ROAS on a small budget.
- **Google Search volume:** aim for a budget that buys 10 to 20 clicks a day (300 to 600 a month). Two clicks a day gives one lead every few days, too little to optimize.
- **Low volume is noisy.** At around $100 a day with a $200 CPA, daily and weekly ROAS will swing a lot. Judge on two to four weeks, not days.

## Tracking checklist

- Meta: pixel plus the Conversions API, with the main event (Purchase, Lead, CompleteRegistration) firing; `get_ads_setup` shows when each pixel last received an event and the 7-day counts. Define audience segments (engaged audience, existing customers) in the ad account settings, otherwise the breakdowns that show where Advantage+ spends are missing.
- Google: conversion actions before launch. Ecommerce tracks purchase, add to cart and begin checkout. Lead gen tracks calls and each form. Make the money actions (booked appointment, qualified lead, purchase) primary and soft actions (contact page view) secondary.
- Leads that close later: import offline conversions from the CRM (Google keeps the click id; Meta and LinkedIn take CRM events too) and optimize for qualified leads or revenue, the deepest event you can measure. Send only the best leads back as the conversion signal.
- Use UTM parameters on every ad link so Google Analytics and the Analytics page attribute the traffic.

## Google Ads

Settings to check on every new Search campaign:

- Locations: choose **Presence** (people in or regularly in the area), never "Presence or interest", and add location exclusions; Google can still leak outside the area.
- Networks: untick **Search Partners** and the **Display Network**. Run image ads in their own campaign if wanted.
- Objective: pick Sales or Leads (or build without guidance). The objective only changes which settings are shown, not performance; never Website traffic for a business that wants leads or sales.
- **Auto-apply recommendations: off**, for all campaigns and all types, including bidding targets.
- Structure: consolidate. One ad group per distinct service (car servicing, car repairs, transmission repairs), not one ad group per keyword. Separate campaigns only for brand versus non-brand, different locations or languages, very different product ranges, and different campaign types.
- Assets: fill every type. Sitelinks to pricing, reviews and contact; callouts for trust ("family run since 1998", "500+ five-star reviews"); structured snippets for services.
- Audiences: add 20 to 30 segments in **Observation** mode (no restriction) to learn who converts.

Bidding path:

1. New account, new product or no conversion data: start on Maximize Clicks (with a CPC cap) or manual CPC while you check traffic quality. Maximize Conversions with no data bids aggressively and CPCs can explode.
2. Once conversions flow: Maximize Conversions.
3. Moving to a target CPA: start at or about 10% above the campaign's current 30-day CPA, never below it.
4. Since August 17, 2026, a budget-limited campaign on target CPA or target ROAS bids toward the target instead of buying the cheapest conversions. If a campaign beats its target and the CPA is acceptable, raise the budget, not the target.

Keep it healthy:

- Read the search terms every week and add negatives, especially on broad match, Dynamic Search Ads or AI Max. Match types now target meaning, so even exact match shows for close variations.
- Add the columns "Search lost IS (budget)" and "Search lost IS (rank)". Losing share to budget with an acceptable CPA is the simplest signal to raise the budget.
- Do not over-optimize: no flurries of negatives, no constant copy changes without a structured test, no bid strategy changes every other week. Let each change settle.
- Performance Max: for lead gen, add it only after Search runs at least a month and the account has roughly 30 to 50 conversions a month. Add a brand exclusion list; run brand in its own Search campaign.

## Meta ads (Facebook and Instagram)

- **Objective:** Sales or Leads from day one. New accounts do not need to warm the pixel with Traffic or Engagement; Meta optimizes literally and a Traffic campaign buys clicks, bots included.
- **Structure:** one long-lived campaign budget (CBO) campaign per business goal (a product line, a country, a men's versus women's range). No separate testing and scaling campaigns: test by adding new ad sets with new creative inside the main campaign; new ads only take spend when they beat the existing ones. Number creative ideas in ad set names to track how many concepts were tried.
- **Creative is the targeting.** Since Meta's Andromeda retrieval update, delivery matches creative to people. Put real variety in an ad set (static and video; UGC, testimonial, demonstration, founder-led) instead of tiny variations. Group near-identical versions (same person, different headline) into one flexible ad, otherwise only a few get delivery.
- **Audiences:** in the default Advantage+ audience, age and gender are suggestions. To make them hard limits, switch to the original setup and untick "use as suggestion". Often better: keep broad targeting and lower bids on low-value segments with value rules.
- **Do not touch winners.** Editing, pausing or moving a winning ad or campaign can wreck it. Scale by raising budget gradually and by duplicating the winner, leaving the original alone. Large one-time budget jumps can multiply the cost per purchase.
- **Read results correctly.** New ads often look great for a few days, then decline as delivery moves to colder people; that is not fatigue. High-spend ads carry a higher CPA because they reach colder audiences; judge the ad set and campaign in aggregate. CTR above 3% with few conversions points at the landing page or a hook that does not match purchase intent.

## TikTok ads

- Creative must look like TikTok: vertical, people talking to camera, captions, fast first second. Reuse what already works organically.
- Spark Ads boost an existing TikTok post (through `ads_call` boostPost) and keep its social proof.
- Smart+ campaigns automate targeting and bidding and work well once the pixel has events.

## LinkedIn ads

- Target by job title or function, seniority, industry and company size; keep audiences specific and switch audience expansion off unless reach is the goal.
- Lead gen forms convert far better than sending people to a site. Offer something worth a work email: a benchmark report, a template, a demo, an event.
- Thought leader ads (a person's post, promoted) and document ads usually beat polished brand creative.
- Expect high CPCs; use `ads_call` for LinkedIn bid pricing and forecasts before setting budgets.

## Creative that works in 2026

- **The hook is the first 3 seconds** (the headline and image for statics). Iterate winners by swapping only the first 3 to 5 seconds and keeping the body.
- Formats that keep scaling: personal story "yapper" ads from creators, founder-led videos, honest testimonials, product demonstrations, comparison and transformation ads (competitors need not be named), educational breakdowns, and video sales letters for complex products.
- Cover every awareness level. Most accounts have too much offer-led and brand-aware creative and too little for people who do not yet know they have the problem.
- Ship new creative on a fixed weekly rhythm, whatever the results. Panic batches after a bad day are weak.
- Use organic social as the free test: the business's posts that take off organically are the best candidates for ads (`get_top_social_posts`, then `create_ads_from_own_videos`).
- Competitor research: in the ad library, long-running ads are the strongest public sign of a winner, but check where each ranks for impressions within the advertiser's ads. An ad active for a year that barely spends is not a winner.
- AI-made creative tends to look like everyone else's. Add something only this business has: real customers, the founder, the actual product, local places.

## Diagnosing problems

| Symptom | Likely cause | First action |
|---|---|---|
| Spend but no conversions | Tracking broken, or wrong optimization event | Check pixel events in `get_ads_setup`; check primary conversions on Google |
| Clicks are cheap but junk | Search Partners/Display on, "Presence or interest", broad terms, Traffic objective | Fix settings; read search terms; switch to a conversion objective |
| Campaign "Limited by budget" with good CPA | Budget too small for demand | Propose a budget increase |
| CPA jumped after a change | Large budget jump, edited winner, new bid strategy | Revert or wait out the learning period; scale more gradually |
| New ads get no spend | Too similar to existing ads, or existing ads are stronger | Make genuinely different concepts; group variants in a flexible ad |
| Good CTR, few sales | Landing page, offer, or hook-to-page mismatch | Review the page; match the page headline to the ad's promise |
| Leads convert poorly | Optimizing for raw leads | Add qualifying questions; import qualified or closed leads as conversions |

## Reporting to the user

Report spend, results, cost per result and the trend against the previous period, then one recommendation with its reason. Use the ad account's currency. Never round a loss into a win, and never claim a campaign is live without its status from `list_ad_campaigns`.
