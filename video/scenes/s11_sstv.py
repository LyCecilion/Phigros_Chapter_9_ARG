"""s11 · SSTV：一段“音频”如何逐行传输一张图。

这一章故意比普通概览讲得细：先把亮度映射成频率，再拆开同步、VIS
和 Scottie S1 的一行，最后把真实解码图逐行长出来。
"""

from pathlib import Path
import wave

import numpy as np
from PIL import Image
from manim import *
from style import *

# --- 真实素材与数据 -----------------------------------------------------------

DATA = Path(__file__).resolve().parents[2] / "artifacts/stage_ii/SSTV"
SPECTROGRAM_PATH = DATA / "spectrogram.png"
DECODED_PATH = DATA / "sstv_img_0.png"
AUDIO_PATH = DATA / "solivault_song.wav"

with wave.open(str(AUDIO_PATH), "rb") as wav:
    AUDIO_RATE = wav.getframerate()
    AUDIO_CHANNELS = wav.getnchannels()
    AUDIO_WIDTH = wav.getsampwidth()
    AUDIO_FRAMES = wav.getnframes()
    AUDIO_SECONDS = AUDIO_FRAMES / AUDIO_RATE

assert (AUDIO_RATE, AUDIO_CHANNELS, AUDIO_WIDTH) == (44100, 1, 2)
assert 111.3 < AUDIO_SECONDS < 111.4

IMAGE_W, IMAGE_H = 320, 256
VIS_CODE = 60
VIS_DATA_BITS = [0, 0, 1, 1, 1, 1, 0]  # low bit first: 60 = 0b0111100
VIS_PARITY = 0
assert sum(bit << i for i, bit in enumerate(VIS_DATA_BITS)) == VIS_CODE
assert sum(VIS_DATA_BITS) % 2 == VIS_PARITY

LINE_PERIOD = 0.4285  # 从音频中的 1200 Hz 同步脉冲测得
assert abs(IMAGE_H * LINE_PERIOD - 109.696) < 0.01

SYNC, PORCH, SCAN, SEP = 0.0090, 0.0015, 0.138240, 0.0090
TIME_SCALE = LINE_PERIOD / 0.44322
LINE_SEGMENTS = [
    ("SYNC", SYNC * TIME_SCALE, ACCENT),
    ("PORCH", PORCH * TIME_SCALE, MUTED),
    ("G", SCAN * TIME_SCALE, OK),
    ("SEP", SEP * TIME_SCALE, MUTED),
    ("B", SCAN * TIME_SCALE, ACCENT),
    ("SEP", SEP * TIME_SCALE, MUTED),
    ("R", SCAN * TIME_SCALE, CIPHER),
]
assert abs(sum(duration for _, duration, _ in LINE_SEGMENTS) - LINE_PERIOD) < 1e-6


def rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"))


DECODED = rgb(DECODED_PATH)
GRAY = DECODED.mean(axis=2)
SAMPLE_ROW_INDEX = 160
ROW = GRAY[SAMPLE_ROW_INDEX]
ROW_SAMPLES = ROW[np.linspace(0, IMAGE_W - 1, 16).astype(int)]
ROW_FREQS = 1500.0 + 800.0 * ROW_SAMPLES / 255.0
assert ROW.shape == (IMAGE_W,)
assert np.all((1500 <= ROW_FREQS) & (ROW_FREQS <= 2300))


# --- 构件 ---------------------------------------------------------------------


def picture(array: np.ndarray, height: float) -> ImageMobject:
    a = np.asarray(array)
    if a.dtype != np.uint8:
        a = np.clip(a, 0, 255).astype(np.uint8)
    if a.ndim == 2:
        a = np.dstack([a, a, a])
    m = ImageMobject(a)
    m.height = height
    return m


def title_block(title: str, subtitle: str) -> VGroup:
    head = VGroup(
        ui(title, 36).set_color(FG),
        ui(subtitle, 20).set_color(MUTED),
    ).arrange(DOWN, buff=0.12)
    return head.to_edge(UP, buff=0.32)


