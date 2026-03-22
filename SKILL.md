---
name: distribb
description: Distribb is an SEO automation tool that handles keyword research, content publishing to WordPress/Webflow/Shopify, high-DR backlink exchange network, internal linking, and social media repurposing. Use this skill when the user wants to create SEO-optimized articles, publish content to their CMS, get backlinks, find keywords, or manage their SEO content calendar.
homepage: https://distribb.io
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["DISTRIBB_API_KEY"]}}}
---

## Install Distribb CLI

```bash
pip install requests python-dotenv
curl -o distribb_cli.py https://raw.githubusercontent.com/distribb/distribb-skill/main/distribb_cli.py
chmod +x distribb_cli.py
```

## Setup

```bash
# Required: Your Distribb API key (get it from Settings in the Distribb dashboard)
export DISTRIBB_API_KEY=your_api_key_here

# Optional: Custom API URL (defaults to https://distribb.io)
export DISTRIBB_API_URL=https://distribb.io
```

---

| Property | Value |
|----------|-------|
| **name** | distribb |
| **description** | SEO automation: keyword research, article publishing, backlink exchange, internal linking |
| **allowed-tools** | Bash(python3 distribb_cli.py:*) |

---

## Core Workflow

The fundamental pattern for using Distribb:

1. **Discover** -- List projects and get business context
2. **Research** -- Find keywords and check backlink targets
3. **Write** -- Generate an SEO article with internal links and backlinks
4. **Submit** -- Send the article to Distribb for calendar display and publishing
5. **Publish** -- Trigger CMS publishing (WordPress, Webflow, Shopify, etc.)

```bash
# 1. Discover
python3 distribb_cli.py projects:list
python3 distribb_cli.py context:get --project-id 42

# 2. Research
python3 distribb_cli.py keywords:search --project-id 42 --keyword "crm software"
python3 distribb_cli.py internal-links:get --project-id 42 --keyword "best crm tools"
python3 distribb_cli.py backlinks:targets --project-id 42 --keyword "best crm tools"

# 3. Write (use your preferred AI to generate HTML content)
# Include internal links and backlink targets in the article

# 4. Submit
python3 distribb_cli.py articles:create \
  --project-id 42 \
  --keyword "best crm tools" \
  --title "10 Best CRM Tools for Small Business in 2026" \
  --content "<h2>Why CRM Matters</h2><p>...</p>" \
  --meta-description "Compare the top CRM tools..." \
  --schedule "2026-04-01T09:00:00Z" \
  --status Planned

# 5. Publish (or wait for scheduled auto-publish)
python3 distribb_cli.py articles:publish --article-id 123
```

---

## Essential Commands

### Projects

```bash
# List all active projects
python3 distribb_cli.py projects:list
# Returns: {"projects": [{"ID": 42, "BusinessName": "Acme", "WebsiteUrl": "https://acme.com", ...}]}
```

### Business Context

```bash
# Get business details, competitors, AI instructions, language
python3 distribb_cli.py context:get --project-id 42
# Returns: {"business_name": "Acme", "competitors": ["competitor1.com"], "ai_instructions": "...", ...}
```

Use this to understand the business before writing. The `competitors` list tells you which sites to NEVER link to. The `ai_instructions` field contains custom writing guidelines from the user.

### Keyword Research

```bash
# Search for keyword ideas with volume and difficulty
python3 distribb_cli.py keywords:search --project-id 42 --keyword "project management"
# Returns: {"suggestions": [{"keyword": "best project management tools", "search_volume": 12000, "difficulty": 35}, ...]}
```

### Internal Links

```bash
# Get published articles to cross-link in new content
python3 distribb_cli.py internal-links:get --project-id 42 --keyword "crm software"
# Returns: {"links": [{"url": "https://acme.com/blog/crm-guide", "title": "CRM Guide", ...}], "num_links_recommended": 5}
```

**IMPORTANT:** Include the recommended number of internal links in your article. Place them naturally in the middle of paragraphs using `<a href="EXACT_URL">descriptive anchor text</a>`. Never use "click here" as anchor text. Space links at least 2 paragraphs apart.

### Backlink Exchange

```bash
# Get backlink targets from the Distribb network
python3 distribb_cli.py backlinks:targets --project-id 42 --keyword "crm software"
# Returns: {"targets": [{"url": "https://partner-site.com/article", "title": "...", ...}], "credits": 87, "instructions": "..."}

# Check backlink credits and status
python3 distribb_cli.py backlinks:status --project-id 42
```

**CRITICAL:** The backlink exchange is how Distribb users get high-DR backlinks. When you include backlink targets in your article as natural references, Distribb detects them on submission and credits your project. Projects that give more backlinks receive more in return. Include 1-2 backlink targets per article.

### Creating Articles

