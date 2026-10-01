#!/usr/bin/env python3
"""Render the SSTV structure of solivault_song.wav as a self-explaining figure.

Four panels, all from the same recording:

  1. 0.70- 2.10 s, 1000-2500 Hz : the VIS header (leader / break / leader /
     start bit / data bits / stop bit)
  2. 1.70- 6.00 s, 1000-2500 Hz : the first scan lines - one 1200 Hz sync pulse
     every ~0.43 s
  3. 8.00-20.00 s, 1000-2500 Hz : the steady tone lines are flat areas of the
     picture being scanned; this is what a listener hears as a "tune"
  4. 8.00-20.00 s,   60-1200 Hz : almost nothing but the line-rate clicks - this
     is what a listener hears as the rhythmic "clunk"

Usage: python3 spectrogram.py [input.wav] [output.png]
"""
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

PANELS = [
    (0.70, 2.10, 1000, 2500, "1. VIS header"),
    (1.70, 6.00, 1000, 2500, "2. first scan lines - 1200 Hz sync every ~0.43 s"),
    (8.00, 20.00, 1000, 2500, "3. steady tone lines = flat areas of the picture (the 'melody')"),
    (8.00, 20.00, 60, 1200, "4. below 1200 Hz: only the line-rate clicks (the 'clunk')"),
]
WIDTH, HEIGHT, LABEL, GAP = 1400, 235, 22, 34


def load(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64)
    return x, sr


def spec_image(x, sr, t0, t1, flo, fhi, win=2048, hop=256):
    a, b = int(t0 * sr), int(t1 * sr)
    f = np.fft.rfftfreq(win, 1 / sr)
    band = (f >= flo) & (f <= fhi)
    frames = [np.abs(np.fft.rfft(x[i : i + win] * np.hanning(win)))[band]
              for i in range(a, b - win, hop)]
    S = np.array(frames).T
    S = 20 * np.log10(S + 1e-9)
    S = (S - S.min()) / (S.max() - S.min())
    idx = (np.arange(WIDTH) * S.shape[1] / WIDTH).astype(int)
    return Image.fromarray((S[:, idx] * 255).astype(np.uint8)[::-1]).resize((WIDTH, HEIGHT))


def tick_positions(t0, t1, n=5):
    return [(t0 + (t1 - t0) * k / n, k) for k in range(n + 1)]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "solivault_song.wav"
    dst = sys.argv[2] if len(sys.argv) > 2 else "spectrogram.png"
    x, sr = load(src)

    canvas = Image.new("RGB", (WIDTH + 70, len(PANELS) * (HEIGHT + LABEL + GAP) + 8), "white")
    draw = ImageDraw.Draw(canvas)
    y = 6
    for t0, t1, flo, fhi, title in PANELS:
        draw.text((76, y + 6), f"{title}   [{flo}-{fhi} Hz, {t0:.2f}-{t1:.2f} s]", fill="black")
        canvas.paste(spec_image(x, sr, t0, t1, flo, fhi), (70, y + LABEL))
        for f in (1000, 1200, 1500, 1900, 2300) if flo > 500 else (200, 600, 1000):
            if flo <= f <= fhi:
                yy = y + LABEL + HEIGHT - int((f - flo) / (fhi - flo) * HEIGHT)
                draw.text((2, yy - 6), str(f), fill="black")
                draw.line([(66, yy), (70, yy)], fill="white")
        for tt, _ in tick_positions(t0, t1):
            xx = 70 + int((tt - t0) / (t1 - t0) * WIDTH)
            draw.text((xx - 12, y + LABEL + HEIGHT + 4), f"{tt:.1f}", fill="black")
        y += HEIGHT + LABEL + GAP
    canvas.save(dst)
    print(f"wrote {dst} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
