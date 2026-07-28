# Link Building Playbooks

The methodology behind `/link-building`. Read this when the user asks you to build links, run outreach, get backlinks outside the exchange, or any variant of "how do I get more sites linking to me".

Six playbooks. Each one is a **give-first** play: you build something the prospect wants and hand it over, and the link is the natural consequence rather than the ask. None of them are "hi I loved your article, please link to me".

---

## Read this before you run any of them

**1. You do not send the email. The user does.**

Distribb's Link Outreach service is a separate, managed product: Distribb's own warmed inboxes email listicle authors on the user's behalf. The API surface for it is **replies only**, two endpoints (`GET /link-outreach/prospects`, `POST /link-outreach/prospects/:id/reply`), and they only work on prospects Distribb generated. Replying in-thread is Accelerator-only. Nothing in the API starts a campaign or generates prospects.

**These six playbooks do not run through that system.** There is no Distribb endpoint that sends arbitrary cold email. So your job ends at a finished, ready-to-send draft plus the asset attached to it. Hand the user the file and let them send from their own inbox. Never claim you sent something you did not send.

**1b. Prospecting data mostly comes from outside Distribb.**

Distribb's `search-console:get` covers the user's **own** property only. `keywords:search` returns keyword ideas, not third-party SERPs. There is no referring-domain lookup for arbitrary URLs, and the only Ahrefs surface Distribb has is a bring-your-own key used for keyword research (`POST /keywords/search`), not backlink or DR data.

So when a playbook below says "pages ranking for the user's money keywords" or "referring domains above a floor", get that from `WebSearch` and `WebFetch`, or from the user's own SEO tool. Say which you used. The one exception is Source Sniping, where Distribb hands you the prospect list directly.

**2. Never invent a fact about a prospect's page.**

Four of these six playbooks work by telling a publisher something about their own content: a fact that decayed, a screenshot that aged, a company that died, a diagram that is missing. The entire play collapses if you are wrong even once, because the publisher's first move is to check. If you cannot verify a claim against a primary source, drop it from the list rather than hedging it in the email.

**3. Volume is not the goal here.**

These replace 500 templated emails with 20 that took real work. Twenty sends with a genuine asset attached beats five hundred without. If the user asks you to scale one of these to thousands of prospects, say plainly that the mechanic stops working at that volume, because the thing that makes it convert is that it is obviously bespoke.

**4. Start from business context.**

Every playbook assumes you have loaded the project first:

```bash
python distribb_cli.py context:get --project-id <id>
```

That gives you the brand voice, the competitor list, and custom instructions. The competitor list in particular drives the Tombstone and Source Sniping playbooks directly.

---

## Which playbook to run

| User says | Run |
|---|---|
| "I need links fast", "quickest win", "we have no links yet" | **1. Invoice Method** |
| "who should I be pitching", "build me a target list", "we get no AI mentions" | **2. Source Sniping** |
| "get me into the best-of lists", "my competitors are on every listicle" | **3. Tombstone Method** |
| "I have budget for outreach but nothing to send" | **4. Fact Decay Audit** |
| "I want links from the pages that already rank for my keywords" | **5. Stale Screenshot** |
| "I have content but nobody links to it" | **6. Missing Visual** |

If the user has no idea where to start, run **Invoice** first (fastest to a live link, no asset to build) and **Source Sniping** second (it reorders every other campaign). Say so, and say why.

---

## 1. The Invoice Method

**What it is.** Every tool the user pays for wants testimonials, logos, and case studies, and almost nobody offers. Their billing history is a list of warm prospects with a commercial reason to say yes.

**Why it is first.** No asset to build, no research to verify, existing relationships. This produces links in days rather than weeks. It is the only playbook here that does not need a prospect to be persuaded of anything.

### Steps

1. **Get the vendor list from the user.** You cannot read their Stripe or their card. Ask them to paste or export the recurring vendors: every SaaS subscription, host, agency, and tool they pay for. Ask for the plan tier and roughly how long they have been a customer, because both go in the testimonial and both raise the hit rate.

2. **Find each vendor's customer proof surface.** For each vendor, check for `/customers`, `/testimonials`, `/case-studies`, `/wall-of-love`, `/reviews`. Record the URL and check whether the page is server rendered, since a fair number are JS widgets (Testimonial.to, Senja) that render client side and pass nothing. If the user has their own Ahrefs access, add the page DR; Distribb's saved Ahrefs key covers keyword research only and will not give you this.

3. **Do not count G2, Capterra, or TrustRadius.** Writing a review there gets the user a byline on the vendor's asset, not an outbound link to the user's site. Worth doing for other reasons. Not a link target, and do not pad the list with them.

