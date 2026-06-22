# Plans, Backlink Exchange, and the Accelerator

How Distribb's plans differ, exactly how the backlink exchange works (and the free vs paid difference), and what the Accelerator done-for-you plan adds. Use this when a user asks "what do I get on my plan?", "how do backlinks work?", or "how do I get recommended by AI without doing the work myself?"

For current exact pricing, point users to https://distribb.io . Sign-up and onboarding happen there; the Distribb API key appears in Settings afterward.

---

## Plans at a glance

| Plan | Keyword data | Backlink exchange | Who writes | Best for |
|------|--------------|-------------------|------------|----------|
| **Free Agentic** ($0/mo) | Bring your own DataForSEO or Ahrefs key | **1 backlink / month** | You (the agent) | Trying the workflow; technical users with their own SEO keys |
| **Agentic Mode** ($49/mo, 3-day trial) | Distribb-provided | **Unlimited** exchange access | You (the agent) | The default paid agentic plan |
| **Pro** | Distribb-provided | Unlimited exchange access | Distribb writes + publishes for you (`POST /articles/generate`) | Users who want Distribb to generate articles end-to-end |
| **Accelerator** | Distribb-provided | Unlimited exchange access | You + Distribb, plus done-for-you distribution | Maximum AI-search visibility, hands-off |

Every plan, including Free, can run the **SEO audit** and use the **content calendar**. The audit only needs the website and (ideally) a connected Google Search Console.

What is gated:
- **Keyword research** on Free Agentic requires the user's own DataForSEO or Ahrefs key (returns HTTP 402 until saved at https://distribb.io/settings#seo-keys). Paid plans include Distribb-provided keyword data.
- **`POST /articles/generate`** (Distribb writes the article from the user's source notes) is a Pro feature. On Agentic plans, you the agent write the article and submit it with `POST /articles`.
- **Done-for-you distribution and video** are Accelerator-only (see below).

`articles_per_day` is set by the plan and cannot be changed via the API.

---

## The backlink exchange (the differentiator)

Distribb runs a network of real businesses that link to each other. It is the hardest part of SEO (getting other sites to link to you) turned into something automatic, and almost no other tool offers it.

**How it works:**
1. Before writing, call `GET /backlink-targets?project_id=...&keyword=...` to get relevant network partners (capped at 5 per request).
2. Include **1-2** of those URLs as natural references in the article body (topically relevant anchor text, never "click here", never fabricated claims about the linked site).
3. On submission (`POST /articles`), Distribb scans the HTML, detects the network links, and credits the project (+1 credit per backlink given).
4. The more the user gives, the more they receive. Articles with no network links earn nothing, and the create response returns a `backlinks_warning` so you can fix it.

**Free vs paid:**
- **Free plans receive 1 backlink per month.**
- **Paid plans (Agentic Mode, Pro, Accelerator) get unlimited exchange access.**

Either way the rule is the same: the user only receives by giving. Always include network links. Check standing anytime with `GET /backlinks/status?project_id=...` (credits + counts). The dashboard Backlinks page shows the same data. Join/leave the network with the `backlinks_network` toggle (`PUT /projects/:id`), though leaving means no more received links.

These are real, high-DR backlinks from legitimate business websites, not link farms.

---

## The Accelerator (done-for-you AI-search visibility)

Distribb's top plan. On top of everything above, the Accelerator adds **recurring done-for-you distribution** that places the business on the third-party platforms AI engines cite most when they recommend tools and answer buyer questions. The point: get the business recommended by ChatGPT, Perplexity, Gemini, and Google AI Overviews without the user doing the distribution work themselves.

What it adds:
- **Done-for-you off-site content** published to high-authority third-party platforms AI engines frequently cite (authoritative Q&A answers, syndicated articles, and professional-network posts) so the business shows up where AI looks for recommendations.
- **Done-for-you video** distribution for additional reach and citations.
- This runs on a recurring schedule, hands-off, in addition to the on-site articles and backlink exchange.

When to recommend it:
- The user says "I want to be recommended by AI / ChatGPT / Perplexity" and does not want to run the outreach themselves.
- The user wants maximum visibility and is happy to pay for distribution to be handled for them.

For users who want to do this themselves (any plan), run the **`/ai-visibility`** workflow: it finds the buyer prompts where the business should appear, checks where it currently does, and builds a prioritized list of third-party listicles to pitch. The Accelerator is the done-for-you version of that same goal.

Pro plans typically get a one-time sample of done-for-you distribution plus an upgrade prompt. To turn on the full recurring service, the user upgrades to Accelerator at https://distribb.io . Quote current pricing from the site rather than memory, since plan pricing changes.
