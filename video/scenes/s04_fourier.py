"""s04 · 二维 Fourier：频谱到底在“看”什么，为什么 layer1 的频谱里有字。

用法：
    ./render.sh -ql scenes/s04_fourier.py FourierWave1D  # 一维热身：三条正弦波相加，再拆回频谱
    ./render.sh -ql scenes/s04_fourier.py FourierStripes # 一种条纹 = 一对对称亮点；变密、旋转
    ./render.sh -ql scenes/s04_fourier.py FourierSum     # 三种条纹相加 = 三对亮点；照片是一团云；公式闪过
    ./render.sh -ql scenes/s04_fourier.py FourierShift   # fftshift：四个象限对调，零频到正中心
    ./render.sh -ql scenes/s04_fourier.py FourierLog     # log1p：线性显示几乎全黑，取对数后细节出来
    ./render.sh -ql scenes/s04_fourier.py FourierReveal  # 真图：layer1 → FFT → outside_the_birdcage；diff 更清楚

合成条纹和频谱都在场景里用 numpy 现算；真图的频谱也现算，并断言与仓库里的
start.layer1.fft.png / start.layer1-start.layer2.fft.png 逐像素一致。
"""

from functools import cache
from pathlib import Path

import numpy as np
from PIL import Image

from manim import *
from style import *

# --- 数据 ---------------------------------------------------------------------

DATA = Path(__file__).resolve().parents[2] / "artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN"


def gray(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L"), dtype=float)


def to_u8(a: np.ndarray) -> np.ndarray:
    """与 fft_view.py 完全相同的归一化：线性拉到 0~255 再截断成 uint8。"""
    return (255 * (a - a.min()) / (a.max() - a.min())).astype("uint8")


@cache
def layer1() -> np.ndarray:
    return gray(DATA / "start.layer1.png")


@cache
def layer1_mag() -> np.ndarray:
    """|fft2(layer1)|，未中心化。"""
    return np.abs(np.fft.fft2(layer1()))


@cache
def layer1_spec() -> np.ndarray:
    out = to_u8(np.log1p(np.fft.fftshift(layer1_mag())))
    assert np.array_equal(out, gray(DATA / "start.layer1.fft.png"))
    return out


@cache
def diff_spec() -> np.ndarray:
    d = layer1() - gray(DATA / "start.layer2.png")
    out = to_u8(np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(d)))))
    assert np.array_equal(out, gray(DATA / "start.layer1-start.layer2.fft.png"))
    return out


# 频谱图上 outside_the_birdcage 那一行（上方那份；下方是它的中心对称像）
BAND = (slice(78, 162), slice(700, 1220))

# 合成条纹
N = 96
YY, XX = np.mgrid[0:N, 0:N]


def grating(u: float, v: float) -> np.ndarray:
    """波矢 (u, v) 的余弦条纹：x 方向每 N 像素 u 个周期，y（向下）方向 v 个周期。"""
    return 0.5 + 0.5 * np.cos(2 * np.pi * (u * XX + v * YY) / N)


