#!/usr/bin/env python3
"""生成 PWA 图标（192 / 512 / maskable-512）。

用矢量图元绘制「¥」符号，避免依赖任何字体——
Linux Actions runner 上若缺失 CJK 字体，用文字渲染会得到空白图标。
"""
from PIL import Image, ImageDraw
import os

C1 = (255, 143, 182)   # 粉 #ff8fb6
C2 = (169, 139, 255)   # 紫 #a98bff
WHITE = (255, 255, 255)
RED = (214, 57, 110)   # #d6396e
STROKE_RATIO = 0.075   # 线宽占尺寸比例


def gradient(size):
    img = Image.new('RGB', (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        r = int(C1[0] + (C2[0] - C1[0]) * t)
        g = int(C1[1] + (C2[1] - C1[1]) * t)
        b = int(C1[2] + (C2[2] - C1[2]) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b))
    return img


def draw_yen(d, cx, cy, size, stroke):
    # 符号包围盒
    Hsym = size * 0.50
    Wsym = size * 0.46
    top = cy - Hsym / 2
    bottom = cy + Hsym / 2
    left = cx - Wsym / 2
    right = cx + Wsym / 2
    split = top + Hsym * 0.45  # 斜线收束处（Y 的叉点）

    # 两条斜线：构成 ¥ 顶部的 V
    d.line([(cx, top), (left, split)], fill=RED, width=stroke, joint='curve')
    d.line([(cx, top), (right, split)], fill=RED, width=stroke, joint='curve')
    # 竖直主干：从顶点直通底部，穿过两条横杠
    d.line([(cx, top), (cx, bottom)], fill=RED, width=stroke, joint='curve')
    # 两条横杠
    bar1 = top + Hsym * 0.63
    bar2 = top + Hsym * 0.80
    d.line([(left, bar1), (right, bar1)], fill=RED, width=stroke, joint='curve')
    d.line([(left, bar2), (right, bar2)], fill=RED, width=stroke, joint='curve')


def make(path, size, maskable=False):
    img = gradient(size)
    d = ImageDraw.Draw(img)
    cx = cy = size / 2
    rad = int(size * (0.34 if maskable else 0.30))
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=WHITE)
    stroke = max(2, int(size * STROKE_RATIO))
    draw_yen(d, cx, cy, size, stroke)
    img.save(path, optimize=True)
    print('saved', path, img.size)


if __name__ == '__main__':
    os.makedirs('icons', exist_ok=True)
    make('icons/icon-192.png', 192)
    make('icons/icon-512.png', 512)
    make('icons/maskable-512.png', 512, maskable=True)
    print('icons done')
