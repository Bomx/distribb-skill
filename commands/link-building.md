---
description: Link Building - run one of six give-first outreach playbooks (Invoice, Source Sniping, Tombstone, Fact Decay, Stale Screenshot, Missing Visual) end to end, from prospecting to a ready-to-send draft with the asset attached
argument-hint: (optional: invoice | source-sniping | tombstone | fact-decay | screenshots | visuals)
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Load the Distribb skill and `references/link-building-playbooks.md`, then run a link building campaign for the user. `$ARGUMENTS` may name a playbook; with no argument, help them pick.

These are give-first plays: you build something the prospect actually wants and hand it over, and the link follows. None of them are "I loved your article, please link to me".

1. **Pick the playbook.** If `$ARGUMENTS` names one, run it. Otherwise ask what they are trying to solve and use the routing table in the reference. If they have no idea, say so plainly: run **Invoice** first because it is the fastest to a live link with no asset to build, and **Source Sniping** second because it reorders every other campaign.

2. **Load business context first.** `python distribb_cli.py context:get --project-id <id>` for brand voice, competitors, and custom instructions. The competitor list drives Tombstone and Source Sniping directly. If the user has more than one project, ask which before doing anything else.

3. **Run the playbook's steps from the reference.** Do not improvise the mechanic. Each playbook has a specific reason it converts, and the shortcuts break it. In particular: Missing Visual builds the graphic from the prospect's own prose, and Fact Decay verifies every claim against a primary source before it goes on the sheet.

4. **Never invent a fact about a prospect's page.** Four of the six work by telling a publisher something about their own content. The publisher's first move is to check. If you cannot verify a claim, drop it rather than hedge it. One wrong correction ends the relationship.

5. **You do not send the email. The user does.** There is no Distribb endpoint for arbitrary cold outreach. Distribb's managed Link Outreach service is a different product with its own warmed inboxes, and it only handles prospects Distribb generated; the `/link-outreach` command just works the replies. Your output is a finished draft plus the asset, saved to a file. Hand it over and say clearly that nothing has been sent.

6. **Prospecting data comes from outside Distribb.** Distribb's `search-console:get` covers the user's own property only, and `keywords:search` returns keyword ideas, not third-party SERPs. For "pages ranking for X" and referring-domain counts, use `WebSearch` and `WebFetch`, or the user's own SEO tool. The one exception is Source Sniping, where `ai-visibility:get --view competitors` gives you the prospect list directly.

7. **Deliver as a file, not as chat.** Per playbook: the prospect table, the drafted emails, and the assets (correction sheets, re-shot screenshot zips, rendered visuals). The user should be able to open it and start sending. Stale Screenshot additionally needs browser control to re-capture the UI; if no browser tool is available in the session, say so rather than faking the screenshots.

Set expectations before the work starts: these are 10 to 30 send campaigns with real assets attached, not volume plays. If the user wants volume, point them at Distribb's managed Link Outreach service (enabled inside Distribb, not from this command) and the backlink exchange, which are built for it.
