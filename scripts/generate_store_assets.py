#!/usr/bin/env python3
"""
Generate Chrome Web Store Promotional Banners:
- Small Promo Tile: 440x280 px (Required for search/category featuring)
- Marquee Promo Tile: 1400x560 px (Featured banner)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_gradient(width, height, start_color, end_color):
    """Create a vertical gradient image."""
    base = Image.new('RGBA', (width, height), start_color)
    top = Image.new('RGBA', (width, height), end_color)
    mask = Image.new('L', (width, height))
    for y in range(height):
        # Subtle diagonal curve
        val = int(255 * (y / height))
        for x in range(width):
            mask.putpixel((x, y), min(255, max(0, val)))
    return Image.composite(top, base, mask)

def draw_small_promo(output_path):
    w, h = 440, 280
    img = create_gradient(w, h, (11, 15, 25, 255), (20, 30, 48, 255))
    draw = ImageDraw.Draw(img)

    # Decorative glow circle behind logo
    for r in range(80, 0, -2):
        alpha = int(25 * (1 - r / 80))
        draw.ellipse([70 - r, 90 - r, 70 + r, 90 + r], fill=(62, 166, 255, alpha))

    # Lightning Icon (⚡)
    lightning_points = [
        (65, 52), (82, 52), (72, 85), (88, 85), (55, 128), (62, 95), (48, 95)
    ]
    draw.polygon(lightning_points, fill=(62, 166, 255, 255))

    # Title: SubDeck
    # Fallback to default font or system fonts
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 38)
        font_tagline = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
        font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_tagline = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    draw.text((105, 60), "SubDeck", font=font_title, fill=(255, 255, 255, 255))
    draw.text((105, 102), "Smart Subscription Folders", font=font_tagline, fill=(160, 175, 200, 255))

    # Subtext / Feature pills
    pill_y = 155
    features = [
        ("📁 Category Decks", (40, 50, 70), (220, 230, 245)),
        ("✨ AI Auto-Organize", (20, 60, 90), (100, 200, 255)),
        ("🎯 Custom Feed", (50, 30, 60), (245, 180, 220)),
    ]

    pill_x = 35
    for text, bg_col, text_col in features:
        bbox = draw.textbbox((0, 0), text, font=font_badge)
        pw = bbox[2] - bbox[0] + 16
        ph = 26
        draw.rounded_rectangle([pill_x, pill_y, pill_x + pw, pill_y + ph], radius=13, fill=bg_col + (255,))
        draw.text((pill_x + 8, pill_y + 6), text, font=font_badge, fill=text_col)
        pill_x += pw + 8

    # Bottom privacy claim
    draw.line([(35, 215), (405, 215)], fill=(40, 50, 70, 255), width=1)
    draw.text((35, 230), "🔒 100% Private & Local  •  Works natively in YouTube™", font=font_badge, fill=(120, 135, 160, 255))

    img.save(output_path, "PNG")
    print(f"✅ Created Small Promo Tile: {output_path} (440x280)")

def draw_marquee_promo(output_path):
    w, h = 1400, 560
    img = create_gradient(w, h, (10, 14, 23, 255), (18, 26, 42, 255))
    draw = ImageDraw.Draw(img)

    # Ambient radial glow
    for r in range(250, 0, -4):
        alpha = int(30 * (1 - r / 250))
        draw.ellipse([250 - r, 240 - r, 250 + r, 240 + r], fill=(62, 166, 255, alpha))

    # Large Lightning Icon
    scale = 3.2
    ox, oy = 160, 130
    pts = [
        (ox + 65*scale, oy + 52*scale),
        (ox + 82*scale, oy + 52*scale),
        (ox + 72*scale, oy + 85*scale),
        (ox + 88*scale, oy + 85*scale),
        (ox + 55*scale, oy + 128*scale),
        (ox + 62*scale, oy + 95*scale),
        (ox + 48*scale, oy + 95*scale)
    ]
    draw.polygon(pts, fill=(62, 166, 255, 255))

    try:
        font_huge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 92)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
        font_pill = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    except Exception:
        font_huge = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_pill = ImageFont.load_default()

    draw.text((500, 150), "SubDeck ⚡", font=font_huge, fill=(255, 255, 255, 255))
    draw.text((505, 260), "Smart Subscription Folders for YouTube™", font=font_sub, fill=(160, 185, 220, 255))

    # Feature tags
    pills = [
        "📁 Accordion Sidebar Folders",
        "✨ AI-Powered Channel Clustering",
        "🎯 Feed Filtering & Infinite Scroll",
        "🔒 100% Private (No Tracking)"
    ]
    px = 505
    py = 340
    for p in pills:
        bbox = draw.textbbox((0, 0), p, font=font_pill)
        pw = bbox[2] - bbox[0] + 24
        draw.rounded_rectangle([px, py, px + pw, py + 42], radius=21, fill=(25, 40, 65, 255))
        draw.text((px + 12, py + 9), p, font=font_pill, fill=(220, 235, 255, 255))
        px += pw + 16
        if px > 1200:
            px = 505
            py += 56

    img.save(output_path, "PNG")
    print(f"✅ Created Marquee Promo Tile: {output_path} (1400x560)")

def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'store')
    os.makedirs(assets_dir, exist_ok=True)

    draw_small_promo(os.path.join(assets_dir, 'promo_small_440x280.png'))
    draw_marquee_promo(os.path.join(assets_dir, 'promo_marquee_1400x560.png'))

if __name__ == '__main__':
    main()