def peaks(img: np.ndarray, k: int) -> set[tuple[int, int]]:
    """频谱里最亮的 k 个非零频点，返回相对中心的 (u, v)。"""
    s = np.abs(np.fft.fftshift(np.fft.fft2(img - img.mean())))
    idx = np.argsort(s, axis=None)[::-1][:k]
    ys, xs = np.unravel_index(idx, s.shape)
    return {(int(x) - N // 2, int(y) - N // 2) for y, x in zip(ys, xs)}


SUM_WAVES = [((6, 0), ACCENT), ((0, 4), GOLD), ((5, -7), CIPHER)]
SUM_IMG = sum(grating(u, v) for (u, v), _ in SUM_WAVES) / len(SUM_WAVES)

assert peaks(grating(4, 0), 2) == {(4, 0), (-4, 0)}
assert peaks(grating(3, 5), 2) == {(3, 5), (-3, -5)}
assert peaks(SUM_IMG, 6) == {p for (u, v), _ in SUM_WAVES for p in ((u, v), (-u, -v))}

# 一维热身：频率 1/3/5，振幅 1/0.5/0.3
WAVES_1D = [(1, 1.0, ACCENT), (3, 0.5, GOLD), (5, 0.3, CIPHER)]
_T = np.arange(256) / 256
_AMP = 2 * np.abs(np.fft.rfft(sum(a * np.sin(2 * np.pi * f * _T) for f, a, _ in WAVES_1D))) / len(_T)
assert np.allclose(_AMP[[1, 3, 5]], [1.0, 0.5, 0.3]) and _AMP[[0, 2, 4, 6, 7]].max() < 1e-9

# --- 构件 ---------------------------------------------------------------------


def picture(a: np.ndarray, height: float, nearest: bool = False) -> ImageMobject:
    """灰度数组（0~1 浮点或 uint8）或 RGB 数组 → ImageMobject。"""
    if a.dtype != np.uint8:
        a = (255 * np.clip(a, 0, 1)).astype("uint8")
    if a.ndim == 2:
        a = np.dstack([a, a, a])
    a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    m = ImageMobject(a)
    m.height = height
    if nearest:
        m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return m


def frame_of(m: Mobject, color=MUTED) -> Rectangle:
    return Rectangle(width=m.width, height=m.height, stroke_color=color, stroke_width=1.5).move_to(m)


def stretch(a: np.ndarray, lo: float = 2, hi: float = 99.7) -> np.ndarray:
    """按百分位拉伸对比度，用于放大截取的频谱带。"""
    p, q = np.percentile(a, [lo, hi])
    return np.clip((a - p) / (q - p), 0, 1)


class FreqPanel(VGroup):
    """频域面板：十字坐标 + 中心零频点；to_point 把 (u, v) 映射到屏幕。"""

    def __init__(self, side: float = 3.2, reach: float = 12, **kw):
        super().__init__(**kw)
        self.side, self.unit = side, side / 2 / reach
        self.border = Square(side, stroke_color=MUTED, stroke_width=1.5).set_fill("#000000", 1)
        h = Line(LEFT * side / 2, RIGHT * side / 2, stroke_color=MUTED, stroke_width=1, stroke_opacity=0.5)
        v = Line(DOWN * side / 2, UP * side / 2, stroke_color=MUTED, stroke_width=1, stroke_opacity=0.5)
        self.dc = Dot(radius=0.05, color=FG)
        self.add(self.border, h, v, self.dc)

    def to_point(self, u: float, v: float) -> np.ndarray:
        # 图像的 y 向下，屏幕的 y 向上
        return self.border.get_center() + self.unit * np.array([u, -v, 0])


def peak_pair(panel: FreqPanel, u: float, v: float, color=GOLD) -> VGroup:
    a, b = panel.to_point(u, v), panel.to_point(-u, -v)
    return VGroup(
        DashedLine(b, a, stroke_color=color, stroke_width=1.5, stroke_opacity=0.5, dash_length=0.06),
        Dot(a, radius=0.08, color=color),
        Dot(b, radius=0.08, color=color),
    )


def heading(text: str, ref: Mobject) -> Text:
    return ui(text, 24).set_color(MUTED).next_to(ref, UP, buff=0.22)


# --- 场景 ---------------------------------------------------------------------


class FourierWave1D(Narrated):
    def construct(self):
        small = []
        for i, (f, a, color) in enumerate(WAVES_1D):
            ax = Axes(x_range=[0, 1, 1], y_range=[-1, 1, 1], x_length=3.8, y_length=1.1,
                      tips=False, axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False})
            ax.move_to([-4.6, 1.9 - 1.55 * i, 0])
            curve = ax.plot(lambda t, f=f, a=a: a * np.sin(2 * np.pi * f * t), x_range=[0, 1, 0.002],
                            color=color, stroke_width=3)
            tag = mono(f"{f} 圈 × {a:g}", 18).set_color(color).next_to(ax, UP, buff=0.02).align_to(ax, LEFT)
            small.append(VGroup(ax, curve, tag))

        big = Axes(x_range=[0, 1, 1], y_range=[-1.8, 1.8, 1], x_length=6.4, y_length=2.6,
                   tips=False, axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False})
        big.move_to([2.6, 1.3, 0])
        total = big.plot(lambda t: sum(a * np.sin(2 * np.pi * f * t) for f, a, _ in WAVES_1D),
                         x_range=[0, 1, 0.002], color=FG, stroke_width=3.5)

        self.say("先看一维：三条快慢不同的正弦波")
        for g in small:
            self.play(Create(g[0]), Create(g[1]), FadeIn(g[2]), run_time=1.0)
        self.wait(1)

        self.say("叠在一起，就成了一条看不出规律的曲线")
        plus = mono("+", 30).set_color(MUTED).move_to([-1.2, 0.35, 0])
        self.play(Create(big), FadeIn(plus))
        ghosts = [total.copy() for _ in small]
        self.play(*[ReplacementTransform(g[1].copy(), gh) for g, gh in zip(small, ghosts)], run_time=2)
        self.remove(*ghosts)
        self.add(total)
        self.wait(1.5)

        self.say("Fourier 变换做的是反过来：把它拆回去")
        spec = Axes(x_range=[0, 7, 1], y_range=[0, 1.1, 0.5], x_length=6.4, y_length=1.7,
                    tips=False, axis_config={"stroke_color": MUTED, "stroke_width": 1.2})
        spec.move_to([2.6, -1.75, 0])
        xlabels = VGroup(*[mono(str(k), 18).set_color(MUTED).next_to(spec.c2p(k, 0), DOWN, buff=0.12) for k in range(8)])
        xname = ui("频率", 20).set_color(MUTED).next_to(spec.x_axis, RIGHT, buff=0.15)
        arrow = Arrow(big.get_bottom(), spec.get_top(), buff=0.08, color=MUTED, stroke_width=3)
        self.play(GrowArrow(arrow), Create(spec), FadeIn(xlabels), FadeIn(xname))

        bars = VGroup()
        for f, _, color in WAVES_1D:
            h = _AMP[f]
            bar = Rectangle(width=0.32, height=spec.c2p(0, h)[1] - spec.c2p(0, 0)[1],
                            stroke_width=0, fill_color=color, fill_opacity=0.9)
            bar.move_to(spec.c2p(f, 0), aligned_edge=DOWN)
            bars.add(bar)
        for g, bar in zip(small, bars):
            self.play(Indicate(g[1], color=g[1].get_color(), scale_factor=1.05),
                      GrowFromEdge(bar, DOWN), run_time=1.0)
        self.wait(0.5)

        self.say("这就是频谱：每种频率的波，各有多强", wait=2)
        self.say("其余频率全是 0：曲线里根本没有它们", wait=2)
        self.hush()
        self.wait(0.5)


