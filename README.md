# Distribb SEO Skill

SEO automation for AI agents. Use any AI model you want. Distribb provides the infrastructure: keyword data, original research, backlinks from real businesses, CMS publishing, and analytics.

## Quick Start

```bash
pip install requests beautifulsoup4 openai python-dotenv
export DISTRIBB_API_KEY=your_key_here
export OPENAI_API_KEY=your_openai_key_here
```

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | OpenClaw/Claude Code skill definition with full workflow and guidelines |
| `distribb_cli.py` | CLI wrapping all Distribb API endpoints |
| `distribb_research.py` | Original research agent. Searches the web, scrapes real data, produces data tables and findings. Runs locally with your AI. |
| `distribb_writer.py` | Reference article writer. Generates SEO-optimized articles using Distribb's API for context, links, and backlinks. |

## Commands

```bash
# Projects
python3 distribb_cli.py projects:list
python3 distribb_cli.py context:get --project-id 42

# Keywords
python3 distribb_cli.py keywords:search --project-id 42 --keyword "crm software"

# Original Research (runs locally with your AI)
python3 distribb_research.py --keyword "best crm tools" --style Listicle --output research.html

# Internal Links & Backlinks
python3 distribb_cli.py internal-links:get --project-id 42 --keyword "crm software"
python3 distribb_cli.py backlinks:targets --project-id 42 --keyword "crm software"
python3 distribb_cli.py backlinks:status --project-id 42

# Articles
python3 distribb_cli.py articles:create --project-id 42 --keyword "best crm" --title "Best CRM" --content-file article.html
python3 distribb_cli.py articles:list --project-id 42
python3 distribb_cli.py articles:get --article-id 123
python3 distribb_cli.py articles:publish --article-id 123

# Reference Writer (full pipeline: context + links + AI + submit)
python3 distribb_writer.py --keyword "best crm tools" --project-id 42

# Integrations
python3 distribb_cli.py integrations:list --project-id 42
```

## Backlink Exchange

Distribb connects real businesses that exchange backlinks. When your article includes a link to a network partner, Distribb detects it on submission and credits your project. More backlinks given = more received. These are high-DR backlinks from legitimate business websites.

## OpenClaw Installation

```bash
claw install distribb
```

Or manually clone this repo and point your agent to `SKILL.md`.

## Get an API Key

Sign up at [distribb.io/agentic](https://distribb.io/agentic). 3-day free trial, $29/mo. Your API key is in Settings after signup.
