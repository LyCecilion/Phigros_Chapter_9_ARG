#!/usr/bin/env python3
"""Minimal SSTV decoder for the Solivault transmission (solivault_song.wav).

Reads the audio, decodes the VIS header (which names the mode), then renders the
image. Tested on ../solivault_song.wav, where it prints `VIS 60 -> Scottie S1`
and writes a 320x256 portrait.

Usage: python3 sstv_decode.py [input.wav] [output.png]

Notes on this particular transmission:
  * it is a *pure* SSTV signal - all energy sits in the 1200-2300 Hz band, with a
    1200 Hz sync pulse at the start of every line;
  * the line rate is 428.5 ms (i.e. ~140 lines per minute), a few percent faster
    than nominal Scottie S1 (443.22 ms), so the intra-line layout below is scaled
    by k = 428.5 / 443.22;
  * line timing jitters by a few tenths of a percent, which is why every line is
    re-aligned on its own sync pulse instead of a fixed grid.
"""

import sys
import wave

import numpy as np
from PIL import Image

SCOTTIE_S1_VIS = 60
WIDTH, HEIGHT = 320, 256
LINE_NOMINAL = 0.44322  # seconds, nominal Scottie S1 line time
SYNC, PORCH, SCAN, SEP = 0.0090, 0.0015, 0.138240, 0.0090  # nominal, seconds


def load(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64)
    return x, sr


def analytic_freq(seg, sr):
    """Instantaneous frequency (Hz) of a real signal, via its analytic signal."""
    n = len(seg)
    spectrum = np.fft.fft(seg)
    step = np.zeros(n)
    step[0] = 1
    step[1 : n // 2] = 2
    if n % 2 == 0:
        step[n // 2] = 1
    phase = np.unwrap(np.angle(np.fft.ifft(spectrum * step)))
    return np.diff(phase) / (2 * np.pi) * sr


def tone_at(x, sr, t, dur=0.005):
    """Dominant frequency in a short window."""
    seg = x[int(t * sr) : int((t + dur) * sr)]
    if len(seg) < 8:
        return 0.0
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    freqs = np.fft.rfftfreq(len(seg), 1 / sr)
    band = (freqs > 900) & (freqs < 2500)
    return freqs[band][np.argmax(spec[band])]


def decode_vis(x, sr, limit=4.0):
    """Return (vis_code, image_start_seconds).

    VIS layout: 300 ms 1900 Hz | 10 ms 1200 Hz | 300 ms 1900 Hz | 30 ms start bit
    (1200 Hz) | 7 data bits + 1 parity bit, 30 ms each (1100 Hz = 1, 1300 Hz = 0).
    """
    hop = 0.002
    times, freqs = [], []
    t = 0.0
    while t < limit:
        times.append(t)
        freqs.append(tone_at(x, sr, t))
        t += hop
    freqs = np.array(freqs)

    def mean_between(a, b):
        m = (np.array(times) >= a) & (np.array(times) < b)
        return freqs[m].mean() if m.any() else 0.0

    # the 10 ms break sits between two 300 ms leaders of 1900 Hz
    t_break = None
    for tt, f in zip(times, freqs):
        if tt < 0.3 or abs(f - 1200) > 120:
            continue
        if (
            abs(mean_between(tt - 0.30, tt - 0.03) - 1900) < 120
            and abs(mean_between(tt + 0.03, tt + 0.30) - 1900) < 120
        ):
            t_break = tt
            break
    if t_break is None:
        raise ValueError("no VIS break tone found")
    t_start = t_break + 0.010 + 0.300  # start of the 30 ms start bit

    bits = []
    for i in range(8):
        f = tone_at(x, sr, t_start + 0.030 * (i + 1.5), 0.020)
        bits.append(1 if abs(f - 1100) < abs(f - 1300) else 0)
    code = sum(b << i for i, b in enumerate(bits[:7]))
    # 8 x 30 ms of data + 30 ms stop bit, then the first line's sync pulse
    return code, t_start + 0.300


def sync_starts(x, sr, t_first, period):
    """Track each line's sync pulse (1200 Hz) around the expected position."""
    freq = analytic_freq(x, sr)
    win = int(0.002 * sr)
    smooth = np.convolve(freq, np.ones(win) / win, mode="same")
    pos = t_first * sr  # float: truncating here would drift ~5 ms over 256 lines
    step = period * sr
    starts = []
    while pos + step < len(smooth):
        lo = max(0, int(pos - 0.015 * sr))
        hi = min(len(smooth), int(pos + 0.015 * sr))
        hit = lo + int(np.argmin(smooth[lo:hi]))
        starts.append(hit)
        pos = hit + step
    return starts


def sample_channel(x, sr, t0, span, edges, n):
    seg = x[int(t0 * sr) : int(t0 * sr) + n]
    if len(seg) < n:
        seg = np.pad(seg, (0, n - len(seg)))
    fr = analytic_freq(seg, sr)
    out = np.empty(WIDTH)
    for j in range(WIDTH):
        a, b = edges[j], edges[j + 1]
        v = fr[a:b].mean() if b > a else 1500.0
        out[j] = 0.0 if not np.isfinite(v) else (v - 1500.0) / 800.0 * 255.0
    return np.clip(out, 0, 255)


def decode(path, out_path):
    x, sr = load(path)
    code, t_image = decode_vis(x, sr)
    print(f"VIS {code} -> {mode_name(code)}")

    period = 0.4285  # measured from the sync pulses
    k = period / LINE_NOMINAL
    sync, porch, scan, sep = (SYNC * k, PORCH * k, SCAN * k, SEP * k)
    n = int(scan * sr)
    edges = np.append((np.arange(WIDTH) * n / WIDTH).astype(int), n)

    starts = sync_starts(x, sr, t_image, period)
    while len(starts) < HEIGHT:
        starts.append(starts[-1] + int(round(period * sr)))
    starts = starts[:HEIGHT]
    img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    for y, s0 in enumerate(starts):
        base = s0 / sr - sync / 2
        g0 = base + sync + porch
        b0 = g0 + scan + sep
        r0 = b0 + scan + sep
        for channel, c0 in ((1, g0), (2, b0), (0, r0)):
            img[y, :, channel] = sample_channel(x, sr, c0, scan, edges, n)
    Image.fromarray(img).save(out_path)
    print(f"wrote {out_path} ({WIDTH}x{HEIGHT})")


def mode_name(code):
    return {60: "Scottie S1", 56: "Scottie S2", 8: "Robot 36"}.get(
        code, f"unknown ({code})"
    )


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "solivault_song.wav"
    dst = sys.argv[2] if len(sys.argv) > 2 else "sstv_decode.png"
    decode(src, dst)
