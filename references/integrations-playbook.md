# Integrations playbook

Everything a user connects on Distribb's Integrations page can be used by you, their agent: their website CMS, social accounts, ad accounts, Google Search Console, Google Business Profile, analytics tools, bank accounts, databases, GitHub, and the newer integrations Distribb keeps adding. This guide covers how to find what is connected, how to get the user connected, how to act on each integration safely, and which connections to set up first for each goal.

The catalog is the source of truth. Which integrations an account can use depends on its plan and on what Distribb has released to it, so always read the catalog instead of assuming.

## The one rule about connecting

Connecting stays with the user. You never ask for a password or an API key in the chat, and you never type one into a form for them. You send the user a connect link; it opens that integration's own card on Distribb, where they sign in with the service or paste their key into Distribb's form. Distribb checks the key before saving it and seals it. You then confirm with the catalog that it shows `connected: true`, and only then say it is connected.

If a user pastes a key into the chat anyway, do not use it. Tell them to paste it on the card instead and, for anything sensitive, to rotate it afterwards.

## How to use integrations, step by step

| Step | MCP tool (Claude, ChatGPT, any MCP client) | Skill CLI | REST |
|---|---|---|---|
| 1. See what exists and what is connected | `integrations_catalog` | `integrations:catalog --project-id 42` | `GET /api/v1/integrations/catalog?project_id=42` |
| 2. Get the link that connects one | `connect_integration` | `integrations:connect --project-id 42 --integration "meta ads"` | `GET /api/v1/integrations/connect?project_id=42&integration=meta%20ads` |
| 3. Find the tools for a job | `find_integration_tools` | `tools:list --area paid_ads` | `GET /api/v1/agent-tools?area=paid_ads` |
| 4. Read, or preview a change | `run_integration_read` | `tools:call --mode read ...` | `POST /api/v1/agent-tools/call` with `"mode": "read"` |
| 5. Make the change | `run_integration_action` | `tools:call --mode action ...` | `POST /api/v1/agent-tools/call` with `"mode": "action"` |
| 6. Collect a long-running result | `get_integration_result` | `tools:job --job-id ...` | `GET /api/v1/agent-tools/jobs/<job_id>` |
| Playbooks | `get_playbook` | `playbooks:get --topic paid-ads` | `GET /api/v1/playbooks/<topic>` |

Details that matter:

- **project_id** comes from `list_projects`. Distribb binds every tool to that project and checks the user can access it. Never put `project_id` inside `arguments`; it is ignored there.
- **Get the schema before you call.** `find_integration_tools` lists tools with short descriptions. Pass `names` (for example `names: ["create_meta_campaign"]`) to get the full description and the `input_schema` before running it.
- **read_only tools** (results, accounts, lists, research) run with `run_integration_read`. Your client will not prompt the user for these.
- **preview_safe tools** have a `confirm` argument. Without `confirm: true` they change nothing and return exactly what would happen. Run the preview with `run_integration_read`, show the user the change in plain words, and only after they say yes run the same call with `run_integration_action` and `"confirm": true`.
- **Everything else** changes something (starts a scan, saves a trigger, writes a draft in a connected tool) and runs with `run_integration_action`.
- **Long calls.** A call that is still working after about 20 seconds comes back with `status: running` and a `job_id`. Wait about 30 seconds and read it with `get_integration_result`. Do not start the same call again; the first one is still running.
- **Errors are information.** `tool_not_available` means the account cannot use that tool yet (plan or release). `project_not_found` means the wrong project_id or no access. `needs_action_mode` means you tried to change something with the read tool. `confirm_required` is a preview, not an error.

### Example: pause a campaign

1. `run_integration_read` with `tool: "list_ad_campaigns"`, `arguments: {"days": 7}`. Find the campaign and its `campaign_id`.
2. `run_integration_read` with `tool: "set_ad_campaign_status"`, `arguments: {"campaign_id": "...", "status": "PAUSED"}`. It returns the exact change and changes nothing.
3. Tell the user: "This pauses Competitor Keywords (spend $54/day over the last week). Pause it?"
4. After they say yes: `run_integration_action` with the same arguments plus `"confirm": true`.

## What to connect first, by goal

Recommend, do not quiz. Pick the two or three connections that move the user's goal, say why in one line each, and send the links.

| Goal | Connect first | Why |
|---|---|---|
| Rank on Google and in AI answers | Website CMS, Google Search Console | Distribb can publish, and every audit and optimization runs on real Search Console data |
| Prove SEO is working | Search Console, Google Analytics, Stripe or Polar | Clicks, sessions and revenue in one place, so results are measured in money |
| Local business (clinic, trades, restaurant, agency) | Google Business Profile, Search Console, CMS | Reviews and Google posts drive local rankings; the practice management system adds the clinic profile |
| Grow on social media | Instagram, TikTok, LinkedIn, YouTube (whichever the audience uses), plus Facebook for Meta Pages | Publishing, scheduling, comment-to-DM, the inbox and post analytics |
| Run paid ads | The ad account (Meta Ads, Google Ads, TikTok Ads or LinkedIn Ads), the matching social account, Google Analytics | Campaigns need the account; Meta ads need the Page and Instagram account; results need analytics |
| Link building and outreach | Hunter, the email tool (Brevo or Kit), LinkedIn | Find and verify the right contact, draft campaigns, follow up |
| Product and revenue analytics | PostHog, Mixpanel or Amplitude; Stripe or Polar; Microsoft Clarity | Behaviour, revenue and session recordings in every answer about results |
| Mobile apps | AppsFlyer or Adjust, plus the ad accounts | Installs and attribution next to ad spend |
| Developer or data teams | GitHub, the production database (read only) | Answers from real data and code; changes go through an Approve card |

