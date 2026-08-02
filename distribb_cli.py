#!/usr/bin/env python3
"""
Distribb CLI -- Command-line interface for the Distribb SEO API.
Used by OpenClaw, Claude Code, and other AI agents to interact with Distribb.

Install: pip install requests python-dotenv
Setup:   export DISTRIBB_API_KEY=your_key_here

Usage:
  python distribb_cli.py projects:list
  python distribb_cli.py articles:list --project-id 42
  python distribb_cli.py articles:create --project-id 42 --keyword "best crm tools" --title "10 Best CRM Tools" --content "<h2>...</h2>..."
  python distribb_cli.py articles:update --article-id 123 --keyword "best crm software" --style listicle
  python distribb_cli.py articles:update --article-id 123 --category "Accessibility Guides"
  python distribb_cli.py articles:update --article-id 123 --published-at 2024-02-05T09:00:00Z
  python distribb_cli.py articles:update --article-id 123 --unschedule
  python distribb_cli.py articles:delete --article-id 123
  python distribb_cli.py articles:publish --article-id 123
  python distribb_cli.py articles:update --article-id 123 --content-file corrected.html --sync   # edit a LIVE post and push it
  python distribb_cli.py articles:sync --article-id 123                                          # push stored edits to the live post
  python distribb_cli.py admin:articles:list --slug best-crm-tools          # ADMIN: search every project
  python distribb_cli.py admin:articles:update --article-id 90199 --content-file new.html --sync  # ADMIN: write straight to BlogArticles
  python distribb_cli.py projects:get --project-id 42
  python distribb_cli.py projects:update --project-id 42 --ai-instructions "Friendly, plain-English tone" --publish-time 09:00 --timezone Europe/Madrid --backlinks-network yes
  python distribb_cli.py projects:update --project-id 42 --set tone=Conversational --set internal_links_per_article=3 --set 'content_pillars=["https://acme.com/crm","https://acme.com/pricing"]'
  python distribb_cli.py projects:update --project-id 42 --json '{"writing_profile":"Balanced SEO","cta_intensity":"Soft","brand_color":"#1d4ed8"}'
  python distribb_cli.py projects:create --website-url https://client.com --business-name "Client Co" --set tone=Conversational
  python distribb_cli.py projects:onboard --project-id 77   # ASK THE USER FIRST — spends credits
  python distribb_cli.py projects:wordpress --project-id 77 --wordpress-url https://client.com --integration-key "<plugin key>"
  python distribb_cli.py keywords:search --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:targets --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:status --project-id 42
  python distribb_cli.py context:get --project-id 42
  python distribb_cli.py internal-links:get --project-id 42 --keyword "crm software"
  python distribb_cli.py integrations:list --project-id 42
  python distribb_cli.py search-console:get --project-id 42 --days 28
  python distribb_cli.py gbp:status --project-id 42
  python distribb_cli.py gbp:reviews --project-id 42 --unreplied
  python distribb_cli.py gbp:reply --project-id 42 --review-id "accounts/.../reviews/AbFvOq..." --message "Thanks Sarah!"
  python distribb_cli.py gbp:posts:create --project-id 42 --text "Spring checks now booking" --link https://acme.com/offer
  python distribb_cli.py link-outreach:replies --project-id 42
  python distribb_cli.py link-outreach:reply --prospect-id 1159 --message "Thanks Bill. What does the #6-10 slot run per year?"   # ASK THE USER FIRST — sends a real email
  python distribb_cli.py suggestions:list --project-id 42 --status pending
  python distribb_cli.py suggestions:run --project-id 42
  python distribb_cli.py suggestions:get --suggestion-id 123
  python distribb_cli.py suggestions:diff --suggestion-id 123
  python distribb_cli.py suggestions:approve --suggestion-id 123
  python distribb_cli.py suggestions:reject --suggestion-id 123 --reason "Page is being deprecated"
  python distribb_cli.py suggestions:publish --suggestion-id 123
  python distribb_cli.py suggestions:regenerate --suggestion-id 123 --feedback "Keep the pricing table, tighten the intro"
  python distribb_cli.py microworkers:campaigns:list --project-id 42
  python distribb_cli.py microworkers:campaigns:create --project-id 42 --title "Post a Reddit Comment" --description "Follow the task page." --template-file mw_template.html
  python distribb_cli.py microworkers:slots:rate --campaign-id 123 --slot-id 456 --rating OK
"""

import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('DISTRIBB_API_KEY', '')
API_URL = os.getenv('DISTRIBB_API_URL', 'https://distribb.io').rstrip('/')


