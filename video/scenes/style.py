"""共享视觉风格：配色、中文字体、常用构件。

场景文件里直接:  from style import *
"""

from manim import *
from manimpango import list_fonts

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


# --- 图形构件 ---------------------------------------------------------------
def box(mob, color=MUTED, buff: float = 0.22, **kw) -> SurroundingRectangle:
    """给任意 mobject 套圆角边框。"""
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, **kw)


def chip(text: str, color=ACCENT, size: float = 24) -> VGroup:
    """小标签：文字 + 同色细框。"""
    label = ui(text, size).set_color(color)
    return VGroup(label, box(label, color=color, buff=0.14))


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


class Narrated(Scene):
    """带底部占位字幕的场景；字幕只给旁白对节奏，剪辑时可整体删掉。"""

    caption: Mobject | None = None

    def say(self, text: str, wait: float = 0.0):
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