## Notes per kind of integration

### Website CMS (Blog tab)

- WordPress: the Distribb plugin is the most reliable connection (it handles images, categories and IndexNow). Use the application password route only when the plugin cannot be installed.
- Shopify, Notion: OAuth, one click. Webflow, Wix, Ghost, Framer, GoHighLevel: an API key or token from the platform's settings; the card says where to find it.
- Webhook: for any custom site or headless CMS. The site receives each article as JSON.
- GitHub: for static sites (Next.js, Astro, Hugo, Jekyll). Articles are committed as Markdown, or opened as pull requests when the user wants to review them.
- Health checks: `probe_integration` checks reachability only. When a publish fails, read `get_publish_failure_details` first, fix the cause with the user, then `replay_publish`. Never send a test article to check a connection.
- `manage_integration` turns a connection on or off, sets auto-posting of new articles to a social account, picks the WordPress category, and switches on IndexNow.

### Google Search Console

- The property must be the user's own site (a Domain property is best). Data lags two to three days.
- With it connected, the SEO audit, the optimization suggestions and keyword planning use real queries instead of estimates. It is the single most valuable connection for SEO.

### Google Business Profile

- Replies to reviews are public and show on Google. Draft them, show the user, post only what they approve.
- Reply to every review, good or bad, within two days. Thank by name, mention the service, never argue, never reveal private health or customer details.
- A Google post every week (offer, update, event, new article) keeps the profile active.

### Social accounts

- Each platform account the user connected appears in `list_social_accounts`. Publish with `publish_social_post` and pick the exact account the user named; projects can have several accounts on one platform.
- Beyond posting, the social tools reach DMs, comments (reply, hide, like), mentions, reviews, post analytics, best times to post, broadcasts, comment-to-DM automations, WhatsApp, Discord, Slack and Telegram. Search them with `find_integration_tools(area: "social")`, start with `zernio_project_accounts`, then `zernio_find_operations` and `zernio_call`.
- Sending, replying, deleting or anything that costs money returns a preview first; it runs only with `confirm: true` after the user approves.
- See the social media playbook for formats and cadence.

### Ad accounts

- Start every ads task with `get_ads_setup`: the accounts, currency, minimum daily budgets, Pages, Instagram accounts, pixels and when each last received an event, and Distribb's budget ceilings.
- New campaigns, ad sets and ads are created paused unless the request says otherwise. Nothing spends until the user resumes them.
- Every change is preview first, then `confirm: true` after the user approves. Never resume a campaign or raise a budget on your own initiative.
- See the paid ads playbook before building or changing anything.

### Analytics tools

- Google Analytics signs in with Google. The others take a read-only key or token; each card explains which scope to create (for example a scoped token limited to one website for DataFast, a restricted read key for Stripe).
- Once connected, `get_analytics_hub` returns every connected source with the last 28 days next to the previous 28 days. `run_analytics_scan` refreshes everything (about a minute; it may come back as a job).
- Which to recommend: Google Analytics for traffic, Stripe or Polar for revenue, PostHog, Mixpanel or Amplitude for product behaviour, Microsoft Clarity for recordings and heatmaps, CallRail for phone leads, AppsFlyer or Adjust for apps, Ahrefs or Semrush when the user already pays for them.

### Bank accounts (Plaid)

- Read only: Plaid is asked for transactions only, which cannot move money. `get_bank_accounts`, `get_bank_transactions` and `get_cash_flow` answer questions about balances, spend by category and runway.
- Treat these numbers as private. Summarize; do not paste account numbers.

### Databases and GitHub (Developer tab)

- Twenty database engines (Postgres, MySQL, Supabase, BigQuery, Snowflake, MongoDB, Pinecone and more) plus GitHub repositories. Start with `list_data_connections`, then `database_schema`, then `query_database` with one read query. Vector stores answer `search_vectors`.
- Agents outside Distribb can read. Changes to a database or a repository are proposed and approved by the user on a card in the Distribb Agent chat.

### The newer integrations

These arrive regularly, so check the catalog's `lab` group. Current ones and what they are good for:

| Integration | Use it for |
|---|---|
| Hunter | Find the right person's email at a domain, verify an address before sending outreach |
| Brevo, Kit | Read newsletter stats, draft a campaign or broadcast for the user to send |
| Bing Webmaster Tools | Bing queries, pages and traffic; Bing's index also feeds several AI search engines |
| Cloudflare | Purge a page from the cache after publishing an update, read traffic per zone |
| UptimeRobot | Check monitors and downtime before blaming a traffic drop on SEO |
| dev.to | Syndicate an article as a draft, with the canonical URL set to the original |
| Pexels | Free, licensed photos for articles and posts |
| Open PageRank | Free authority scores to vet backlink and outreach targets in bulk |
| HeyGen, Seedance, Fish Audio | Avatar videos, short generated clips, voice-overs |
| Cliniko, Halaxy, Nookal, Splose, Zanda | Read a clinic's profile (practitioners, services, locations) from its practice management system |

Tools for these are named after the integration (`hunter_find_email`, `cloudflare_purge_urls`), so `find_integration_tools(integration: "hunter")` finds them.

## Habits that keep users safe

- Read before you write. List the campaign, the post or the record before changing it, and quote what you are about to change.
- One approval covers one change. A yes to pausing one campaign is not a yes to pausing three.
- Public actions (posts, review replies, DMs, emails) are shown word for word before sending.
- Never report something as done without the result that proves it: a live URL, a status, an id.
- When a tool says a connection expired, send the user the connect link again instead of retrying.
