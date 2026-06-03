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
  python distribb_cli.py articles:update --article-id 123 --unschedule
  python distribb_cli.py articles:delete --article-id 123
  python distribb_cli.py articles:publish --article-id 123
  python distribb_cli.py projects:get --project-id 42
  python distribb_cli.py projects:update --project-id 42 --ai-instructions "Friendly, plain-English tone" --publish-time 09:00 --timezone Europe/Madrid --backlinks-network yes
  python distribb_cli.py keywords:search --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:targets --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:status --project-id 42
  python distribb_cli.py context:get --project-id 42
  python distribb_cli.py internal-links:get --project-id 42 --keyword "crm software"
  python distribb_cli.py integrations:list --project-id 42
  python distribb_cli.py search-console:get --project-id 42 --days 28
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
            r = requests.delete(url, headers=headers, timeout=30)
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
    if args.schedule: data['scheduled_date'] = args.schedule
    if args.style: data['article_style'] = args.style
    if args.status: data['status'] = args.status
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
    if args.keyword is not None: data['keyword'] = args.keyword
    if args.style is not None: data['article_style'] = args.style
    if args.status is not None: data['status'] = args.status
    if args.unschedule:
        data['scheduled_date'] = None  # clears the date; a Planned article drops to Draft
    elif args.schedule is not None:
        data['scheduled_date'] = args.schedule
    if not data:
        print(json.dumps({"error": "Nothing to update. Pass at least one of --title/--content/--keyword/--style/--status/--schedule/--unschedule/--meta-description."}))
        sys.exit(1)
    print(json.dumps(api('PUT', f'/api/v1/articles/{args.article_id}', json_data=data), indent=2))


def cmd_articles_delete(args):
    print(json.dumps(api('DELETE', f'/api/v1/articles/{args.article_id}'), indent=2))


def cmd_projects_get(args):
    print(json.dumps(api('GET', f'/api/v1/projects/{args.project_id}'), indent=2))


def cmd_projects_update(args):
    data = {}
    if args.ai_instructions is not None: data['ai_instructions'] = args.ai_instructions
    if args.business_description is not None: data['business_description'] = args.business_description
    if args.publish_time is not None: data['publish_time'] = args.publish_time
    if args.timezone is not None: data['timezone'] = args.timezone
    if args.backlinks_network is not None:
        data['backlinks_network'] = args.backlinks_network.lower() in ('yes', 'true', '1', 'on', 'enabled')
    if not data:
        print(json.dumps({"error": "Nothing to update. Pass at least one of --ai-instructions/--business-description/--publish-time/--timezone/--backlinks-network."}))
        sys.exit(1)
    print(json.dumps(api('PUT', f'/api/v1/projects/{args.project_id}', json_data=data), indent=2))


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
    p.add_argument('--schedule', type=str, help='ISO 8601 date')
    p.add_argument('--style', type=str, choices=['professional', 'casual', 'technical', 'listicle', 'how-to'])
    p.add_argument('--status', type=str, choices=['Draft', 'Planned'])
    p.set_defaults(func=cmd_articles_create)

    p = sub.add_parser('articles:get', help='Get article details')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_get)

    p = sub.add_parser('articles:publish', help='Publish an article to CMS')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_publish)

    p = sub.add_parser('articles:update', help='Update an article (title, content, keyword, style, status, schedule)')
    p.add_argument('--article-id', type=int, required=True)
    p.add_argument('--title', type=str)
    p.add_argument('--content', type=str)
    p.add_argument('--content-file', type=str, help='Path to HTML file with article content')
    p.add_argument('--meta-description', type=str)
    p.add_argument('--keyword', type=str, help='Change the main keyword (also regenerates the slug)')
    p.add_argument('--style', type=str, choices=['professional', 'casual', 'technical', 'listicle', 'how-to'])
    p.add_argument('--status', type=str, choices=['Draft', 'Planned'])
    p.add_argument('--schedule', type=str, help='ISO 8601 date to (re)schedule')
    p.add_argument('--unschedule', action='store_true', help='Clear the scheduled date (Planned -> Draft)')
    p.set_defaults(func=cmd_articles_update)

    p = sub.add_parser('articles:delete', help='Delete a Draft or Planned article')
    p.add_argument('--article-id', type=int, required=True)
    p.set_defaults(func=cmd_articles_delete)

    p = sub.add_parser('projects:get', help="Get a single project's settings")
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=cmd_projects_get)

    p = sub.add_parser('projects:update', help='Update project settings (instructions, description, publish time, timezone, backlink network)')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--ai-instructions', type=str, help='Customize Article Instructions text')
    p.add_argument('--business-description', type=str)
    p.add_argument('--publish-time', type=str, help='24-hour HH:MM, e.g. 09:00')
    p.add_argument('--timezone', type=str, help='IANA name, e.g. Europe/Madrid')
    p.add_argument('--backlinks-network', type=str, choices=['yes', 'no', 'true', 'false', 'on', 'off'], help='Join/leave the backlink exchange network')
    p.set_defaults(func=cmd_projects_update)

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