def api(method, path, params=None, json_data=None):
    url = f"{API_URL}{path}"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        if method == 'GET':
            r = requests.get(url, headers=headers, params=params, timeout=30)
        elif method == 'PUT':
            r = requests.put(url, headers=headers, json=json_data, timeout=60)
        elif method == 'DELETE':
            r = requests.delete(url, headers=headers, json=json_data, timeout=30)
        else:
            r = requests.post(url, headers=headers, json=json_data, timeout=60)
        if r.status_code == 401:
            print(json.dumps({"error": "Invalid API key. Set DISTRIBB_API_KEY."}))
            sys.exit(1)
        return r.json()
    except requests.exceptions.ConnectionError:
        print(json.dumps({"error": f"Cannot connect to {API_URL}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_projects_list(args):
    print(json.dumps(api('GET', '/api/v1/projects'), indent=2))


def cmd_articles_list(args):
    params = {}
    if args.project_id: params['project_id'] = args.project_id
    if args.status: params['status'] = args.status
    if args.limit: params['limit'] = args.limit
    print(json.dumps(api('GET', '/api/v1/articles', params=params), indent=2))


def cmd_articles_create(args):
    data = {
        'project_id': args.project_id,
        'keyword': args.keyword,
    }
    if args.title: data['title'] = args.title
    if args.content: data['content'] = args.content
    if args.content_file:
        with open(args.content_file, 'r') as f:
            data['content'] = f.read()
    if args.meta_description: data['meta_description'] = args.meta_description
    if args.feature_image: data['feature_image'] = args.feature_image
    if args.alt_text: data['alt_text'] = args.alt_text
    if args.schedule: data['scheduled_date'] = args.schedule
    if args.style: data['article_style'] = args.style
    if args.status: data['status'] = args.status
    if args.category is not None: data['category'] = args.category
    if args.published_at is not None: data['published_at'] = args.published_at
    print(json.dumps(api('POST', '/api/v1/articles', json_data=data), indent=2))


def cmd_articles_get(args):
    print(json.dumps(api('GET', f'/api/v1/articles/{args.article_id}'), indent=2))


def cmd_articles_publish(args):
    print(json.dumps(api('POST', f'/api/v1/articles/{args.article_id}/publish'), indent=2))


def cmd_articles_update(args):
    data = {}
    if args.title is not None: data['title'] = args.title
    if args.content is not None: data['content'] = args.content
    if args.content_file:
        with open(args.content_file, 'r') as f:
            data['content'] = f.read()
    if args.meta_description is not None: data['meta_description'] = args.meta_description
    # '' is meaningful here: it clears the hero. Test against None, not truthiness.
    if args.feature_image is not None: data['feature_image'] = args.feature_image
    if args.alt_text is not None: data['alt_text'] = args.alt_text
    if args.keyword is not None: data['keyword'] = args.keyword
    if args.style is not None: data['article_style'] = args.style
    if args.status is not None: data['status'] = args.status
    if args.category is not None: data['category'] = args.category
    if args.published_at is not None: data['published_at'] = args.published_at
    if args.unschedule:
        data['scheduled_date'] = None  # clears the date; a Planned article drops to Draft
    elif args.schedule is not None:
        data['scheduled_date'] = args.schedule
    if args.sync:
        data['sync'] = True  # published articles only: also push the edit to the live CMS post
    if not data:
        print(json.dumps({"error": "Nothing to update. Pass at least one of --title/--content/--keyword/--style/--status/--schedule/--unschedule/--meta-description/--category/--published-at/--feature-image/--alt-text."}))
        sys.exit(1)
    print(json.dumps(api('PUT', f'/api/v1/articles/{args.article_id}', json_data=data), indent=2))


def cmd_articles_sync(args):
    print(json.dumps(api('POST', f'/api/v1/articles/{args.article_id}/sync'), indent=2))


def _admin_article_body(args):
    """Build an admin PUT body from --json, repeated --set key=value, and the
    explicit flags. Later sources win. The literal string 'null' clears a field."""
    data = {}
    if getattr(args, 'json', None):
        try:
            data.update(json.loads(args.json))
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"--json is not valid JSON: {e}"}))
            sys.exit(1)
    for pair in (getattr(args, 'set', None) or []):
        if '=' not in pair:
            print(json.dumps({"error": f"--set expects key=value, got {pair!r}"}))
            sys.exit(1)
        k, v = pair.split('=', 1)
        data[k.strip()] = None if v == 'null' else v
    for flag, key in (('title', 'title'), ('content', 'content'),
                      ('meta_description', 'meta_description'), ('keyword', 'keyword'),
                      ('slug', 'slug'), ('status', 'status'), ('category', 'category'),
                      ('url', 'url'), ('author', 'author'), ('published_at', 'published_at')):
        value = getattr(args, flag, None)
        if value is not None:
            data[key] = None if value == 'null' else value
    if getattr(args, 'content_file', None):
        with open(args.content_file, 'r') as f:
            data['content'] = f.read()
    return data


