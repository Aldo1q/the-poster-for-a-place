#!/usr/bin/env python3
"""Render the VELUMBRA travel poster entirely in code with PIL.

VELUMBRA, the City of the Second Dawn: a harbour city terraced into a
white salt cliff on a tidal strait where the sun rises twice -- once over
the sea, then again as a pale reflection off the salt face. Landmark: the
Lantern Stair, a coral-striped lighthouse reached by 214 steps cut into
the rock, with the Port Serein ferry crossing below.

Output: entry.png, 768 x 1024, under 1,048,576 bytes.
Palette: cream/peach sky, coral sun, teal sea, ink-navy type.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 768, 1024

INK = (16, 32, 54)
CREAM = (255, 243, 214)
PEACH = (255, 205, 150)
CORAL = (240, 96, 64)
CORAL_DARK = (198, 66, 44)
TEAL = (18, 110, 116)
TEAL_DEEP = (10, 74, 88)
SALT = (250, 246, 236)
SALT_SHADE = (226, 216, 196)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw letterspaced text centred on cx; return its total width."""
    widths = []
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=fnt)
        widths.append(bbox[2] - bbox[0])
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def gradient(size, top, bottom):
    """Vertical two-stop gradient image."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for yy in range(h):
        t = yy / max(1, h - 1)
        px_row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for xx in range(w):
            px[xx, yy] = px_row
    return img


def build_poster():
    # ---- sky: cream at top warming to peach at the horizon -------------
    img = gradient((W, H), (255, 246, 218), (255, 196, 138))
    draw = ImageDraw.Draw(img, "RGBA")

    horizon = 618

    # ---- sea: teal block below the horizon, left of the cliff ----------
    sea = gradient((W, H - horizon), (32, 138, 142), TEAL_DEEP)
    img.paste(sea, (0, horizon))
    draw = ImageDraw.Draw(img, "RGBA")
    # sun glitter path on the water
    grng = random.Random(42)
    for i in range(40):
        yy = horizon + 16 + i * 7
        half = grng.randint(8, 26) + i // 3
        cx = 218 + int(26 * math.sin(i * 0.55)) + grng.randint(-14, 14)
        draw.line([(cx - half, yy), (cx + half, yy)],
                  fill=(255, 226, 170, 105), width=2)

    # ---- first sun: the coral sun rising over the sea ------------------
    sun_c = (218, 470)
    sun_r = 104
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in ((190, 26), (158, 40), (128, 58)):
        gd.ellipse([sun_c[0] - r, sun_c[1] - r, sun_c[0] + r, sun_c[1] + r],
                   fill=(255, 150, 96, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    glow.filter(ImageFilter.GaussianBlur(18))
                                    ).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse([sun_c[0] - sun_r, sun_c[1] - sun_r,
                  sun_c[0] + sun_r, sun_c[1] + sun_r], fill=CORAL + (255,))
    draw.ellipse([sun_c[0] - sun_r + 14, sun_c[1] - sun_r + 12,
                  sun_c[0] + sun_r - 30, sun_c[1] + sun_r - 48],
                 fill=(246, 122, 80, 255))

    # ---- the white salt cliff, terraced, right two-thirds --------------
    cliff_poly = [(392, 1024), (452, 700), (508, 520), (560, 408),
                  (640, 330), (768, 300), (768, 1024)]
    cliff_mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(cliff_mask).polygon(cliff_poly, fill=255)
    cliff_img = gradient((W, H), (252, 249, 240), (233, 222, 198))
    img.paste(cliff_img, (0, 0), cliff_mask)
    draw = ImageDraw.Draw(img, "RGBA")

    # strata bands, clipped to the cliff by drawing through the mask
    strata = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(strata)
    rng = random.Random(1911)
    yy = 356
    while yy < 1010:
        band_h = rng.randint(16, 30)
        shade = SALT_SHADE + (rng.randint(60, 110),)
        sd.line([(380, yy), (768, yy - 26)], fill=shade, width=band_h // 2)
        yy += band_h + rng.randint(14, 30)
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    Image.composite(strata, Image.new(
                                        "RGBA", (W, H), (0, 0, 0, 0)),
                                        cliff_mask)).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    # cliff edge highlight
    draw.line(cliff_poly[:6], fill=(255, 255, 250, 255), width=4)

    # ---- second sun: pale disc low on the salt face --------------------
    s2 = (648, 668)
    r2 = 56
    draw.ellipse([s2[0] - r2 - 13, s2[1] - r2 - 13, s2[0] + r2 + 13,
                  s2[1] + r2 + 13], outline=(244, 130, 92, 200), width=5)
    draw.ellipse([s2[0] - r2, s2[1] - r2, s2[0] + r2, s2[1] + r2],
                 fill=(255, 238, 196, 255))
    draw.ellipse([s2[0] - r2 + 10, s2[1] - r2 + 8, s2[0] + r2 - 22,
                  s2[1] + r2 - 30], fill=(255, 246, 218, 255))

    # ---- terraced houses stepping down the cliff -----------------------
    terraces = [(566, 452, 44), (596, 500, 52), (622, 552, 58),
                (540, 560, 40), (648, 612, 62), (576, 636, 46),
                (676, 700, 58), (612, 724, 44), (700, 792, 52),
                (648, 812, 40)]
    roof_cols = [CORAL, TEAL, CORAL_DARK, (214, 132, 60)]
    for i, (hx, hy, hw) in enumerate(terraces):
        hh = int(hw * 0.72)
        draw.rectangle([hx, hy, hx + hw, hy + hh], fill=(252, 248, 238, 255),
                       outline=INK + (255,), width=2)
        rc = roof_cols[i % len(roof_cols)]
        draw.polygon([(hx - 4, hy), (hx + hw + 4, hy),
                      (hx + hw - 8, hy - 13), (hx + 8, hy - 13)],
                     fill=rc + (255,))
        draw.rectangle([hx + hw // 2 - 5, hy + hh - 16, hx + hw // 2 + 5,
                        hy + hh], fill=INK + (255,))
        draw.rectangle([hx + 7, hy + 9, hx + 16, hy + 18],
                       fill=(255, 205, 110, 255))

    # ---- the Lantern Stair lighthouse on the cliff top -----------------
    lx, base_y = 668, 348
    # light beams first, under the tower
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    lamp = (lx, base_y - 118)
    bd.polygon([lamp, (196, 196), (252, 268)], fill=(255, 226, 150, 100))
    bd.polygon([lamp, (768, 196), (768, 230)], fill=(255, 226, 150, 64))
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    beam.filter(ImageFilter.GaussianBlur(6))
                                    ).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    # striped tower: coral and salt bands tapering upward
    bands = 6
    for i in range(bands):
        y0 = base_y - i * 17
        y1 = base_y - (i + 1) * 17
        half0 = 25 - i * 2
        half1 = 25 - (i + 1) * 2
        col = CORAL if i % 2 == 0 else SALT
        draw.polygon([(lx - half0, y0), (lx + half0, y0),
                      (lx + half1, y1), (lx - half1, y1)], fill=col + (255,))
    draw.rectangle([lx - 17, base_y - 122, lx + 17, base_y - 102],
                   fill=INK + (255,))
    draw.ellipse([lx - 8, base_y - 119, lx + 8, base_y - 105],
                 fill=(255, 214, 110, 255))
    draw.polygon([(lx - 21, base_y - 122), (lx + 21, base_y - 122),
                  (lx, base_y - 142)], fill=CORAL_DARK + (255,))
    draw.rectangle([lx - 30, base_y - 4, lx + 30, base_y + 2],
                   fill=INK + (255,))

    # ---- the Lantern Stair: 214 steps zigzagging down the rock ---------
    stair = [(lx - 6, base_y + 2), (612, 428), (668, 486), (600, 548),
             (660, 614), (588, 682), (646, 752), (560, 826), (520, 884)]
    for a, b in zip(stair, stair[1:]):
        draw.line([a, b], fill=(255, 255, 252, 255), width=9)
        draw.line([a, b], fill=INK + (255,), width=2)
    for pt in stair:
        draw.ellipse([pt[0] - 4, pt[1] - 4, pt[0] + 4, pt[1] + 4],
                     fill=CORAL + (255,))

    # ---- Port Serein ferry crossing the strait --------------------------
    fx, fy = 176, 838
    draw.polygon([(fx - 96, fy + 26), (fx + 96, fy + 26), (fx + 70, fy + 52),
                  (fx - 70, fy + 52)], fill=INK + (255,))
    draw.rectangle([fx - 58, fy - 2, fx + 58, fy + 26],
                   fill=(252, 248, 238, 255), outline=INK + (255,), width=2)
    draw.rectangle([fx - 34, fy - 26, fx + 30, fy - 2],
                   fill=(252, 248, 238, 255), outline=INK + (255,), width=2)
    for wx in range(fx - 48, fx + 50, 16):
        draw.rectangle([wx, fy + 6, wx + 8, fy + 15],
                       fill=(255, 205, 110, 255))
    draw.rectangle([fx + 38, fy - 34, fx + 50, fy - 2], fill=CORAL + (255,))
    draw.line([(fx - 120, fy + 62), (fx - 30, fy + 58)], fill=(255, 255, 255, 170), width=3)
    draw.line([(fx - 104, fy + 72), (fx - 16, fy + 67)], fill=(255, 255, 255, 120), width=3)
    draw_tracked(draw, fx, fy + 84, "PORT SEREIN", font(SANS_BOLD, 14),
                 (235, 250, 248, 255), 3)

    # ---- gulls, kept clear of the title block ---------------------------
    for gx, gy, s in ((84, 330, 13), (138, 296, 10), (58, 372, 9),
                      (356, 300, 11), (410, 336, 8)):
        draw.arc([gx - s, gy - s // 2, gx, gy + s // 2], 200, 330,
                 fill=INK + (255,), width=3)
        draw.arc([gx, gy - s // 2, gx + s, gy + s // 2], 210, 340,
                 fill=INK + (255,), width=3)

    # ---- type: headline, strapline, tagline -----------------------------
    draw_tracked(draw, W // 2, 56, "VELUMBRA", font(SERIF_BOLD, 96),
                 INK + (255,), 6)
    draw.line([(150, 180), (618, 180)], fill=CORAL + (255,), width=3)
    draw_tracked(draw, W // 2, 194, "THE CITY OF THE SECOND DAWN",
                 font(SANS_BOLD, 21), INK + (255,), 5)
    draw_tracked(draw, W // 2, 228,
                 "Arrive for the first sunrise. Stay for the second.",
                 font(SERIF_ITALIC, 24), CORAL_DARK + (255,), 0)

    # ---- bottom band: the close-look details ----------------------------
    band_y = 936
    draw.rectangle([0, band_y, W, H], fill=INK + (255,))
    draw.rectangle([0, band_y, W, band_y + 3], fill=CORAL + (255,))
    draw_tracked(draw, W // 2, band_y + 10,
                 "FESTIVAL OF THE SECOND DAWN · 14-21 JUNE",
                 font(SANS_BOLD, 16), CREAM + (255,), 2)
    draw_tracked(draw, W // 2, band_y + 36,
                 "PORT SEREIN FERRIES  06:10 · 09:40 · 15:20",
                 font(SANS, 15), (196, 226, 224, 255), 1)
    draw_tracked(draw, W // 2, band_y + 58,
                 "Last ferry leaves before the tide forgets the way home",
                 font(SERIF_ITALIC, 15), PEACH + (255,), 0)

    # ---- frame -----------------------------------------------------------
    draw.rectangle([10, 10, W - 10, H - 10], outline=INK + (255,), width=3)
    draw.rectangle([17, 17, W - 17, H - 17], outline=INK + (160,), width=1)
    draw_tracked(draw, W // 2, 22, "VELUMBRA SALT LINE · EST. 1911",
                 font(SANS_BOLD, 11), (70, 84, 96, 255), 3)

    return img, horizon


def add_grain(img, seed=7, strength=9):
    """Fine print grain: subtle, never a wash over the whole poster."""
    rng = random.Random(seed)
    noise = Image.new("L", (W, H))
    noise.putdata([rng.randint(128 - strength, 128 + strength)
                   for _ in range(W * H)])
    grey = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, grey, 0.05)


if __name__ == "__main__":
    poster, _ = build_poster()
    poster = add_grain(poster)
    poster.save("entry.png", optimize=True)
    print("wrote entry.png", poster.size)