class FourierStripes(Narrated):
    def construct(self):
        r, th = ValueTracker(4), ValueTracker(0)

        def uv():
            return r.get_value() * np.cos(th.get_value()), r.get_value() * np.sin(th.get_value())

        img = picture(grating(*uv()), 3.6, nearest=True).move_to([-3.4, 0.35, 0])

        def refresh(m):
            new = picture(grating(*uv()), 3.6, nearest=True)
            m.pixel_array = new.pixel_array

        img.add_updater(refresh)
        img_frame = frame_of(img)
        panel = FreqPanel(side=3.6, reach=12).move_to([3.4, 0.35, 0])
        pair = always_redraw(lambda: peak_pair(panel, *uv()))
        left_h, right_h = heading("图像：一种条纹", img_frame), heading("频谱：零频在正中心", panel)

        self.say("二维也一样，只是“波”变成了条纹")
        self.play(FadeIn(img), Create(img_frame), FadeIn(left_h))
        self.wait(1)
        self.play(FadeIn(panel), FadeIn(right_h))
        self.play(FadeIn(pair))
        self.say("一种条纹，在频谱上就是一对对称的亮点", wait=2)

        self.say("条纹越密，亮点离中心越远")
        self.play(r.animate.set_value(10), run_time=3, rate_func=there_and_back_with_pause)
        self.wait(0.5)
        self.play(r.animate.set_value(7), run_time=1.2)

        self.say("条纹转，亮点跟着转：连线垂直于条纹")
        self.play(th.animate.set_value(PI / 3), run_time=3)
        self.wait(1)
        self.play(th.animate.set_value(-PI / 4), run_time=3)
        self.wait(1.5)

        why = ui("为什么成对？实数图像的频谱一定中心对称", 24).set_color(MUTED).move_to([0, -2.75, 0])
        self.say("两个点其实是同一种条纹，只是方向正反")
        self.play(FadeIn(why))
        self.wait(2.5)
        self.hush()
        img.clear_updaters()
        self.wait(0.5)


