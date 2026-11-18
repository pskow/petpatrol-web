import re
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
WP = DIST / "wordpress"
PREVIEW = DIST / "podglad"
CACHE = ROOT / ".cache"

MEDIA_BASE = sys.argv[1] if len(sys.argv) > 1 else "/wp-content/uploads/2026/11/"
UPLOADS = "https://www.petpatrol.pl/wp-content/uploads/"

FONTS = [
    "https://cdn.jsdelivr.net/npm/@fontsource-variable/jost@5/index.css",
    "https://cdn.jsdelivr.net/npm/@fontsource/big-shoulders-display@5/800.css",
    "https://cdn.jsdelivr.net/npm/@fontsource/big-shoulders-display@5/900.css",
]

PAGES = {
    "strona-glowna": (1466, "Strona Startowa", "/"),
    "o-nas": (3968, "O Nas", "/o-nas/"),
    "pomagam": (5259, "Jak Pomóc", "/pomagam/"),
    "zostan-wolontariuszem": (5496, "Zostań wolontariuszem!", "/zostan-wolontariuszem/"),
    "warsztaty": (5968, "Warsztaty", "/warsztaty/"),
    "warunki-adopcji": (1519, "Warunki adopcji", "/warunki-adopcji/"),
    "kontakt": (1919, "Kontakt", "/kontakt/"),
    "dokumenty": (5702, "Dokumenty i Sprawozdania Roczne", "/dokumenty/"),
    "regulamin-warsztatow": (5949, "Regulamin warsztatów", "/regulamin-warsztatow/"),
    "standardy-ochrony-maloletnich": (5951, "Standardy Ochrony Małoletnich", "/standardy-ochrony-maloletnich/"),
    "polityka-prywatnosci": (644, "Polityka prywatności", "/polityka-prywatnosci/"),
}

STROKE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
FILL = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{}</svg>'

