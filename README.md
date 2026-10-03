# yt-notes

Turn any YouTube lecture into **first-principles study notes** and a clean, readable HTML page.

I built this because I kept watching long lectures, taking rough notes, and forgetting everything.
The tool takes a video link, reads the transcript, and writes notes that teach the ideas from the
ground up, with practice questions at the end.

## How it works

```
YouTube URL -> transcript -> time-based chunks -> LLM notes per chunk
            -> overview + flashcards -> Markdown file -> styled HTML page
```

| Step | File | Uses LLM? | What it does |
|------|------|-----------|--------------|
| 1 | `ytnotes/transcript.py` | No | Fetches the captions with timestamps |
| 2 | `ytnotes/chunker.py` | No | Splits the transcript into ~5 minute chunks |
| 3 | `ytnotes/pipeline.py` + `prompts.py` | Yes | Writes teaching notes for each chunk |
| 4 | `ytnotes/pipeline.py` | Yes | Writes TL;DR, big picture, flashcards, practice tasks |
| 5 | `ytnotes/pipeline.py` | No | Joins everything into `notes/<id>.md` with timestamp links |
| 6 | `to_html.py` | No | Turns the Markdown into a styled HTML study page |

## What the notes look like
- Every part starts with **the question it answers**, so the problem comes before the idea
- **Hard idea** boxes: why it exists, intuition, step-by-step mechanism, tiny worked example, common mistake
- A **Pause and predict** question in each part
- Anything the AI added beyond the lecturer is tagged **[Added]**; doubtful claims get **[Check]**
- Fixes mangled technical terms from auto-captions using context
- Every part links to its exact moment in the video
- Overview with TL;DR, big picture, topic map and prerequisites
- Click-to-reveal flashcards, "explain it back" prompts and a hands-on task

The HTML page adds a contents sidebar with progress tracking, a timeline layout, and dark mode.

## Setup (Linux / WSL / Mac)
```bash
git clone https://github.com/simrun09/yt-notes.git
cd yt-notes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY='your-key'   # free key: https://aistudio.google.com/apikey
```

## Usage
```bash
# Test on the first chunk only
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --title "Exact lecture title" --limit 1

# Whole video
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --title "Exact lecture title"

# Make the HTML page
python to_html.py notes/VIDEO_ID.md
```

Tips:
- Use the exact video title. It helps the LLM spell the key terms correctly.
- Finished chunks are cached in `work/`, so a failed run resumes where it stopped.
- Choose another model with `export GEMINI_MODEL='model-name'` (model names change over time).

## Known limits
- The free Gemini tier allows roughly 20 requests per day per model, and a 90-minute video
  uses about 20. If you hit the limit, run the same command again the next day.
- The transcript has no slides, code or diagrams from the video.
- The notes are written by an LLM, so spot-check them against the video. Look for `[Check]` tags.
- YouTube may block transcript requests from cloud servers such as Colab.

## Tests
```bash
pip install pytest && pytest
```

## Roadmap
- Fewer API calls per video (bigger chunks, merged final calls)
- Carry context from the previous chunk into the next
- A `--terms` option to force correct spellings
- Review pass that checks notes against the transcript
- Anki export for flashcards
- Whisper fallback when a video has no captions
- Playlist support and other LLM providers