4. **Draft one testimonial per vendor, each with a real number in it.** Generic praise gets binned by the vendor's marketing team. Specific outcomes get published, because they are what the team is short of. Pull real numbers from the project's Search Console data where relevant:

   ```bash
   python distribb_cli.py search-console:get --project-id <id>
   ```

   Never invent the number. If the user cannot give you a real outcome for a vendor, write the testimonial about a specific workflow instead, not a fabricated result.

5. **Offer three formats.** A written quote. A written quote plus headshot and logo. A 60 second video. Video is the scarcest of the three for most marketing teams, so it may pull best, but treat that as a hypothesis for the user to test rather than a fact to assert.

6. **Address it to marketing, not support.** Support tickets do not reach the person who owns the customers page.

### Deliverable

A table: vendor, proof page URL, page DR where the user can supply it, the drafted testimonial, and the contact. Plus the outreach email, once, as a template with the per-vendor line slotted in.

### The email

> We have been on your Scale plan for 14 months. Happy to write you a testimonial with our actual numbers in it, or record 60 seconds on camera if that is more useful. No ask, but if you list customers with a link that would be nice.

### Honest note for the user

The testimonial has to be genuinely offered whether or not they link. Partly because that is what makes it convert, and partly because a free deliverable conditioned on a link is an exchange rather than a gift, and Google's guidance on links is explicit about goods traded for links. Offer it, then let them decide.

---

## 2. Source Sniping

**What it is.** Stop prospecting by Domain Rating. Prospect by which domains AI engines actually cite when they answer your buyers' questions.

**Why it matters.** DR is a proxy for authority that predates language models. Citation frequency is a thing Distribb measures directly, so you can skip the proxy. Be honest with the user about the size of the effect: at the head, DR and AI citation largely agree, and the most cited domains across engines are the obvious ones. The divergence is in the tail, which is exactly where the user's realistic prospects live, and where nobody else is looking because DR sorting hides them.

**Distribb does the hard part.** `view=competitors` returns `other_cited`: the most cited domains that are neither the user nor a tracked competitor. That is the target list.

### Steps

1. **Load the buyer prompts, and replace the defaults.** Every project seeds about 10 auto prompts that skew brand-y ("is X a good tool"). Those are near useless for this. Write the real buying queries and add them:

   ```bash
   python distribb_cli.py ai-visibility:prompts:add --project-id <id> --prompt "best crm for a 10 person team"
   ```

   Cap is 25 tracked prompts per project, user prompts scanned first. Remove auto prompts to make room:

   ```bash
   python distribb_cli.py ai-visibility:prompts:remove --project-id <id> --prompt "<the auto one>"
   ```

   Bias hard toward buying intent: "best X for <segment>", "X vs Y", "alternatives to X", "is X worth it". Skip informational queries, they cite encyclopedias and teach you nothing about who to pitch.

2. **Scan.**

   ```bash
   python distribb_cli.py ai-visibility:scan --project-id <id>
   ```

   Returns 202 and queues. The **per-project** daily manual scan cap is shared with the dashboard "Scan now" button and the Distribb Agent, so do not burn it on repeat scans. On 429 the response carries `manual_scans_used` and `manual_scans_limit` and resets at midnight UTC. Tell the user rather than retrying.

3. **Pull the cited domains.**

   ```bash
   python distribb_cli.py ai-visibility:get --project-id <id> --view competitors
   python distribb_cli.py ai-visibility:get --project-id <id> --view cited_pages
   ```

   `other_cited` is the prospect list. `rows` is the competitor citation counts, useful context for the pitch. `cited_pages` shows which of the user's own URLs already get cited, which is where new links should point.

4. **Rank and cut the head.** Sort `other_cited` by citation count. Drop Reddit, Wikipedia, YouTube, LinkedIn and the major publishers off the top: the user already knows about them and cannot realistically place there this quarter. What is left in the tail is the list worth working.

5. **Match each target to a playbook.** For each domain in the tail, look at what it publishes. A listicle gets Tombstone. An old tutorial with screenshots gets Stale Screenshot. A stats-heavy explainer gets Fact Decay. A long unillustrated guide gets Missing Visual. This is the step that makes Source Sniping worth running: it is a prospecting layer, not a campaign, and on its own it produces zero links.

6. **Do not script the consumer chat UIs.** If the user asks you to run the prompts by automating ChatGPT or Perplexity in a browser, use the Distribb scan or the paid APIs instead. The chat UIs rate limit, break constantly, and return dirtier data than the scan already gives you.

### Deliverable

The citation-frequency ranking is the deliverable on its own. If the user has their own Ahrefs or similar, add a DR column beside it and show the two orderings together, because the gap is the argument. Distribb does not return DR for third-party domains, so do not fabricate that column or imply the API produced it. Then the tail list with a playbook assigned per domain.

