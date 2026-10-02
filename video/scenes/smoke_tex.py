"""MathTex 冒烟测试：验证 LaTeX + dvisvgm 链路。

运行:
    ./render.sh -ql scenes/smoke_tex.py SmokeTex
"""

from manim import *
from style import *


class SmokeTex(Scene):
    def construct(self):
        head = VGroup(
            cn("公式呈现自检", 40).set_color(FG),
            cn("LaTeX → dvisvgm → SVG", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.7)

        sha = MathTex(r"h = \mathrm{SHA512}(\mathrm{pw})", font_size=56).set_color(ACCENT)
        keys = MathTex(r"K = h[0:32],\qquad IV = h[32:48]", font_size=56).set_color(OK)
        cbc = MathTex(r"C_i = E_K\!\left(P_i \oplus C_{i-1}\right)", font_size=56).set_color(GOLD)

        rows = VGroup(sha, keys, cbc).arrange(DOWN, buff=0.7).shift(DOWN * 0.15)

        self.play(FadeIn(head, shift=DOWN * 0.2))
        for row in rows:
            self.play(Write(row), run_time=0.8)
            self.wait(0.35)
        self.play(Indicate(keys, color=OK, scale_factor=1.04))
        self.wait(0.6)
