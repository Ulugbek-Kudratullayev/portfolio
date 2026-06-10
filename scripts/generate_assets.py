"""Generate branded placeholder assets for the portfolio frontend.

Creates dark space-themed gradient covers for featured projects, category
placeholders, nav-link previews, the OG image and an initials avatar.
Run with the backend venv (Pillow installed):
    .venv\\Scripts\\python.exe ..\\scripts\\generate_assets.py
"""

import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ASSETS = FRONTEND / "public" / "assets"
GENERATED = ASSETS / "projects-screenshots" / "generated"
FALLBACK = FRONTEND / "src" / "data" / "projects-fallback.json"

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"

# Hue accents per category key (r, g, b)
CATEGORY_ACCENTS = {
    "ai": (168, 85, 247),        # purple
    "mobile": (34, 197, 94),     # green
    "bot": (56, 189, 248),       # sky
    "desktop": (251, 146, 60),   # orange
    "security": (244, 63, 94),   # rose
    "edu": (250, 204, 21),       # yellow
    "tools": (148, 163, 184),    # slate
    "web": (99, 102, 241),       # indigo
}


def category_key(category: str) -> str:
    c = category.lower()
    if "ai" in c or "ml" in c:
        return "ai"
    if "mobil" in c:
        return "mobile"
    if "bot" in c:
        return "bot"
    if "desktop" in c:
        return "desktop"
    if "kiber" in c or "siem" in c or "security" in c:
        return "security"
    if "bmi" in c or "kurs" in c or "o'quv" in c:
        return "edu"
    if "cli" in c or "skill" in c or "vosita" in c:
        return "tools"
    return "web"


