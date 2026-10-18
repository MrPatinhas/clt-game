import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

BRAIN_DIR = Path(r"C:\Users\thiag\.gemini\antigravity-cli\brain\0643bde1-0248-49e5-922d-793e68ff4d6e")
ASSETS_DIR = Path(r"C:\Users\thiag\Documents\CLT\assets")
EMBLEMS_DIR = ASSETS_DIR / "emblems"
POWERUPS_DIR = ASSETS_DIR / "powerups"
RULES_DIR = ASSETS_DIR / "rules"
UI_DIR = ASSETS_DIR / "ui"

for d in [EMBLEMS_DIR, POWERUPS_DIR, RULES_DIR, UI_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Official CLT Palette
CREAM = (253, 251, 247, 255)      # #FDFBF7
AMBER = (249, 160, 63, 255)       # #F9A03F
VERMILION = (224, 83, 60, 255)    # #E0533C
GOLD = (242, 194, 73, 255)        # #F2C249
INK = (46, 42, 39, 255)           # #2E2A27
SAPPHIRE = (58, 134, 200, 255)    # #3A86C8


def extract_brand_logo():
    src = ASSETS_DIR / "Gemini_Generated_Image_wpoozewpoozewpoo.jpg"
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    # Central circular logo occupies the middle square of the 16:9 image
    size = int(min(w, h) * 0.94)
    left = (w - size) // 2
    top = (h - size) // 2
    cropped = img.crop((left, top, left + size, top + size))
    cropped = cropped.resize((512, 512), Image.Resampling.LANCZOS)
    cropped.save(UI_DIR / "clt_logo.png", format="PNG")
    print("-> Saved cropped brand logo to", UI_DIR / "clt_logo.png")


def copy_ai_generated_assets():
    mapping = {
        "squad_a_1792326867696.jpg": EMBLEMS_DIR / "squad_a.png",
        "squad_b_1792326899702.jpg": EMBLEMS_DIR / "squad_b.png",
        "squad_c_1792326935515.jpg": EMBLEMS_DIR / "squad_c.png",
        "squad_d_1792326975445.jpg": EMBLEMS_DIR / "squad_d.png",
        "squad_e_1792327021648.jpg": EMBLEMS_DIR / "squad_e.png",
        "reveal_zeroed_1792326880713.jpg": POWERUPS_DIR / "reveal_zeroed.png",
        "copycat_1792326927984.jpg": POWERUPS_DIR / "copycat.png",
        "grenal_1792327006800.jpg": POWERUPS_DIR / "grenal.png",
        "gabriel_jesus_1792327105101.jpg": RULES_DIR / "gabriel_jesus.png",
        "mano_menezes_1792326870688.jpg": RULES_DIR / "mano_menezes.png",
        "vanderlei_1792326905053.jpg": RULES_DIR / "vanderlei.png",
        "garcom_1792326942063.jpg": RULES_DIR / "garcom.png",
        "buda_1792326982087.jpg": RULES_DIR / "buda.png",
        "open_capitao_1792327044842.jpg": RULES_DIR / "open_capitao.png",
    }
    for src_name, dst_path in mapping.items():
        src_path = BRAIN_DIR / src_name
        if src_path.exists():
            im = Image.open(src_path).convert("RGBA")
            im = im.resize((512, 512), Image.Resampling.LANCZOS)
            im.save(dst_path, format="PNG")
            print(f"-> Saved AI-generated {dst_path.relative_to(ASSETS_DIR)}")


def draw_gear(draw, cx, cy, r_outer, r_inner, teeth, fill_color, outline_color=INK, width=5):
    pts = []
    steps = teeth * 4
    for i in range(steps):
        ang = (2 * math.pi * i) / steps
        r = r_outer if (i % 4 in (0, 1)) else r_inner
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill_color, outline=outline_color, width=width)
    hole_r = r_inner * 0.45
    draw.ellipse((cx - hole_r, cy - hole_r, cx + hole_r, cy + hole_r), fill=CREAM, outline=outline_color, width=width)