class FourierSum(Narrated):
    def construct(self):
        thumbs = Group()
        for (u, v), color in SUM_WAVES:
            t = picture(grating(u, v), 1.5, nearest=True)
            thumbs.add(Group(t, frame_of(t, color)))
        thumbs.arrange(RIGHT, buff=0.55).move_to([-3.3, 2.3, 0])
        plus = VGroup(*[mono("+", 28).set_color(MUTED).move_to((thumbs[i].get_right() + thumbs[i + 1].get_left()) / 2)
                        for i in range(2)])

        mix = picture(SUM_IMG, 3.1, nearest=True).move_to([-3.3, -0.55, 0])
        mix_frame = frame_of(mix, FG)
        panel = FreqPanel(side=3.6, reach=12).move_to([3.4, 0.35, 0])
        right_h = heading("频谱（现算）", panel)

        self.say("几种条纹叠在一起呢？")
        self.play(LaggedStart(*[FadeIn(t) for t in thumbs], lag_ratio=0.3), FadeIn(plus))
        ghosts = [t[0].copy() for t in thumbs]
        self.play(*[g.animate.move_to(mix).set_opacity(0) for g in ghosts], FadeIn(mix), Create(mix_frame), run_time=1.5)
        self.remove(*ghosts)
        self.wait(1)

        self.say("频谱里就多出几对亮点，一种条纹一对")
        self.play(FadeIn(panel), FadeIn(right_h))
        found = peaks(SUM_IMG, 6)
        for t, ((u, v), color) in zip(thumbs, SUM_WAVES):
            assert (u, v) in found and (-u, -v) in found
            self.play(Indicate(t, scale_factor=1.08, color=color), FadeIn(peak_pair(panel, u, v, color)), run_time=1.0)
        self.wait(2)

        self.say("看着乱成一团的图，频谱上一眼就能拆开", wait=1.5)

        formula = MathTex(r"F(u,v)=\sum_{x,y} f(x,y)\,e^{-2\pi i\,(ux/W+vy/H)}", font_size=34).set_color(FG)
        formula.next_to(panel, DOWN, buff=0.35)
        self.say("数学上就是这一行：拿每种条纹去和图像比对")
        self.play(Write(formula), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(formula))
        self.hush()

        self.play(*[FadeOut(m) for m in self.mobjects])
        photo_a = gray(DATA / "start.layer2.png")
        photo_s = to_u8(np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(photo_a)))))
        photo = picture(photo_a.astype("uint8"), 3.2).move_to([-3.4, 0.35, 0])
        cloud = picture(photo_s, 3.2).move_to([3.4, 0.35, 0])
        arrow = Arrow(photo.get_right(), cloud.get_left(), buff=0.25, color=MUTED, stroke_width=3)
        fft = mono("FFT", 22).set_color(ACCENT).next_to(arrow, UP, buff=0.1)

        self.say("一张普通的图，频谱只是中心一团弥散的云")
        self.play(FadeIn(photo), FadeIn(heading("layer2（普通的图）", photo)))
        self.play(GrowArrow(arrow), FadeIn(fft))
        self.play(FadeIn(cloud), FadeIn(heading("它的频谱", cloud)))
        self.wait(1.5)
        self.say("要是有人往图里叠了整齐的周期纹理……", wait=1)
        self.say("它就会在云外面，变成格外整齐的亮斑", wait=2)
        self.hush()
        self.wait(0.5)


