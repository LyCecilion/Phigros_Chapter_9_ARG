"""冒烟测试：验证「中文渲染 + mp4 出片 + 关键构件」链路可用。

运行:
    ./render.sh -ql scenes/smoke.py Smoke
产物:
    media/videos/smoke/480p15/Smoke.mp4
"""

from manim import *
from style import *


class Smoke(Scene):
    """一条极简流水线：password --SHA512--> h --切片--> Key/IV。"""

    def construct(self):
        title = cn("穹顶孤舟 · 原理呈现", 54).set_color(FG)
        sub = cn("渲染链路自检", 26).set_color(MUTED)
        head = VGroup(title, sub).arrange(DOWN, buff=0.24).to_edge(UP, buff=0.7)

        pw = VGroup(mono("password", 28).set_color(ACCENT), cn("输入口令", 20).set_color(MUTED))
        hz = VGroup(mono("SHA512", 28).set_color(ACCENT), cn("哈希 64 字节", 20).set_color(MUTED))
        kv = VGroup(
            mono("Key = h[0:32]", 28).set_color(OK),
            mono("IV  = h[32:48]", 28).set_color(OK),
        )
        stages = VGroup(pw, hz, kv)
        for stage in stages:
            stage.arrange(DOWN, buff=0.22)
            stage.add(box(stage))
        stages.arrange(RIGHT, buff=1.5).shift(DOWN * 0.2)

        arrows = VGroup(
            Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.12, color=MUTED,
                  max_tip_length_to_length_ratio=0.16),
            Arrow(stages[1].get_right(), stages[2].get_left(), buff=0.12, color=MUTED,
                  max_tip_length_to_length_ratio=0.16),
        )

        self.play(FadeIn(head, shift=DOWN * 0.2))
        self.play(FadeIn(stages[0], shift=RIGHT * 0.3))
        self.play(GrowArrow(arrows[0]), FadeIn(stages[1]))
        self.play(GrowArrow(arrows[1]), FadeIn(stages[2]))
        self.play(Indicate(stages[2], color=OK, scale_factor=1.06))
        self.wait(0.8)
