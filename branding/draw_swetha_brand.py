from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "swetha-master-logo.png"
OUT = ROOT
PAPER = "#fcfcfa"
ORANGE = "#ff5a00"
INK = "#111111"


def crop_alpha(image):
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def fit_square(image, size, background=(0, 0, 0, 0), padding=0.12):
    canvas = Image.new("RGBA", (size, size), background)
    max_side = int(size * (1 - 2 * padding))
    scale = min(max_side / image.width, max_side / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    return canvas


def main():
    src = Image.open(SOURCE).convert("RGBA")
    logo = crop_alpha(src)
    profile = fit_square(logo, 1024)
    profile.save(OUT / "swetha-profile-1024.png")

    # The S mark is the left portion of the supplied master logo.
    mark = src.crop((70, 350, 500, 900))
    mark = crop_alpha(mark)
    s = fit_square(mark, 1024)
    s.save(OUT / "swetha-s-1024.png")
    s.resize((180, 180), Image.Resampling.LANCZOS).save(OUT / "swetha-apple-touch-icon.png")
    s.resize((192, 192), Image.Resampling.LANCZOS).save(OUT / "swetha-192.png")
    s.resize((512, 512), Image.Resampling.LANCZOS).save(OUT / "swetha-512.png")

    for size in (192, 512):
        fit_square(mark, size, (252, 252, 250, 255), 0.22).save(OUT / f"swetha-maskable-{size}.png")

    card = Image.new("RGB", (1200, 630), PAPER)
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, 1200, 14), fill=ORANGE)
    small_logo = logo.resize((400, round(400 * logo.height / logo.width)), Image.Resampling.LANCZOS)
    card.paste(small_logo, (65, 115), small_logo)
    bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    normal = ImageFont.truetype("DejaVuSans.ttf", 28)
    small = ImageFont.truetype("DejaVuSans.ttf", 21)
    draw.text((545, 115), "Swetha Senthilkumar", font=bold, fill=INK)
    draw.text((545, 190), "Semiconductor Engineering Student", font=normal, fill=INK)
    draw.text((545, 235), "Tech Innovator · Student Leader", font=normal, fill=INK)
    draw.text((545, 315), "Projects · Engineering · Communication", font=small, fill=ORANGE)
    draw.text((545, 350), "Wired & Inspired", font=small, fill=ORANGE)
    card.save(OUT / "swetha-og-1200x630.png", quality=95)


if __name__ == "__main__":
    main()
