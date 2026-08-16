#!/usr/bin/env python3
# 在 GitHub Actions 运行期生成 PWA 图标（192 / 512 / maskable-512）。
from PIL import Image, ImageDraw, ImageFont
import os

W = 512
C1 = (255, 143, 182)
C2 = (169, 139, 255)


def gradient():
    img = Image.new('RGB', (W, W))
    d = ImageDraw.Draw(img)
    for y in range(W):
        t = y / W
        r = int(C1[0] + (C2[0] - C1[0]) * t)
        g = int(C1[1] + (C2[1] - C1[1]) * t)
        b = int(C1[2] + (C2[2] - C1[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def find_font(size):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simhei.ttf',
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size, index=0)
            except Exception:
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
    return ImageFont.load_default()


def make(path, size):
    base = gradient().resize((size, size))
    d = ImageDraw.Draw(base)
    m = size // 2
    rad = int(size * 0.30)
    d.ellipse([m - rad, m - rad, m + rad, m + rad], fill=(255, 255, 255))
    font = find_font(int(size * 0.42))
    txt = '¥'
    bb = d.textbbox((0, 0), txt, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    d.text((m - tw / 2, m - th / 2 - int(size * 0.02)), txt, font=font, fill=(214, 57, 110))
    base.save(path)
    print('saved', path, base.size)


os.makedirs('icons', exist_ok=True)
make('icons/icon-192.png', 192)
make('icons/icon-512.png', 512)
make('icons/maskable-512.png', 512)
print('icons done')
