#!/usr/bin/env python3
"""
Distribb SEO Writer (Local Reference Implementation)
=====================================================
This script is a REFERENCE/EXAMPLE for Agentic Mode users. It demonstrates
how to generate SEO-optimized articles locally using your own AI and submit
them to Distribb for publishing, analytics, and calendar display.

You are free to modify this script, swap out components (web search, scraping,
AI provider), or rewrite it entirely. The only requirement is that finished
articles are submitted via the Distribb API.

Install: pip install openai requests python-dotenv

Environment variables:
  DISTRIBB_API_KEY  - Your API key (from Distribb Settings)
  DISTRIBB_API_URL  - API base (default: https://distribb.io)
  OPENAI_API_KEY    - Or any OpenAI-compatible provider key
  AI_BASE_URL       - Custom AI base URL (e.g. https://api.groq.com/openai/v1)
  AI_MODEL          - Model name (default: gpt-4.1-mini)
"""

import os
import re
import json
import time
import logging
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('distribb_writer')

# ── Configuration ──

DISTRIBB_API_KEY = os.getenv('DISTRIBB_API_KEY', '')
DISTRIBB_API_URL = os.getenv('DISTRIBB_API_URL', 'https://distribb.io').rstrip('/')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4.1-mini')
AI_BASE_URL = os.getenv('AI_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Hardcoded test parameters (set these to test without CLI args)
TEST_KEYWORD = "best project management tools for startups"
TEST_PROJECT_ID = None
TEST_ARTICLE_STYLE = "professional"
TEST_LANGUAGE = "en"

# ── AI Client (swap this for your preferred provider) ──

def get_ai_client():
    from openai import OpenAI
    kwargs = {'api_key': OPENAI_API_KEY}
    if AI_BASE_URL:
        kwargs['base_url'] = AI_BASE_URL
    return OpenAI(**kwargs)


def ai_chat(system_prompt: str, user_prompt: str, temperature: float = 0.3,
            max_tokens: int = 4000, json_mode: bool = False) -> str:
    client = get_ai_client()
    kwargs = {
        'model': AI_MODEL,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        'temperature': temperature,
        'max_tokens': max_tokens,
    }
    if json_mode:
        kwargs['response_format'] = {'type': 'json_object'}

    for attempt in range(3):
        try:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI call attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise
    return ""


def parse_json_from_ai(text: str) -> dict:
    if not text:
        return {}
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        match = re.search(r'\[[\s\S]*\]', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    logger.warning(f"Failed to parse JSON from AI: {text[:200]}...")
    return {}


# ══════════════════════════════════════════════════════════════
#  DISTRIBB API CLIENT
#  These functions are the interface to Distribb's server.
#  They handle data that MUST come from Distribb:
#    - Internal links (your published articles for cross-linking)
#    - Backlink targets (network exchange URLs)
#    - Business context (competitors, brand voice, AI instructions)
#    - Article submission (saving content to the Distribb calendar)
# ══════════════════════════════════════════════════════════════

def distribb_api(method: str, path: str, params=None, json_data=None) -> dict:
    url = f"{DISTRIBB_API_URL}{path}"
    headers = {
        'Authorization': f'Bearer {DISTRIBB_API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            resp = requests.post(url, headers=headers, json=json_data, timeout=60)

        if resp.status_code == 401:
            logger.error("Authentication failed. Check your DISTRIBB_API_KEY.")
            return {'error': 'Invalid API key'}
        if resp.status_code >= 400:
            logger.error(f"API error {resp.status_code}: {resp.text[:500]}")
            return {'error': f'HTTP {resp.status_code}', 'detail': resp.text[:500]}

        return resp.json()
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to {DISTRIBB_API_URL}. Check DISTRIBB_API_URL.")
        return {'error': 'Connection failed'}
    except Exception as e:
        logger.error(f"API request failed: {e}")
        return {'error': str(e)}


def get_projects() -> dict:
    """List your active projects."""
    return distribb_api('GET', '/api/v1/projects')


def get_business_context(project_id: int) -> dict:
    """Get business name, competitors, AI instructions, language, target audience."""
    logger.info(f"Fetching business context for project {project_id}...")
    return distribb_api('GET', '/api/v1/business-context', params={'project_id': project_id})


def get_internal_links(project_id: int, keyword: str) -> dict:
    """Get published article URLs for internal cross-linking."""
    logger.info(f"Fetching internal link candidates for '{keyword}'...")
    return distribb_api('GET', '/api/v1/internal-links',
                        params={'project_id': project_id, 'keyword': keyword})


def get_backlink_targets(project_id: int, keyword: str) -> dict:
    """Get backlink exchange URLs from the Distribb network."""
    logger.info(f"Fetching backlink exchange targets for '{keyword}'...")
    return distribb_api('GET', '/api/v1/backlink-targets',
                        params={'project_id': project_id, 'keyword': keyword})


def submit_article(project_id: int, keyword: str, title: str, content: str,
                    meta_description: str, scheduled_date: str = None) -> dict:
    """Submit a finished article to Distribb. This is the CRITICAL call --
    it saves the article to your calendar and makes it available for
    CMS publishing, social repurposing, and analytics."""
    logger.info(f"Submitting article to Distribb: '{title}'...")
    return distribb_api('POST', '/api/v1/articles', json_data={
        'project_id': project_id,
        'keyword': keyword,
        'title': title,
        'content': content,
        'meta_description': meta_description,
        'scheduled_date': scheduled_date,
        'status': 'Planned' if scheduled_date else 'Draft',
    })


def publish_article(article_id: int) -> dict:
    """Trigger CMS publishing for an article (WordPress, Webflow, etc.)."""
    logger.info(f"Publishing article {article_id}...")
    return distribb_api('POST', f'/api/v1/articles/{article_id}/publish')


# ══════════════════════════════════════════════════════════════
#  SEO WRITING PRINCIPLES
#  These are the rules that make Distribb articles rank well.
#  Incorporate these into your writing process however you prefer.
# ══════════════════════════════════════════════════════════════

SEO_WRITING_RULES = """
FORMAT FIRST (most important):
- Decide the format from search intent before writing: Listicle ("best X", "top X",
  "X tools/agencies/alternatives"), Comparison ("X vs Y"), Review, How-to ("how to X"),
  Explainer ("what is X"), or Resources ("X templates/examples/statistics").
- Then follow that format's spine:
  * Listicle:   short intro -> "## 1. [Named option]" ... "## N. [Named option]" -> FAQ
  * Comparison: short intro -> quick context -> one section per option (same criteria) -> verdict -> FAQ
  * How-to:     short intro -> "## Step 1: [Action]" ... -> FAQ
  * Explainer:  short intro (answers the question in 2 sentences) -> definition -> how it works -> pitfalls -> FAQ
- The worst mistake is writing a "best X" listicle as a how-to ("Step 1: define goals").
  Name the actual options. That IS the article.

GO STRAIGHT TO THE POINT:
- Intro is 2-4 sentences, under ~80 words. Hook, one line of stakes, then the payoff.
- In a listicle/comparison, do NOT add a "Why X matters" / "What is X" / "Benefits of X"
  preamble section. Fold a one-line definition into the intro at most, then go straight
  to the named items. Intro -> the list -> FAQ -> done.
- Never start a section with "In today's...", "When it comes to...", "Whether you're X or Y."

WRITE LIKE A HUMAN (humanizer pass -- run on the finished draft):
- Vary sentence length hard. Have an opinion. Use specific, sourced detail.
- Use plain verbs: "is / has", not "serves as / boasts / features / offers".
- CUT: significance inflation ("a testament to", "plays a pivotal role", "stands as"),
  promotional fluff ("vibrant", "robust", "seamless", "boasts", "game-changer"),
  vague attribution ("experts believe", "studies show" with no source),
  "-ing" tails that fake depth ("..., highlighting its value"),
  "not just X, it's Y", forced rule-of-three, "from X to Y" false ranges,
  signposting ("Let's dive in", "Here's what you need to know"),
  filler ("in order to" -> "to", "due to the fact that" -> "because"),
  "**Label:** description" inline-header lists, mechanical bold, emojis, em dashes.
- Never bold the primary keyword. Straight quotes only.

LENGTH -- MATCH THE TOP RESULTS, THEN BUILD ON TOP (not shortness for its own sake):
- Decide length from the TOP 3 ranking pages for the keyword: match their depth, then build
  a little on top (skyscraper). Cap around 3,000 words; never runaway-pad. They rank for a
  reason -- emulate them, then go a bit beyond.
- Reach that length with REAL substance (examples, sourced facts, specifics, depth per
  section), never filler. Don't pad past the depth the topic needs, and DON'T undershoot it
  by writing thin. (If the project's instructions ask for short/punchy, follow them.)

FAQ + CONCLUSION:
- FAQ (4-6 Qs as people type them; 40-80 word answers; direct answer first sentence).
- Short conclusion: one direct recommendation + next action. Do NOT recap with the
  keyword stuffed in ("We've walked through the best X 2026...").

INTERNAL LINKING:
- Place links in the middle of substantive paragraphs, never in intros or conclusions.
- Descriptive anchor text (never "click here", "read more", "our blog"). Never two links
  in the same or consecutive paragraphs. Format: <a href="EXACT_URL_FROM_LIST">anchor</a>

BACKLINK EXCHANGE:
- Weave network backlinks as natural references; include only the ones that genuinely fit.
- Do NOT fabricate information about linked sites; use only what their title/description says.

COMPETITOR PROTECTION:
- Never link to or rank a direct competitor above the client. In a "best X" list you MUST
  name competitors (factually, unlinked) with the client positioned as the top pick.

OUTPUT:
- Valid HTML (not markdown). H2 for sections, H3 for subsections.
- Meta description (155 chars max) with the primary keyword, written for a human to click.
"""


# ══════════════════════════════════════════════════════════════
#  EXAMPLE PIPELINE
#  This is ONE way to generate an article. Feel free to replace
#  the web search, scraping, research, or section writing with
#  your own tools and methods.
# ══════════════════════════════════════════════════════════════

def generate_article(keyword: str, project_id: int, article_style: str = "professional",
                      language: str = "en", scheduled_date: str = None,
                      auto_publish: bool = False) -> dict:
    """Example article generation pipeline. Modify as needed."""
    logger.info(f"{'='*60}")
    logger.info(f"Generating article: '{keyword}' (project {project_id})")
    logger.info(f"{'='*60}")

    if not DISTRIBB_API_KEY:
        logger.error("DISTRIBB_API_KEY not set. Get your key from Distribb Settings.")
        return {'error': 'DISTRIBB_API_KEY not set'}
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set.")
        return {'error': 'OPENAI_API_KEY not set'}

    # ── Step 1: Get server-side data from Distribb ──
    biz = get_business_context(project_id)
    if biz.get('error'):
        return biz
    logger.info(f"Business: {biz.get('business_name', '?')} ({biz.get('website_url', '?')})")

    links_data = get_internal_links(project_id, keyword)
    internal_links = links_data.get('links', [])
    num_internal = links_data.get('num_links_recommended', 5)
    logger.info(f"Internal links: {len(internal_links)} candidates, recommended: {num_internal}")

    bl_data = get_backlink_targets(project_id, keyword)
    backlink_targets = bl_data.get('targets', [])
    logger.info(f"Backlink targets: {len(backlink_targets)}, credits: {bl_data.get('credits', 0)}")

    # ── Step 2: Build the article context for the AI ──
    competitor_list = ', '.join(biz.get('competitors', [])[:5])

    internal_links_text = ""
    if internal_links:
        internal_links_text = "AVAILABLE INTERNAL LINKS (use " + str(num_internal) + " of these):\n"
        internal_links_text += "\n".join(f"  - {l['url']} | {l['title']}" for l in internal_links[:15])

    backlinks_text = ""
    if backlink_targets:
        backlinks_text = "BACKLINK EXCHANGE URLS (include 1-2 naturally):\n"
        backlinks_text += "\n".join(f"  - {t['url']} | {t.get('title', '')}" for t in backlink_targets[:5])

    competitor_text = ""
    if competitor_list:
        competitor_text = f"COMPETITORS (never link to these): {competitor_list}"

    # ── Step 3: Generate the article in one shot (or adapt to multi-section) ──
    prompt = f"""Write a comprehensive, SEO-optimized article about: "{keyword}"

TODAY'S DATE: {datetime.now().strftime('%B %d, %Y')}
STYLE: {article_style}
LANGUAGE: {language}
BUSINESS: {biz.get('business_name', '')} - {biz.get('description', '')[:400]}
TARGET AUDIENCE: {biz.get('target_audience', '')}

{SEO_WRITING_RULES}

{internal_links_text}

{backlinks_text}

{competitor_text}

{biz.get('ai_instructions', '')}

OUTPUT FORMAT (JSON):
{{
  "title": "SEO title with primary keyword",
  "meta_description": "155 chars max, includes keyword",
  "content": "<h2>First Section</h2>... full article HTML ...",
  "word_count": 3000
}}

Pick the format from search intent and follow its spine (see FORMAT FIRST above). Keep
the intro to 2-4 sentences, then go straight to the payoff. Write a thorough, substantive
article (most land in the ~2000-word range; match the depth that ranks) -- reach it with real
substance, never filler, and don't undershoot it by writing thin. After drafting, run the
humanizer pass over the whole article and rewrite every AI tell. Include internal links and
backlinks naturally. Output valid HTML, not markdown."""

    logger.info("Generating article content with AI...")
    raw = ai_chat(
        "You are an expert SEO content writer. Return only the requested JSON.",
        prompt, temperature=0.4, max_tokens=12000, json_mode=True
    )
    result = parse_json_from_ai(raw)

    if not result.get('content'):
        logger.error("AI did not return article content.")
        return {'error': 'Article generation failed'}

    title = result.get('title', keyword.title())
    content = result['content']
    meta_desc = result.get('meta_description', '')
    word_count = len(content.split())

    logger.info(f"Article generated: '{title}' ({word_count} words)")

    # ── Step 4: Submit to Distribb (REQUIRED) ──
    submission = submit_article(
        project_id=project_id, keyword=keyword, title=title,
        content=content, meta_description=meta_desc,
        scheduled_date=scheduled_date
    )

    if submission.get('error'):
        logger.error(f"Submission failed: {submission['error']}")
        return submission

    article_id = submission.get('article_id')
    logger.info(f"Article submitted: ID={article_id}, status={submission.get('status')}")

    # ── Step 5: Auto-publish if requested ──
    if auto_publish and article_id:
        pub_result = publish_article(article_id)
        logger.info(f"Publish result: {pub_result}")
        submission['publish_result'] = pub_result

    logger.info(f"{'='*60}")
    logger.info(f"DONE: '{title}' ({word_count} words) -> article ID {article_id}")
    logger.info(f"{'='*60}")

    return {
        'article_id': article_id,
        'title': title,
        'word_count': word_count,
        'keyword': keyword,
        'status': submission.get('status', 'Draft')
    }


# ── CLI ──

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distribb SEO Writer - Reference Implementation')
    parser.add_argument('--keyword', type=str, default=TEST_KEYWORD, help='Target keyword')
    parser.add_argument('--project-id', type=int, default=TEST_PROJECT_ID, help='Distribb project ID')
    parser.add_argument('--style', type=str, default=TEST_ARTICLE_STYLE,
                        choices=['professional', 'casual', 'technical', 'listicle', 'how-to'],
                        help='Article writing style')
    parser.add_argument('--language', type=str, default=TEST_LANGUAGE, help='Content language')
    parser.add_argument('--schedule', type=str, default=None,
                        help='Schedule date (ISO 8601, e.g. 2026-03-25T09:00:00Z)')
    parser.add_argument('--publish', action='store_true', help='Auto-publish after generation')

    args = parser.parse_args()

    if not args.project_id:
        projects = get_projects()
        if projects.get('projects'):
            print("\nAvailable projects:")
            for p in projects['projects']:
                print(f"  ID: {p['ID']} - {p.get('BusinessName', 'Unnamed')} ({p.get('WebsiteUrl', '')})")
            print(f"\nRun with: --project-id <ID>\n")
        else:
            print("No projects found. Set up a project in Distribb first.")
        exit(1)

    result = generate_article(
        keyword=args.keyword,
        project_id=args.project_id,
        article_style=args.style,
        language=args.language,
        scheduled_date=args.schedule,
        auto_publish=args.publish,
    )

    print(json.dumps(result, indent=2, default=str))
