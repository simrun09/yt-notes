"""Usage: python main.py "<youtube url>" --title "Lecture title" [--limit 2]"""
import argparse

from ytnotes.pipeline import run

parser = argparse.ArgumentParser(description="YouTube lecture -> study notes")
parser.add_argument("url")
parser.add_argument("--title", required=True, help="Lecture title, gives the LLM context")
parser.add_argument("--chunk-minutes", type=int, default=5)
parser.add_argument("--limit", type=int, help="Only process the first N chunks (for testing)")
args = parser.parse_args()

run(args.url, args.title, args.chunk_minutes, args.limit)
