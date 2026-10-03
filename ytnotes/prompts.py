"""All prompts live here so they are easy to tune."""

CHUNK_PROMPT = """You are making study notes from one segment of a lecture.
Lecture title: {title}
This is part {index} of {total}, starting at {time} in the video.

The lecture is in Hinglish and the transcript comes from auto-captions, so
technical terms are often misspelled. Fix them using context. Write in clear
English.

Write the notes in Markdown:
- Follow the lecturer's order. Keep the actual content of the lecture, do not
  summarise it away.
- Use only ### or #### headings (no # or ##).
- For every idea a beginner would find hard, add a block that starts with
  "> **Hard idea:**" and explain it from first principles: why it exists, an
  intuition or analogy, a step-by-step build-up, and a tiny worked example.
- Anything you add that the lecturer did not say must begin with [Added].
- End with "**Key terms**" and one-line definitions.
- Do not add an intro or outro sentence. Output only the notes.

Transcript:
{text}
"""

TLDR_PROMPT = """Below are study notes for the lecture "{title}".
Write, in Markdown:
1. **TL;DR**: 5 lines maximum.
2. **Topic map**: a bullet list of the main topics in order.
3. **Prerequisites**: what a learner should already know.
Output only these three sections.

Notes:
{notes}
"""

CARDS_PROMPT = """Below are study notes for the lecture "{title}".
Write, in Markdown:
1. **Flashcards**: 12 to 15 cards as "**Q:** ... / **A:** ..." pairs.
2. **Explain it back**: 4 questions that make the learner explain an idea in
   their own words.
3. **Try this next**: one small hands-on task.
Output only these three sections.

Notes:
{notes}
"""