class FourierShift(Narrated):
    def construct(self):
        raw = to_u8(np.log1p(layer1_mag()))
        h, w = raw.shape
        assert h % 2 == 0 and w % 2 == 0
        H = 4.6
        full = picture(raw, H).move_to([0, 0.35, 0])
        border = frame_of(full)

        self.say("直接算出来的频谱，长这样")
        self.play(FadeIn(full), Create(border))
        self.wait(1)

        corners = VGroup(*[Circle(radius=0.38, color=GOLD, stroke_width=3).move_to(full.get_corner(c))
                           for c in (UL, UR, DL, DR)])
        self.say("零频和低频，全挤在四个角上")
        self.play(LaggedStart(*[Create(c) for c in corners], lag_ratio=0.2))
        self.wait(2)
        self.play(FadeOut(corners))

        # 四个象限各自成图，然后沿对角线互换
        hh, hw = h // 2, w // 2
        quads = {
            "tl": raw[:hh, :hw], "tr": raw[:hh, hw:],
            "bl": raw[hh:, :hw], "br": raw[hh:, hw:],
        }
        qh = H / 2
        qw = qh * hw / hh
        c = full.get_center()
        pos = {"tl": c + [-qw / 2, qh / 2, 0], "tr": c + [qw / 2, qh / 2, 0],
               "bl": c + [-qw / 2, -qh / 2, 0], "br": c + [qw / 2, -qh / 2, 0]}
        swap = {"tl": "br", "br": "tl", "tr": "bl", "bl": "tr"}
        tiles = {k: picture(a, qh).move_to(pos[k]) for k, a in quads.items()}
        outlines = {k: frame_of(t, ACCENT) for k, t in tiles.items()}

        swapped = np.block([[quads["br"], quads["bl"]], [quads["tr"], quads["tl"]]])
        assert np.array_equal(swapped, np.fft.fftshift(raw))

        self.say("fftshift：把四个象限沿对角线对调")
        self.add(*tiles.values())
        self.remove(full)
        self.play(*[Create(o) for o in outlines.values()])
        self.play(*[t.animate.scale(0.92) for t in tiles.values()],
                  *[o.animate.scale(0.92) for o in outlines.values()], run_time=0.6)
        self.play(*[tiles[k].animate.move_to(pos[swap[k]]).scale(1 / 0.92) for k in tiles],
                  *[outlines[k].animate.move_to(pos[swap[k]]).scale(1 / 0.92) for k in tiles],
                  run_time=2.5)
        self.play(*[FadeOut(o) for o in outlines.values()])

        centered = picture(np.fft.fftshift(raw), H).move_to(c)
        self.add(centered)
        self.remove(*tiles.values())
        mark = Circle(radius=0.32, color=GOLD, stroke_width=3).move_to(c)
        self.say("四个角拼到一起，零频落在正中心")
        self.play(Create(mark))
        self.wait(2)
        self.say("这只是换个摆法，信息一点没变", wait=1.5)
        self.play(FadeOut(mark))
        self.hush()
        self.wait(0.5)


