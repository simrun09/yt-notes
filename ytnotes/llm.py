"""Thin wrapper around Gemini with retries and clear error messages."""
import os
import time

from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"


def get_client():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "GEMINI_API_KEY is not set.\n"
            "Get a free key at https://aistudio.google.com/apikey, then run:\n"
            "  export GEMINI_API_KEY='your-key'"
        )
    return genai.Client(api_key=key)


def ask(client, prompt: str, retries: int = 5) -> str:
    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    for attempt in range(1, retries + 1):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            if not resp.text:
                raise RuntimeError("Model returned empty text.")
            return resp.text.strip()
        except Exception as err:  # rate limit, overload, network
            msg = str(err)
            if "404" in msg or "not found" in msg.lower():
                raise SystemExit(
                    f"Model '{model}' was not found. Set another one, e.g.\n"
                    "  export GEMINI_MODEL='gemini-2.0-flash'\n"
                    f"Original error: {msg}"
                )
            if attempt == retries:
                raise
            wait = 15 * attempt
            print(f"  LLM error ({msg[:80]}...). Retrying in {wait}s [{attempt}/{retries}]")
            time.sleep(wait)