ICONS = {
    "arrow": STROKE.format('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "check": STROKE.format('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    "chevron": STROKE.format('<path d="M6 9l6 6 6-6"/>'),
    "menu": STROKE.format('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": STROKE.format('<path d="M6 6l12 12M18 6L6 18"/>'),
    "mail": STROKE.format('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>'),
    "phone": STROKE.format('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "pin": STROKE.format('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "file": STROKE.format('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
    "download": STROKE.format('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>'),
    "heart": STROKE.format('<path d="M12 20s-7.5-4.6-9.2-9.1C1.6 7.6 3.8 4.5 7.1 4.5c2 0 3.6 1.1 4.9 2.8 1.3-1.7 2.9-2.8 4.9-2.8 3.3 0 5.5 3.1 4.3 6.4C19.5 15.4 12 20 12 20z"/>'),
    "home": STROKE.format('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    "alert": STROKE.format('<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.5h.01"/>'),
    "medical": STROKE.format('<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/>'),
    "car": STROKE.format('<path d="M5 11l1.6-4.2A1.5 1.5 0 0 1 8 6h8a1.5 1.5 0 0 1 1.4.8L19 11"/><rect x="3" y="11" width="18" height="6" rx="2"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>'),
    "camera": STROKE.format('<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>'),
    "jar": STROKE.format('<rect x="4" y="8" width="16" height="12" rx="2.5"/><path d="M9.5 12h5"/><circle cx="12" cy="4.3" r="1.8"/>'),
    "tag": STROKE.format('<path d="M4 4h7.5L20 12.5 12.5 20 4 11.5z"/><circle cx="8.5" cy="8.5" r="1.5"/>'),
    "building": STROKE.format('<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>'),
    "users": STROKE.format('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 5.5 5.8"/>'),
    "calendar": STROKE.format('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    "clock": STROKE.format('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "coins": STROKE.format('<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>'),
    "shield": STROKE.format('<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    "book": STROKE.format('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/>'),
    "box": STROKE.format('<path d="M3 7.5l9-4.5 9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>'),
    "copy": STROKE.format('<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>'),
    "external": STROKE.format('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "message": STROKE.format('<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>'),
    "cat": STROKE.format('<path d="M5 20v-8.5L4 4l4.5 3.5h7L20 4l-1 7.5V20"/><path d="M5 20h14M9.5 13h.01M14.5 13h.01M11 16.5h2"/>'),
    "paw": FILL.format('<ellipse cx="6.2" cy="9.4" rx="2.3" ry="3"/><ellipse cx="17.8" cy="9.4" rx="2.3" ry="3"/><ellipse cx="9.8" cy="5.2" rx="2.3" ry="3.1"/><ellipse cx="14.2" cy="5.2" rx="2.3" ry="3.1"/><path d="M12 10.6c-3.7 0-7.2 3.4-7.2 6.6 0 1.9 1.3 2.9 2.9 2.9 1.7 0 2.7-1.1 4.3-1.1s2.6 1.1 4.3 1.1c1.6 0 2.9-1 2.9-2.9 0-3.2-3.5-6.6-7.2-6.6z"/>'),
    "facebook": FILL.format('<path d="M14.2 8.2h2.6V4.6h-2.6c-2.8 0-4.5 1.7-4.5 4.4v2.2H7.2v3.6h2.5V22h3.6v-7.2h2.7l.5-3.6h-3.2V9.4c0-.8.4-1.2 1.2-1.2z"/>'),
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="17.4" cy="6.6" r="1.4" fill="currentColor"/></svg>',
    "tiktok": FILL.format('<path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>'),
}

BANNERS = {
    "support": [
        ("https://www.ratujemyzwierzaki.pl/pet-patrol-rybnik", "2026/08/ratujemy-zwierzaki-768x307.png", "Ratujemy Zwierzaki – zbiórka", True),
        ("https://patronite.pl/petpatrolrybnik", "2026/08/patronite-768x192.png", "Patronite", False),
    ],
    "find": [
        ("https://www.olx.pl/oferty/uzytkownik/rC6dZ/", "2026/08/olx-ogloszenia-768x192.png", "OLX – ogłoszenia adopcyjne", False),
        ("https://www.facebook.com/groups/1894736440695762/", "2026/08/fb-bazarek-768x192.png", "Facebook – bazarek fundacji", False),
        ("https://www.facebook.com/share/ZciUeDb3JBih9Ja8/?mibextid=K35XfP", "2026/08/fb-zaginione-768x192.png", "Facebook – zaginione i znalezione", False),
    ],
}


INDEX = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url=podglad/strona-glowna.html">
<title>Pet Patrol Rybnik – podgląd nowej strony</title>
</head>
<body>
<p><a href="podglad/strona-glowna.html">Przejdź do podglądu nowej strony Pet Patrol Rybnik</a></p>
</body>
</html>
"""


def banners(group):
    out = []
    for href, img, alt, contain in BANNERS[group]:
        cls = "ppw-banner ppw-banner--contain" if contain else "ppw-banner"
        out.append(f'<a class="{cls}" href="{href}" target="_blank" rel="noopener"><img src="{UPLOADS}{img}" alt="{alt}" loading="lazy" width="768" height="192"></a>')
    return "".join(out)


def render(text, media):
    text = re.sub(r"\{\{i:([a-z]+)\}\}", lambda m: f'<span class="ppw-ico">{ICONS[m.group(1)]}</span>', text)
    text = re.sub(r"\{\{svg:([a-z]+)\}\}", lambda m: ICONS[m.group(1)], text)
    text = re.sub(r"\{\{banners:([a-z]+)\}\}", lambda m: banners(m.group(1)), text)
    text = text.replace("{{m}}", media)
    left = re.findall(r"\{\{[^}]*\}\}", text)
    if left:
        sys.exit(f"unresolved tokens: {sorted(set(left))}")
    return text


def head_snippet():
    links = "\n".join(f'<link rel="stylesheet" href="{u}">' for u in FONTS)
    css = (SRC / "site.css").read_text().strip()
    return f'<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n{links}\n<style id="ppw-site-css">\n{css}\n</style>\n'


def body_snippet(media):
    return render((SRC / "header.html").read_text(), media)


def footer_snippet(media):
    js = (SRC / "site.js").read_text().strip()
    return render((SRC / "footer.html").read_text(), media) + f"<script>\n{js}\n</script>\n"


EXTRA_PREVIEWS = {
    "wpis-przyklad": "https://www.petpatrol.pl/zwierzeta-a-upaly/",
}


def fetch_page(url, name):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{name}.html"
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        path.write_text(urllib.request.urlopen(req).read().decode("utf-8"))
    return path.read_text()


def template():
    return fetch_page("https://www.petpatrol.pl/pomagam/", "template")


def wrap_preview(html):
    media = "../media/"
    html = re.sub(r'<link rel="canonical"[^>]*>\s*', "", html)
    html = re.sub(r'<meta name="robots"[^>]*>\s*', "", html)
    html = html.replace("</head>", '<meta name="robots" content="noindex, nofollow">\n' + head_snippet() + "</head>", 1)
    body = re.search(r"<body[^>]*>", html)
    html = html[: body.end()] + "\n" + body_snippet(media) + html[body.end():]
    html = html.replace("</body>", footer_snippet(media) + "</body>", 1)
    html = html.replace('class="cookie-notice-hidden', 'style="display:none" class="cookie-notice-hidden')
    return preview_links(html)


def preview_links(html):
    def repl(m):
        href = m.group(1)
        for slug, (_, _, path) in PAGES.items():
            if href == path:
                return f'href="{slug}.html"'
        return f'href="https://www.petpatrol.pl{href}"'
    html = re.sub(r'href="(/[^"]*)"', repl, html)
    return html.replace('action="/"', 'action="https://www.petpatrol.pl/"')


def build_preview(slug, page_html):
    page_id, title, _ = PAGES[slug]
    media = "../media/"
    html = template()
    html = re.sub(r"<title>.*?</title>", f"<title>{title} | Pet Patrol Rybnik</title>", html, count=1, flags=re.S)
    html = html.replace("page-id-5259", f"page-id-{page_id}")
    start = html.index('<div class="entry-content">') + len('<div class="entry-content">')
    end = html.index("</div><!-- .entry-content -->")
    html = html[:start] + "\n" + render(page_html, media) + "\n" + html[end:]
    return wrap_preview(html)


def main():
    if WP.exists():
        shutil.rmtree(WP)
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    (WP / "strony").mkdir(parents=True)
    PREVIEW.mkdir(parents=True)

    (WP / "1-wpcode-header.html").write_text(head_snippet())
    (WP / "2-wpcode-body.html").write_text(body_snippet(MEDIA_BASE))
    (WP / "3-wpcode-footer.html").write_text(footer_snippet(MEDIA_BASE))

    for slug in PAGES:
        src = SRC / "pages" / f"{slug}.html"
        if not src.exists():
            print(f"skip {slug} (no source)")
            continue
        page = src.read_text()
        block = render(page, MEDIA_BASE).strip()
        (WP / "strony" / f"{slug}.html").write_text(f"<!-- wp:html -->\n{block}\n<!-- /wp:html -->\n")
        (PREVIEW / f"{slug}.html").write_text(build_preview(slug, page))
        print(f"built {slug}")

    for name, url in EXTRA_PREVIEWS.items():
        (PREVIEW / f"{name}.html").write_text(wrap_preview(fetch_page(url, name)))
        print(f"built preview {name}")

    (DIST / "index.html").write_text(INDEX)
    print(f"media base: {MEDIA_BASE}")
    for f in sorted(WP.rglob("*.html")):
        print(f"{f.relative_to(DIST)}  {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
