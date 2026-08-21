# Free .gov Backlinks: Browser Automation Playbook (`/gov-backlinks`)

Government registries give any real business a public profile on a .gov domain, with a
website field that links to the business site. They are real supplier directories, not link
farms, and they are free. This playbook teaches the agent to drive the user's browser
through the registrations, and tells it exactly where it must stop and hand the keyboard
to the user.

Works with any browser automation the user has: Claude in Chrome, the built-in browser,
a Playwright MCP, or computer use. The click targets below describe the pages, not pixel
positions, so any of them work.

## The hard handoff rules (read first, non-negotiable)

The agent NEVER does these. The user always does:

- Create accounts or enter passwords (login.gov, SBA, state portals)
- Click Agree on Terms of Use dialogs
- Enter the EIN, TIN, or any tax or bank detail
- Tick any certification checkbox ("I certify that...")
- Click the final SUBMIT of a registration

Everything else (navigation, wizard questions, form fields with business facts the user
provided, reading pages, verifying results) is the agent's job. When a handoff point
arrives, say plainly what the user needs to do and wait. SAM.gov's own terms prohibit
using another person's account, so this split is not just polite, it is required.

## What the user gets

1. A SAM.gov entity registration with a Unique Entity ID.
2. A public profile on SBA's Small Business Search (a .gov page) showing the business
   name and website URL. This is the backlink. It exists only on the full "All Awards"
   registration with the small business self-certification, not on a UEI-only or
   financial-assistance-only registration.
3. Optional stacking: state vendor portals (every US state runs one) and international
   equivalents (Australia: buy.nsw.gov.au and each state's portal; UK and EU: the
   national procurement registry).

## Before starting, collect from the user

- Legal business name exactly as registered (from formation documents or an IRS letter)
- Physical address as registered
- Whether the entity is US or foreign. Foreign entities need an NCAGE code BEFORE
  starting SAM registration (the wizard links the NCAGE Request Tool). US territory
  entities count as US
- Website URL (this is the link, never skip it)
- Business start year and fiscal year end
- What the business sells, for NAICS code suggestions

## The SAM.gov click-path

Registration is free. If any site or email asks for payment to register, it is a
middleman, not the government. Say so to the user.

1. Go to `sam.gov/content/entity-registration`, select Get Started.
2. A Terms of Use dialog appears before sign-in. HANDOFF: the user agrees and signs in
   or creates their login.gov account (email, password, 2FA are all theirs).
3. After sign-in, SAM may show an optional "Request Role" onboarding page. Skip and
   Finish. It is for joining an existing entity, not registering one.
4. Back at entity registration, Get Started, then Create New Entity. The wizard asks:
   - What is your goal? "Directly with the U.S. federal government", then "Bid on a
     federal procurement opportunity as a prime contractor". This is the path that
     produces the SBA listing. The financial assistance path skips representations and
     certifications and does NOT create the public SBA profile. All Awards includes
     grants anyway, so the user loses nothing.
   - Who required your entity to be in SAM.gov? "I decided on my own".
   - Registering a government entity? No, plus "My entity is physically located in the
     United States".
   - Do you already have a CAGE code? No (SAM assigns one during registration).
   - Choose an Option: select All Awards (the wizard recommends it).
5. Entity Search: enter the legal name and registered address, then Search. Three outcomes:
   - SAM finds the entity with the SAME address: confirm "No, do not update".
   - SAM finds it with a DIFFERENT address: STOP and ask the user which address is
     current. Old IRS letters often carry stale addresses. Updating triggers a
     documentation request.
   - SAM finds an entity that is NOT the user's business: stop. Never claim someone
     else's record.
6. Leave Doing Business As BLANK unless the user holds a document showing the legal
   name and DBA together. Filling DBA without that document triggers a validation
   dead-end. The website URL field is where the link lives, so the DBA adds nothing.
7. Enter the Entity URL (the user's website). This is the field the whole playbook
   exists for. Verify it before moving on.
8. Review, then HANDOFF: the user clicks SUBMIT on the Business Information section.
   SAM assigns the Unique Entity ID immediately and emails a confirmation.
9. A UEI is NOT the finish line. Select CONTINUE REGISTRATION. The next page asks the
   user's relationship to the entity and carries an "I certify" checkbox. HANDOFF.
10. Taxpayer Information is next. HANDOFF: the user types the EIN and IRS-registered
    name themselves.
11. The agent can drive Business Types, Goods and Services (propose NAICS codes and let
    the user approve), and Points of Contact from facts the user provided.
12. Representations and Certifications is where the small business self-certification
    lives, the tick that feeds the SBA public search. HANDOFF: every certification and
    the final submit belong to the user.

## Browser automation notes (learned the hard way)

- SAM's radio buttons are custom-rendered. The real input sits off-screen, so clicking
  the visual circle can silently fail. Click the label text, or if the tool supports it,
  trigger the label element directly. After every selection, verify state before Next.
- Cancel does not destroy progress. The wizard remembers answers and completed sections
  on the next run, so a mis-click is recoverable. Re-enter the flow and it fast-forwards.
- The Next button stays disabled until every required control on the page registered.
  If Next looks dead, a selection did not land.
- Page layouts reflow when follow-up questions appear, so never reuse coordinates from
  a previous screenshot after the page changed.

## After submission

- Activation takes up to 10 business days (IRS TIN match plus CAGE assignment). Nothing
  is publicly visible until the registration shows Active. The user gets an email.
- Once Active, verify two pages: the SAM public entity search (search the UEI at
  sam.gov/search) and the SBA Small Business Search profile. Confirm the profile shows
  the website URL. That page is the backlink.
- The registration expires every 365 days. Tell the user to diary the renewal, because
  the listing disappears if it lapses.
- Suggest the user sign into SBA's site afterward to enrich the profile (capabilities
  narrative, keywords). More fields, same .gov page.

## State portals and international

Same handoff rules apply everywhere.

- US states: search "<state> vendor registration". Examples: MyFloridaMarketPlace
  (Florida), Cal eProcure (California). Register as a supplier, fill the profile, put
  the website URL in.
- Australia: each state runs a supplier portal, for example buy.nsw.gov.au.
- Elsewhere: search "<country> government supplier registration".
- Keep name, address, and website identical across every registry. The consistency is
  part of the trust signal.

## Verify the links

- Search `site:sba.gov "<business name>"` and `site:.gov "<business name>"` once active.
- Log every live listing (URL, date, renewal date) wherever the user tracks links.
- Expect Google indexing of a new profile page to lag its going live.
