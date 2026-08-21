---
description: Free .gov backlinks - drive the user's browser through SAM.gov, the SBA small business listing, and state vendor portals to earn real government-directory links, handing off at every account, tax, and certification step
argument-hint: (optional: sam | state | international | verify)
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

Load the Distribb skill and `references/gov-backlinks-playbook.md`, then walk the user's business into the free government registries that give a public .gov profile linking to their site. `$ARGUMENTS` may name a stage (`sam`, `state`, `international`, `verify`); with no argument, start at SAM.gov.

1. **Read the playbook first.** `references/gov-backlinks-playbook.md` carries the exact SAM.gov wizard answers, the DBA documentation trap, the custom-radio clicking notes, and the hard handoff rules. Do not improvise the click-path.

2. **Collect the business facts** before opening a browser: legal name as registered, physical address, US or foreign entity, website URL, start year, fiscal year end, what they sell. If Distribb is connected, `GET /api/v1/business-context` fills most of this.

3. **Confirm the user has a browser tool connected** (Claude in Chrome, Playwright MCP, or computer use). If not, hand them the playbook as manual instructions instead. It reads fine as a human checklist.

4. **Drive the registration** per the playbook, announcing each handoff before it arrives so the user is ready: account creation and sign-in, Terms of Use, the Business Information SUBMIT, the relationship certification, the EIN, every representation and certification, and the final submit. The agent never performs any of those.

5. **Set expectations at the end:** activation takes up to 10 business days, the public SBA profile appears after that, the registration renews every 365 days, and registering is free everywhere (anyone charging is a middleman).

6. **On `verify`** (or when the user returns later): check the SAM public search for the UEI, open the SBA Small Business Search profile, confirm the website URL is displayed, and log the live listing. Offer the same loop for one state portal and, outside the US, the national equivalent.

## Rules
- The handoff list in the playbook is absolute. Never create accounts, agree to terms, enter tax identifiers, tick certifications, or click final submits, even if asked to.
- Never claim an entity record that is not the user's business.
- Leave the DBA blank unless the user holds documentation showing legal name and DBA together.
- The website URL field is the point of the whole exercise. Verify it made it into the registration.
