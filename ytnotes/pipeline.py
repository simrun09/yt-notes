"""Runs all steps and writes the final Markdown notes."""
import json
from pathlib import Path

from . import prompts
from .chunker import chunk_segments, fmt_time
from .llm import ask, get_client
from .transcript import extract_video_id, fetch_segments


def run(url: str, title: str, chunk_minutes: int = 5, limit: int | None = None) -> Path:
    video_id = extract_video_id(url)
    work = Path("work") / video_id
    work.mkdir(parents=True, exist_ok=True)

    # Step 1: transcript (cached)
    seg_file = work / "segments.json"
    if seg_file.exists():
        segments = json.loads(seg_file.read_text(encoding="utf-8"))
        print(f"[1/4] Loaded cached transcript ({len(segments)} segments)")
    else:
        print("[1/4] Fetching transcript...")
        segments = fetch_segments(video_id)
        seg_file.write_text(json.dumps(segments, ensure_ascii=False), encoding="utf-8")

    # Step 2: chunks
    chunks = chunk_segments(segments, chunk_minutes)
    if limit:
        chunks = chunks[:limit]
    print(f"[2/4] {len(chunks)} chunks of ~{chunk_minutes} min")

    # Step 3: notes per chunk (each result is cached, so reruns resume)
    client = get_client()
    sections = []
    for i, chunk in enumerate(chunks, 1):
        cache = work / f"chunk_{i:02d}.md"
        if cache.exists():
            notes = cache.read_text(encoding="utf-8")
        else:
            print(f"[3/4] Writing notes for chunk {i}/{len(chunks)}...")
            notes = ask(client, prompts.CHUNK_PROMPT.format(
                title=title, index=i, total=len(chunks),
                time=fmt_time(chunk["start"]), text=chunk["text"]))
            cache.write_text(notes, encoding="utf-8")
        link = f"https://youtu.be/{video_id}?t={int(chunk['start'])}"
        sections.append(f"## Part {i} - [{fmt_time(chunk['start'])}]({link})\n\n{notes}")

    # Step 4: TL;DR and flashcards from the notes
    print("[4/4] Writing summary and flashcards...")
    body = "\n\n---\n\n".join(sections)
    tldr = ask(client, prompts.TLDR_PROMPT.format(title=title, notes=body))
    cards = ask(client, prompts.CARDS_PROMPT.format(title=title, notes=body))

    out = Path("notes")
    out.mkdir(exist_ok=True)
    out_file = out / f"{video_id}.md"
    out_file.write_text(
        f"# {title}\n\nSource: {url}\n\n{tldr}\n\n---\n\n{body}\n\n---\n\n{cards}\n",
        encoding="utf-8",
    )
    print(f"Done: {out_file}")
    return out_file
