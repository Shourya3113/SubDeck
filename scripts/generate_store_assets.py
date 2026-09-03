#!/usr/bin/env python3
"""
Generate Chrome Web Store Promotional Banners using the new premium icon:
- Small Promo Tile: 440x280 px
- Marquee Promo Tile: 1400x560 px
"""

import os
from PIL import Image, ImageDraw, ImageFont

def draw_small_promo(icon_img, output_path):
    w, h = 440, 280
    canvas = Image.new('RGBA', (w, h), (10, 14, 23, 255))
    draw = ImageDraw.Draw(canvas)

    # Place resized icon on the left
    icon_resized = icon_img.resize((150, 150), Image.Resampling.LANCZOS)
    canvas.paste(icon_resized, (25, 45), icon_resized if icon_resized.mode == 'RGBA' else None)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
        font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    draw.text((195, 55), "SubDeck", font=font_title, fill=(255, 255, 255, 255))
    draw.text((195, 95), "Smart Subscription Folders", font=font_sub, fill=(160, 185, 220, 255))
    draw.text((195, 115), "for YouTube™", font=font_sub, fill=(62, 166, 255, 255))

    # Feature tags
    pills = [("📁 Folders", (30, 45, 70)), ("✨ AI Clustering", (18, 55, 85)), ("🎯 Feed Filter", (45, 30, 55))]
    px = 195
    py = 145
    for text, bg in pills:
        bbox = draw.textbbox((0, 0), text, font=font_tag)
        pw = bbox[2] - bbox[0] + 16
        draw.rounded_rectangle([px, py, px + pw, py + 22], radius=11, fill=bg + (255,))
        draw.text((px + 8, py + 4), text, font=font_tag, fill=(230, 240, 255, 255))
        px += pw + 6

    # Bottom bar
    draw.line([(25, 220), (415, 220)], fill=(30, 42, 60, 255), width=1)
    draw.text((25, 235), "🔒 100% Private & Local  •  Zero Data Collection", font=font_tag, fill=(130, 150, 180, 255))

    canvas.save(output_path, "PNG")
    print(f"✅ Created Small Promo Tile: {output_path} (440x280)")

def draw_marquee_promo(icon_img, output_path):
    w, h = 1400, 560
    canvas = Image.new('RGBA', (w, h), (9, 13, 22, 255))
    draw = ImageDraw.Draw(canvas)

    # Place large icon on the left
    icon_resized = icon_img.resize((360, 360), Image.Resampling.LANCZOS)
    canvas.paste(icon_resized, (120, 100), icon_resized if icon_resized.mode == 'RGBA' else None)

    try:
        font_huge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 76)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
        font_pill = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except Exception:
        font_huge = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_pill = ImageFont.load_default()

    draw.text((540, 140), "SubDeck ⚡", font=font_huge, fill=(255, 255, 255, 255))
    draw.text((545, 235), "Smart Subscription Folders for YouTube™", font=font_sub, fill=(160, 185, 220, 255))

    pills = [
        "📁 Native Sidebar Accordion Folders",
        "✨ AI Channel Clustering (Gemini)",
        "🎯 Feed Filtering & Infinite Scroll",
        "🔒 100% Private & Local Storage"
    ]
    px = 545
    py = 310
    for p in pills:
        bbox = draw.textbbox((0, 0), p, font=font_pill)
        pw = bbox[2] - bbox[0] + 24
        draw.rounded_rectangle([px, py, px + pw, py + 38], radius=19, fill=(22, 36, 58, 255))
        draw.text((px + 12, py + 8), p, font=font_pill, fill=(220, 235, 255, 255))
        px += pw + 14
        if px > 1220:
            px = 545
            py += 52

    canvas.save(output_path, "PNG")
    print(f"✅ Created Marquee Promo Tile: {output_path} (1400x560)")

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_src = os.path.join(root, 'assets', 'icons', 'icon128.png')
    store_dir = os.path.join(root, 'assets', 'store')
    os.makedirs(store_dir, exist_ok=True)

    icon_img = Image.open(icon_src).convert('RGBA')
    draw_small_promo(icon_img, os.path.join(store_dir, 'promo_small_440x280.png'))
    draw_marquee_promo(icon_img, os.path.join(store_dir, 'promo_marquee_1400x560.png'))

if __name__ == '__main__':
    main()
