# Distribb 90-Day SEO Sprint, sub-skill

This is a sub-skill of [`Bomx/distribb-skill`](https://github.com/Bomx/distribb-skill). It's the opinionated way to use Distribb for the first 90 days of a new (or low-DA) project.

## What you get

- A founder-built tracker spreadsheet with **7 tabs**: Cover, Dashboard, Task Tracker (31 pre-filled tasks), Keywords (30 rows), Backlinks (15 starter directories), Content Calendar (18 suggested entries), Day 90 Audit.
- A **13-week execution plan** broken into 4 phases: Pre-launch -> Foundation -> Content Engine -> Authority.
- An [AI agent SKILL.md](./SKILL.md) that opens the tracker in the user's browser, walks them through each phase, and wires every step to the parent Distribb skill (keyword research, internal links, backlink targets, article submission, publishing, Microworkers).

## How users get the tracker

The agent opens [the master Google Sheet](https://docs.google.com/spreadsheets/d/1mBiXCNMymK0OTlptdO9QMa4IQbOHOycSLjt-joCL-wM/edit?usp=sharing) in the user's browser, and the user hits `File -> Make a copy` to get their own editable copy in their Drive. To work offline, they can download that copy as `.xlsx` from Google Sheets and open it in Excel or Numbers.

## When the agent should invoke this sub-skill

Trigger phrases:

- "Where do I start with SEO?"
- "Walk me through a 90-day SEO plan."
- "Give me an SEO roadmap / sprint / tracker."
- "How do I get my first 1,000 organic visitors?"
- "Run the SEO sprint for project [X]."

If the user only wants a single article published or a single keyword researched, stay in the parent Distribb skill, don't invoke this sub-skill.

## Full landing page

The long-form playbook (with the email gate that delivers this tracker) is at **[distribb.io/90-day-seo-sprint](https://distribb.io/90-day-seo-sprint)**.
