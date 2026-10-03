"""Turn a notes .md file into an engaging, self-contained HTML study page.

Usage:  python to_html.py notes/VIDEO_ID.md      ->  notes/VIDEO_ID.html
"""
import html
import re
import sys
from pathlib import Path

import markdown

CSS = """
:root{--bg:#faf8f4;--card:#fff;--text:#262a33;--muted:#6b7280;--line:#e7e2d9;--accent:#4f46e5;
--accent2:#7c3aed;--hard:#eef0ff;--add:#fff1c9;--term:#f3f1ec;--side:#f4f1ea}
[data-theme=dark]{--bg:#14161b;--card:#1b1e25;--text:#e4e6eb;--muted:#9aa3b2;--line:#2a2e38;
--accent:#8b93ff;--accent2:#b794ff;--hard:#222650;--add:#4a3d12;--term:#22252d;--side:#181b21}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:18px/1.8 Georgia,Charter,"Times New Roman",serif}
h1,h2,h3,h4,nav,.tag,.chip,summary,.num,.time,button{font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
#bar{position:fixed;top:0;left:0;height:4px;width:0;z-index:9;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.layout{display:flex;max-width:1200px;margin:0 auto}
nav{position:sticky;top:0;height:100vh;overflow-y:auto;width:290px;flex-shrink:0;padding:30px 16px;
background:var(--side);border-right:1px solid var(--line);font-size:14px;line-height:1.4}
nav b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 8px 12px}
nav a{display:flex;gap:10px;padding:8px;border-radius:8px;color:var(--text);text-decoration:none;align-items:baseline}
nav a span{color:var(--muted);font-weight:700;min-width:1.4em}
nav a:hover{background:var(--line)}nav a.on{background:var(--card);box-shadow:0 1px 4px #0002;color:var(--accent);font-weight:600}
main{flex:1;min-width:0;max-width:800px;padding:0 36px 120px}
.hero{margin:0 -36px 34px;padding:56px 36px 40px;color:#fff;background:linear-gradient(135deg,#4f46e5,#7c3aed 60%,#db2777)}
.hero h1{margin:0 0 14px;font-size:2.1em;line-height:1.2}
.chip{display:inline-block;margin:4px 6px 0 0;padding:4px 12px;border-radius:99px;background:#ffffff2b;color:#fff;font-size:13px;text-decoration:none}
button{float:right;border:0;border-radius:99px;padding:6px 12px;cursor:pointer;background:#ffffff33;color:#fff}
.overview{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 26px 14px;margin-bottom:46px;box-shadow:0 4px 18px #0000000d}
.overview h3{margin:1.2em 0 .2em;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.part{position:relative;padding:0 0 18px 34px;margin-bottom:26px;border-left:3px solid var(--line)}
.part>header{display:flex;align-items:center;gap:12px;margin:0 0 6px -34px;transform:translateX(-19px)}
.num{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:700;
background:linear-gradient(135deg,var(--accent),var(--accent2));box-shadow:0 0 0 5px var(--bg)}
.time{font-size:13px;padding:3px 11px;border-radius:99px;background:var(--card);border:1px solid var(--line);color:var(--accent);text-decoration:none}
h2{font-size:1.5em;margin:1.6em 0 .4em}h3{font-size:1.35em;line-height:1.3;margin:.2em 0 .5em}h4{font-size:1.05em;margin:1.4em 0 .3em;color:var(--muted)}
a{color:var(--accent)}p,li{margin:.65em 0}ul,ol{padding-left:1.3em}
.callout{margin:1.5em 0;padding:14px 22px 6px;border-radius:12px;background:var(--term);border:1px solid var(--line)}
.callout.hard{background:var(--hard);border:0;border-left:5px solid var(--accent)}
.tag{display:inline-block;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);margin-bottom:2px}
.added{font-family:-apple-system,"Segoe UI",sans-serif;background:var(--add);font-size:.72em;font-weight:700;padding:2px 8px;border-radius:99px;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
details.terms{margin:1.4em 0;background:var(--term);border-radius:10px;padding:2px 18px}
details.terms summary,details.card summary{cursor:pointer;font-weight:600;padding:10px 0}
code{background:var(--term);padding:.12em .4em;border-radius:5px;font-size:.88em;font-family:ui-monospace,Consolas,monospace}
pre{background:var(--term);padding:14px 16px;border-radius:10px;overflow-x:auto}pre code{background:none;padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:8px 12px}
.extra{margin-top:60px}.extra h2{border:0;padding:0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
details.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:6px 18px;box-shadow:0 2px 8px #0000000a}
details.card[open]{border-color:var(--accent)}details.card summary{color:var(--text)}
details.card div{border-top:1px dashed var(--line);margin-top:4px;font-size:.95em}
.try{background:var(--hard);border-left:5px solid var(--accent2);border-radius:12px;padding:6px 22px}
@media(max-width:860px){nav{display:none}main{padding:0 18px 90px}.hero{margin:0 -18px 28px;padding:40px 18px 30px}body{font-size:17px}}
@media print{nav,#bar,button{display:none}.hero{color:#000;background:none}}
"""

