"""Step 2: split the transcript into time-based chunks."""


def chunk_segments(segments: list[dict], minutes: int = 5) -> list[dict]:
    """Group segments into chunks of roughly `minutes` minutes each."""
    chunks, current, start = [], [], 0.0
    for seg in segments:
        if current and seg["start"] - start >= minutes * 60:
            chunks.append({"start": start, "text": " ".join(current)})
            current, start = [], seg["start"]
        if not current:
            start = seg["start"]
        current.append(seg["text"])
    if current:
        chunks.append({"start": start, "text": " ".join(current)})
    return chunks


def fmt_time(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