def label(text: str, point, color=MUTED, size=22) -> Text:
    return ui(text, size).set_color(color).move_to(point)


def frequency_bar(value: float, width: float = 0.33, height: float = 1.7) -> VGroup:
    """亮度样本对应的频率柱。"""
    frac = (value - 1500) / 800
    frame = Rectangle(width=width, height=height, stroke_color=MUTED, stroke_width=1)
    fill = Rectangle(width=width - 0.04, height=max(0.02, height * frac), stroke_width=0)
    fill.set_fill(ACCENT, opacity=0.9).align_to(frame, DOWN)
    return VGroup(frame, fill)


def vis_block(text: str, width: float, color, size: float = 20) -> VGroup:
    rect = RoundedRectangle(width=width, height=0.72, corner_radius=0.06,
                           stroke_color=color, stroke_width=1.6)
    rect.set_fill(color, opacity=0.16)
    return VGroup(rect, mono(text, size).set_color(color).move_to(rect))


def line_timeline() -> tuple[VGroup, list[VGroup]]:
    total_width = 7.7
    x = -total_width / 2
    blocks = []
    for name, duration, color in LINE_SEGMENTS:
        width = total_width * duration / LINE_PERIOD
        rect = Rectangle(width=width, height=0.72, stroke_color=color, stroke_width=1.5)
        rect.set_fill(color, opacity=0.18)
        mob = VGroup(rect)
        mob.move_to([x + width / 2, 0.55, 0])
        blocks.append(mob)
        x += width
    return VGroup(*blocks), blocks


# --- 场景 ---------------------------------------------------------------------


class SSTVFrequency(Narrated):
    """亮度映射到频率：图像的一行就是一条滑动音调。"""

    def construct(self):
        title = title_block("SSTV · 亮度就是频率", "不是把图片作为文件发送，而是把每个像素变成音调")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        gradient = VGroup()
        for i in range(16):
            rect = Rectangle(width=0.27, height=1.05, stroke_width=0)
            rect.set_fill(interpolate_color(BLACK, WHITE, i / 15), opacity=1)
            gradient.add(rect)
        gradient.arrange(RIGHT, buff=0.02).move_to([-3.75, 1.25, 0])
        gradient_tag = label("暗", gradient.get_left() + DOWN * 0.38, MUTED, 21)
        gradient_tag2 = label("亮", gradient.get_right() + DOWN * 0.38, FG, 21)
        scale = VGroup(
            mono("1500 Hz", 24).set_color(ACCENT),
            mono("2300 Hz", 24).set_color(GOLD),
        ).arrange(RIGHT, buff=1.0).move_to([-3.75, -0.15, 0])

        self.say("SSTV 的关键规则很简单：亮度越高，频率越高")
        self.play(FadeIn(gradient), FadeIn(gradient_tag), FadeIn(gradient_tag2), FadeIn(scale))
        self.wait(1.2)

        bars = VGroup(*[frequency_bar(v, width=0.26) for v in ROW_FREQS])
        bars.arrange(RIGHT, buff=0.08).move_to([3.0, 1.02, 0])
        bars_tag = label("同一组亮度 → 一组频率", bars.get_top() + UP * 0.32, ACCENT, 22)
        axis = Line(bars.get_left() + DOWN * 1.0, bars.get_right() + DOWN * 1.0, color=MUTED, stroke_width=1.2)
        self.say("把一行像素拿出来，每个亮度都对应 1500～2300 Hz 中的一个值")
        self.play(FadeIn(bars_tag), Create(axis))
        self.play(LaggedStart(*[GrowFromEdge(bar[1], DOWN) for bar in bars], lag_ratio=0.08), run_time=2.0)
        self.wait(1.2)

        formula = MathTex(r"f=1500+800\times\frac{b}{255}", font_size=32).set_color(FG)
        formula.move_to([0, -1.45, 0])
        note = label("所以图像的二维信息，先被压成一维声音", [0, -2.15, 0], MUTED, 23)
        self.play(Write(formula))
        self.play(FadeIn(note))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, gradient, gradient_tag, gradient_tag2, scale, bars, bars_tag, axis, formula, note)))