def cmd_admin_articles_list(args):
    params = {}
    for flag in ('project_id', 'slug', 'status', 'user', 'q', 'limit', 'offset'):
        value = getattr(args, flag, None)
        if value is not None:
            params[flag] = value
    print(json.dumps(api('GET', '/api/v1/admin/articles', params=params), indent=2))


def cmd_admin_articles_get(args):
    print(json.dumps(api('GET', f'/api/v1/admin/articles/{args.article_id}'), indent=2))


def cmd_admin_articles_update(args):
    data = _admin_article_body(args)
    if args.sync:
        data['sync'] = True
    if not data:
        print(json.dumps({"error": "Nothing to update. Pass flags, --set key=value, --json '{...}', or --sync."}))
        sys.exit(1)
    print(json.dumps(api('PUT', f'/api/v1/admin/articles/{args.article_id}', json_data=data), indent=2))


def cmd_admin_articles_sync(args):
    print(json.dumps(api('POST', f'/api/v1/admin/articles/{args.article_id}/sync'), indent=2))


def cmd_articles_delete(args):
    print(json.dumps(api('DELETE', f'/api/v1/articles/{args.article_id}'), indent=2))


def cmd_projects_get(args):
    print(json.dumps(api('GET', f'/api/v1/projects/{args.project_id}'), indent=2))


def _parse_set_pairs(pairs):
    """Parse repeated --set key=value into a dict, JSON-decoding each value when
    possible (so booleans, numbers, and JSON lists work: --set first_person_writing=false,
    --set 'competitors=["https://a.com","https://b.com"]')."""
    out = {}
    for item in (pairs or []):
        if '=' not in item:
            print(json.dumps({"error": f"--set must be key=value, got: {item!r}"}))
            sys.exit(1)
        k, v = item.split('=', 1)
        try:
            out[k.strip()] = json.loads(v)
        except (ValueError, TypeError):
            out[k.strip()] = v
    return out


def _settings_from_args(args):
    """Merge --json-file, then --json, then --set into one settings dict.

    This is the escape hatch that lets the agent send ANY of the ~30 writable
    project fields (the full Settings UI) in one shot, even ones without a
    dedicated flag. GET /api/v1/projects/:id shows every writable key."""
    data = {}
    if getattr(args, 'json_file', None):
        with open(args.json_file, 'r') as f:
            data.update(json.load(f))
    if getattr(args, 'json', None):
        data.update(json.loads(args.json))
    if getattr(args, 'set', None):
        data.update(_parse_set_pairs(args.set))
    return data


def cmd_projects_update(args):
    data = _settings_from_args(args)
    # Explicit flags take precedence over --json/--set for the same key.
    if args.ai_instructions is not None: data['ai_instructions'] = args.ai_instructions
    if args.business_description is not None: data['business_description'] = args.business_description
    if args.publish_time is not None: data['publish_time'] = args.publish_time
    if args.timezone is not None: data['timezone'] = args.timezone
    if args.backlinks_network is not None:
        data['backlinks_network'] = args.backlinks_network.lower() in ('yes', 'true', '1', 'on', 'enabled')
    if not data:
        print(json.dumps({"error": "Nothing to update. Pass explicit flags, --set key=value (repeatable), or --json '{...}'. Run projects:get to see every writable key."}))
        sys.exit(1)
    print(json.dumps(api('PUT', f'/api/v1/projects/{args.project_id}', json_data=data), indent=2))


def cmd_projects_create(args):
    data = _settings_from_args(args)
    data['website_url'] = args.website_url
    if args.business_name is not None: data['business_name'] = args.business_name
    if args.business_description is not None: data['business_description'] = args.business_description
    if args.target_audience: data['target_audience'] = args.target_audience
    print(json.dumps(api('POST', '/api/v1/projects', json_data=data), indent=2))


def cmd_projects_onboard(args):
    """Start keyword research + first articles. ASK THE USER before running — it spends credits."""
    print(json.dumps(api('POST', f'/api/v1/projects/{args.project_id}/onboarding'), indent=2))


def cmd_projects_wordpress(args):
    data = {'wordpress_url': args.wordpress_url, 'integration_key': args.integration_key}
    if getattr(args, 'wp_username', None): data['wp_username'] = args.wp_username
    print(json.dumps(api('POST', f'/api/v1/projects/{args.project_id}/wordpress', json_data=data), indent=2))


def cmd_keywords_search(args):
    data = {'project_id': args.project_id, 'keyword': args.keyword}
    if args.limit: data['limit'] = args.limit
    print(json.dumps(api('POST', '/api/v1/keywords/search', json_data=data), indent=2))


def cmd_backlinks_targets(args):
    params = {'project_id': args.project_id, 'keyword': args.keyword}
    print(json.dumps(api('GET', '/api/v1/backlink-targets', params=params), indent=2))


