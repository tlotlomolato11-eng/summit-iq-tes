"""Inline shared CSS/JS into each question page so every output file is self-contained."""
from pathlib import Path
here = Path(__file__).parent
src = here / "src"
css = (src / "shared.css").read_text()
js = (src / "shared.js").read_text()
head = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap">')
for page in sorted(src.glob("q*.html")):
    out = page.read_text().replace("<!--HEAD-->", head).replace("/*SHARED_CSS*/", css).replace("/*SHARED_JS*/", js)
    (here / page.name).write_text(out)
    print("built", page.name)
