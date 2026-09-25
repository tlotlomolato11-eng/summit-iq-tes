"""Inline the shared Summit IQ CSS/JS (from maatla/src) plus bio.css into each biology page."""
from pathlib import Path
here = Path(__file__).parent
src = here / "src"
shared = here.parent.parent / "maatla" / "src"
css = (shared / "shared.css").read_text() + (src / "bio.css").read_text()
js = (shared / "shared.js").read_text() + (src / "bio.js").read_text()
head = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap">')
for page in sorted(src.glob("b*.html")):
    out = page.read_text().replace("<!--HEAD-->", head).replace("/*SHARED_CSS*/", css).replace("/*SHARED_JS*/", js)
    (here / page.name).write_text(out)
    print("built", page.name)
