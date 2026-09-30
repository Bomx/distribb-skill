"""Social publishing commands shared by Distribb skill distributions."""
import json
from pathlib import Path

import requests


def register_social_commands(sub, api_key, api_url):
    def call(method, path, *, body=None, params=None, file=None):
        headers = {'Authorization': f'Bearer {api_key}',
                   'User-Agent': 'Mozilla/5.0 (compatible; DistribbCLI/1.1)'}
        kwargs = {'headers': headers, 'timeout': (10, 90), 'params': params}
        if file:
            kwargs.update(files={'file': (Path(file).name, Path(file).read_bytes())}, data=body)
        else:
            kwargs['json'] = body
        try:
            response = requests.request(method, api_url.rstrip('/') + path, **kwargs)
            result = response.json()
        except (requests.RequestException, ValueError):
            raise SystemExit('Request result was not confirmed. Use social:posts to check existing posts before retrying a publish.')
        if not response.ok:
            raise SystemExit(json.dumps(result))
        return result

    def show(value):
        print(json.dumps(value, indent=2))

    def read_json(path):
        return json.loads(Path(path).read_text())

    def accounts(args):
        show(call('GET', '/api/v1/social/accounts', params={'project_id': args.project_id}))

    def upload(args):
        body = {'project_id': args.project_id}
        if args.media_url:
            body['media_url'] = args.media_url
        show(call('POST', '/api/v1/social/media', body=body, file=args.file))

    def publish(args):
        platforms = [p.strip().lower() for p in args.platforms.split(',') if p.strip()]
        if args.account_id:
            if len(platforms) != 1:
                raise SystemExit('--account-id requires exactly one platform. Use separate requests for other accounts.')
            platforms = [{'platform': platforms[0], 'account_id': args.account_id}]
        if args.guide_config_file and not args.account_id:
            raise SystemExit('--guide-config-file requires an explicit --account-id from social:accounts.')
        body = {'project_id': args.project_id, 'platforms': platforms,
                'content': Path(args.content_file).read_text() if args.content_file else args.content}
        if args.link:
            body['link'] = args.link
        if args.scheduled_for:
            body['scheduled_for'] = args.scheduled_for
        if args.overrides_file:
            body['platform_overrides'] = read_json(args.overrides_file)
        if args.media_files:
            body['media_files'] = read_json(args.media_files)
        if args.media_file:
            hosted = call('POST', '/api/v1/social/media', body={'project_id': args.project_id}, file=args.media_file)
            body['media_files'] = [hosted['media']]
        if args.guide_config_file:
            body.update(is_comment_for_guide=True, comment_for_guide_config=read_json(args.guide_config_file))
        show(call('POST', '/api/v1/social/publish', body=body))

    def post(args):
        show(call('GET', f'/api/v1/social/posts/{args.post_id}'))

    def posts(args):
        show(call('GET', '/api/v1/social/posts', params={'project_id': args.project_id, 'limit': args.limit}))

    def configure(args):
        body = {'is_comment_for_guide': not args.disable}
        if args.guide_config_file:
            body['comment_for_guide_config'] = read_json(args.guide_config_file)
        show(call('PUT', f'/api/v1/social/posts/{args.post_id}/comment-for-guide', body=body))

    p = sub.add_parser('social:accounts', help='List social account IDs and handles for a project')
    p.add_argument('--project-id', type=int, required=True)
    p.set_defaults(func=accounts)

    p = sub.add_parser('social:upload', help='Host an image or video for publishing through the API')
    p.add_argument('--project-id', type=int, required=True)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--file', help='Local image or MP4/MOV video')
    source.add_argument('--media-url', help='Public media download URL')
    p.set_defaults(func=upload)

    p = sub.add_parser('social:publish', help='Publish or schedule authorized copy and media, with optional comment-triggered DMs')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--platforms', required=True, help='Comma-separated platforms, e.g. instagram')
    p.add_argument('--account-id', help='Exact account ID returned by social:accounts')
    content = p.add_mutually_exclusive_group(required=True)
    content.add_argument('--content')
    content.add_argument('--content-file', help='UTF-8 caption file')
    p.add_argument('--link')
    p.add_argument('--scheduled-for', help='Future ISO8601 UTC datetime; omit to publish now')
    p.add_argument('--overrides-file', help='JSON object of platform overrides')
    media = p.add_mutually_exclusive_group()
    media.add_argument('--media-files', help='JSON file containing the media_files array')
    media.add_argument('--media-file', help='Local media to upload before publishing')
    p.add_argument('--guide-config-file', help='JSON comment_for_guide_config including keyword, delivery URL and message with {url}')
    p.set_defaults(func=publish)

    p = sub.add_parser('social:post', help='Verify publishing and auto-reply status for an existing post')
    p.add_argument('--post-id', type=int, required=True)
    p.set_defaults(func=post)

    p = sub.add_parser('social:posts', help='Find recent posts before retrying an uncertain publish')
    p.add_argument('--project-id', type=int, required=True)
    p.add_argument('--limit', type=int, default=20)
    p.set_defaults(func=posts)

    p = sub.add_parser('social:auto-reply', help='Configure, retry or disable delivery on an existing post without republishing')
    p.add_argument('--post-id', type=int, required=True)
    p.add_argument('--guide-config-file', help='Replacement configuration; omit to retry saved settings')
    p.add_argument('--disable', action='store_true')
    p.set_defaults(func=configure)