def cmd_backlinks_status(args):
    params = {'project_id': args.project_id}
    print(json.dumps(api('GET', '/api/v1/backlinks/status', params=params), indent=2))


def cmd_link_outreach_replies(args):
    params = {}
    if getattr(args, 'project_id', None): params['project_id'] = args.project_id
    if getattr(args, 'status', None): params['status'] = args.status
    if getattr(args, 'limit', None): params['limit'] = args.limit
    print(json.dumps(api('GET', '/api/v1/link-outreach/prospects', params=params), indent=2))


def cmd_link_outreach_reply(args):
    body = {'body': args.message}
    print(json.dumps(api('POST', f'/api/v1/link-outreach/prospects/{args.prospect_id}/reply', json_data=body), indent=2))


def cmd_context_get(args):
    params = {'project_id': args.project_id}
    print(json.dumps(api('GET', '/api/v1/business-context', params=params), indent=2))


def cmd_internal_links(args):
    params = {'project_id': args.project_id, 'keyword': args.keyword}
    print(json.dumps(api('GET', '/api/v1/internal-links', params=params), indent=2))


def cmd_integrations_list(args):
    params = {}
    if args.project_id: params['project_id'] = args.project_id
    print(json.dumps(api('GET', '/api/v1/integrations', params=params), indent=2))


def cmd_search_console(args):
    params = {'project_id': args.project_id}
    if args.days: params['days'] = args.days
    if args.limit: params['limit'] = args.limit
    print(json.dumps(api('GET', '/api/v1/search-console', params=params), indent=2))


def cmd_gbp_status(args):
    print(json.dumps(api('GET', '/api/v1/gbp/status', params={'project_id': args.project_id}), indent=2))


def cmd_gbp_reviews(args):
    params = {'project_id': args.project_id}
    if args.unreplied: params['has_reply'] = 'false'
    elif args.has_reply is not None: params['has_reply'] = args.has_reply
    if args.min_rating: params['min_rating'] = args.min_rating
    if args.max_rating: params['max_rating'] = args.max_rating
    if args.limit: params['limit'] = args.limit
    if args.cursor: params['cursor'] = args.cursor
    print(json.dumps(api('GET', '/api/v1/gbp/reviews', params=params), indent=2))


def cmd_gbp_reply(args):
    body = {'project_id': args.project_id, 'review_id': args.review_id, 'message': args.message}
    print(json.dumps(api('POST', '/api/v1/gbp/reviews/reply', json_data=body), indent=2))


def cmd_gbp_reply_delete(args):
    body = {'project_id': args.project_id, 'review_id': args.review_id}
    print(json.dumps(api('DELETE', '/api/v1/gbp/reviews/reply', json_data=body), indent=2))


def cmd_gbp_post_create(args):
    body = {'project_id': args.project_id, 'text': args.text}
    if args.link: body['link'] = args.link
    if args.image_url: body['image_url'] = args.image_url
    if args.scheduled_date: body['scheduled_date'] = args.scheduled_date
    print(json.dumps(api('POST', '/api/v1/gbp/posts', json_data=body), indent=2))


def cmd_gbp_analytics(args):
    print(json.dumps(api('GET', '/api/v1/gbp/analytics', params={'project_id': args.project_id}), indent=2))


def cmd_suggestions_list(args):
    params = {'project_id': args.project_id}
    if args.status: params['status'] = args.status
    if args.limit: params['limit'] = args.limit
    print(json.dumps(api('GET', '/api/v1/suggestions', params=params), indent=2))


def cmd_suggestions_get(args):
    print(json.dumps(api('GET', f'/api/v1/suggestions/{args.suggestion_id}'), indent=2))


def cmd_suggestions_diff(args):
    print(json.dumps(api('GET', f'/api/v1/suggestions/{args.suggestion_id}/diff'), indent=2))


def cmd_suggestions_run(args):
    print(json.dumps(api('POST', '/api/v1/suggestions/run', json_data={'project_id': args.project_id}), indent=2))


def cmd_suggestions_approve(args):
    print(json.dumps(api('POST', f'/api/v1/suggestions/{args.suggestion_id}/approve'), indent=2))


def cmd_suggestions_reject(args):
    data = {}
    if args.reason: data['reason'] = args.reason
    print(json.dumps(api('POST', f'/api/v1/suggestions/{args.suggestion_id}/reject', json_data=data), indent=2))


def cmd_suggestions_publish(args):
    print(json.dumps(api('POST', f'/api/v1/suggestions/{args.suggestion_id}/publish'), indent=2))


def cmd_suggestions_regenerate(args):
    data = {}
    if args.feedback: data['feedback'] = args.feedback
    print(json.dumps(api('POST', f'/api/v1/suggestions/{args.suggestion_id}/regenerate', json_data=data), indent=2))


