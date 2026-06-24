#!/usr/bin/env python3
"""
Find fresh news topics for a niche via Google News RSS (no API key needed).

Usage:
  python3 news_topics.py "<query1>" ["<query2>" ...]
  python3 news_topics.py --days 7 "ai search" "google algorithm update"

Flow:
  1. For each query, pull Google News RSS (recent results, US / English).
  2. Parse headlines (title, source, publish date, link).
  3. Dedupe by normalized title and filter to the last N days.
  4. Rank by recency (newest first) and write news_topics_export.csv.

No external dependencies — standard library only (mirrors the other seo-tools
scripts). Writes its CSV next to itself, like the rest of the toolkit.
"""

import csv
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"
DEFAULT_DAYS    = 14          # only keep headlines from the last N days
MAX_PER_QUERY   = 30          # cap headlines pulled per query
HL, GL, CEID    = "en-US", "US", "US:en"   # language / country / edition
OUT_FILE        = Path(__file__).parent / "news_topics_export.csv"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")


# ── HTTP ─────────────────────────────────────────────────────────────────────

def fetch_rss(query: str) -> str:
    params = {"q": query, "hl": HL, "gl": GL, "ceid": CEID}
    url = f"{GOOGLE_NEWS_RSS}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


# ── Parsing ──────────────────────────────────────────────────────────────────

def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def parse_items(xml_text: str, query: str) -> list[dict]:
    items: list[dict] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    for item in root.iter("item"):
        title = html.unescape((item.findtext("title") or "").strip())
        link  = (item.findtext("link") or "").strip()
        pub   = item.findtext("pubDate")

        source_el = item.find("source")
        source = ""
        if source_el is not None and source_el.text:
            source = source_el.text.strip()

        # Google appends " - <Source>" to every headline; strip it when known.
        if source and title.endswith(f" - {source}"):
            title = title[: -len(f" - {source}")].strip()

        try:
            dt = parsedate_to_datetime(pub) if pub else None
            if dt is not None and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            dt = None

        if not title:
            continue
        items.append({
            "title":  title,
            "source": source,
            "dt":     dt,
            "link":   link,
            "query":  query,
        })
        if len(items) >= MAX_PER_QUERY:
            break
    return items


# ── Main ─────────────────────────────────────────────────────────────────────

def parse_args(argv: list[str]) -> tuple[int, list[str]]:
    days = DEFAULT_DAYS
    queries: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--days":
            if i + 1 >= len(argv):
                sys.exit("ERROR: --days needs a number")
            try:
                days = int(argv[i + 1])
            except ValueError:
                sys.exit(f"ERROR: --days must be an integer, got {argv[i + 1]!r}")
            i += 2
        else:
            queries.append(argv[i])
            i += 1
    return days, queries


def main() -> None:
    days, queries = parse_args(sys.argv[1:])
    if not queries:
        sys.exit('Usage: python3 news_topics.py "<query1>" ["<query2>" ...]')

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    print(f"\n📰  News topics — last {days} days")
    print(f"🔎  Queries: {', '.join(queries)}\n")

    collected: list[dict] = []
    failures = 0
    for q in queries:
        print(f"🔍  {q!r} ...")
        try:
            xml_text = fetch_rss(q)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"    ❌  fetch failed: {e}")
            failures += 1
            continue
        items = parse_items(xml_text, q)
        print(f"    → {len(items)} headlines")
        collected.extend(items)

    if not collected:
        if failures:
            sys.exit("ERROR: every query failed to fetch. Check your connection "
                     "or try again — Google News RSS may be rate-limiting.")
        sys.exit("ERROR: no headlines found for those queries.")

    # Dedupe by normalized title (keep the first / most relevant occurrence).
    seen: set[str] = set()
    deduped: list[dict] = []
    for it in collected:
        key = normalize_title(it["title"])
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(it)

    # Recency filter — keep undated items (Google sometimes omits pubDate).
    fresh = [it for it in deduped if it["dt"] is None or it["dt"] >= cutoff]

    # Newest first; undated sink to the bottom.
    fresh.sort(key=lambda it: it["dt"] or datetime.min.replace(tzinfo=timezone.utc),
               reverse=True)

    rows = []
    for it in fresh:
        rows.append({
            "Date":   it["dt"].strftime("%Y-%m-%d") if it["dt"] else "",
            "Title":  it["title"],
            "Source": it["source"],
            "Query":  it["query"],
            "URL":    it["link"],
        })

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Title", "Source", "Query", "URL"])
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "─" * 60)
    print(f"✅  {len(rows)} fresh topics ({len(collected) - len(deduped)} duplicates removed)\n")
    print(f"📁  {OUT_FILE}\n")
    print("Most recent headlines:")
    for r in rows[:15]:
        date = r["Date"] or "  ?  "
        src  = f"  ({r['Source']})" if r["Source"] else ""
        print(f"  [{date}]  {r['Title'][:70]}{src}")


if __name__ == "__main__":
    main()
