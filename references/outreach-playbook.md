# Outreach playbook

How to run outreach for a Distribb user: getting links and mentions from other sites, getting the business onto the "best X" lists that rank on Google and feed AI answers, and reaching potential customers who show buying signals. For six step-by-step link building tactics (the Invoice Method, Source Sniping and others) read `link-building-playbooks.md`.

## The four kinds of outreach

| Kind | Goal | Distribb lane |
|---|---|---|
| Backlink exchange | Links from other real businesses, automatically | The exchange: articles carry partner links and earn the project links back. Nothing to send |
| Link outreach to listicles | Get added to "best X" articles that name competitors | Link Outreach: discovery, contacts, drafts, managed sending on Accelerator, reply handling |
| Editorial link building | Earn links with data, fixes and better resources | `research_backlink_opportunities`, the link building playbooks, statistics pages, journalist requests |
| Buying-signal outreach | Reach people asking for what the business sells | Outreach triggers watched by the user's own agent (the High-Intent Outreach skill) |

Start with the exchange (free, automatic), then listicle outreach (the fastest way into AI answers), then editorial links, then buying-signal outreach when the user wants leads directly.

## Link outreach to listicles

"Best X" articles that rank on Google are where buyers and AI assistants look. If a listicle names three competitors and not the user, getting added is worth more than most new links.

1. **See the pipeline:** `get_listicle_outreach` lists opportunities (listicles that rank for the user's terms and name competitors), the author contacts found, the drafted emails, what was contacted and every reply with any asking price.
2. **Find fresh ones:** `run_listicle_outreach_discovery` searches Google and AI answers for listicles mentioning competitors, finds author contacts and drafts emails. It runs in the background for several minutes and is limited to two runs a day per project.
3. **Send:** on Accelerator, `queue_listicle_outreach_send` sends one approved draft (plus two follow-ups) from Distribb's warmed inboxes. Only after the user approves that specific prospect. On other plans, give the user the draft to send from their own inbox.
4. **Handle replies:** `get_listicle_outreach_thread` reads the conversation, `draft_listicle_outreach_reply` drafts the answer, `reply_to_listicle_outreach` sends it in the same thread after the user approves the wording (it needs `confirm: true`).
5. **Record the outcome:** `manage_backlinks` with `prospect_outcome` (won with the live URL, rejected, or skip).

What makes a listicle pitch work:

- Name the article and the exact list. Show you read it.
- Give the author a reason that helps their readers: what the product does that the listed ones do not, a fact they can check, a free account to test it.
- Make it easy: a ready one-paragraph entry in their style, the logo and a screenshot available on request.
- Short: under 120 words, one ask.
- Some authors ask for payment. That is the user's decision. If they pay, the link should be marked sponsored (Google's rules on paid links), and the price should be compared with what the listing is worth.

## Editorial link building

- **Verify before recommending.** `research_backlink_opportunities` returns targets with one primary-source page each and labels whether the site accepts contributions and links, verified or not. Never present web search results, guessed domain ratings or traffic as verified opportunities.
- **Linkable assets earn links on their own.** A statistics page with sourced numbers (see `statistics-page-playbook.md`), original survey data, free tools and calculators, and clear definitions of industry terms get cited by journalists and bloggers.
- **Fixes are the easiest yes.** Broken links on resource pages, outdated statistics, dead tools in a "best of" list: offer the replacement.
- **Journalist requests** (Qwoted, Featured and similar) want a real expert quote fast. Answer within hours, with a specific, quotable insight and credentials.
- **Government and directory profiles** for local and B2B businesses: see `gov-backlinks-playbook.md`.
- **Vet targets** with Open PageRank (`openpagerank_domains`) when it is connected: skip sites nobody links to.

## Cold email that gets replies (and stays out of spam)

Deliverability:

- Send from a separate domain or subdomain set up for outreach, never the main domain the business uses for customers and invoices.
- SPF, DKIM and DMARC set up on that domain. Warm new inboxes for two to four weeks before sending at volume.
- Start under 20 sends a day per inbox and stay under about 50. Plain text, no images, at most one link, no attachments in the first email.
- Verify every address before sending (`hunter_verify_email` when Hunter is connected). Keep bounces under 2%.

Writing:

- First line about them: their article, their product, their recent post. Not about the sender.
- One clear ask. Under 120 words. No fake "Re:" subjects, no fake familiarity.
- Two follow-ups at most, three to four days and then about a week later, each adding something new.
- Always an easy way out: "Not a fit? Just say so and I will not follow up." Honour it everywhere.

Rules:

- Include who is writing and a way to opt out; follow CAN-SPAM in the US and GDPR in the EU and UK (B2B outreach to work addresses on a legitimate interest basis, never bought lists of personal emails).
- Never invent facts, results, customers or prices in an email.
- The user approves the template and every email that goes out in their name, unless they set a standing rule.

## Finding the right contact

- `hunter_find_contacts` lists people at a domain with their role; `hunter_find_email` finds a named person's address; `hunter_verify_email` checks it.
- For an article, the author is usually better than a generic inbox; for a partnership, the person who owns the channel (head of content, partnerships, the founder at a small company).
- LinkedIn is often better than email for founders and marketers: a short connection note, then the ask after they accept.

## Buying-signal outreach

The High-Intent Outreach skill runs on the user's own computer and watches platforms (LinkedIn, X, Reddit, communities and more) for people showing they need what the business sells: asking for recommendations, complaining about a competitor, hiring for the problem.

- `get_outreach_triggers` shows the saved triggers, the search phrases per platform, the customer types and buying moments learned from the website, and the competitors.
- `save_outreach_trigger` adds or changes a trigger. Propose one complete trigger in a single message (name, platform, what to watch, which campaign), save it when the user agrees. The user's agent picks it up on its next run.
- Good triggers are narrow: "asks for an alternative to <competitor>", "posts about missed calls at their clinic", "hiring a part-time bookkeeper". Broad keywords bring noise.
- On social platforms: be useful in public before sending a DM, respect daily caps and cooldowns, never automate in ways the platform forbids, and stop at any sign of disinterest.

## Newsletters and owned email

When Brevo or Kit is connected, read campaign stats (`brevo_list_stats`, `kit_audience_stats`) and draft campaigns or broadcasts (`brevo_create_campaign_draft`, `kit_create_broadcast_draft`) for the user to review and send. Turning each new article into a short newsletter keeps the list warm and sends the first readers to new pages.

## Benchmarks

| Outreach | Healthy reply rate | Healthy win rate |
|---|---|---|
| Listicle inclusion pitches | 5 to 15% | 1 to 5% of pitches become a listing |
| Broken link and resource fixes | 5 to 10% | 2 to 5% |
| Cold B2B sales email | 1 to 5% | Depends on the offer |
| Journalist requests | Varies; speed and specificity decide it | A few percent get quoted |

Low replies usually mean the wrong person, a generic first line or a weak reason to care, rarely the subject line.

## Reporting

Tell the user what was sent, who replied and what they said (asking prices included), what was won with live URLs, and the next three prospects worth contacting. Never count a link as won until the live URL shows it.
