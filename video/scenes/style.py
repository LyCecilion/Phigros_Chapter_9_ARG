"""共享视觉风格：配色、中文字体、常用构件。

场景文件里直接:  from style import *
"""

import os

from manim import *
from manimpango import list_fonts

from collections.abc import Sequence

_AVAILABLE = frozenset(list_fonts())


def pick_font(*candidates: str) -> str:
    """返回第一个真实存在的字体名（都不存在时返回最后一个作为兜底）。"""
    for name in candidates:
        if name in _AVAILABLE:
            return name
    return candidates[-1]


# --- 字体 -------------------------------------------------------------------
CJK = pick_font("LXGW WenKai", "Noto Sans CJK SC", "Sarasa UI CL", "sans-serif")
CJK_SANS = pick_font("Noto Sans CJK SC", "Sarasa UI CL", "LXGW WenKai", "sans-serif")
CJK_MONO = pick_font("Sarasa Mono SC", "Sarasa Mono CL", "Noto Sans Mono CJK SC", "monospace")

# --- 配色 -------------------------------------------------------------------
BG = "#0E1116"      # 背景
FG = "#E8EAED"      # 正文
MUTED = "#8B93A7"   # 次要说明
ACCENT = "#4CC2FF"  # 主题青
CIPHER = "#C792EA"  # 密文 / 未知
DANGER = "#FF5C7A"  # 拒绝 / 错误
OK = "#59D9A4"      # 通过 / 校验成功
GOLD = "#FFC857"    # 关键高亮


# --- 文本构件 ---------------------------------------------------------------
def cn(text: str, size: float = 32, **kw) -> Text:
    """正文中文（霞鹜文楷）。"""
    return Text(text, font=CJK, font_size=size, **kw)


def ui(text: str, size: float = 32, **kw) -> Text:
    """界面感中文（黑体）。"""
    return Text(text, font=CJK_SANS, font_size=size, **kw)


def mono(text: str, size: float = 26, **kw) -> Text:
    """等宽文本：伪代码、十六进制、地址。"""
    return Text(text, font=CJK_MONO, font_size=size, **kw)


# --- 排版 ---------------------------------------------------------------------

CHIP_PAD = 0.14  # 文字与细框之间的留白
CHIP_REF = "Hg字"  # 升部 · 降部 · 汉字：三个都盖住，chip 的框高才是固定的


def baseline_offset(text: str, size: float, font: str = CJK_MONO, **kw) -> float:
    """一行文字的基线相对它墨迹中心的纵坐标偏移（借平底的 H 当基线探针）。

    Manim 的 Text 拿墨迹范围当包围盒：带降部的行（j、_、~）会被撑高，纯大写的行更矮。
    要是按中心摆放，同一排 / 同一列的文字就会各自浮一截，排整齐得对齐基线。
    """
    probe = Text(text + "H", font=font, font_size=size, **kw)
    below = probe.get_bottom()[1] - probe[-1].get_bottom()[1]  # 基线以下多深，≤ 0
    return -Text(text, font=font, font_size=size, **kw).height / 2 - below


def place_baseline(mob: Mobject, text: str, size: float, baseline_y: float, font: str = CJK_MONO, **kw) -> Mobject:
    """把一行文字（Text）的基线摆到 baseline_y。"""
    mob.shift(UP * (baseline_y - mob.get_center()[1] - baseline_offset(text, size, font, **kw)))
    return mob


def baseline_row(
    texts: Sequence[str],
    size: float,
    font: str = CJK_MONO,
    buff: float = 0.35,
    baseline_y: float | None = None,
    **kw,
) -> VGroup:
    """一排共享基线的文字；给了 baseline_y 就把这条基线摆到那个高度。"""
    texts = list(texts)
    row = VGroup(*[Text(t, font=font, font_size=size, **kw) for t in texts]).arrange(RIGHT, buff=buff)
    for item, t in zip(row, texts):
        item.shift(DOWN * baseline_offset(t, size, font, **kw))
    if baseline_y is not None:
        row.shift(UP * baseline_y)  # 各字形的基线此时都在 0
    return row


# --- 图形构件 ---------------------------------------------------------------
def box(mob, color=MUTED, buff: float = 0.22, **kw) -> SurroundingRectangle:
    """给任意 mobject 套圆角边框。"""
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, **kw)


def chip(text: str, color=ACCENT, size: float = 24) -> VGroup:
    """小标签：文字 + 同色细框。

    框高按固定行框（升部 + 降部 + 汉字）算，不跟着墨迹走；文字统一坐在同一条基线上，
    于是 tEXt / pHYs / gAMA 这种大小写混排的标签不会一个高一个矮、字也不会错行。
    """
    label = ui(text, size).set_color(color)
    ref = ui(CHIP_REF, size)
    place_baseline(label, text, size, ref[0].get_bottom()[1], CJK_SANS)
    rect = RoundedRectangle(
        width=label.width + 2 * CHIP_PAD,
        height=ref.height + 2 * CHIP_PAD,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=4,
    )
    return VGroup(label, rect)


def glyphs(text: Text, source: str, sub: str, nth: int = 0) -> VGroup:
    """取出 Text 中第 nth 处 sub 对应的字形（Text 的子对象不含空白字符）。"""
    start = -1
    for _ in range(nth + 1):
        start = source.index(sub, start + 1)
    def count(s: str) -> int:
        return sum(not ch.isspace() for ch in s)
    a = count(source[:start])
    return text[a : a + count(sub)]


# --- 场景基类 ---------------------------------------------------------------
CAPTION_Y = -3.62

# 出片时设 OMP_NO_CAPTION=1：底部字幕不上屏，但每句话占的时长原样保留，
# 于是「带字幕版」和「纯画面版」的动画节奏、总时长完全一致（方便拿画面配旁白）。
NO_CAPTION = bool(os.environ.get("OMP_NO_CAPTION"))


class Narrated(Scene):
    """带底部占位字幕的场景；字幕只给旁白对节奏，剪辑时可整体删掉。"""

    caption: Mobject | None = None

    def say(self, text: str, wait: float = 0.0):
        if NO_CAPTION:
            # 看不见的占位字幕：让后面 FadeOut(self.caption) 的时长与带字幕版一致
            self.caption = Dot(radius=0.01).set_opacity(0).move_to([0, CAPTION_Y, 0])
            self.wait(0.6)
            if wait:
                self.wait(wait)
            return
        new = cn(text, 26).set_color(FG).move_to([0, CAPTION_Y, 0])
        if self.caption is None:
            self.play(FadeIn(new, shift=UP * 0.15), run_time=0.6)
        else:
            self.play(FadeOut(self.caption, shift=UP * 0.15), FadeIn(new, shift=UP * 0.15), run_time=0.6)
        self.caption = new
        if wait:
            self.wait(wait)

    def hush(self):
        """收起当前字幕。"""
        if self.caption is not None:
            self.play(FadeOut(self.caption), run_time=0.4)
            self.caption = None