class SSTVRowTone(Narrated):
    """用真实解码图的一行，展示像素与音调曲线的对应。"""

    def construct(self):
        title = title_block("SSTV · 一行像素变成一条曲线", "接收端只需要沿着时间读回频率")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        row = VGroup()
        for value in ROW_SAMPLES:
            rect = Rectangle(width=0.34, height=0.72, stroke_color=MUTED, stroke_width=1)
            rect.set_fill(interpolate_color(BLACK, WHITE, float(value) / 255), opacity=1)
            row.add(rect)
        row.arrange(RIGHT, buff=0.025).move_to([-3.3, 1.9, 0])
        row_frame = SurroundingRectangle(row, color=MUTED, buff=0.08)
        row_tag = label(
            f"真实解码图 · 第 {SAMPLE_ROW_INDEX + 1} 行 · 抽样放大",
            row.get_left() + LEFT * 0.3 + UP * 0.65,
            MUTED,
            21,
        )
        self.say("这里取真实解码图的第 161 行，并把它放大成 16 个采样格")
        self.play(FadeIn(row), Create(row_frame), FadeIn(row_tag))
        self.wait(0.8)

        ax = Axes(
            x_range=[0, 1, 0.25], y_range=[1400, 2400, 200],
            x_length=7.0, y_length=2.6, tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False},
        ).move_to([0, -0.45, 0])
        curve = ax.plot(
            lambda t: float(np.interp(t, np.linspace(0, 1, len(ROW_FREQS)), ROW_FREQS)),
            x_range=[0, 1, 0.01], color=ACCENT, stroke_width=3,
        )
        low = label("1500", ax.c2p(0, 1500) + LEFT * 0.35, ACCENT, 18)
        high = label("2300 Hz", ax.c2p(0, 2300) + LEFT * 0.55, GOLD, 18)
        xname = label("时间 →", ax.get_right() + RIGHT * 0.35, MUTED, 20)
        self.say("沿着这一行从左到右扫描，就得到一条随时间变化的频率曲线")
        self.play(Create(ax), FadeIn(low), FadeIn(high), FadeIn(xname), Create(curve), run_time=1.8)

        dots = VGroup(*[
            Dot(ax.c2p(i / (len(ROW_FREQS) - 1), value), radius=0.055, color=GOLD)
            for i, value in enumerate(ROW_FREQS)
        ])
        for i in range(len(ROW_FREQS)):
            self.play(Indicate(row[i], color=GOLD, scale_factor=1.08), FadeIn(dots[i]), run_time=0.22)
        self.say("亮的地方，曲线就往高频走；暗的地方，曲线就往低频走", wait=1.8)
        self.hush()
        self.play(FadeOut(Group(title, row, row_frame, row_tag, ax, curve, low, high, xname, dots)))


class SSTVSync(Narrated):
    """解释每行开头的 1200 Hz 同步脉冲。"""

    def construct(self):
        title = title_block("SSTV · 每一行先打一个同步脉冲", "没有标记，接收端就不知道下一行从哪里开始")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        ax = Axes(
            x_range=[0, 2.14, 0.4285], y_range=[1000, 2400, 400],
            x_length=8.8, y_length=3.0, tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False},
        ).move_to([0, 0.1, 0])
        self.play(Create(ax))

        # 用真实协议的频率层级画出两行半：1200 Hz 短脉冲，扫描区在 1500~2300 Hz。
        period = LINE_PERIOD
        pulse_width = SYNC * TIME_SCALE

        def sync_wave(t):
            phase = t % period
            return 1200 if phase < pulse_width else 1800 + 250 * np.sin(phase * 20)

        wave = ax.plot(sync_wave, x_range=[0, 2.14, 0.002], color=FG, stroke_width=2.2)
        self.say("每隔约 0.428 秒，先发一小段固定的 1200 Hz")
        self.play(Create(wave), run_time=2.2)

        marks = VGroup()
        for i in range(5):
            t = i * period
            line = DashedLine(ax.c2p(t, 1000), ax.c2p(t, 2400), color=ACCENT, stroke_width=1.6, dash_length=0.08)
            tag = mono("1200 Hz", 19).set_color(ACCENT).next_to(line, UP, buff=0.08)
            marks.add(line, tag)
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.12), run_time=1.5)
        period_tag = chip("行周期 ≈ 0.428 s", GOLD, 22).move_to([0, -1.85, 0])
        self.say("接收端只要找这些低频脉冲，就能把连续音频切回一行一行")
        self.play(FadeIn(period_tag, shift=UP * 0.15))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, ax, wave, marks, period_tag)))


