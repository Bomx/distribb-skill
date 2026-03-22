#!/usr/bin/env python3
"""
Distribb Original Research Agent (Standalone)
==============================================
Runs original data research locally using YOUR AI and basic web scraping.
No Distribb server dependencies. Produces a research bundle (hook, key findings,
data table) that can be woven into articles before submitting to Distribb.

3-step pipeline:
  1. AI Research Planner  — decides strategy, search queries, extraction instructions
  2. Data Collector       — searches web, scrapes pages, extracts structured data
  3. AI Data Analyst      — finds patterns, produces hook/table/findings

Every data point traces to a real scraped URL. The AI extracts and analyses;
it never generates data.

Install:  pip install openai requests beautifulsoup4 python-dotenv
Setup:    export OPENAI_API_KEY=your_key  (or any OpenAI-compatible provider)

Environment variables:
  OPENAI_API_KEY   - Required. Your AI provider key.
  AI_BASE_URL      - Optional. Custom endpoint (e.g. https://api.groq.com/openai/v1)
  AI_MODEL         - Optional. Model name (default: gpt-4.1-mini)
  RESEARCH_MODEL   - Optional. Separate model for research planning/analysis
"""

import os
import re
import json
import time
import statistics
import logging
import argparse
from datetime import datetime
from urllib.parse import urlparse, quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('distribb_research')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
AI_BASE_URL = os.getenv('AI_BASE_URL')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4.1-mini')
RESEARCH_MODEL = os.getenv('RESEARCH_MODEL') or AI_MODEL

MAX_URLS = int(os.getenv('RESEARCH_MAX_URLS', '12'))
MAX_QUERIES = int(os.getenv('RESEARCH_MAX_QUERIES', '4'))
SCRAPE_TIMEOUT = int(os.getenv('RESEARCH_SCRAPE_TIMEOUT', '90'))
PARALLEL_WORKERS = int(os.getenv('RESEARCH_PARALLEL_WORKERS', '3'))

TEST_KEYWORD = "best CRM software for small businesses"
TEST_STYLE = "Listicle"
TEST_BUSINESS = "SaaS review website helping small businesses find the right tools"
TEST_AUDIENCE = "Small business owners and startup founders"

SKIP_DOMAINS = frozenset([
    'youtube.com', 'youtu.be', 'twitter.com', 'x.com',
    'facebook.com', 'instagram.com', 'tiktok.com', 'pinterest.com',
    'linkedin.com', 'amazon.com', 'ebay.com',
])

SCRAPE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml',
}


# ── AI Client ──

def _get_ai_client():
    from openai import OpenAI
    kwargs = {'api_key': OPENAI_API_KEY}
    if AI_BASE_URL:
        kwargs['base_url'] = AI_BASE_URL
    return OpenAI(**kwargs)


def _ai_call(prompt, system="", model=None, temperature=0.3, max_tokens=4096, retries=2):
    client = _get_ai_client()
    model = model or RESEARCH_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    for attempt in range(1, retries + 2):
        try:
            resp = client.chat.completions.create(
                model=model, messages=messages,
                temperature=temperature, max_tokens=max_tokens
            )
            text = (resp.choices[0].message.content or "").strip()
            if text:
                return text
            logger.warning(f"AI returned empty on attempt {attempt}")
        except Exception as e:
            logger.warning(f"AI call failed (attempt {attempt}/{retries+1}): {e}")
            if attempt <= retries:
                time.sleep(2 * attempt)
    return ""


def _parse_json(text):
    if not text:
        return {}
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        cleaned = "\n".join(lines[start:end])
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        for pattern in [r'\{[\s\S]*\}', r'\[[\s\S]*\]']:
            m = re.search(pattern, cleaned)
            if m:
                try:
                    return json.loads(m.group())
                except json.JSONDecodeError:
                    pass
    return {}


# ── Web Search (DuckDuckGo HTML, no API key needed) ──

