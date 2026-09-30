# Publish reels and configure comment-triggered DMs

Use Distribb's API or MCP tools for the full flow: select the account, upload the media, publish the caption and configure delivery. A browser is only needed if the user must connect a social account through OAuth. Follow the user's existing authorization: a request to write a caption and publish it authorizes those actions. Do not ask for the same permission again.

## MCP: ChatGPT, Claude Code and other clients

Connect to `https://distribb.io/mcp`. ChatGPT and Claude use the same tool definitions and API routes.

1. `list_projects` finds the project.
2. `list_social_accounts` returns its connected accounts. Match the requested `username` or `account_name` and retain its `account_id`. A project may have several Instagram accounts.
3. `upload_social_media` hosts an existing image or video. Pass `project_id` and `media_url`, or an attached `file` with `download_url`. Its `media` object goes into the next call's `media_files` array. MP4/MOV videos have a 64 MB limit; images have a 12 MB limit.
4. `publish_social_post` takes `project_id`, the final caption in `content`, `platforms: [{"platform":"instagram","account_id":"..."}]`, and `media_files: [{"type":"video","s3_url":"..."}]`. For auto-DMs, also set `is_comment_for_guide: true` and the config below. Omit `scheduled_for` to publish now, or pass a future ISO8601 UTC datetime.
5. Save the returned `posts[].post_id`. Call `get_social_post` and check both publishing status and `comment_for_guide.automation.status`. Report active only when the rule has passed readback verification.
6. If setup is pending, failed or unverified, call `configure_social_post_auto_reply` with that existing `post_id`. Omitting the config retries the saved settings. Passing a replacement config updates the rule. Setting `is_comment_for_guide: false` disables it. Verify the result with `get_social_post`.

Do not publish the reel again to retry DM setup. If a publish response is lost, call `list_social_posts` to find the saved post before trying again. A successful upload or publish alone does not confirm that the DM rule is active. No test comment or test DM is sent by these configuration tools.

If a client cached an older tool list, refresh the connector's tools. Until the new tools appear, use the REST API below with the user's Distribb API key. The browser composer is unnecessary for these settings.

## Comment-for-guide configuration

```json
{
  "match_mode": "keyword",
  "trigger_keyword": "PARASITE",
  "delivery_method": "dm",
  "delivery_url": "https://example.com/your-plugin-or-guide",
  "custom_message": "Here's the ChatGPT SEO plugin that automates this: {url}",
  "is_active": true
}
```

Use the same keyword in the spoken CTA, caption and rule. Use the delivery link the user supplied. The server replaces `{url}` with `delivery_url`; keep the placeholder in `custom_message`. Matching is case-insensitive containment. `match_mode: "all"` matches every comment and clears any saved keywords.

Private DM delivery is supported for Instagram in this API. For supported public-comment platforms, use `delivery_method: "reply"`; TikTok and Pinterest do not support comment-for-guide here. A DM request for another platform is rejected. Use one account per platform in a publish request and an explicit `account_id` for every comment-for-guide post.

Delivery states are `scheduled`, `pending`, `active`, `disabled`, `failed` or `unverified`. Scheduled rules activate after the post publishes. The existing worker retries pending DM setup after publishing; the configure endpoint also supports immediate retries. The rule is attached to the account and numeric media ID of the published reel. Retrying reconciles the existing rule rather than creating another post.

## REST API

Authenticate every request with `Authorization: Bearer $DISTRIBB_API_KEY`. Never print the key or include it in saved request files.

| Method and endpoint | Purpose |
|---|---|
| `GET /api/v1/social/accounts?project_id=42` | Connected accounts, names, usernames and account IDs |
| `POST /api/v1/social/media` | Upload multipart `file` plus `project_id`, or JSON `project_id` and `media_url` / `file.download_url` |
| `POST /api/v1/social/publish` | Publish or schedule caption, media and comment-for-guide settings |
| `GET /api/v1/social/posts?project_id=42&limit=20` | Find recent saved posts, including after an uncertain publish response |
| `GET /api/v1/social/posts/{post_id}` | Read the saved post, publishing results and verified delivery state |
| `PUT /api/v1/social/posts/{post_id}/comment-for-guide` | Configure, retry or disable delivery on an existing post |

Save the full publish request to `publish.json`, then send it with `--data-binary @publish.json`:

```json
{
  "project_id": 42,
  "content": "Your caption. Comment PARASITE for a ChatGPT SEO plugin that automates this.",
  "platforms": [{"platform": "instagram", "account_id": "ACCOUNT_FROM_LIST_SOCIAL_ACCOUNTS"}],
  "media_files": [{"type": "video", "s3_url": "URL_FROM_UPLOAD_SOCIAL_MEDIA"}],
  "is_comment_for_guide": true,
  "comment_for_guide_config": {
    "match_mode": "keyword",
    "trigger_keyword": "PARASITE",
    "delivery_method": "dm",
    "delivery_url": "https://example.com/your-plugin-or-guide",
    "custom_message": "Here's the ChatGPT SEO plugin that automates this: {url}",
    "is_active": true
  }
}
```

`GET /social/accounts` returns `connected: false` when the user needs to connect an account at `https://distribb.io/integrations`. Select the handle before publishing. Every endpoint checks the API user's access to the project, and publishing checks that the account belongs to it.

## CLI

The CLI reads `DISTRIBB_API_KEY` and an optional `DISTRIBB_API_URL`. Keep `social_cli.py` beside `distribb_cli.py`; downloadable packages include both.

```bash
python distribb_cli.py social:accounts --project-id 42
python distribb_cli.py social:upload --project-id 42 --file reel.mp4

# guide.json contains only the configuration object shown above.
python distribb_cli.py social:publish --project-id 42 --platforms instagram \
  --account-id ACCOUNT_ID --content-file caption.txt \
  --media-file reel.mp4 --guide-config-file guide.json

# Use the returned saved post ID for verification and delivery retries.
python distribb_cli.py social:post --post-id POST_ID
python distribb_cli.py social:posts --project-id 42 --limit 20
python distribb_cli.py social:auto-reply --post-id POST_ID
python distribb_cli.py social:auto-reply --post-id POST_ID --guide-config-file updated-guide.json
python distribb_cli.py social:auto-reply --post-id POST_ID --disable
```

The publish command can upload `--media-file` itself. If you already uploaded the file, use `--media-files media.json`, containing an array of the returned media objects. Use either upload path once. `--scheduled-for` schedules; `--overrides-file` supplies per-platform settings; `--content` accepts a caption directly.

## Other platforms and scheduling

Supported publishing platforms: `x` (or `twitter`), `linkedin`, `facebook`, `instagram`, `threads`, `bluesky`, `reddit`, `tiktok`, `youtube`, `pinterest`, `telegram`, `snapchat`, `googlebusiness`.

`platform_overrides` can supply per-platform `text` and network options: X `threadSteps`, LinkedIn `firstComment`, Reddit `subredditName` and `title`. `link` is optional and is appended for preview cards on LinkedIn and Facebook. Public links belong in the caption when appropriate; the DM delivery link belongs in `delivery_url`.

With `scheduled_for`, Distribb stores the post as scheduled and the watchdog publishes within five minutes of that UTC time. The response is HTTP 201 and includes the saved IDs. The user can edit or delete it in the Social Composer until publishing starts. Keep captions within the server's character limits: X 280; Bluesky 300; Threads and Pinterest 500; Google Business 1500; Instagram and TikTok 2200; LinkedIn 3000; YouTube 5000.