class SSTVScottieS1(Narrated):
    """拆开 Scottie S1 的一行：G、B、R 三段扫描。"""

    def construct(self):
        title = title_block("SSTV · VIS 告诉我们使用 Scottie S1", "认错模式，行时长和颜色顺序都会错")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        mode = VGroup(
            chip("VIS 60", GOLD, 25),
            mono("→ Scottie S1", 30).set_color(OK),
        ).arrange(RIGHT, buff=0.35).move_to([0, 2.25, 0])
        self.play(FadeIn(mode))

        timeline, blocks = line_timeline()
        self.say("Scottie S1 的一行不是一段颜色，而是 G、B、R 依次扫描")
        self.play(FadeIn(timeline), run_time=1.0)

        names = VGroup(
            label("同步", blocks[0].get_center() + UP * 0.62, ACCENT, 18),
            label("门廊", blocks[1].get_center() + DOWN * 0.65, MUTED, 18),
            label("G", blocks[2].get_center() + UP * 0.62, OK, 25),
            label("B", blocks[4].get_center() + UP * 0.62, ACCENT, 25),
            label("R", blocks[6].get_center() + UP * 0.62, CIPHER, 25),
        )
        durations = VGroup(
            mono("9 ms", 18).set_color(ACCENT),
            mono("1.5 ms", 18).set_color(MUTED),
            mono("138 ms", 20).set_color(OK),
            mono("138 ms", 20).set_color(ACCENT),
            mono("138 ms", 20).set_color(CIPHER),
        ).arrange(RIGHT, buff=0.62).move_to([0, -0.62, 0])
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.14), run_time=1.3)
        self.play(FadeIn(durations))
        self.say("每一段彩色扫描约 138 毫秒，中间用短暂的分隔音隔开")
        self.wait(1.4)

        summary = VGroup(
            mono("320 像素 × 3 色", 28).set_color(FG),
            mono("≈ 0.428 s / 行", 28).set_color(GOLD),
            mono("256 行", 28).set_color(OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -1.65, 0])
        self.play(FadeIn(summary, shift=UP * 0.15))
        self.say("256 行拼起来，就是一张 320 × 256 的彩色图", wait=2)
        self.hush()
        self.play(FadeOut(VGroup(title, mode, timeline, names, durations, summary)))


