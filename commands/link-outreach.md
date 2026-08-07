---
description: Link Outreach: review the listicle authors who replied to your backlink outreach, and reply to them in-thread from Distribb's inbox (Accelerator)
argument-hint: (optional: replies | reply)
allowed-tools: Bash, Read, Glob, Grep
---

Load the Distribb skill (Link Outreach section) and help the user work their backlink outreach replies. `$ARGUMENTS` may name a focus (`replies`, `reply`); with no argument, run the full loop.

Link Outreach is Distribb's managed service that emails "best of" and "top tools" listicle authors, from Distribb's warmed inboxes, asking to add the user's business to lists that rank their competitors. This command is for AFTER an author replies: reviewing what they said and answering them, in the same thread, without leaving Distribb. Replying in-thread is Accelerator-only; on other plans the user replies from their own inbox.

1. Pull the replies: `python distribb_cli.py link-outreach:replies --project-id <id>` (defaults to `replied` + `offer` prospects; add `--status all` for the full pipeline, or drop `--project-id` to span every project the API key owns). Each row has `prospect_id`, `host`, `author_name`, `status`, the author's `reply`, and any `offer_amount` / `offer_currency` (their asking price for a placement).
2. Summarize for the user: who replied, what they said, and any asking price. Quote the `reply` and `offer_amount` exactly as returned. Never invent a price, terms, or intent the author did not state.
3. **Draft a reply, get explicit approval, then send.** Write a short, specific reply in the user's voice. Most listicle placements are paid; that is the industry norm. Whether to accept, negotiate, or pass is ALWAYS the user's decision, never yours, and Distribb never agrees to or pays for anything on their behalf. Show the exact wording and get a clear go-ahead before sending.
4. Send it: `python distribb_cli.py link-outreach:reply --prospect-id <id> --message "<the approved reply>"`. This sends a REAL email from Distribb's warmed inbox, in the same thread the author replied on, so it stays connected and lands in their inbox. It is not reversible. Never send a reply the user has not seen and approved word for word.

The reply goes out from the Distribb inbox that ran the original outreach, on purpose: it keeps the thread intact and preserves deliverability. If the user would rather move the conversation to their own inbox, they can just email the author directly instead.