def build_remaining_4_illustrations():
    """
    Creates the 4 remaining illustrations (squad_f, squad_g, felipe_melo, futsal)
    by combining authentic steampunk medallion textures from our AI-generated set
    with bespoke hand-styled ink-and-watercolor overlays in the exact 6-color CLT palette.
    """
    # 1. Squad F — Vórtice de Cronos (Temporal Sapphire & Amber Vortex)
    base_b = Image.open(EMBLEMS_DIR / "squad_b.png").convert("RGBA")
    base_c = Image.open(EMBLEMS_DIR / "squad_c.png").convert("RGBA")
    # Rotate and color-shift into a deep sapphire-amber temporal vortex
    vortex = base_b.rotate(180, resample=Image.Resampling.BICUBIC)
    r, g, b, a = vortex.split()
    # Swap warm/cool emphasis for distinct sapphire-vortex identity
    vortex = Image.merge("RGBA", (b, g, r, a))
    # Blend outer parchment ring from base_b so background remains #FDFBF7
    mask = Image.new("L", (512, 512), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((68, 68, 444, 444), fill=220)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    squad_f = Image.composite(vortex, base_b, mask)
    draw_f = ImageDraw.Draw(squad_f)
    # Add swirling sapphire & amber vortex rings + clock hands
    for rad, col in [(165, SAPPHIRE), (130, AMBER), (95, GOLD)]:
        draw_f.arc((256 - rad, 256 - rad, 256 + rad, 256 + rad), start=20, end=310, fill=col, width=7)
    draw_f.Save = None
    squad_f.save(EMBLEMS_DIR / "squad_f.png", format="PNG")
    print("-> Saved emblems/squad_f.png")

    # 2. Squad G — Oráculo Eterno (Mystical Pocket-Watch Eye & Golden Astrolabe)
    squad_g = base_c.copy()
    inner_rot = base_c.rotate(90, resample=Image.Resampling.BICUBIC)
    squad_g = Image.composite(inner_rot, squad_g, mask)
    draw_g = ImageDraw.Draw(squad_g)
    # Draw ornate golden eye-of-time medallion in center
    draw_g.polygon([(146, 256), (256, 190), (366, 256), (256, 322)], fill=CREAM, outline=INK, width=6)
    draw_g.ellipse((212, 212, 300, 300), fill=SAPPHIRE, outline=INK, width=6)
    draw_g.ellipse((236, 236, 276, 276), fill=GOLD, outline=INK, width=5)
    draw_g.ellipse((248, 248, 264, 264), fill=INK)
    squad_g.save(EMBLEMS_DIR / "squad_g.png", format="PNG")
    print("-> Saved emblems/squad_g.png")

    # 3. Crazy Rule — Regra de Felipe Melo (Cards Are Glory / Gladiator Crest)
    grenal_im = Image.open(POWERUPS_DIR / "grenal.png").convert("RGBA")
    fm_im = grenal_im.copy()
    draw_fm = ImageDraw.Draw(fm_im)
    # Draw giant heroic Yellow & Red Referee Cards crowned in gold in the center
    draw_gear(draw_fm, 256, 256, 135, 112, 12, GOLD, INK, width=6)
    # Left Tilted Yellow Card (#F2C249)
    card_y = [(175, 170), (245, 155), (265, 295), (195, 310)]
    draw_fm.polygon(card_y, fill=GOLD, outline=INK, width=6)
    # Right Tilted Red Card (#E0533C)
    card_r = [(245, 165), (320, 180), (300, 320), (225, 305)]
    draw_fm.polygon(card_r, fill=VERMILION, outline=INK, width=6)
    # Golden Trophy Star in center
    star_pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 38 if i % 2 == 0 else 16
        star_pts.append((256 + rad * math.cos(ang), 252 + rad * math.sin(ang)))
    draw_fm.polygon(star_pts, fill=AMBER, outline=INK, width=4)
    fm_im.save(RULES_DIR / "felipe_melo.png", format="PNG")
    print("-> Saved rules/felipe_melo.png")

    # 4. Crazy Rule — Regra do Futsal (Tiki-Taka Geometric Court & Broken Offside Flag)
    gj_im = Image.open(RULES_DIR / "gabriel_jesus.png").convert("RGBA")
    fut_im = gj_im.copy()
    draw_fut = ImageDraw.Draw(fut_im)
    # Draw vintage amber futsal court inside the steampunk medallion
    draw_fut.rounded_rectangle((116, 156, 396, 356), radius=18, fill=AMBER, outline=INK, width=7)
    draw_fut.rectangle((132, 172, 380, 340), fill= None, outline=CREAM, width=4)
    draw_fut.line((256, 172, 256, 340), fill=CREAM, width=4)
    draw_fut.ellipse((216, 216, 296, 296), outline=CREAM, width=4)
    # Geometric sapphire tiki-taka passing lines & nodes
    nodes = [(165, 210), (235, 195), (295, 255), (210, 305), (345, 225)]
    for i in range(len(nodes) - 1):
        draw_fut.line([nodes[i], nodes[i + 1]], fill=SAPPHIRE, width=7)
    for nx, ny in nodes:
        draw_fut.ellipse((nx - 14, ny - 14, nx + 14, ny + 14), fill=GOLD, outline=INK, width=4)
    fut_im.save(RULES_DIR / "futsal.png", format="PNG")
    print("-> Saved rules/futsal.png")


if __name__ == "__main__":
    extract_brand_logo()
    copy_ai_generated_assets()
    build_remaining_4_illustrations()
