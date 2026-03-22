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
  python distribb_cli.py articles:publish --article-id 123
  python distribb_cli.py keywords:search --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:targets --project-id 42 --keyword "crm software"
  python distribb_cli.py backlinks:status --project-id 42
  python distribb_cli.py context:get --project-id 42
  python distribb_cli.py internal-links:get --project-id 42 --keyword "crm software"
  python distribb_cli.py integrations:list --project-id 42
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

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
