---
description: Plan, audit, build and scale ads on Meta, Google, TikTok and LinkedIn through the ad accounts connected to Distribb, following the paid ads playbook
argument-hint: (optional: audit | launch | scale | creative | report, or a network such as "google ads")
allowed-tools: Bash, Read, Glob, Grep
---

Load the Distribb skill (Integrations section) and read `references/paid-ads-playbook.md` first. `$ARGUMENTS` may name a focus (`audit`, `launch`, `scale`, `creative`, `report`) or a network.

1. Resolve `project_id` (`GET /api/v1/projects`), then read the setup: `tools:call --tool get_ads_setup` (mode read). It shows the ad accounts, currency, minimum daily budgets, Pages, Instagram accounts, pixels with their latest events, and Distribb's budget ceilings.
   - No ad account connected, or the ads tools are not available (`tool_not_available`): read the catalog (`integrations:catalog --category ads`). If an ad account is available to connect, send the user its `connect_url`. If not, say ad management is not on their account yet and stop.
2. When the account has it, ask the knowledge base before deciding: `tools:call --tool search_ads_knowledge --args '{"query": "<the situation in one sentence>", "network": "<meta|google|tiktok|linkedin>"}'`.
3. **audit / report:** `list_ad_campaigns` and `list_my_ads` (with `days`), plus `audit_meta_ads` or `audit_marketing` (area `google_ads`, `tracking`) when available. Report spend, results, cost per result and the trend, then the one or two changes worth making, each with its reason.
4. **creative:** research competitors (`get_competitor_ads_setup`, `scan_competitor_ads` one target per call, `list_competitor_ads`), then make ads with `create_video_ad` or from the business's best organic videos (`get_top_social_posts`, then `create_ads_from_own_videos`). Settle the angle, offer and audience with the user first.
5. **launch:** check tracking first (playbook checklist). Find targeting ids with `search_ads_targeting`, size it with `estimate_ads_reach`, then build with `create_meta_campaign`, `create_google_campaign`, `create_tiktok_campaign`, `create_linkedin_campaign` or `launch_video_ad`. The first call is a preview: show the full setup, budget and audience. Only after the user approves, run it again with `--mode action` and `"confirm": true`. New campaigns are created paused; resuming is its own approved step (`set_ad_campaign_status`).
6. **scale:** follow the playbook's scaling rules (raise budgets gradually, duplicate winners instead of editing them, raise the budget rather than the target on budget-limited Google campaigns). Every change is preview, approval, then `confirm: true` (`update_ad_campaign_budget`, `update_ads`).
7. Anything else on the ad accounts (audiences, lead forms and leads, pixels, conversions, keywords and negatives, search terms, sitelinks): `ads_find_operations` then `ads_call`, same preview and approval rule.

Never spend, resume or raise a budget without the user's explicit yes for that specific change. Report with the ad account's currency and the campaign's status from `list_ad_campaigns` as proof.