JS = """
const bar=document.getElementById('bar'),d=document.documentElement;
addEventListener('scroll',()=>{bar.style.width=(d.scrollTop/(d.scrollHeight-d.clientHeight||1)*100)+'%'});
const links=[...document.querySelectorAll('nav a')];
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(
l=>l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-15% 0px -75% 0px'});
document.querySelectorAll('.part').forEach(s=>io.observe(s));
d.dataset.theme=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
document.getElementById('theme').onclick=()=>{d.dataset.theme=d.dataset.theme=='dark'?'light':'dark'};
"""

LIST_RE = re.compile(r"^\s*([-*+]|\d+\.)\s+")
EXTRA_RE = re.compile(r"(?im)^[ \t]*(?:\d+\.\s*)?(?:#+\s*)?\**\s*(Flashcards|Explain it back|Try this next)\s*\**\s*:?\s*\**[ \t]*$")


def fix_lists(text):
    """Markdown needs a blank line before a list; LLM output often skips it."""
    out, prev = [], ""
    for line in text.split("\n"):
        if LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def md(text):
    return markdown.markdown(fix_lists(text), extensions=["extra", "sane_lists", "nl2br"])


def callouts(h):
    def sub(m):
        inner = m.group(1)
        hard = re.match(r"\s*<p>\s*<strong>\s*Hard idea:?\s*</strong>:?\s*", inner)
        if hard:
            return ('<aside class="callout hard"><div class="tag">💡 Hard idea</div><p>'
                    + inner[hard.end():] + "</aside>")
        return '<aside class="callout">' + inner + "</aside>"
    h = re.sub(r"<blockquote>(.*?)</blockquote>", sub, h, flags=re.S)
    h = re.sub(r"<p><strong>Key terms:?</strong>:?</p>\s*(<ul>.*?</ul>)",
               r'<details class="terms"><summary>📖 Key terms</summary>\1</details>', h, flags=re.S)
    return h.replace("[Added]", '<span class="added" title="Not said in the lecture; added by the AI">Beyond the lecture</span>')