def cmd_microworkers_campaigns_list(args):
    params = {}
    if args.project_id: params['project_id'] = args.project_id
    if args.limit: params['limit'] = args.limit
    print(json.dumps(api('GET', '/api/v1/microworkers/campaigns', params=params), indent=2))


def cmd_microworkers_campaigns_get(args):
    print(json.dumps(api('GET', f'/api/v1/microworkers/campaigns/{args.campaign_id}'), indent=2))


def cmd_microworkers_campaigns_register(args):
    data = {
        'project_id': args.project_id,
        'campaign_id': args.campaign_id,
    }
    if args.platform: data['platform'] = args.platform
    if args.campaign_type: data['campaign_type'] = args.campaign_type
    if args.title: data['title'] = args.title
    print(json.dumps(api('POST', '/api/v1/microworkers/campaigns/register', json_data=data), indent=2))


def cmd_microworkers_campaigns_create(args):
    if not args.template_file:
        print(json.dumps({"error": "--template-file is required so Microworkers knows what proof fields to collect."}))
        sys.exit(1)
    with open(args.template_file, 'r') as f:
        template_html = f.read()
    data = {
        'project_id': args.project_id,
        'title': args.title,
        'description': args.description,
        'template_html': template_html,
        'available_positions': args.available_positions,
        'payment_per_task': args.payment_per_task,
        'category_id': args.category_id,
        'platform': args.platform,
        'campaign_type': args.campaign_type,
        'minutes_to_finish': args.minutes_to_finish,
        'ttr': args.ttr,
        'speed': args.speed,
    }
    if args.template_title: data['template_title'] = args.template_title
    if args.number_of_file_proofs is not None: data['number_of_file_proofs'] = args.number_of_file_proofs
    if args.allowed_file_types: data['allowed_file_types'] = [item.strip() for item in args.allowed_file_types.split(',') if item.strip()]
    print(json.dumps(api('POST', '/api/v1/microworkers/campaigns', json_data=data), indent=2))


def cmd_microworkers_slots_list(args):
    params = {}
    if args.page: params['page'] = args.page
    if args.page_size: params['pageSize'] = args.page_size
    if args.status: params['status'] = args.status
    print(json.dumps(api('GET', f'/api/v1/microworkers/campaigns/{args.campaign_id}/slots', params=params), indent=2))


def cmd_microworkers_slots_rate(args):
    data = {
        'campaign_id': args.campaign_id,
        'rating': args.rating,
    }
    if args.comment: data['comment'] = args.comment
    print(json.dumps(api('POST', f'/api/v1/microworkers/slots/{args.slot_id}/rate', json_data=data), indent=2))


