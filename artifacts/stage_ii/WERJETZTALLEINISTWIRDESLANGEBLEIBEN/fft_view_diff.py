#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

here = Path(__file__).parent
l1, l2 = here / "start.layer1.png", here / "start.layer2.png"
a_path, b_path = ([Path(p) for p in sys.argv[1:3]] + [l1, l2])[:2]

gray = lambda p: np.asarray(Image.open(p).convert("L"), dtype=float)
m = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(gray(a_path) - gray(b_path)))))
m = (255 * (m - m.min()) / (m.max() - m.min())).astype("uint8")
out = here / f"{a_path.stem}-{b_path.stem}.fft.png"
Image.fromarray(m).save(out)
print(f"{a_path.name} - {b_path.name} → {out.name}")