### Worth telling the user

There is decent evidence that unlinked brand mentions move AI visibility too, not just links. If that holds, a mention-only placement on one of these domains is a win rather than a failed outreach, which widens what they can pitch and who will say yes.

---

## 3. The Tombstone Method

**What it is.** Broken link building aimed at dead companies instead of dead URLs.

**Why it works and why nobody runs it.** Broken link tools look for a 404. They miss the richer case: the URL still resolves fine, but the company behind it shut down, got acquired, or sunset the product. The listicle still lists them. The comparison page still compares them. Nothing flags it, so nobody is pitching it. And these are **slots**, not just links: getting into a "best X tools" list is worth more than a mention in a paragraph.

### Steps

1. **Build the death list.** Start from the project's competitor set:

   ```bash
   python distribb_cli.py context:get --project-id <id>
   ```

   Then hunt for shutdowns and acquisitions across that category: sunset and changelog pages, "we are winding down" posts, Crunchbase acquisition records, the Product Hunt graveyard, pricing pages that quietly went to contact-sales, X and LinkedIn announcements. Also count partial deaths: a product that moved upmarket out of the segment the listicle covers is just as stale as one that closed.

2. **Verify the death and keep the receipt.** Screenshot the notice, capture the date, save the URL. The receipt is what makes the email work. Do not pitch a shutdown you cannot evidence.

3. **Find who still lists them.** For each dead product, pull the pages linking to it. Prioritise listicles, "best tools" pages, and comparison posts. Use the user's own backlink tool if they have one; Distribb has no referring-domain lookup for third-party URLs. Otherwise search the dead product's name alongside listicle patterns with `WebSearch`.

4. **Cross reference against Source Sniping.** A dead competitor sitting on a domain that AI engines cite constantly is the highest value target in this whole reference. Work those first.

5. **Draft the edit note per page.** Which entry is stale, what the replacement copy should say, and the closest honest alternative. Write the replacement copy for them, in their page's voice, so the edit is a paste rather than a task.

6. **Be honest about whether the user is the replacement.** If they are not the closest alternative, say who is and let the user take the credit link anyway. That reply is what buys the next three placements on that domain. A publisher who catches you overselling once will not open the next email.

### Deliverable

Per target page: the URL, the dead entry, the receipt, the drafted replacement copy, and the editor contact.

### The email

> Number four on your list shut down in March, here is their notice. Your page is the top result for this so it is sending people to a dead product. Here is replacement copy for that slot if it is useful.

---

## 4. The Fact Decay Audit

**What it is.** Broken link building, but for facts instead of URLs. You audit a page for claims that stopped being true and hand the publisher a dated correction sheet.

**Why it works.** Nobody has ever received this email. It is a genuine gift with a receipt attached, and it puts the user in the position of the person who improved the page rather than the person who wanted something from it. The link arrives because a corrected claim needs a source, and the user brought it.

### Steps

1. **Pick targets that matter.** Pages ranking for the user's money keywords. If Source Sniping has run, pages on the tail domains. Not random high-DR pages.

2. **Extract every checkable claim.** Numbers, dates, prices, named entities, market sizes, "currently", "as of", "the latest". Anything with a truth value that could have moved.

3. **Verify each against a primary source.** The vendor's own pricing page, the original study, the company's own announcement, the regulator's own text. Not a secondary summary, and not another blog. Classify each claim: still true, changed, superseded, could not verify.

4. **Mark unverified as unverified.** Do not guess and do not soften a guess into a hedge. A correction sheet with six solid items and one honest "could not confirm" is credible. One wrong correction makes the user an automated pest and ends the relationship.

5. **Build the sheet.** Claim, current status, source URL, and the suggested replacement sentence. Write the replacement sentence in their voice so it is paste-ready.

6. **Send with no link request in the first email.** This matters. The sheet is the whole message. The link comes from the replacement sentences on the second exchange, or from the publisher adding the source themselves without being asked, which happens more than you would expect.

### Deliverable

One correction sheet per target page, dated, each row sourced. Plus the covering email.

### The email

> Seven things on this page are now out of date. Pricing in the table changed in January, the 2019 study in section two was superseded last year, and one of the five tools shut down. Full list with sources attached. No ask, I just use this page a lot.

### Cost note

This is the playbook where the verification work is real and did not get cheap. Budget human review before sending. Being fast here is worth nothing and being wrong is expensive.

---

## 5. The Stale Screenshot Method

**What it is.** High authority tutorials and reviews carry software screenshots from years ago. The UI has moved on. The author knows the page is stale and will not fix it, because re-capturing 40 UI states is an afternoon of clicking and the page still ranks. You do that afternoon for them.

