#!/usr/bin/env python3
"""Render the VELUMBRA travel poster with Pillow.

VELUMBRA — a harbour city terraced into a white salt cliff on a tidal
strait, famous for its Second Dawn: the sun rises over the sea, sets
behind the cliff for twenty minutes, then rises again, reflected and
real, off the salt face. Landmark: the Lantern Stair, a lighthouse
climbed by 214 steps cut into the cliff.

Drawn entirely in code: gradient sky, two suns, layered salt cliff,
terraced houses, lighthouse, ferry, gulls, vintage grain. Output is a
768x1024 PNG kept well under the 1 MiB gate.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 768, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Palette — vintage travel poster: cream, coral, teal, ink navy.
CREAM = (246, 234, 205)
PEACH = (244, 178, 120)
CORAL = (224, 92, 62)
CORAL_D = (178, 62, 44)
GOLD = (238, 176, 74)
TEAL = (26, 96, 104)
TEAL_D = (16, 62, 74)
TEAL_L = (64, 140, 138)
INK = (24, 38, 54)
SALT = (250, 244, 228)
SALT_SH = (226, 208, 178)
WHITE = (255, 252, 244)


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def centered(draw, cx, y, text, fnt, fill, spacing=0):
    if spacing:
        x = cx - sum(draw.textlength(ch, font=fnt) + spacing for ch in text) / 2 + spacing / 2
        for ch in text:
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += draw.textlength(ch, font=fnt) + spacing
        return
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def main():
    rng = random.Random(214)
    # --- sky: cream at top warming to peach at the horizon -------------
    img = vgrad((W, H), (250, 240, 214), (247, 196, 128))
    d = ImageDraw.Draw(img, "RGBA")

    horizon = 640

    # --- first sun: low, huge, coral, sitting on the horizon -----------
    sun_cx, sun_cy, sun_r = 500, horizon - 118, 118
    for r, col in [(sun_r + 26, (244, 150, 92, 70)), (sun_r + 12, (240, 128, 80, 90))]:
        d.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r], fill=col)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], fill=CORAL)
    d.ellipse([sun_cx - sun_r + 16, sun_cy - sun_r + 14, sun_cx + sun_r - 30, sun_cy + sun_r - 60],
              fill=(232, 110, 72))

    # --- sea ------------------------------------------------------------
    sea = vgrad((W, H - horizon), TEAL_L, TEAL_D)
    img.paste(sea, (0, horizon))
    d = ImageDraw.Draw(img, "RGBA")
    # sun path glitter on the water
    for i in range(90):
        y = horizon + 8 + int((i / 90) ** 1.4 * (H - horizon - 190))
        spread = 26 + (y - horizon) * 0.55
        x = sun_cx + rng.uniform(-spread, spread)
        ln = rng.uniform(10, 44) * (0.5 + (y - horizon) / 300)
        d.line([x - ln / 2, y, x + ln / 2, y], fill=(250, 205, 130, 150), width=3)

    # --- the salt cliff: one great layered headland, left ---------------
    cliff = [(0, 300), (86, 268), (196, 252), (292, 286), (338, 360),
             (352, 470), (330, 590), (296, horizon + 6), (0, horizon + 6)]
    d.polygon(cliff, fill=SALT)
    # strata bands, clipped to the cliff silhouette so they can never
    # spill past its edge
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(cliff, fill=255)
    bands = Image.new("RGB", (W, H), SALT)
    bd = ImageDraw.Draw(bands)
    for y0, col in [(352, SALT_SH), (416, (236, 220, 192)), (482, SALT_SH),
                    (548, (232, 214, 184)), (606, SALT_SH)]:
        bd.rectangle([0, y0, W, y0 + 26], fill=col)
    img.paste(bands, (0, 0), mask)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(cliff, outline=(198, 176, 140), width=3)
    # second dawn: the cliff face catches the light — a bright reflected
    # disc, the famous second sunrise, low on the salt face
    d.ellipse([62, 478, 146, 562], fill=(250, 214, 140, 235))
    d.ellipse([78, 494, 130, 546], fill=(252, 232, 170, 255))

    # --- terraced houses climbing the cliff ------------------------------
    houses = [(36, 300, 44, 34), (96, 282, 38, 30), (150, 292, 42, 32),
              (58, 348, 40, 30), (118, 336, 36, 28), (182, 330, 40, 30),
              (84, 398, 38, 28), (146, 388, 34, 26), (206, 372, 38, 28),
              (120, 448, 36, 26), (180, 436, 34, 26), (238, 420, 34, 26)]
    roof_cols = [CORAL_D, TEAL_D, (150, 84, 52)]
    for i, (x, y, w, h) in enumerate(houses):
        d.rectangle([x, y, x + w, y + h], fill=(252, 246, 230))
        d.polygon([(x - 4, y), (x + w / 2, y - 13), (x + w + 4, y)], fill=roof_cols[i % 3])
        d.rectangle([x + w / 2 - 4, y + h - 14, x + w / 2 + 4, y + h], fill=INK)
        d.rectangle([x + 6, y + 8, x + 13, y + 15], fill=GOLD)

    # --- the Lantern Stair lighthouse on the point -----------------------
    lx, lbase = 316, horizon + 2
    d.polygon([(lx - 34, lbase), (lx + 30, lbase), (lx + 12, 408), (lx - 16, 408)], fill=(250, 246, 234))
    for yy, ww in [(452, 24), (508, 28), (564, 31)]:
        d.rectangle([lx - ww + 2, yy, lx + ww - 6, yy + 22], fill=CORAL)
    d.rectangle([lx - 22, 384, lx + 20, 408], fill=INK)          # lantern room
    d.ellipse([lx - 16, 388, lx + 14, 406], fill=(252, 226, 150, 120))  # glow
    d.ellipse([lx - 7, 392, lx + 5, 402], fill=GOLD)            # lamp
    d.polygon([(lx - 26, 384), (lx - 1, 362), (lx + 24, 384)], fill=CORAL_D)  # cap
    # light beams
    d.polygon([(lx - 1, 397), (lx - 190, 330), (lx - 196, 372)], fill=(252, 226, 150, 90))
    d.polygon([(lx - 1, 397), (lx + 210, 356), (lx + 204, 396)], fill=(252, 226, 150, 70))
    # the stair: a zigzag cut down the cliff point to the quay
    sx, sy = lx - 30, 470
    pts = [(sx, sy)]
    for i in range(6):
        sx -= 16
        pts.append((sx, sy))
        sy += 26
        pts.append((sx, sy))
    d.line(pts, fill=INK, width=4)

    # --- distant headland, right -----------------------------------------
    d.polygon([(598, horizon), (668, 556), (724, 574), (768, 560), (768, horizon)],
              fill=(44, 106, 110))
    d.polygon([(598, horizon), (668, 556), (724, 574), (768, 560), (768, 596),
               (700, 610), (640, 604), (598, horizon)], fill=(36, 92, 98))

    # --- ferry crossing to the city ---------------------------------------
    fx, fy = 520, 716
    d.polygon([(fx - 74, fy), (fx + 78, fy), (fx + 56, fy + 22), (fx - 52, fy + 22)], fill=INK)
    d.rectangle([fx - 52, fy - 26, fx + 48, fy], fill=WHITE)
    d.rectangle([fx - 30, fy - 44, fx + 26, fy - 26], fill=WHITE)
    d.rectangle([fx + 34, fy - 52, fx + 44, fy - 26], fill=CORAL_D)
    for wx in range(fx - 44, fx + 42, 16):
        d.rectangle([wx, fy - 20, wx + 8, fy - 10], fill=GOLD)
    d.line([fx - 130, fy + 30, fx - 60, fy + 26], fill=(255, 255, 255, 160), width=3)
    d.line([fx - 150, fy + 40, fx - 84, fy + 36], fill=(255, 255, 255, 110), width=3)

    # --- gulls -------------------------------------------------------------
    for gx, gy, s in [(452, 268, 14), (548, 288, 10), (648, 300, 12), (690, 262, 9), (420, 312, 9)]:
        d.arc([gx - s, gy - s // 2, gx, gy + s // 2], 200, 330, fill=INK, width=3)
        d.arc([gx, gy - s // 2, gx + s, gy + s // 2], 210, 340, fill=INK, width=3)

    # --- foreground quay silhouette ----------------------------------------
    d.rectangle([0, H - 148, W, H], fill=INK)
    d.rectangle([0, H - 148, W, H - 140], fill=CORAL)
    # lamp posts on the quay
    for px_ in (70, 690):
        d.line([px_, H - 148, px_, H - 196], fill=INK, width=5)
        d.ellipse([px_ - 8, H - 212, px_ + 8, H - 196], fill=GOLD)

    # --- typography ----------------------------------------------------------
    centered(d, W / 2, 36, "THE CITY OF THE SECOND DAWN", font(SANS_B, 25), TEAL_D, spacing=6)
    centered(d, W / 2, 66, "VELUMBRA", font(SERIF_B, 104), INK)
    d.line([120, 196, W - 120, 196], fill=CORAL_D, width=3)
    centered(d, W / 2, 208, "Arrive for the first sunrise.  Stay for the second.",
             font(SERIF, 27), (58, 52, 44))

    # bottom band copy — concrete details that reward a close look
    centered(d, W / 2, H - 128, "FESTIVAL OF THE SECOND DAWN  ·  14–21 JUNE", font(SANS_B, 22), CREAM)
    centered(d, W / 2, H - 96,
             "Ferries from Port Serein 06:10 · 09:40 · 15:20 — Lantern Stair, 214 steps",
             font(SANS, 18), (214, 222, 224))
    centered(d, W / 2, H - 66,
             "Last ferry leaves before the tide forgets the way home",
             font(SERIF, 19), GOLD)
    centered(d, W / 2, H - 36, "VELUMBRA SALT LINE  ·  EST. 1911", font(SANS_B, 15), (168, 182, 186), spacing=3)

    # --- border + grain -------------------------------------------------------
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=4)
    d.rectangle([24, 24, W - 24, H - 24], outline=(24, 38, 54, 120), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    # subtle print grain: a faint noise layer blended over the top
    grain = Image.new("L", (W, H))
    gp = grain.load()
    for y in range(H):
        for x in range(W):
            gp[x, y] = rng.randint(96, 160)
    img = Image.blend(img, grain.convert("RGB"), 0.05)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
