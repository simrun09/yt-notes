"""Step 1: get the transcript for a YouTube URL."""
import re

from youtube_transcript_api import YouTubeTranscriptApi

_ID_PATTERNS = [
    r"v=([A-Za-z0-9_-]{11})",
    r"youtu\.be/([A-Za-z0-9_-]{11})",
    r"youtube\.com/(?:embed|shorts|live)/([A-Za-z0-9_-]{11})",
]


def extract_video_id(url: str) -> str:
    for pattern in _ID_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not find a video ID in: {url}")


def fetch_segments(video_id: str) -> list[dict]:
    """Return [{'start': seconds, 'text': str}, ...]."""
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=["en", "hi"])
    except Exception:
        fetched = next(iter(api.list(video_id))).fetch()
    segments = []
    for item in fetched:
        text = item.text.replace("\n", " ").strip()
        if text and not re.fullmatch(r"\[.*\]", text):  # drop [Music] etc.
            segments.append({"start": item.start, "text": text})
    return segments
