#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

here = Path(__file__).parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "background-7-7.png"
dst = (
    Path(sys.argv[2])
    if len(sys.argv) > 2
    else src.with_name(src.stem + "_enhanced.png")
)

im = Image.open(src).convert("RGB")
g = im.convert("L")
res = np.asarray(g, float) - np.asarray(
    g.filter(ImageFilter.GaussianBlur(6)), float
)  # 细节层（高通）
base = 255.0 * (np.asarray(im, float) / 255.0) ** (1 / 2.4)  # gamma 提亮中间调
w = np.exp(-np.abs(res) / 18.0)  # 强网格线权重小
out = np.clip(base + 6.0 * res[..., None] * w[..., None], 0, 255).astype("uint8")
Image.fromarray(out).save(dst)
print(f"{src.name} → {dst.name}")