def web_search(query, num_results=6):
    results = []
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        resp = requests.get(url, headers=SCRAPE_HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Search returned {resp.status_code}")
            return results
        soup = BeautifulSoup(resp.text, 'html.parser')
        for r in soup.select('.result__body')[:num_results]:
            title_el = r.select_one('.result__a')
            snippet_el = r.select_one('.result__snippet')
            if not title_el:
                continue
            href = title_el.get('href', '')
            if 'uddg=' in href:
                from urllib.parse import parse_qs
                parsed = parse_qs(urlparse(href).query)
                href = parsed.get('uddg', [href])[0]
            results.append({
                'title': title_el.get_text(strip=True),
                'link': href,
                'snippet': snippet_el.get_text(strip=True) if snippet_el else '',
            })
    except Exception as e:
        logger.warning(f"Web search error: {e}")
    return results


# ── Web Scraping ──

def scrape_page(url, max_chars=30000):
    try:
        resp = requests.get(url, headers=SCRAPE_HEADERS, timeout=15, verify=False)
        if resp.status_code != 200:
            return {'error': f'HTTP {resp.status_code}', 'content': ''}
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        title = soup.title.string.strip() if soup.title and soup.title.string else ''
        text = soup.get_text(separator='\n', strip=True)
        return {'title': title, 'content': text[:max_chars]}
    except Exception as e:
        return {'error': str(e), 'content': ''}


# ── Step 1: Research Planner ──

PLANNER_SYSTEM = """You are an elite research strategist. Plan an original data study that produces
a compelling data table for a blog article using ONLY publicly available web data.

Choose strategy: product_comparison | statistics_compilation | community_analysis |
multi_source_aggregation | checklist_extraction

Generate 4 search queries targeting DATA-DENSE pages (comparison charts, pricing tables,
complete lists). Return ONLY valid JSON:
{
  "strategy": "...",
  "research_angle": "We compared X across Y...",
  "search_queries": ["query1", "query2", "query3", "query4"],
  "data_points_to_extract": ["name", "metric1", "metric2", "metric3"],
  "table_columns": ["Name", "Metric 1", "Metric 2", "Metric 3"],
  "minimum_items": 8,
  "extraction_instructions": "Very specific instructions for what to pull from each page"
}"""


def plan_research(keyword, article_style, business_description, target_audience, language="en"):
    logger.info(f"[STEP 1] Planning research for: \"{keyword}\"")
    prompt = f"""Plan an original research study for a blog article.

Topic/Keyword: "{keyword}"
Article Style: {article_style}
Business: {business_description}
Audience: {target_audience}
Language: {language}
Date: {datetime.now().strftime("%B %d, %Y")}

Think step by step:
1. What strategy fits this topic type?
2. What search queries will find pages with DENSE, STRUCTURED data?
3. What specific data points can be extracted per item?
4. What would make the reader say "I had no idea"?

Return your research plan as JSON."""

    raw = _ai_call(prompt, system=PLANNER_SYSTEM, temperature=0.35)
    plan = _parse_json(raw)

    if not plan or 'strategy' not in plan:
        logger.warning("[STEP 1] Planner returned invalid JSON. Using fallback.")
        plan = {
            "strategy": "multi_source_aggregation",
            "research_angle": f"We reviewed multiple sources about {keyword}",
            "search_queries": [
                f"{keyword} statistics data 2025 2026",
                f"{keyword} comparison guide",
                f"{keyword} expert recommendations",
            ],
            "data_points_to_extract": ["name", "key_detail", "source", "category"],
            "table_columns": ["Name", "Detail", "Category", "Source"],
            "minimum_items": 6,
            "extraction_instructions": f"Extract specific facts and data about {keyword} from the page."
        }

    logger.info(f"[STEP 1] Strategy: {plan.get('strategy')}, Queries: {len(plan.get('search_queries', []))}")
    return plan


# ── Step 2: Data Collection ──

def _extract_data_from_page(text, source_url, extraction_instructions, data_points, keyword, title=""):
    if not text or len(text) < 100:
        return []
    prompt = f"""Extract structured data from this page about "{keyword}".

PAGE TITLE: {title}
SOURCE: {source_url}

WHAT TO EXTRACT: {extraction_instructions}
USE THESE EXACT JSON KEYS: {json.dumps(data_points)}

RULES:
1. Extract EVERY relevant item on the page.
2. Only include data EXPLICITLY on the page. Use null for missing fields.
3. Add "_source_quote" with a 10-20 word verbatim phrase proving the item exists.
4. Return a JSON array. Empty [] if nothing relevant.

PAGE CONTENT:
{text[:25000]}

JSON array only."""

    raw = _ai_call(prompt, temperature=0.05, max_tokens=6000)
    items = _parse_json(raw)
    if isinstance(items, dict):
        items = [items] if items else []
    elif not isinstance(items, list):
        items = []
    for item in items:
        if isinstance(item, dict):
            item['_source_url'] = source_url
    kept = [i for i in items if isinstance(i, dict) and
            sum(1 for k, v in i.items() if not k.startswith('_') and v is not None and v != "") >= 2]
    logger.info(f"[extract] {len(kept)} items from {source_url[:60]}")
    return kept


def _scrape_and_extract(url, extraction_instructions, data_points, keyword):
    try:
        result = scrape_page(url)
        if result.get('error') or not result.get('content'):
            return url, []
        items = _extract_data_from_page(
            result['content'], url, extraction_instructions,
            data_points, keyword, result.get('title', '')
        )
        return url, items
    except Exception as e:
        logger.warning(f"[collect] Error for {url[:60]}: {e}")
        return url, []


def collect_data(plan, keyword):
    logger.info(f"[STEP 2] Collecting data (strategy: {plan.get('strategy')})")
    queries = plan.get('search_queries', [])[:MAX_QUERIES]
    extraction_instructions = plan.get('extraction_instructions', '')
    data_points = plan.get('data_points_to_extract', [])

    candidate_urls = []
    seen_urls = set()

    for qi, query in enumerate(queries, 1):
        logger.info(f"[collect] Search {qi}/{len(queries)}: \"{query}\"")
        results = web_search(query, num_results=6)
        for r in results:
            url = r.get('link', '')
            if not url or url in seen_urls:
                continue
            try:
                domain = urlparse(url).netloc.lower()
                if any(sd in domain for sd in SKIP_DOMAINS):
                    continue
            except Exception:
                pass
            seen_urls.add(url)
            candidate_urls.append(url)
            if len(candidate_urls) >= MAX_URLS:
                break

    logger.info(f"[collect] Scraping {len(candidate_urls)} URLs (workers={PARALLEL_WORKERS})")
    all_items = []
    start = time.time()

    for batch_start in range(0, len(candidate_urls), PARALLEL_WORKERS):
        if time.time() - start > SCRAPE_TIMEOUT:
            logger.warning(f"[collect] Timeout ({SCRAPE_TIMEOUT}s). Stopping.")
            break
        batch = candidate_urls[batch_start:batch_start + PARALLEL_WORKERS]
        with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
            futures = {executor.submit(_scrape_and_extract, url, extraction_instructions, data_points, keyword): url
                       for url in batch}
            for future in as_completed(futures):
                try:
                    _, items = future.result()
                    all_items.extend(items)
                except Exception as e:
                    logger.warning(f"[collect] Future error: {e}")

    logger.info(f"[STEP 2] Collected {len(all_items)} items from {len(candidate_urls)} pages")
    return all_items


# ── Step 3: Data Analyst ──

ANALYST_SYSTEM = """You are a senior data analyst. You receive raw data extracted from real web pages
and produce original research findings. You ALWAYS deliver, even with small datasets.

RULES:
- ONLY use data present in the raw input. Never invent data.
- Use the pre-computed metrics provided (averages, medians, ranges).
- Each finding MUST include a specific number or percentage.
- Build an HTML table: <table class="research-table"> with <thead>, <tbody>.
- Use <strong> to highlight notable values. Use em-dash for missing values.
- Last column = source domain (short name, not full URL).
- 3-4 key findings, ordered most surprising to most actionable.

Return ONLY valid JSON:
{
  "hook": "We [verb] X items across Y sources and found [insight]...",
  "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
  "narrative_threads": ["Angle 1", "Angle 2"],
  "table_html": "<table class='research-table'>...</table>",
  "methodology": "What was searched, pages scraped, date",
  "quality_score": 7,
  "quality_reasoning": "Brief explanation"
}"""


def _deduplicate(items, data_points):
    if not data_points:
        return items
    name_field = data_points[0]
    seen = {}
    unique = []
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_name = str(item.get(name_field, '')).strip().lower()
        canonical = re.sub(r'[^a-z0-9 ]', ' ', raw_name).strip()
        canonical = ' '.join(canonical.split())
        if not canonical or canonical in ('none', 'null'):
            unique.append(item)
            continue
        clean = canonical.replace(' ', '')
        match_key = None
        for existing in seen:
            if existing == canonical or existing.replace(' ', '') == clean:
                match_key = existing
                break
            if canonical in existing or existing in canonical:
                if len(min(canonical, existing, key=len)) >= 3:
                    match_key = existing
                    break
        if match_key:
            idx = seen[match_key]
            merged = dict(unique[idx])
            for k, v in item.items():
                if v is not None and v != "" and (merged.get(k) is None or merged.get(k) == ""):
                    merged[k] = v
            unique[idx] = merged
        else:
            seen[canonical] = len(unique)
            unique.append(item)
    if len(items) != len(unique):
        logger.info(f"[dedup] {len(items)} -> {len(unique)} items")
    return unique


def _compute_metrics(items, data_points):
    metrics = {}
    total = len(items)
    if not total:
        return metrics
    for dp in data_points:
        values = []
        categories = {}
        raw_count = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            v = item.get(dp)
            if v is None or v == '' or v == 'null':
                continue
            raw_count += 1
            num = None
            if isinstance(v, (int, float)):
                num = float(v)
            elif isinstance(v, str):
                cleaned = re.sub(r'[$,€£]', '', v.strip())
                cleaned = re.sub(r'\s*(per|/).*', '', cleaned, flags=re.IGNORECASE)
                cleaned = re.sub(r'^(from|starting at|~)\s*', '', cleaned, flags=re.IGNORECASE)
                m = re.search(r'[\d.]+', cleaned)
                if m:
                    try:
                        num = float(m.group())
                    except ValueError:
                        pass
            if num is not None:
                values.append(num)
            else:
                cat = str(v).strip()[:60]
                categories[cat] = categories.get(cat, 0) + 1
        info = {"fill_rate": f"{raw_count}/{total} ({round(100*raw_count/total)}%)"}
        if values:
            info["type"] = "numeric"
            info["count"] = len(values)
            info["average"] = round(statistics.mean(values), 2)
            info["median"] = round(statistics.median(values), 2)
            info["min"] = round(min(values), 2)
            info["max"] = round(max(values), 2)
        elif categories:
            info["type"] = "categorical"
            info["unique_values"] = len(categories)
            top = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
            info["top_values"] = {k: v for k, v in top}
        metrics[dp] = info
    return metrics


def analyze_data(plan, raw_items, keyword, language="en"):
    logger.info(f"[STEP 3] Analyzing {len(raw_items)} items")
    if not raw_items:
        return {"quality_score": 0, "quality_reasoning": "No data collected"}

    data_points = plan.get('data_points_to_extract', [])
    unique = _deduplicate(raw_items, data_points)

    source_urls = set()
    for item in unique:
        if isinstance(item, dict) and item.get('_source_url'):
            source_urls.add(item['_source_url'])

    metrics = _compute_metrics(unique, data_points)

    cleaned = []
    for item in unique[:35]:
        c = {}
        for k, v in item.items():
            if k == '_source_quote':
                continue
            if k == '_source_url':
                try:
                    c['_source'] = urlparse(v).netloc.replace('www.', '')
                except Exception:
                    c['_source'] = v
                continue
            if v is not None:
                c[k] = v
        cleaned.append(c)

    prompt = f"""Analyze this research data for a blog article about "{keyword}".

STRATEGY: {plan.get('strategy')}
ANGLE: {plan.get('research_angle')}
COLUMNS: {json.dumps(plan.get('table_columns', []))}
LANGUAGE: {language}
DATE: {datetime.now().strftime("%B %d, %Y")}
ITEMS: {len(unique)} | SOURCES: {len(source_urls)}

PRE-COMPUTED METRICS (use these exact numbers):
{json.dumps(metrics, indent=2, default=str)}

DATA:
{json.dumps(cleaned, indent=2, default=str)[:25000]}

Produce hook, findings, table, methodology. Return JSON only."""

    raw = _ai_call(prompt, system=ANALYST_SYSTEM, temperature=0.25, max_tokens=8000)
    result = _parse_json(raw)

    if not result or 'hook' not in result:
        return {"quality_score": 0, "quality_reasoning": "Analyst failed"}

    result['_raw_item_count'] = len(unique)
    result['_source_count'] = len(source_urls)
    result['_source_urls'] = list(source_urls)

    logger.info(f"[STEP 3] Quality: {result.get('quality_score', 0)}/10")
    logger.info(f"[STEP 3] Hook: {result.get('hook', '')[:120]}")
    return result


# ── Main Pipeline ──

def run_research(keyword, article_style="Informative", business_description="",
                 target_audience="", language="en"):
    start = time.time()
    logger.info(f"\n{'#'*60}")
    logger.info(f"# RESEARCH PIPELINE: {keyword}")
    logger.info(f"{'#'*60}")

    plan = plan_research(keyword, article_style, business_description, target_audience, language)
    raw_items = collect_data(plan, keyword)

    if not raw_items:
        logger.warning("No data collected. Try different keywords or check your internet connection.")
        return {"status": "Failed", "keyword": keyword, "error": "No data collected"}

    analysis = analyze_data(plan, raw_items, keyword, language)

    elapsed = time.time() - start
    logger.info(f"\n{'#'*60}")
    logger.info(f"# DONE in {int(elapsed)}s | Quality: {analysis.get('quality_score', 0)}/10")
    logger.info(f"{'#'*60}")

    return {
        "status": "Completed",
        "keyword": keyword,
        "strategy": plan.get('strategy'),
        "hook": analysis.get('hook', ''),
        "key_findings": analysis.get('key_findings', []),
        "narrative_threads": analysis.get('narrative_threads', []),
        "table_html": analysis.get('table_html', ''),
        "methodology": analysis.get('methodology', ''),
        "quality_score": analysis.get('quality_score', 0),
        "source_urls": analysis.get('_source_urls', []),
        "raw_item_count": analysis.get('_raw_item_count', 0),
    }


def save_research_html(result, output_path="research_output.html"):
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Research: {result.get('keyword', '')}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
.research-table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
.research-table th, .research-table td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
.research-table th {{ background: #f5f5f5; font-weight: 600; }}
.research-table tr:nth-child(even) {{ background: #fafafa; }}
h2 {{ color: #333; border-bottom: 2px solid #4f46e5; padding-bottom: 8px; }}
.finding {{ background: #f0f4ff; padding: 12px 16px; margin: 8px 0; border-left: 3px solid #4f46e5; }}
.hook {{ font-size: 1.1em; font-weight: 500; color: #1a1a2e; margin: 20px 0; }}
</style></head><body>
<h1>Research: {result.get('keyword', '')}</h1>
<p class="hook">{result.get('hook', '')}</p>
<h2>Key Findings</h2>
{''.join(f'<div class="finding">{f}</div>' for f in result.get('key_findings', []))}
<h2>Data Table</h2>
{result.get('table_html', '<p>No table generated.</p>')}
<h2>Methodology</h2>
<p>{result.get('methodology', '')}</p>
<p><small>Quality: {result.get('quality_score', 0)}/10 | Items: {result.get('raw_item_count', 0)} | Sources: {len(result.get('source_urls', []))}</small></p>
</body></html>"""
    with open(output_path, 'w') as f:
        f.write(html)
    logger.info(f"Research saved to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distribb Original Research Agent')
    parser.add_argument('--keyword', default=TEST_KEYWORD)
    parser.add_argument('--style', default=TEST_STYLE)
    parser.add_argument('--business', default=TEST_BUSINESS)
    parser.add_argument('--audience', default=TEST_AUDIENCE)
    parser.add_argument('--language', default='en')
    parser.add_argument('--output', default='research_output.html')
    args = parser.parse_args()

    if not OPENAI_API_KEY:
        print("Set OPENAI_API_KEY (or any OpenAI-compatible provider key).")
        exit(1)

    result = run_research(
        keyword=args.keyword, article_style=args.style,
        business_description=args.business, target_audience=args.audience,
        language=args.language,
    )

    print(json.dumps(result, indent=2, default=str))

    if result.get('status') == 'Completed':
        save_research_html(result, args.output)