def cards(sec):
    pairs = re.findall(r"\*\*Q\s*:?\s*\*\*\s*:?(.*?)\*\*A\s*:?\s*\*\*\s*:?(.*?)(?=\*\*Q\s*:?\s*\*\*|\Z)", sec, flags=re.S)
    def clean(s):
        s = re.sub(r"\n\s*(?:\d+\.|[-*])\s*$", "", s.strip())
        return re.sub(r"^[\s/]+|[\s/]+$", "", s)
    out = []
    for q, a in pairs:
        qh = re.sub(r"^<p>|</p>$", "", md(clean(q)).strip())
        out.append(f'<details class="card"><summary>{qh}</summary><div>{md(clean(a))}</div></details>')
    return '<div class="cards">' + "".join(out) + "</div>" if out else md(sec)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python to_html.py notes/VIDEO_ID.md")
    src = Path(sys.argv[1])
    text = src.read_text(encoding="utf-8")

    title = next((l[2:].strip() for l in text.split("\n") if l.startswith("# ")), src.stem)
    url = (re.search(r"Source:\s*(\S+)", text) or [None, ""])[1]
    first = re.search(r"(?m)^## Part ", text)
    front = text[:first.start()] if first else text
    rest = text[first.start():] if first else ""
    front = re.sub(r"(?m)^# .*$|^Source:.*$|^\s*---\s*$", "", front)

    extras = list(EXTRA_RE.finditer(rest))
    tail = ""
    if extras:
        tail, rest = rest[extras[0].start():], rest[:extras[0].start()]
    rest = re.sub(r"(\n\s*---\s*)+$", "", rest.strip())

    parts, nav = [], []
    for chunk in re.split(r"(?m)^(?=## Part )", rest):
        m = re.match(r"## Part (\d+)\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*(.*)", chunk, flags=re.S)
        if not m:
            continue
        n, stamp, link, body = m.groups()
        body = re.sub(r"\n\s*---\s*$", "", body.strip())
        h = callouts(md(body))
        t = re.search(r"<h[34]>(.*?)</h[34]>", h)
        label = re.sub(r"<[^>]+>", "", t.group(1)) if t else f"Part {n}"
        nav.append(f'<a href="#part-{n}"><span>{n}</span>{label}</a>')
        parts.append(f'<section class="part" id="part-{n}"><header><div class="num">{n}</div>'
                     f'<a class="time" href="{link}" target="_blank">▶ Watch from {stamp}</a></header>{h}</section>')

    extra_html = ""
    for i, e in enumerate(extras):
        end = extras[i + 1].start() - extras[0].start() if i + 1 < len(extras) else len(tail)
        sec = tail[e.start() - extras[0].start():end]
        sec = sec[sec.index("\n") + 1:] if "\n" in sec else ""
        name = e.group(1).capitalize() if e.group(1).lower() != "explain it back" else "Explain it back"
        icon = {"Flashcards": "🃏", "Explain it back": "🗣️", "Try this next": "🛠️"}.get(name, "")
        if name == "Flashcards":
            body = cards(sec)
        elif name == "Try this next":
            body = '<div class="try">' + md(sec) + "</div>"
        else:
            body = md(sec)
        nav_id = name.lower().replace(" ", "-")
        nav.append(f'<a href="#{nav_id}"><span>{icon}</span>{name}</a>')
        extra_html += f'<section class="extra" id="{nav_id}"><h2>{icon} {name}</h2>{body}</section>'

    mins = max(1, round(len(text.split()) / 200))
    overview = re.sub(r"<p><strong>(TL;DR|Topic map|Prerequisites)[:]?</strong>:?</p>", r"<h3>\1</h3>", md(front))
    overview = re.sub(r"<strong>(TL;DR|Topic map|Prerequisites):?</strong>:?", r"<h3>\1</h3>", overview)
    chips = f'<span class="chip">⏱ ~{mins} min read</span><span class="chip">{len(parts)} parts</span>'
    if url:
        chips += f'<a class="chip" href="{html.escape(url)}" target="_blank">▶ Watch the video</a>'

    page = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body><div id="bar"></div>'
            f'<div class="layout"><nav><b>Contents</b>{"".join(nav)}</nav><main>'
            f'<div class="hero"><button id="theme">◐ Theme</button><h1>{html.escape(title)}</h1>{chips}</div>'
            f'<div class="overview">{overview}</div>{"".join(parts)}{extra_html}</main></div>'
            f'<script>{JS}</script></body></html>')
    out = src.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(f"Saved {out}  ({len(parts)} parts, {len(extras)} extra sections)")


if __name__ == "__main__":
    main()
