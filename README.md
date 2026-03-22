# Distribb CLI & OpenClaw Skill

Command-line interface for the [Distribb](https://distribb.io) SEO API. Works with OpenClaw, Claude Code, and any AI agent.

## What is Distribb?

Distribb automates SEO: keyword research, article publishing to your CMS (WordPress, Webflow, Shopify), high-DR backlink exchange, internal linking, and social media repurposing. The Agentic Mode lets you use your own AI to write content while Distribb handles everything else.

## Quick Start

```bash
pip install requests python-dotenv
export DISTRIBB_API_KEY=your_key_here

python3 distribb_cli.py projects:list
python3 distribb_cli.py keywords:search --project-id 42 --keyword "your topic"
python3 distribb_cli.py articles:create --project-id 42 --keyword "your keyword" --content-file article.html --status Planned
```

## OpenClaw Installation

```bash
npx playbooks add skill distribb/distribb-skill --skill distribb
```

## Commands

| Command | Description |
|---------|-------------|
| `projects:list` | List active projects |
| `context:get` | Get business context, competitors, instructions |
| `keywords:search` | Find keywords with volume and difficulty |
| `internal-links:get` | Get published articles for cross-linking |
| `backlinks:targets` | Get backlink exchange URLs from the network |
| `backlinks:status` | Check backlink credits |
| `articles:create` | Submit an article to Distribb |
| `articles:list` | List articles |
| `articles:get` | Get article details |
| `articles:publish` | Publish to CMS |
| `integrations:list` | List connected platforms |

## How the Backlink Exchange Works

Distribb runs a backlink exchange network. When your article includes a link to another network member's site, you earn credits. Credits let your site receive backlinks from other members' articles. The more you give, the more you get.

## Get Your API Key

1. Sign up at [distribb.io/signup?plan=AGENTIC](https://distribb.io/signup?plan=AGENTIC)
2. Go to Settings
3. Copy your API key

## License

MIT