def base_canvas(width: int, height: int, accent: tuple, seed: str) -> Image.Image:
    """Dark vertical gradient with an accent glow and particle field."""
    img = Image.new("RGB", (width, height))
    top = (10, 10, 24)
    bottom = (24, 18, 48)
    for y in range(height):
        t = y / height
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        ImageDraw.Draw(img).line([(0, y), (width, y)], fill=color)

    # Accent glow blob
    glow = Image.new("RGB", (width, height), (0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    rng = random.Random(seed)
    gx, gy = int(width * rng.uniform(0.6, 0.85)), int(height * rng.uniform(0.15, 0.45))
    radius = int(min(width, height) * 0.55)
    glow_draw.ellipse(
        [gx - radius, gy - radius, gx + radius, gy + radius],
        fill=tuple(int(c * 0.55) for c in accent),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius // 2))
    img = Image.blend(img, Image.composite(glow, img, glow.convert("L")), 0.5)

    # Particles
    draw = ImageDraw.Draw(img)
    for _ in range(90):
        x, y = rng.randint(0, width), rng.randint(0, height)
        size = rng.choice([1, 1, 1, 2, 2, 3])
        brightness = rng.randint(90, 220)
        draw.ellipse(
            [x, y, x + size, y + size],
            fill=(brightness, brightness, min(255, brightness + 20)),
        )
    return img


def fit_text(draw, text: str, max_width: int, font_path: str, start: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 16:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(font_path, 16)


def wrap_title(draw, text: str, font_path: str, max_width: int, start: int):
    """Return (lines, font) wrapping at most two lines."""
    font = fit_text(draw, text, max_width * 2, font_path, start)
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]
        font = fit_text(draw, lines[1], max_width, font_path, font.size)
    return lines, font


def draw_pill(draw, xy, text, font, fg=(15, 15, 30), bg=(235, 235, 245)):
    x, y = xy
    pad_x, pad_y = 18, 10
    w = draw.textlength(text, font=font)
    bbox = font.getbbox(text)
    h = bbox[3] - bbox[1]
    draw.rounded_rectangle(
        [x, y, x + w + pad_x * 2, y + h + pad_y * 2], radius=(h + pad_y * 2) // 2, fill=bg
    )
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=fg)


def project_cover(slug: str, title: str, category: str):
    accent = CATEGORY_ACCENTS[category_key(category)]
    img = base_canvas(1200, 800, accent, slug)
    draw = ImageDraw.Draw(img)

    lines, font = wrap_title(draw, title, FONT_BOLD, 1000, 76)
    total_height = sum(font.getbbox(line)[3] for line in lines) + 10 * (len(lines) - 1)
    y = (800 - total_height) // 2 + 40
    for line in lines:
        draw.text((100, y), line, font=font, fill=(245, 245, 250))
        y += font.getbbox(line)[3] + 10

    pill_font = ImageFont.truetype(FONT_REGULAR, 26)
    draw_pill(draw, (100, y + 24), category, pill_font)

    brand_font = ImageFont.truetype(FONT_BOLD, 24)
    draw.text((100, 720), "ULUG'BEK KUDRATULLAYEV", font=brand_font, fill=accent)

    img.save(GENERATED / f"{slug}.png", optimize=True)


def category_cover(key: str):
    accent = CATEGORY_ACCENTS[key]
    img = base_canvas(1200, 800, accent, f"cat-{key}")
    draw = ImageDraw.Draw(img)
    label = {
        "ai": "AI / ML",
        "mobile": "Mobile App",
        "bot": "Telegram Bot",
        "desktop": "Desktop App",
        "security": "Cybersecurity",
        "edu": "Education",
        "tools": "Developer Tool",
        "web": "Web Platform",
    }[key]
    font = ImageFont.truetype(FONT_BOLD, 84)
    w = draw.textlength(label, font=font)
    draw.text(((1200 - w) // 2, 330), label, font=font, fill=(240, 240, 248))
    brand_font = ImageFont.truetype(FONT_BOLD, 24)
    draw.text((100, 720), "ULUG'BEK KUDRATULLAYEV", font=brand_font, fill=accent)
    img.save(GENERATED / f"cat-{key}.png", optimize=True)


def nav_preview(name: str, label: str):
    accent = CATEGORY_ACCENTS["web"]
    img = base_canvas(1200, 800, accent, f"nav-{name}")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, 110)
    w = draw.textlength(label, font=font)
    draw.text(((1200 - w) // 2, 310), label, font=font, fill=(240, 240, 248))
    sub_font = ImageFont.truetype(FONT_REGULAR, 30)
    sub = "bekfolio · portfolio"
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((1200 - sw) // 2, 460), sub, font=sub_font, fill=(150, 150, 180))
    (ASSETS / "nav-link-previews").mkdir(parents=True, exist_ok=True)
    img.save(ASSETS / "nav-link-previews" / f"{name}.png", optimize=True)


def og_image():
    accent = CATEGORY_ACCENTS["ai"]
    img = base_canvas(1200, 630, accent, "og-image")
    draw = ImageDraw.Draw(img)
    name_font = ImageFont.truetype(FONT_BOLD, 72)
    draw.text((90, 200), "Ulug'bek", font=name_font, fill=(245, 245, 250))
    draw.text((90, 285), "Kudratullayev", font=name_font, fill=(245, 245, 250))
    role_font = ImageFont.truetype(FONT_REGULAR, 34)
    draw.text(
        (90, 400),
        "Data Scientist · ML Engineer · Software Developer",
        font=role_font,
        fill=(170, 170, 200),
    )
    (ASSETS / "seo").mkdir(parents=True, exist_ok=True)
    img.save(ASSETS / "seo" / "og-image.png", optimize=True)


def avatar():
    img = Image.new("RGB", (600, 600), (16, 14, 36))
    draw = ImageDraw.Draw(img)
    accent = CATEGORY_ACCENTS["ai"]
    for i in range(300, 0, -4):
        t = i / 300
        color = tuple(int(c * (0.25 + 0.45 * (1 - t))) for c in accent)
        draw.ellipse([300 - i, 300 - i, 300 + i, 300 + i], fill=color)
    font = ImageFont.truetype(FONT_BOLD, 220)
    text = "UK"
    w = draw.textlength(text, font=font)
    bbox = font.getbbox(text)
    draw.text(
        ((600 - w) // 2, (600 - (bbox[3] - bbox[1])) // 2 - bbox[1]),
        text,
        font=font,
        fill=(245, 245, 250),
    )
    img.save(ASSETS / "me.jpg", quality=92)


def main():
    GENERATED.mkdir(parents=True, exist_ok=True)
    projects = json.loads(FALLBACK.read_text(encoding="utf-8"))

    featured = [p for p in projects if p["is_featured"]]
    for p in featured:
        project_cover(p["slug"], p["title"], p["category"])
    print(f"covers: {len(featured)}")

    for key in CATEGORY_ACCENTS:
        category_cover(key)
    print("category placeholders: 8")

    for name, label in [
        ("landing", "Home"),
        ("about", "About"),
        ("skills", "Skills"),
        ("projects", "Projects"),
        ("blog", "All Projects"),
        ("contact", "Contact"),
    ]:
        nav_preview(name, label)
    print("nav previews: 6")

    og_image()
    avatar()
    print("og-image + avatar done")


if __name__ == "__main__":
    main()