def main():
    if not API_KEY:
        print(json.dumps({"error": "DISTRIBB_API_KEY not set. Get your key from Distribb Settings."}))
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Distribb SEO CLI', prog='distribb')
    sub = parser.add_subparsers(dest='command', help='Command to run')

    sub.add_parser('projects:list', help='List your active projects').set_defaults(func=cmd_projects_list)

    p = sub.add_parser('articles:list', help='List articles')
    p.add_argument('--project-id', type=int)
    p.add_argument('--status', type=str)
    p.add_argument('--limit', type=int)
    p.set_defaults(func=cmd_articles_list)

    p = sub.add_parser('articles:create', help='Submit an article')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--keyword', type=str, required=True)
    p.add_argument('--title', type=str)
    p.add_argument('--content', type=str)
    p.add_argument('--content-file', type=str, help='Path to HTML file with article content')
    p.add_argument('--meta-description', type=str)
    p.add_argument('--feature-image', type=str, help='Absolute http(s) URL for the hero image')
    p.add_argument('--alt-text', type=str, help='Alt text for the hero image (defaults to the title)')
    p.add_argument('--schedule', type=str, help='ISO 8601 date')
    p.add_argument('--style', type=str, choices=['professional', 'casual', 'technical', 'listicle', 'how-to'])
    p.add_argument('--status', type=str, choices=['Draft', 'Planned'])
    p.add_argument('--category', type=str, help='CMS category NAME to assign (must already exist on the CMS)')
    p.add_argument('--published-at', type=str, help='Past ISO 8601 timestamp to BACKDATE the CMS post (does not move it on the calendar)')
    p.set_defaults(func=cmd_articles_create)

    p = sub.add_parser('articles:get', help='Get article details')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_get)

    p = sub.add_parser('articles:publish', help='Publish an article to CMS')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_publish)

    p = sub.add_parser('articles:update', help='Update an article (title, content, keyword, style, status, schedule, category, published-at, feature image)')
    p.add_argument('--article-id', type=int, required=True)
    p.add_argument('--feature-image', type=str, help="Absolute http(s) URL for the hero image ('' clears it)")
    p.add_argument('--alt-text', type=str, help='Alt text for the hero image')
    p.add_argument('--title', type=str)
    p.add_argument('--content', type=str)
    p.add_argument('--content-file', type=str, help='Path to HTML file with article content')
    p.add_argument('--meta-description', type=str)
    p.add_argument('--keyword', type=str, help='Change the main keyword (also regenerates the slug)')
    p.add_argument('--style', type=str, choices=['professional', 'casual', 'technical', 'listicle', 'how-to'])
    p.add_argument('--status', type=str, choices=['Draft', 'Planned'])
    p.add_argument('--schedule', type=str, help='ISO 8601 date to (re)schedule')
    p.add_argument('--unschedule', action='store_true', help='Clear the scheduled date (Planned -> Draft)')
    p.add_argument('--category', type=str, help='CMS category NAME to assign (must already exist on the CMS); pass "" to clear')
    p.add_argument('--published-at', type=str, help='Past ISO 8601 timestamp to BACKDATE the CMS post (does not move it on the calendar); pass "" to clear')
    p.add_argument('--sync', action='store_true', help='Published articles: also push this edit to the live CMS post')
    p.set_defaults(func=cmd_articles_update)

    p = sub.add_parser('articles:sync', help='Push edits to an ALREADY-PUBLISHED article out to the live CMS post (updates in place)')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_sync)

    # --- Admin only (Distribb staff API keys). Reaches any project. Every write is audit-logged. ---
    p = sub.add_parser('admin:articles:list', help='ADMIN: find articles across ALL projects')
    p.add_argument('--project-id', type=int)
    p.add_argument('--slug', type=str, help='Exact slug match')
    p.add_argument('--status', type=str, choices=['Draft', 'Planned', 'Published'])
    p.add_argument('--user', type=str, help='Owner email')
    p.add_argument('--q', type=str, help='Title or keyword contains')
    p.add_argument('--limit', type=int, help='Default 50, max 200')
    p.add_argument('--offset', type=int)
    p.set_defaults(func=cmd_admin_articles_list)

    p = sub.add_parser('admin:articles:get', help='ADMIN: read any article (full content, URL, ExternalID, owner)')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_admin_articles_get)

    p = sub.add_parser('admin:articles:update', help='ADMIN: write straight to BlogArticles for any project')
    p.add_argument('--article-id', type=int, required=True)
    p.add_argument('--title', type=str)
    p.add_argument('--content', type=str)
    p.add_argument('--content-file', type=str, help='Path to an HTML file to use as the content')
    p.add_argument('--meta-description', type=str)
    p.add_argument('--keyword', type=str)
    p.add_argument('--slug', type=str, help='CAUTION on live posts: the slug is the public URL and the key safe_sync matches on')
    p.add_argument('--status', type=str, choices=['Draft', 'Planned', 'Published'])
    p.add_argument('--category', type=str)
    p.add_argument('--url', type=str, help='CAUTION: repoints the row at a different live URL')
    p.add_argument('--author', type=str)
    p.add_argument('--published-at', type=str, help='ISO 8601, or "null" to clear')
    p.add_argument('--set', action='append', help='Any other field as key=value (repeatable). Use value "null" to clear.')
    p.add_argument('--json', type=str, help='Raw JSON body for full control')
    p.add_argument('--sync', action='store_true', help='Also push the result to the connected CMS')
    p.set_defaults(func=cmd_admin_articles_update)

    p = sub.add_parser('admin:articles:sync', help="ADMIN: push any article's stored state to its CMS")
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_admin_articles_sync)

    p = sub.add_parser('articles:delete', help='Delete a Draft or Planned article')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_delete)

    p = sub.add_parser('projects:get', help="Get a single project's settings")
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_projects_get)

    p = sub.add_parser('projects:update', help='Update project settings — the FULL UI surface (~30 fields). Use --json/--set for any field.')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--ai-instructions', type=str, help='Customize Article Instructions text')
    p.add_argument('--business-description', type=str)
    p.add_argument('--publish-time', type=str, help='24-hour HH:MM, e.g. 09:00')
    p.add_argument('--timezone', type=str, help='IANA name, e.g. Europe/Madrid')
    p.add_argument('--backlinks-network', type=str, choices=['yes', 'no', 'true', 'false', 'on', 'off'], help='Join/leave the backlink exchange network')
    p.add_argument('--set', action='append', metavar='KEY=VALUE',
                   help='Set any writable field (repeatable). Values are JSON-decoded: '
                        '--set tone=Conversational --set internal_links_per_article=3 '
                        "--set 'competitors=[\"https://a.com\"]'")
    p.add_argument('--json', type=str, help='Raw JSON object of settings (the bulk-settings blob)')
    p.add_argument('--json-file', type=str, help='Path to a JSON file of settings')
    p.set_defaults(func=cmd_projects_update)

    p = sub.add_parser('projects:create', help='Create a new project (gated to paid slots) and optionally configure it')
    p.add_argument('--website-url', type=str, required=True, help='Client website, e.g. https://client.com')
    p.add_argument('--business-name', type=str)
    p.add_argument('--business-description', type=str)
    p.add_argument('--target-audience', action='append', metavar='AUDIENCE', help='Repeatable target-audience entry')
    p.add_argument('--set', action='append', metavar='KEY=VALUE', help='Configure any settings field on create (repeatable, JSON-decoded)')
    p.add_argument('--json', type=str, help='Raw JSON object of extra settings to apply on create')
    p.add_argument('--json-file', type=str, help='Path to a JSON file of extra settings')
    p.set_defaults(func=cmd_projects_create)

    p = sub.add_parser('projects:onboard', help='Start keyword research + first articles (ASK THE USER FIRST — spends credits)')
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_projects_onboard)

    p = sub.add_parser('projects:wordpress', help='Connect/reconnect a WordPress site via the Distribb plugin')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--wordpress-url', type=str, required=True, help='WordPress site URL')
    p.add_argument('--integration-key', type=str, required=True, help='Distribb plugin Integration Key')
    p.add_argument('--wp-username', type=str, help='Optional WordPress username')
    p.set_defaults(func=cmd_projects_wordpress)

    p = sub.add_parser('keywords:search', help='Search for keyword ideas')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--keyword', type=str, required=True)
    p.add_argument('--limit', type=int)
    p.set_defaults(func=cmd_keywords_search)

    p = sub.add_parser('backlinks:targets', help='Get backlink exchange targets')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--keyword', type=str, required=True)
    p.set_defaults(func=cmd_backlinks_targets)

    p = sub.add_parser('backlinks:status', help='Get backlink credits and status')
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_backlinks_status)

    p = sub.add_parser('link-outreach:replies', help='List Link Outreach prospects who replied (prospect_id, their message, asking price)')
    p.add_argument('--project-id', type=int, help='Optional: only this project')
    p.add_argument('--status', type=str, help="Comma statuses (default 'replied,offer'; use 'all' for every status)")
    p.add_argument('--limit', type=int, help='Max rows (default 50)')
    p.set_defaults(func=cmd_link_outreach_replies)

    p = sub.add_parser('link-outreach:reply', help='Reply IN-THREAD to a Link Outreach prospect from our inbox (Accelerator only; confirm wording with the user first)')
    p.add_argument('--prospect-id', type=int, required=True, help='prospect_id from link-outreach:replies')
    p.add_argument('--message', type=str, required=True, help='The exact reply text the user approved')
    p.set_defaults(func=cmd_link_outreach_reply)

    p = sub.add_parser('context:get', help='Get business context for a project')
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_context_get)

    p = sub.add_parser('internal-links:get', help='Get internal link candidates')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--keyword', type=str, required=True)
    p.set_defaults(func=cmd_internal_links)

    p = sub.add_parser('integrations:list', help='List CMS and social integrations')
    p.add_argument('--project-id', type=int)
    p.set_defaults(func=cmd_integrations_list)

    p = sub.add_parser('search-console:get', help="Get the project's Google Search Console performance (queries, pages, totals)")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--days', type=int, help='Lookback window in days (default 28, max 90)')
    p.add_argument('--limit', type=int, help='Rows per list (default 25, max 100)')
    p.set_defaults(func=cmd_search_console)

    p = sub.add_parser('gbp:status', help="Google Business Profile connection + live review summary")
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_gbp_status)

    p = sub.add_parser('gbp:reviews', help="List Google reviews live from Google (filter/paginate)")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--unreplied', action='store_true', help='Only reviews without a business reply')
    p.add_argument('--has-reply', type=str, choices=['true', 'false'], help='Filter by reply status')
    p.add_argument('--min-rating', type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument('--max-rating', type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument('--limit', type=int, help='1-50, default 25')
    p.add_argument('--cursor', type=str, help="Previous response's next_cursor")
    p.set_defaults(func=cmd_gbp_reviews)

    p = sub.add_parser('gbp:reply', help="Post the business's PUBLIC reply to a review (confirm wording with the user first)")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--review-id', type=str, required=True, help='review_id from gbp:reviews')
    p.add_argument('--message', type=str, required=True)
    p.set_defaults(func=cmd_gbp_reply)

    p = sub.add_parser('gbp:reply:delete', help="Delete the business's reply on a review")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--review-id', type=str, required=True)
    p.set_defaults(func=cmd_gbp_reply_delete)

    p = sub.add_parser('gbp:posts:create', help="Queue a Google Business post (draft, or scheduled with --scheduled-date)")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--text', type=str, required=True, help='Post text, max 1500 chars')
    p.add_argument('--link', type=str, help="Becomes the post's Learn More button")
    p.add_argument('--image-url', type=str, help='Public http(s) image URL')
    p.add_argument('--scheduled-date', type=str, help="'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM' UTC")
    p.set_defaults(func=cmd_gbp_post_create)

    p = sub.add_parser('gbp:analytics', help="Analytics for Google Business posts published through Distribb")
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_gbp_analytics)

    p = sub.add_parser('suggestions:list', help="List a project's content-optimization suggestions")
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--status', type=str, choices=['pending', 'rewriting', 'ready', 'published', 'rejected', 'failed', 'superseded'])
    p.add_argument('--limit', type=int)
    p.set_defaults(func=cmd_suggestions_list)

    p = sub.add_parser('suggestions:get', help='Get a single suggestion (includes the proposed rewrite once ready)')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.set_defaults(func=cmd_suggestions_get)

    p = sub.add_parser('suggestions:diff', help='Get the before/after rewrite + the GSC trigger snapshot for a suggestion')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.set_defaults(func=cmd_suggestions_diff)

    p = sub.add_parser('suggestions:run', help='Scan a project now (pull GSC + score articles) to generate new pending suggestions')
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_suggestions_run)

    p = sub.add_parser('suggestions:approve', help='Approve a pending suggestion (starts a background rewrite)')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.set_defaults(func=cmd_suggestions_approve)

    p = sub.add_parser('suggestions:reject', help='Reject a suggestion')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.add_argument('--reason', type=str, help='Optional reason for rejecting')
    p.set_defaults(func=cmd_suggestions_reject)

    p = sub.add_parser('suggestions:publish', help='Publish a ready rewrite to the connected CMS')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.set_defaults(func=cmd_suggestions_publish)

    p = sub.add_parser('suggestions:regenerate', help='Re-run a ready rewrite with optional feedback')
    p.add_argument('--suggestion-id', type=int, required=True)
    p.add_argument('--feedback', type=str, help='Steer the rewrite (tone, focus, fixes)')
    p.set_defaults(func=cmd_suggestions_regenerate)

    p = sub.add_parser('microworkers:campaigns:list', help='List registered Microworkers campaigns')
    p.add_argument('--project-id', type=int)
    p.add_argument('--limit', type=int)
    p.set_defaults(func=cmd_microworkers_campaigns_list)

    p = sub.add_parser('microworkers:campaigns:get', help='Get live Microworkers campaign status')
    p.add_argument('--campaign-id', type=str, required=True)
    p.set_defaults(func=cmd_microworkers_campaigns_get)

    p = sub.add_parser('microworkers:campaigns:register', help='Register an existing Microworkers campaign')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--campaign-id', type=str, required=True)
    p.add_argument('--platform', type=str, default='generic')
    p.add_argument('--campaign-type', type=str, default='basic')
    p.add_argument('--title', type=str)
    p.set_defaults(func=cmd_microworkers_campaigns_register)

    p = sub.add_parser('microworkers:campaigns:create', help='Create a Microworkers Basic Campaign')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--title', type=str, required=True)
    p.add_argument('--description', type=str, required=True)
    p.add_argument('--template-file', type=str, required=True, help='HTML template file for worker proof fields')
    p.add_argument('--template-title', type=str)
    p.add_argument('--available-positions', type=int, default=50)
    p.add_argument('--payment-per-task', type=float, default=0.15)
    p.add_argument('--category-id', type=str, default='4004')
    p.add_argument('--platform', type=str, default='generic')
    p.add_argument('--campaign-type', type=str, default='basic')
    p.add_argument('--minutes-to-finish', type=int, default=10)
    p.add_argument('--ttr', type=int, default=3)
    p.add_argument('--speed', type=int, default=300)
    p.add_argument('--number-of-file-proofs', type=int)
    p.add_argument('--allowed-file-types', type=str, help='Comma-separated list, e.g. png,jpeg')
    p.set_defaults(func=cmd_microworkers_campaigns_create)

    p = sub.add_parser('microworkers:slots:list', help='List submissions for a Microworkers campaign')
    p.add_argument('--campaign-id', type=str, required=True)
    p.add_argument('--page', type=int)
    p.add_argument('--page-size', type=int)
    p.add_argument('--status', type=str)
    p.set_defaults(func=cmd_microworkers_slots_list)

    p = sub.add_parser('microworkers:slots:rate', help='Rate a Microworkers slot')
    p.add_argument('--campaign-id', type=str, required=True)
    p.add_argument('--slot-id', type=str, required=True)
    p.add_argument('--rating', type=str, required=True, choices=['OK', 'NOK', 'REVISE'])
    p.add_argument('--comment', type=str)
    p.set_defaults(func=cmd_microworkers_slots_rate)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
