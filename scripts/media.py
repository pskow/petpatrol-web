import json
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
STUDIO = Path.home() / "Git" / "pet-patrol-studio"
ORIG = STUDIO / "assets" / "KALENDARZ 2027"
ASSETS = Path.home() / ".cursor" / "projects" / "Users-przemek-cursor-agents-petpatrol-web" / "assets"
OUT = ROOT / "dist" / "media"
CACHE = ROOT / ".cache"

HEADS = {m["file"]: m["head"] for m in json.loads((STUDIO / "data/photos/2027/photos.json").read_text())["months"]}

PHOTOS = {
    "nugat": ("Nugat 3.jpg", 4 / 5, 900),
    "kaprys": ("Kaprys 2.jpg", 4 / 3, 1100),
    "kobi": ("Kobi 1.jpg", 4 / 3, 1100),
    "tofik": ("Tofik.jpeg", 4 / 3, 1100),
    "farfocel": ("Farfocel 2.jpg", 4 / 3, 1100),
    "henio": ("Henio.jpeg", 4 / 3, 1000),
}



def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def head_center(im, file):
    w, h = im.size
    l, t, r, b = HEADS.get(file, (0.3, 0.2, 0.7, 0.6))
    return (l + r) / 2 * w, (t + b) / 2 * h, (r - l) * w, (b - t) * h


def clamp_box(cx, cy, cw, ch, w, h):
    x = min(max(cx - cw / 2, 0), w - cw)
    y = min(max(cy - ch / 2, 0), h - ch)
    return int(x), int(y), int(x + cw), int(y + ch)


def crop_photo(file, aspect, width):
    im = load(ORIG / file)
    w, h = im.size
    cx, cy, _, _ = head_center(im, file)
    cw = min(w, h * aspect)
    ch = cw / aspect
    box = clamp_box(cx, cy + ch * 0.08, cw, ch, w, h)
    out = im.crop(box)
    out.thumbnail((width, round(width / aspect)), Image.LANCZOS)
    return out


def fetch(url, name):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / name
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        path.write_bytes(urllib.request.urlopen(req).read())
    return path


def trim(im, bg=(255, 255, 255), tol=12):
    rgb = im.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            p = px[x, y]
            if any(abs(p[i] - bg[i]) > tol for i in range(3)):
                xs.append(x)
                ys.append(y)
    return im.crop((max(min(xs) - 2, 0), max(min(ys) - 2, 0), min(max(xs) + 3, w), min(max(ys) + 3, h)))


def save(im, name, quality=80):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.save(path, "WEBP", quality=quality, method=6)
    print(f"{name:32} {im.size[0]}x{im.size[1]}  {path.stat().st_size // 1024} KB")


def find_asset(prefix):
    hits = sorted(ASSETS.glob(f"{prefix}*.png"))
    if not hits:
        sys.exit(f"missing asset {prefix}*.png in {ASSETS}")
    return hits[-1]


def main():
    for key, (file, aspect, width) in PHOTOS.items():
        save(crop_photo(file, aspect, width), f"ppw-foto-{key}.webp", 78)

    logo = Image.open(find_asset("Logo-")).convert("RGBA")
    flat = Image.new("RGB", logo.size, "white")
    flat.paste(logo, mask=logo.split()[3])
    flat = trim(flat)
    side = max(flat.size)
    square = Image.new("RGB", (side, side), "white")
    square.paste(flat, ((side - flat.width) // 2, (side - flat.height) // 2))
    save(square.resize((400, 400), Image.LANCZOS), "ppw-logo.webp", 88)

    blik = Image.open(find_asset("blik-")).convert("RGBA")
    bbox = blik.split()[3].point(lambda a: 255 if a > 8 else 0).getbbox()
    blik = blik.crop(bbox) if bbox else blik
    if blik.getpixel((0, 0))[3] == 255:
        blik = trim(blik.convert("RGB")).convert("RGBA")
    blik.thumbnail((240, 120), Image.LANCZOS)
    save(blik, "ppw-blik.webp", 90)

    team = load(fetch("https://www.petpatrol.pl/wp-content/uploads/2023/12/wspolne.png", "wspolne.png"))
    team.thumbnail((1600, 800), Image.LANCZOS)
    save(team, "ppw-zespol.webp", 76)


if __name__ == "__main__":
    main()
