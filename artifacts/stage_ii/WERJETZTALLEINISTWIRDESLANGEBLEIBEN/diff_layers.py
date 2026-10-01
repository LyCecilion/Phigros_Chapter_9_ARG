#!/usr/bin/env python3
import sys
from pathlib import Path

from PIL import Image, ImageChops

here = Path(__file__).parent
l1, l2 = here / "start.layer1.png", here / "start.layer2.png"
a_path, b_path = ([Path(p) for p in sys.argv[1:3]] + [l1, l2])[:2]

a, b = (Image.open(p).convert("RGB") for p in (a_path, b_path))

ImageChops.difference(a, b).point(lambda v: min(255, v * 8)).save(
    here / "start.diff_x8.png"
)