class SSTVVIS(Narrated):
    """逐段读 VIS 头，得到低位在前的 60。"""

    def construct(self):
        title = title_block("SSTV · VIS 头会自报模式", "Vertical Interval Signaling：接收端先读这一小段“身份证”")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        segments = [
            ("1900", 1.7, ACCENT, "300 ms"),
            ("1200", 0.45, MUTED, "10 ms"),
            ("1900", 1.7, ACCENT, "300 ms"),
            ("START", 0.55, GOLD, "30 ms"),
        ]
        blocks = VGroup()
        for text, width, color, duration in segments:
            b = vis_block(text, width, color, 17)
            b.add(label(duration, b.get_bottom() + DOWN * 0.28, color, 17))
            blocks.add(b)
        blocks.arrange(RIGHT, buff=0.12).move_to([-1.1, 1.95, 0])
        self.say("先是引导音、间隔、引导音，再用 1200 Hz 标出起始位")
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), run_time=1.8)

        data = VGroup()
        data_labels = VGroup()
        for i, bit in enumerate(VIS_DATA_BITS + [VIS_PARITY]):
            freq = 1100 if bit else 1300
            color = OK if bit else ACCENT
            b = vis_block(str(bit), 0.58, color, 24)
            b.add(label(f"{freq}", b.get_bottom() + DOWN * 0.28, color, 15))
            data.add(b)
            data_labels.add(label(f"b{i}", ORIGIN, MUTED, 16))
        data.arrange(RIGHT, buff=0.08).move_to([0, 0.15, 0])
        for mob, bit_block in zip(data_labels, data):
            mob.next_to(bit_block, UP, buff=0.14)
        self.say("接下来 7 个数据位和 1 个校验位，用 1100 / 1300 Hz 表示 1 / 0")
        self.play(LaggedStart(*[FadeIn(b) for b in data], lag_ratio=0.12), run_time=1.8)
        self.play(FadeIn(data_labels))

        bits_text = mono("低位在前：0 0 1 1 1 1 0 0", 27).set_color(FG).move_to([0, -0.95, 0])
        calc = VGroup(
            mono("60", 48).set_color(GOLD),
            mono("= 0×1 + 0×2 + 1×4 + 1×8 + 1×16 + 1×32", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.18).move_to([0, -1.65, 0])
        result = chip("VIS 60  →  Scottie S1", OK, 25).move_to([0, -2.65, 0])
        self.say("数据位按低位在前读取：得到 VIS 码 60")
        self.play(FadeIn(bits_text), FadeIn(calc, shift=UP * 0.12))
        self.play(FadeIn(result, shift=UP * 0.15))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, blocks, data, data_labels, bits_text, calc, result)))


class SSTVDecode(Narrated):
    """把真实 SSTV 解码图按扫描行逐段显示出来。"""

    def construct(self):
        title = title_block("SSTV · 256 行之后，图像出现", "同一段音频：找同步 → 取 G/B/R → 拼成像素")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        spec = picture(rgb(SPECTROGRAM_PATH), 2.35).move_to([-3.9, 0.3, 0])
        spec_frame = SurroundingRectangle(spec, color=MUTED, buff=0.06)
        spec_tag = label("真实音频的频谱", spec.get_top() + UP * 0.25, MUTED, 20)
        arrow = Arrow(spec.get_right() + RIGHT * 0.2, [0.0, 0.3, 0], color=ACCENT, stroke_width=3)
        self.say("把真实音频按 VIS 识别出的 Scottie S1 规则切开")
        self.play(FadeIn(spec), Create(spec_frame), FadeIn(spec_tag), GrowArrow(arrow))

        image_height = 4.25
        image = picture(DECODED, image_height).move_to([3.35, 0.15, 0])
        image_frame = SurroundingRectangle(image, color=OK, buff=0.06)
        image_bottom = image.get_bottom()[1]
        strip_height = image_height / 8
        strips = []
        for i in range(8):
            a, b = i * IMAGE_H // 8, (i + 1) * IMAGE_H // 8
            strip = picture(DECODED[a:b], strip_height)
            strip.move_to([image.get_center()[0], image.get_top()[1] - strip_height * (i + 0.5), 0])
            strips.append(strip)

        counter = mono("row 0 / 256", 25).set_color(GOLD).move_to([-2.0, -2.45, 0])
        self.play(FadeIn(counter))
        for i, strip in enumerate(strips):
            self.play(FadeIn(strip, shift=UP * 0.10), run_time=0.45)
            new = mono(f"row {(i + 1) * IMAGE_H // 8:3d} / 256", 25).set_color(GOLD).move_to(counter)
            self.play(Transform(counter, new), run_time=0.18)
        self.play(Create(image_frame), run_time=0.8)
        self.say("每一行都由三段颜色扫描填回 320 个像素，最终得到角色立绘")

        final = VGroup(
            chip("Scottie S1", OK, 23),
            mono("320 × 256", 28).set_color(FG),
            mono("≈ 109.7 s", 28).set_color(GOLD),
        ).arrange(RIGHT, buff=0.28).move_to([2.55, -2.45, 0])
        self.play(FadeIn(final, shift=UP * 0.15))
        self.wait(2.2)
        self.hush()
        self.play(FadeOut(Group(title, spec, spec_frame, spec_tag, arrow, *strips, image_frame, counter, final)))