class FourierLog(Narrated):
    def construct(self):
        mag = np.fft.fftshift(layer1_mag())
        ratio = mag.max() / np.median(mag)
        assert 40_000 < ratio < 60_000

        H = 4.0
        lin = picture(to_u8(mag), H).move_to([-1.6, 0.4, 0])
        border = frame_of(lin)
        tag = chip("线性显示", DANGER).next_to(border, UP, buff=0.18)

        self.say("还有一步：要是直接把强度当亮度画……")
        self.play(FadeIn(lin), Create(border), FadeIn(tag))
        self.wait(1)
        self.say("几乎全黑，只有正中心一个亮点")
        self.play(Circumscribe(Dot(lin.get_center(), radius=0.12), shape=Circle, color=GOLD, fade_out=True), run_time=1.5)
        self.wait(1)

        stat = VGroup(
            ui("零频的强度", 24).set_color(MUTED),
            mono(f"≈ 中位数 × {round(ratio, -3):,.0f}", 28).set_color(GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(border, RIGHT, buff=0.6)
        self.say("因为零频比别的点强了好几万倍")
        self.play(FadeIn(stat, shift=LEFT * 0.2))
        self.wait(2)

        formula = MathTex(r"y=\ln(1+x)", font_size=44).set_color(FG)
        formula.next_to(stat, DOWN, buff=0.6, aligned_edge=LEFT)
        ax = Axes(x_range=[0, 10, 10], y_range=[0, 2.5, 2.5], x_length=2.6, y_length=1.3, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 1.2, "include_ticks": False})
        ax.next_to(formula, DOWN, buff=0.3, aligned_edge=LEFT)
        curve = ax.plot(lambda x: np.log1p(x), color=ACCENT, stroke_width=3)

        self.say("log1p：取个对数，把几万倍压成几倍")
        self.play(Write(formula), Create(ax), Create(curve), run_time=1.5)
        self.wait(1.5)

        log_img = picture(layer1_spec(), H).move_to(lin)
        tag2 = chip("取对数后", OK).move_to(tag)
        self.play(FadeTransform(lin, log_img), FadeTransform(tag, tag2), run_time=2)
        self.say("暗处的细节全都浮上来了", wait=2)
        self.play(FadeOut(formula), FadeOut(ax), FadeOut(curve))
        self.say("这就是 fft_view.py 的全部：fft2 → fftshift → log1p", wait=2.5)
        self.hush()
        self.wait(0.5)


class FourierReveal(Narrated):
    def construct(self):
        H = 2.9
        src_rgb = np.asarray(Image.open(DATA / "start.layer1.png").convert("RGB"))
        src = picture(src_rgb, H).move_to([-3.6, 1.3, 0])
        spec = picture(layer1_spec(), H).move_to([3.6, 1.3, 0])
        arrow = Arrow(src.get_right(), spec.get_left(), buff=0.25, color=MUTED, stroke_width=3)
        fft = mono("FFT", 22).set_color(ACCENT).next_to(arrow, UP, buff=0.1)

        self.say("回到 layer1：四角那种细密的波纹，就是线索")
        self.play(FadeIn(src), FadeIn(heading("start.layer1.png", src)))
        self.wait(1.5)
        self.play(GrowArrow(arrow), FadeIn(fft))
        self.play(FadeIn(spec), FadeIn(heading("它的频谱", spec)))
        self.wait(1)

        def region(img_mob: Mobject, band) -> Rectangle:
            h, w = layer1_spec().shape
            ys, xs = band
            sx, sy = img_mob.width / w, img_mob.height / h
            ul = img_mob.get_corner(UL)
            rect = Rectangle(width=(xs.stop - xs.start) * sx, height=(ys.stop - ys.start) * sy,
                             stroke_color=GOLD, stroke_width=2.5)
            rect.move_to(ul + [(xs.start + xs.stop) / 2 * sx, -(ys.start + ys.stop) / 2 * sy, 0])
            return rect

        top = region(spec, BAND)
        h, w = layer1_spec().shape
        mirror_band = (slice(h - BAND[0].stop + 1, h - BAND[0].start + 1), slice(w - BAND[1].stop + 1, w - BAND[1].start + 1))
        bottom = region(spec, mirror_band)
        self.say("云的外面，上下各有一行整齐的亮斑")
        self.play(Create(top), Create(bottom))
        self.wait(1.5)

        crop1 = picture(stretch(layer1_spec()[BAND].astype(float)), 1.55).move_to([0, -1.55, 0])
        self.say("把上面那行放大")
        self.play(TransformFromCopy(top, frame_of(crop1, GOLD)), FadeIn(crop1), run_time=1.5)
        word = mono("outside_the_birdcage", 30).set_color(GOLD).next_to(crop1, DOWN, buff=0.2)
        self.play(Write(word))
        self.wait(2)
        self.say("下面那行是它转了 180°：还是那个中心对称", wait=2.5)

        self.hush()
        self.play(*[FadeOut(m) for m in self.mobjects])

        # diff：把底图减掉，只剩被叠加进去的那层
        diff_rgb = np.asarray(Image.open(DATA / "start.diff_x8.png").convert("RGB"))
        l2_rgb = np.asarray(Image.open(DATA / "start.layer2.png").convert("RGB"))
        Hs = 2.0
        a = picture(src_rgb, Hs)
        b = picture(l2_rgb, Hs)
        d = picture(diff_rgb, Hs)
        minus, eq = mono("−", 36).set_color(MUTED), mono("=", 36).set_color(MUTED)
        row = Group(a, minus, b, eq, d).arrange(RIGHT, buff=0.35).move_to([0, 1.9, 0])
        labels = [ui(t, 20).set_color(MUTED).next_to(m, DOWN, buff=0.12)
                  for t, m in ((
                      "layer1", a), ("layer2（底图）", b), ("diff（放大 8 倍）", d))]

        self.say("更好的办法：先把底图 layer2 减掉")
        self.play(FadeIn(a), FadeIn(minus), FadeIn(b), *[FadeIn(l) for l in labels[:2]])
        self.play(FadeIn(eq), FadeIn(d), FadeIn(labels[2]))
        self.wait(1)
        self.say("剩下的，正是出题人叠进去的那层纹理", wait=2)

        c_l1 = picture(stretch(layer1_spec()[BAND].astype(float)), 1.15)
        c_df = picture(stretch(diff_spec()[BAND].astype(float)), 1.15)
        col = Group(c_l1, c_df).arrange(DOWN, buff=0.5).move_to([0.9, -1.75, 0])
        t1 = ui("layer1 的频谱", 22).set_color(MUTED).next_to(c_l1, LEFT, buff=0.35)
        t2 = ui("diff 的频谱", 22).set_color(OK).next_to(c_df, LEFT, buff=0.35)

        self.say("同一处放大对比：没有底图的干扰，字更干净")
        self.play(FadeIn(c_l1), FadeIn(t1))
        self.play(FadeIn(c_df), FadeIn(t2), Create(frame_of(c_df, OK)))
        self.wait(3)
        self.hush()
        self.wait(0.5)
