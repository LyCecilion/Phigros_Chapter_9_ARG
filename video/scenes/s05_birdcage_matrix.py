"""s05 · 13 个字符串：第一列排成 IGNORANCE，尾字母是 DISPOSSESSION。

用法：
    ./render.sh -ql scenes/s05_birdcage_matrix.py BirdcageOrder  # 13 个字符串 → 矩阵 + 两个黑体词
    ./render.sh -ql scenes/s05_birdcage_matrix.py BirdcagePhrase # 四个六边形读出的片段 → 拉丁文

说明：三角形网格与六边形那一段（Figma 叠加、顺时针读 6 格）改由录屏手动演示，
这里只保留 Manim 做得比录屏更清楚的部分。

矩阵与片段都在加载时现算，并与 README 的结果逐项断言：
    - 第 3..11 行的首字符拼成 IGNORANCE（前面 2 行与最后 2 行是干扰项）
    - 13 个尾字母拼成 DISPOSSESSION
    - 四个片段按先后接起来就是 Cogito,_ubi_sit_refugium

四个片段对应的六边形位置（左上角，行列）与顺时针读序，留作录屏时的参照：
    (3, 4) → Cogito      (2, 7) → fugium
    (7, 2) → sit_re       (10, 9) → ,_ubi_
    顺时针：右上 → 右中 → 右下 → 左下 → 左中 → 左上
"""

from manim import *
from style import *

# --- 数据 ---------------------------------------------------------------------

MATRIX = [
    "?aT?~!4*jK^D",
    "$6&Dj#f=6T+I",
    "IV7aN2emf9nS",
    "G#TroCyuuH#P",
    "Nf9etodigrAO",
    "OU/@ig=!9~VS",
    "R#m6Aya#N=$S",
    "ALes@K3@MtmE",
    "N2riNdAuY~US",
    "C4_tubAxU+/S",
    "E&r%JaM/9_,I",
    "u~D4wBeN3i_O",
    "1$R&fuH6AbuN",
]

ROWS, COLS = len(MATRIX), len(MATRIX[0])
ORDER = "IGNORANCE"
TAIL = "DISPOSSESSION"

FIRSTS = "".join(s[0] for s in MATRIX)
LASTS = "".join(s[-1] for s in MATRIX)
assert (ROWS, COLS) == (13, 12)
assert FIRSTS[2:11] == ORDER, FIRSTS  # 跳过开头的 ? $ 与结尾的 u 1
assert LASTS == TAIL, LASTS

# 六边形顺时针读出的四个片段（按在最终字符串中的先后）
WORDS = ["Cogito", ",_ubi_", "sit_re", "fugium"]
TARGET = "Cogito,_ubi_sit_refugium"
assert "".join(WORDS) == TARGET, WORDS
PHRASE_ZH = "我思，避难所何在？"


# --- 场景 ---------------------------------------------------------------------


class BirdcageOrder(Narrated):
    """13 个乱序字符串 → 第一列排成 IGNORANCE，尾字母是 DISPOSSESSION。"""

    def construct(self):
        rows = VGroup(*[mono(s, 24).set_color(FG) for s in MATRIX])
        rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0.5, 0.65, 0])
        idx = VGroup(*[mono(str(i), 18).set_color(MUTED) for i in range(ROWS)])
        for k, t in enumerate(idx):
            t.next_to(rows[k], LEFT, buff=0.4)

        self.say("玩家从 highlights 里攒到 13 个字符串，每个 12 个字符，看着全是乱码")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.06, run_time=2), FadeIn(idx))
        self.wait(1.5)

        self.say("注意第一列")
        self.play(*[Indicate(rows[k][0], color=GOLD, scale_factor=1.6) for k in range(ROWS)], run_time=1.8)
        col = VGroup(*[mono(s[0], 26).set_color(GOLD) for s in MATRIX]).arrange(RIGHT, buff=0.18)
        col.move_to([0, -2.35, 0])
        self.play(LaggedStart(*[TransformFromCopy(rows[k][0], col[k]) for k in range(ROWS)], lag_ratio=0.05), run_time=1.5)
        self.wait(1)
        self.say("从上往下读：? $ I G N O R A N C E u 1")
        self.wait(2)

        brace = Brace(VGroup(*col[2:11]), DOWN, buff=0.12, color=GOLD)
        word = mono(ORDER, 34).set_color(GOLD).next_to(brace, DOWN, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(word))
        self.say("第 3 到第 11 行正好是 IGNORANCE，前面 2 个和最后 2 个是干扰项", wait=2.5)
        self.play(FadeOut(brace), FadeOut(word), run_time=0.5)

        self.say("再看最后一列")
        lasts = VGroup(*[mono(s[-1], 26).set_color(CIPHER) for s in MATRIX]).arrange(RIGHT, buff=0.18)
        lasts.move_to([0, -2.35, 0])
        self.play(FadeOut(col), FadeIn(lasts), run_time=1.2)
        self.wait(1)
        self.say("13 个尾字母也是同一个词：DISPOSSESSION")
        tail = mono("D I S P O S S E S S I O N", 30).set_color(CIPHER).move_to([0, -3.05, 0])
        self.play(Transform(lasts, tail), run_time=1.5)
        self.wait(1.5)
        self.say("Stage I 那三句诗的最后一句，就是 the way of dispossession", wait=2.5)
        self.hush()
        self.wait(0.5)


class BirdcagePhrase(Narrated):
    """四个六边形读出的片段 → Cogito,_ubi_sit_refugium。"""

    def construct(self):
        self.say("四个六边形读出来的四段字符串")
        items = VGroup(*[mono(w, 42).set_color(GOLD) for w in WORDS])
        items.arrange(RIGHT, buff=0.75).move_to([0, 1.2, 0])
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.2) for i in items], lag_ratio=0.3, run_time=2))
        self.wait(2)

        self.say("按它们在最终字符串里的先后接起来")
        bar = Line(LEFT * 6.4, RIGHT * 6.4, color=MUTED, stroke_width=1.5).move_to(UP * 0.35)
        self.play(Create(bar), run_time=0.8)
        phrase = mono(TARGET, 44).set_color(FG).move_to(UP * -0.35)
        self.play(Write(phrase), run_time=2)
        self.wait(1.5)

        self.say("这是一句拉丁文")
        zh = cn(PHRASE_ZH, 36).set_color(MUTED).next_to(phrase, DOWN, buff=0.7)
        ety = cn("cogito 我思 · refugium 避难所", 26).set_color(GOLD).next_to(zh, DOWN, buff=0.4)
        self.play(FadeIn(zh, shift=UP * 0.1))
        self.wait(1)
        self.play(FadeIn(ety, shift=UP * 0.1))
        self.wait(2)
        self.say("拼到 wiki 的地址后面，进入下一层", wait=2.5)
        self.hush()
        self.wait(0.5)


# 录屏时给 Figma 用的参照：四个六边形的左上角（行列）与顺时针读序
HEXES = {(2, 7): "fugium", (3, 4): "Cogito", (7, 2): "sit_re", (10, 9): ",_ubi_"}
CW = [(0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (0, 0)]


def read_hex(m: list[str], r: int, c: int) -> str:
    """按顺时针读序取出一个六边形的 6 个字符（供核对用，不参与渲染）。"""
    return "".join(m[r + dr][c + dc] for dr, dc in CW)


for _pos, _word in HEXES.items():
    assert read_hex(MATRIX, *_pos) == _word, (_pos, _word)
assert sorted(HEXES.values(), key=TARGET.index) == WORDS