**Why it is new.** This was not executable before agents got browser control. It is also the single hardest of the six for a competitor to copy.

### Steps

1. **Find candidates.** Pages ranking for the user's money keywords that contain product screenshots. Date the images by UI generation, upload date, or last-modified header.

2. **Score by actual drift.** Skip cosmetic changes. Target pages where navigation, naming, pricing, or a whole screen changed. A screenshot that is merely old is not a reason to email. A screenshot showing a sidebar that no longer exists is.

3. **Re-capture from a real account.** Same crop, same step in the flow, same annotation style as the original. Use browser control. Shoot from an account the user legitimately has on a product they actually pay for. Never mock up or fabricate a UI: the publisher will open the tool eventually, and that is the one failure mode that ends the relationship permanently.

4. **Build the mapping table.** Image 3 becomes this. Image 7 becomes this. Image 11 no longer exists because that screen was removed. The table is what turns a zip of images into ten minutes of work for the publisher instead of an hour.

5. **Deliver the zip and ask for a credit line.** Same rule as the Invoice Method: the zip goes over whether or not they credit. If they do not, you have still put the user in front of a publisher who now owes them a favour.

### Deliverable

A zip of re-shot images, the mapping table, and the email.

### The email

> Your Notion guide is the top result for this and the screenshots are from the 2022 UI, so the sidebar in image two does not exist any more. I re-shot all 14 in the current version at your crop. Zip attached. A credit line is all I would ask.

---

## 6. The Missing Visual Method

**What it is.** Infographic link building, which died because each graphic cost hundreds of dollars, so people made one and blasted five hundred prospects with it. Marginal cost is now cents, so the economics flip: one bespoke graphic per prospect.

**The mechanic that makes it work.** Do not send the user's data. Build the visual **out of the prospect's own article**. Parse their page, find the process, comparison, timeline, or hierarchy they already wrote in prose, and render exactly that. Nothing added, nothing changed. They cannot dispute the facts because they wrote them, and the email stops being a pitch and becomes proofreading.

### Steps

1. **Find image debt.** Pages ranking top 20 for the user's money keywords, with referring domains above a floor, that have zero or one in-body image excluding the hero.

2. **Check the prose is renderable.** Classify what the page structurally contains: a numbered process, a comparison of options, a timeline, a hierarchy, a set of stats. If it is none of those, skip it. Most pages are none of those, and forcing a diagram onto prose that has no shape produces something obviously generated.

3. **Render from code, not from an image model.** SVG or HTML to PNG. Diffusion models still garble dense text and an infographic is mostly text. This also changes what it costs: budget tokens plus a render step, not image generations.

4. **Hard rule: never add a number that is not in their text.** The whole angle rests on the visual being their article. One invented figure and the user is the person who sent a stranger a graphic with a made-up statistic on it.

5. **Produce two versions.** One with a small credit line, one clean. Send the clean one attached and link the credited one.

### Deliverable

Per prospect: the rendered visual in both versions, and the email.

### The email

> You describe a seven step process in section three and there is no diagram. I made you one from your own wording. Attached, no strings. If you use it a credit link is appreciated, and if you would rather have it without the credit, here it is too.

---

## Publishing the on-domain side

Three of these playbooks are stronger when the user has something on their own domain worth linking to. When the outreach target asks "link to what", the answer should not be the homepage.

- **Fact Decay** and **Tombstone** both point naturally at a comparison or alternatives page. Write and publish one through Distribb (`articles:create`, then `articles:publish`) before the campaign, not after.
- **Source Sniping** should point at pages that already get cited. Pull `ai-visibility:get --view cited_pages` and send links at those, since engines have already decided they are quotable.
- If the user has no linkable asset at all, run `/statistics-page-writer` first. A statistics page is the best single target for every playbook here, and `references/statistics-page-playbook.md` covers it.

Standard article flow:

```bash
python distribb_cli.py articles:create --project-id <id> --keyword "<kw>" --title "<title>" --content "<html>" --status Draft
python distribb_cli.py articles:publish --article-id <id>
```

Remember the backlink exchange still applies to anything published this way: linking out to network partners credits the project. See `references/plans-and-backlinks.md`.

---

## What to tell the user about results

Be straight about the shape of it. These are 10 to 30 send campaigns with real assets attached, not volume plays. A good campaign is a handful of placements on pages that matter, not a percentage. If the user wants volume, point them at Distribb's managed Link Outreach service, which is enabled inside Distribb rather than from the API (the `/link-outreach` command only works the replies), and at the backlink exchange. Both are built for volume and neither needs a bespoke asset per prospect.

Set the expectation before the work, not after.
