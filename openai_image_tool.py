"""
openai_image_tool.py: make article images with OpenAI's gpt-image-2 and, with
--upload, host them on Distribb in the same step.

For agents that cannot generate images themselves (Claude, for example). The
customer supplies their own OpenAI API key, so the images are made on their
account. Do NOT stand in charts, graphs or SVG drawings for real images: they
look poor in an article. Use this tool, or real screenshots
(POST /api/v1/screenshots) for the websites a listicle ranks.

Setup:
  pip install openai requests
  export OPENAI_API_KEY=sk-...        # the customer's key: platform.openai.com/api-keys
  export DISTRIBB_API_KEY=...         # only needed for --upload

Examples:
  # Feature image, hosted on Distribb, prints the URL to use as feature_image
  python openai_image_tool.py --upload \
    --prompt "Editorial photo of a potter glazing a bowl in a bright studio, natural light, no text"

  # Follow the look of a product photo or brand image
  python openai_image_tool.py --upload --reference-image product.jpg \
    --prompt "The same ceramic bowl on a rustic kitchen table, morning light, no text"

Prompt tips: describe a real scene in the project's image style (get_article_brief
returns it with the owner's image instructions and brand colour). Ask for no text
unless it is a title card, and never put phone numbers, emails or web addresses in
an image.

The last line printed is JSON: {"files": [...], "hosted": [{"url": ..., "width": ..., "height": ...}]}
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = "gpt-image-2"
# Landscape 3:2, what Distribb's own writer uses for article images.
DEFAULT_SIZE = "1536x1024"
DEFAULT_QUALITY = "medium"
DEFAULT_OUTPUT_DIR = "distribb-images"
DISTRIBB_IMAGES_URL = os.getenv("DISTRIBB_API_BASE", "https://distribb.io/api/v1").rstrip("/") + "/images"


def log(message):
    print(f"[openai_image_tool] {message}", file=sys.stderr)


def load_env():
    try:
        from dotenv import load_dotenv
        for candidate in (Path.cwd() / ".env", Path(__file__).resolve().parent / ".env"):
            if candidate.exists():
                load_dotenv(candidate)
    except ImportError:
        pass
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Ask the customer for their OpenAI API key "
                         "(platform.openai.com/api-keys) and export it before running.")


def slugify(value, fallback="image"):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", (value or "").strip().lower()).strip("-")
    return value[:60] or fallback


def image_bytes(item):
    b64 = getattr(item, "b64_json", None) or (item.get("b64_json") if isinstance(item, dict) else None)
    if b64:
        return base64.b64decode(b64)
    url = getattr(item, "url", None) or (item.get("url") if isinstance(item, dict) else None)
    if url:
        import requests
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        return resp.content
    raise ValueError("OpenAI returned no image data.")


def generate(args):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    params = {"model": args.model, "prompt": args.prompt, "n": args.n,
              "size": args.size, "quality": args.quality}
    if args.output_format:
        params["output_format"] = args.output_format
    started = time.time()
    if args.reference_image:
        handles = [open(Path(p).expanduser(), "rb") for p in args.reference_image]
        try:
            params["image"] = handles if len(handles) > 1 else handles[0]
            response = client.images.edit(**params)
        finally:
            for handle in handles:
                handle.close()
    else:
        response = client.images.generate(**params)
    log(f"generated {len(response.data)} image(s) in {round(time.time() - started, 1)}s")
    return response.data


def upload(path):
    """Host the file on Distribb (POST /api/v1/images) and return the JSON reply."""
    key = os.getenv("DISTRIBB_API_KEY")
    if not key:
        raise SystemExit("DISTRIBB_API_KEY is not set, so --upload cannot host the image.")
    body = {"image_base64": base64.b64encode(Path(path).read_bytes()).decode("ascii")}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
               "User-Agent": "distribb-openai-image-tool/1.0"}
    try:
        import requests
        resp = requests.post(DISTRIBB_IMAGES_URL, json=body, headers=headers, timeout=120)
        status, payload = resp.status_code, resp.json()
    except ImportError:
        import urllib.request
        req = urllib.request.Request(DISTRIBB_IMAGES_URL, data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            status, payload = resp.status, json.loads(resp.read())
    if status >= 400 or not payload.get("url"):
        raise SystemExit(f"Distribb could not host {path}: HTTP {status} {payload}")
    return payload


def main():
    parser = argparse.ArgumentParser(description="Make article images with OpenAI gpt-image-2.")
    parser.add_argument("--prompt", default="", help="What the image shows.")
    parser.add_argument("--prompt-file", default="", help="Read the prompt from a text file instead.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default=DEFAULT_SIZE, help="WxH, default 1536x1024 (landscape).")
    parser.add_argument("--quality", default=DEFAULT_QUALITY, help="low, medium or high.")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--output-format", default="png", help="png, jpeg or webp.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--reference-image", action="append", default=[],
                        help="A photo to follow (product, brand). Repeatable.")
    parser.add_argument("--upload", action="store_true",
                        help="Host each image on Distribb and print its URL.")
    args = parser.parse_args()

    if args.prompt_file:
        args.prompt = Path(args.prompt_file).expanduser().read_text(encoding="utf-8").strip()
    if not args.prompt:
        raise SystemExit("Give the image a --prompt (or --prompt-file).")
    load_env()

    out_dir = Path(args.output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    files, hosted = [], []
    for index, item in enumerate(generate(args), start=1):
        path = out_dir / f"{slugify(args.prompt)}-{stamp}-{index:02d}.{args.output_format}"
        path.write_bytes(image_bytes(item))
        files.append(str(path))
        log(f"saved {path}")
        if args.upload:
            reply = upload(path)
            hosted.append({k: reply.get(k) for k in ("url", "width", "height")})
            log(f"hosted {reply['url']}")
    print(json.dumps({"files": files, "hosted": hosted}))


if __name__ == "__main__":
    main()
