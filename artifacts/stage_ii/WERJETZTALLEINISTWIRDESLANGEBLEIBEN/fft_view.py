#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

here = Path(__file__).parent
p = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "start.layer1.png"

a = np.asarray(Image.open(p).convert("L"), dtype=float)
m = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(a))))
m = (255 * (m - m.min()) / (m.max() - m.min())).astype("uint8")
out = here / f"{p.stem}.fft.png"
Image.fromarray(m).save(out)
print(f"{p.name} {a.shape[1]}x{a.shape[0]} → {out.name}")
