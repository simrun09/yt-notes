from ytnotes.chunker import chunk_segments, fmt_time
from ytnotes.transcript import extract_video_id


def test_chunking_splits_by_time():
    segs = [{"start": i * 10, "text": f"w{i}"} for i in range(100)]  # ~16 min
    chunks = chunk_segments(segs, minutes=5)
    assert len(chunks) == 4
    assert chunks[0]["start"] == 0
    assert chunks[1]["start"] == 300


def test_fmt_time():
    assert fmt_time(125) == "02:05"
    assert fmt_time(3725) == "1:02:05"


def test_video_id():
    for u in ["https://www.youtube.com/watch?v=abcdefghijk&t=5",
              "https://youtu.be/abcdefghijk",
              "https://www.youtube.com/shorts/abcdefghijk"]:
        assert extract_video_id(u) == "abcdefghijk"