```bash
# Submit a completed article
python3 distribb_cli.py articles:create \
  --project-id 42 \
  --keyword "best crm tools for startups" \
  --title "10 Best CRM Tools for Startups in 2026" \
  --content "<h2>Introduction</h2><p>Finding the right CRM...</p><h2>Top Picks</h2>..." \
  --meta-description "Compare the 10 best CRM tools for startups in 2026. Features, pricing, and expert recommendations." \
  --schedule "2026-04-01T09:00:00Z" \
  --status Planned

# Submit content from a file
python3 distribb_cli.py articles:create \
  --project-id 42 \
  --keyword "best crm tools" \
  --title "10 Best CRM Tools" \
  --content-file article.html \
  --status Draft
```

The response includes `backlinks_processed` (number of network backlinks detected) and may include a `backlinks_warning` if no backlinks were found.

### Managing Articles

```bash
# List articles
python3 distribb_cli.py articles:list --project-id 42
python3 distribb_cli.py articles:list --project-id 42 --status Published

# Get article details
python3 distribb_cli.py articles:get --article-id 123

# Publish to CMS immediately
python3 distribb_cli.py articles:publish --article-id 123
```

Articles with `status: Planned` and a `scheduled_date` are auto-published when the date arrives.

### Integrations

```bash
# List connected CMS and social platforms
python3 distribb_cli.py integrations:list --project-id 42
# Returns: {"integrations": [{"type": "Blog", "platform": "WordPress", "status": "Active"}, ...]}
```

---

## SEO Article Writing Guidelines

When generating content for Distribb, follow these rules for best SEO results:

### Content Quality
- Write like a knowledgeable human, not AI. Vary sentence length.
- Use specific examples, data points, and actionable advice.
- Target 2500-3500 words across 5-8 sections (H2 headings).
- Use H2 for section headings, H3 for subsections.
- Output valid HTML, not markdown.

### Words and Phrases to Avoid
These trigger AI detection: "crucial", "comprehensive", "robust", "leverage", "streamline", "delve", "It's worth noting", "In conclusion", "In the ever-evolving landscape", "Game-changer", "Unlock the power", "Take your X to the next level".

### Opening Lines
Never start sections with "In today's..." or "When it comes to...". Start with a strong statement, question, or data point.

### Internal Linking
- Use the exact URLs from `internal-links:get`.
- Place links in the middle of substantive paragraphs, never in intros or conclusions.
- Use descriptive anchor text (not "click here" or "read more").
- Space links at least 2 paragraphs apart.
- Format: `<a href="https://site.com/exact-url">descriptive anchor text</a>`

### Backlink Exchange
- Include 1-2 URLs from `backlinks:targets` as natural references.
- Do NOT fabricate information about linked sites.
- Use topically relevant anchor text.
- Distribb detects these on submission and credits your project.

### Competitor Protection
- Check competitors from `context:get`.
- Never link to competitor websites.
- You may mention competitors factually but without outbound links.

---

## Complete Example: End-to-End SEO Article

```bash
# Step 1: Get project info
python3 distribb_cli.py projects:list
# Pick project ID 42

# Step 2: Get business context
python3 distribb_cli.py context:get --project-id 42
# Note: competitors are ["hubspot.com", "salesforce.com"]

# Step 3: Find a keyword
python3 distribb_cli.py keywords:search --project-id 42 --keyword "crm software"
# Pick: "best crm for small business" (volume: 8100, difficulty: 42)

# Step 4: Get internal links
python3 distribb_cli.py internal-links:get --project-id 42 --keyword "best crm for small business"
# Got 5 links to include

# Step 5: Get backlink targets
python3 distribb_cli.py backlinks:targets --project-id 42 --keyword "best crm for small business"
# Got 3 targets to weave in

# Step 6: Write the article (using your AI)
# Include internal links and backlink targets in the HTML content
# Follow the SEO writing guidelines above
# Save to article.html

# Step 7: Submit to Distribb
python3 distribb_cli.py articles:create \
  --project-id 42 \
  --keyword "best crm for small business" \
  --title "Best CRM for Small Business: 2026 Guide" \
  --content-file article.html \
  --meta-description "Find the best CRM for your small business. Expert comparison with pricing, features, and recommendations for 2026." \
  --schedule "2026-04-01T09:00:00Z" \
  --status Planned

# Step 8: Article appears in the Distribb content calendar
# It will auto-publish at the scheduled time, or publish immediately:
python3 distribb_cli.py articles:publish --article-id 456
```

---

## Tips

- Always run `context:get` first to understand the business, competitors, and custom instructions before writing.
- The `internal-links:get` response tells you exactly how many links to include (`num_links_recommended`).
- Check `backlinks:status` to see how many credits the project has. More credits = more backlinks received.
- Use `--content-file` for long articles instead of `--content` to avoid shell escaping issues.
- Articles with `status: Planned` and a `scheduled_date` auto-publish. Use `status: Draft` if the user wants to review first.
- All responses are JSON. Parse them to extract IDs, URLs, and data for the next step.
- If `articles:create` returns a `backlinks_warning`, the article had no network backlinks. Consider revising to include some.
