#!/usr/bin/env python3
"""
Nano Banana 2 thumbnail generator/editor.

Run this on the USER's machine (e.g. via Desktop Commander start_process),
NOT inside a sandboxed environment with restricted network access — it needs
to reach api.replicate.com and replicate.delivery directly.

Usage:
    python3 generate_thumbnail.py \
        --image /path/to/source_or_previous_version.png \
        --prompt-file /path/to/prompt.txt \
        --out /path/to/output_vN.jpeg \
        --token $REPLICATE_API_TOKEN

The prompt should be written to a text file first (avoids shell quoting hell
with long multi-line prompts containing quotes).
"""

import argparse
import base64
import json
import mimetypes
import subprocess
import sys
import tempfile
import os


MODEL = "google/nano-banana-2"  # NOT plain "nano-banana" — see SKILL.md known failure modes


def build_payload(image_path: str, prompt: str) -> dict:
    mime, _ = mimetypes.guess_type(image_path)
    mime = mime or "image/png"
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    data_uri = f"data:{mime};base64,{b64}"
    return {"input": {"prompt": prompt, "image_input": [data_uri]}}


def run_prediction(payload: dict, token: str) -> dict:
    """
    Uses curl via subprocess instead of `requests`/`urllib` directly, because
    on some macOS Python builds urllib hits SSL_CERTIFICATE_VERIFY_FAILED
    (missing local CA bundle) — curl uses the system's trust store and works.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as pf:
        json.dump(payload, pf)
        payload_path = pf.name

    result_path = payload_path + ".result.json"
    try:
        cmd = [
            "curl", "-s", "-X", "POST",
            "-H", f"Authorization: Token {token}",
            "-H", "Content-Type: application/json",
            "-H", "Prefer: wait",
            "--data-binary", f"@{payload_path}",
            f"https://api.replicate.com/v1/models/{MODEL}/predictions",
            "-o", result_path,
            "-w", "%{http_code}",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        http_code = proc.stdout.strip()
        with open(result_path) as f:
            result = json.load(f)
        result["_http_code"] = http_code
        return result
    finally:
        for p in (payload_path, result_path):
            if os.path.exists(p):
                os.remove(p)


def download(url: str, out_path: str):
    cmd = ["curl", "-s", "-o", out_path, url]
    subprocess.run(cmd, check=True, timeout=60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="Source screenshot OR previous accepted version (for edits)")
    ap.add_argument("--prompt-file", required=True, help="Path to a .txt file containing the full prompt")
    ap.add_argument("--out", required=True, help="Where to save the resulting thumbnail")
    ap.add_argument("--token", default=None, help="Replicate API token (defaults to $REPLICATE_API_TOKEN env var)")
    args = ap.parse_args()

    token = args.token or os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print(
            "No Replicate API token found. Pass --token or set REPLICATE_API_TOKEN "
            "as an environment variable. See SKILL.md Prerequisites for setup steps.",
            file=sys.stderr,
        )
        sys.exit(1)
    args.token = token

    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    payload = build_payload(args.image, prompt)
    result = run_prediction(payload, args.token)

    if result.get("status") != "succeeded":
        print("FAILED:", result.get("_http_code"), file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    output_url = result["output"]
    if isinstance(output_url, list):
        output_url = output_url[0]

    download(output_url, args.out)
    print(f"Saved: {args.out}")
    print(f"Source URL: {output_url}")


if __name__ == "__main__":
    main()
