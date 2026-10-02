"""s05 · 13 个字符串：尾字母 DISPOSSESSION、首字母 IGNORANCE → 排成矩阵。

用法：
    ./render.sh -ql scenes/s05_birdcage_matrix.py BirdcageOrder  # 13 个字符串 → 两个词 → 矩阵
    ./render.sh -ql scenes/s05_birdcage_matrix.py BirdcagePhrase # 四个六边形读出的片段 → 拉丁文

说明：三角形网格与六边形那一段（Figma 叠加、顺时针读 6 格）改由录屏手动演示，
这里只保留 Manim 做得比录屏更清楚的部分。

BirdcageOrder 按玩家实际的思路走一遍：
    1. 13 个字符串先按 README 里 sort 之后的顺序排开；
    2. 取出每一行的最后一个字符（全是大写字母），重排成 DISPOSSESSION；
    3. 取出每一行第一个字符里的大写字母（另外 4 个是干扰项），重排成 IGNORANCE；
    4. 按第一列大写字母的顺序把这 13 行换位，得到最终矩阵。

矩阵与片段都在加载时现算，并与 README 的结果逐项断言：
    - 13 个尾字母就是 DISPOSSESSION 的字母，首字母里的大写字母就是 IGNORANCE 的字母
    - 换位后第一列自上而下是 ? $ I G N O R A N C E u 1，最后一列恰好是 DISPOSSESSION
    - 四个片段按先后接起来就是 Cogito,_ubi_sit_refugium

四个片段对应的六边形位置（左上角，行列）与顺时针读序，留作录屏时的参照：
    (3, 4) → Cogito      (2, 7) → fugium
    (7, 2) → sit_re       (10, 9) → ,_ubi_
    顺时针：右上 → 右中 → 右下 → 左下 → 左中 → 左上
"""

from manim import *
from style import *

# --- 数据 ---------------------------------------------------------------------

# 玩家从 highlights 接口攒到的 13 个字符串，按 README 里 sort 之后的顺序排开
SORTED = [
    "$6&Dj#f=6T+I",
    "1$R&fuH6AbuN",
    "ALes@K3@MtmE",
    "?aT?~!4*jK^D",
    "C4_tubAxU+/S",
    "E&r%JaM/9_,I",
    "G#TroCyuuH#P",
    "IV7aN2emf9nS",
    "N2riNdAuY~US",
    "Nf9etodigrAO",
    "OU/@ig=!9~VS",
    "R#m6Aya#N=$S",
    "u~D4wBeN3i_O",
]

# 按第一列的大写字母重新排好之后得到的矩阵
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

ROWS, COLS = len(SORTED), len(SORTED[0])
ORDER = "IGNORANCE"
TAIL = "DISPOSSESSION"

PERM = [SORTED.index(s) for s in MATRIX]  # 换位后第 i 行来自 SORTED 的第 PERM[i] 行
HEAD_UPPER = "".join(s[0] for s in SORTED if s[0].isupper())
LASTS_SORTED = "".join(s[-1] for s in SORTED)
UPHEADS = [k for k, s in enumerate(SORTED) if s[0].isupper()]

FIRSTS = "".join(s[0] for s in MATRIX)
LASTS = "".join(s[-1] for s in MATRIX)
assert (ROWS, COLS) == (13, 12)
assert {*SORTED} == {*MATRIX} and len({*SORTED}) == ROWS  # 同一批字符串，只是换了位置
assert sorted(PERM) == list(range(ROWS))
assert LASTS_SORTED.isupper(), LASTS_SORTED  # 13 个尾字母清一色大写
assert sorted(LASTS_SORTED) == sorted(TAIL), LASTS_SORTED
assert HEAD_UPPER == "ACEGINNOR" and sorted(HEAD_UPPER) == sorted(ORDER), HEAD_UPPER
assert FIRSTS[2:11] == ORDER, FIRSTS  # 换位后跳过开头的 ? $ 与结尾的 u 1
assert LASTS == TAIL, LASTS  # 换位后最后一列自上而下正好拼出 DISPOSSESSION

# 六边形顺时针读出的四个片段（按在最终字符串中的先后）
WORDS = ["Cogito", ",_ubi_", "sit_re", "fugium"]
TARGET = "Cogito,_ubi_sit_refugium"
assert "".join(WORDS) == TARGET, WORDS
PHRASE_ZH = "我思，避难所何在？"


# --- 构件 ---------------------------------------------------------------------

# 版面：13 行正文在上，两个「取出来的词」并排在下
ROW_SIZE = 26  # 13 行正文
ROW_STEP = 0.44  # 行距按基线算，不是按包围盒中心
ROW_BASE_Y = 3.42  # 第一行的基线
IDX_SIZE = 18  # 行号
IDX_GAP = 0.34
STRIP_SIZE = 40  # 取出来的字母（放大一档，方便看清）
STRIP_Y = -2.75
STRIP_GAP = 0.9  # 两个词之间的间隔


def baseline_dy(text: str, size: float) -> float:
    """一行文字的基线相对它墨迹中心的偏移（借平底的 H 当基线探针）。

    Text 的包围盒是墨迹范围：带 j、_、~ 的行会被降部撑高。要是按中心摆放，
    13 行的基线最多能差 0.10 scene unit（1080p 下约 14 px），整张表看着会浮。
    这里统一把基线摆到刻度上。
    """
    probe = mono(text + "H", size)
    below = probe.get_bottom()[1] - probe[-1].get_bottom()[1]  # 基线以下的深度，≤ 0
    return -mono(text, size).height / 2 - below


def nth_targets(src: str, dst: str) -> list[int]:
    """第 k 个字符该去 dst 里「同字符第 n 次出现」的位置，即一次重排。"""
    assert sorted(src) == sorted(dst), (src, dst)
    seen: dict[str, int] = {}
    out: list[int] = []
    for ch in src:
        seen[ch] = seen.get(ch, 0) + 1
        out.append([j for j, d in enumerate(dst) if d == ch][seen[ch] - 1])
    return out


# --- 场景 ---------------------------------------------------------------------


class BirdcageOrder(Narrated):
    """13 个字符串：尾字母 → DISPOSSESSION，首字母 → IGNORANCE，再换位成矩阵。"""

    def construct(self):
        # 1. 13 行先按 sort 之后的顺序排开；按基线对齐，降部就不会把行距带歪
        row_w = max(mono(s, ROW_SIZE).width for s in SORTED)
        tag_w = mono(str(ROWS), IDX_SIZE).width
        row_x = -(tag_w + IDX_GAP + row_w) / 2 + tag_w + IDX_GAP

        rows: list[Text] = []
        lines: list[VGroup] = []
        for k, s in enumerate(SORTED):
            base = ROW_BASE_Y - k * ROW_STEP
            row = mono(s, ROW_SIZE).set_color(FG)
            row.move_to([row_x, base - baseline_dy(s, ROW_SIZE), 0], aligned_edge=LEFT)
            tag = mono(str(k + 1), IDX_SIZE).set_color(MUTED)
            tag.move_to([row_x - IDX_GAP, base - baseline_dy(str(k + 1), IDX_SIZE), 0], aligned_edge=RIGHT)
            rows.append(row)
            lines.append(VGroup(tag, row))

        self.say("玩家从 highlights 接口那里攒到 13 个字符串，每行 12 个字符")
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.15) for line in lines], lag_ratio=0.05, run_time=1.8))
        self.wait(1.2)

        # 2. 尾字母清一色大写，取下来重排成 DISPOSSESSION
        tail_w = mono(TAIL, STRIP_SIZE).width
        head_w = mono(ORDER, STRIP_SIZE).width
        span = (tail_w + STRIP_GAP + head_w) / 2
        tail_x, head_x = -span + tail_w / 2, span - head_w / 2

        self.say("先看每一行的最后一个字符：清一色都是大写字母")
        self.play(*[Indicate(rows[k][-1], color=CIPHER, scale_factor=2.2) for k in range(ROWS)], run_time=1.6)
        self.play(*[rows[k][-1].animate.set_color(CIPHER) for k in range(ROWS)], run_time=0.4)

        slots = mono(LASTS_SORTED, STRIP_SIZE).move_to([tail_x, STRIP_Y, 0])  # 只借它的位置
        strip = VGroup(
            *[mono(ch, STRIP_SIZE).set_color(CIPHER).move_to(slots[k].get_center()) for k, ch in enumerate(LASTS_SORTED)]
        )
        self.say("把这 13 个尾字母取下来，先按行的顺序排成一排")
        self.play(LaggedStart(*[TransformFromCopy(rows[k][-1], strip[k]) for k in range(ROWS)], lag_ratio=0.08), run_time=1.8)
        self.add(strip)
        self.wait(0.8)

        self.say("重新排列之后，就是 Stage I 那句 the way of dispossession")
        tail_word = mono(TAIL, STRIP_SIZE).move_to([tail_x, STRIP_Y, 0])
        self.play(
            *[strip[k].animate.move_to(tail_word[j].get_center()) for k, j in enumerate(nth_targets(LASTS_SORTED, TAIL))],
            run_time=2.0,
        )
        self.wait(0.8)
        self.say("DISPOSSESSION —— 舍弃占有", wait=1.5)

        # 3. 首字母里只有 9 个大写字母是真信息
        self.say("再看每一行的第一个字符")
        self.play(*[Indicate(rows[k][0], color=GOLD, scale_factor=2.2) for k in range(ROWS)], run_time=1.6)
        self.play(*[rows[k][0].animate.set_color(MUTED) for k in range(ROWS) if k not in UPHEADS], run_time=0.5)
        self.say("$ 1 ? u 只是干扰项，只有 9 个大写字母是真信息", wait=0.8)
        self.play(*[rows[k][0].animate.set_color(GOLD) for k in UPHEADS], run_time=0.5)

        slots = mono(HEAD_UPPER, STRIP_SIZE).move_to([head_x, STRIP_Y, 0])
        head = VGroup(
            *[mono(ch, STRIP_SIZE).set_color(GOLD).move_to(slots[i].get_center()) for i, ch in enumerate(HEAD_UPPER)]
        )
        self.say("把这 9 个大写字母也取下来")
        self.play(LaggedStart(*[TransformFromCopy(rows[k][0], head[i]) for i, k in enumerate(UPHEADS)], lag_ratio=0.08), run_time=1.8)
        self.add(head)
        self.wait(0.8)

        self.say("重排之后得到 IGNORANCE —— the way of ignorance")
        head_word = mono(ORDER, STRIP_SIZE).move_to([head_x, STRIP_Y, 0])
        self.play(
            *[head[i].animate.move_to(head_word[j].get_center()) for i, j in enumerate(nth_targets(HEAD_UPPER, ORDER))],
            run_time=1.8,
        )
        self.wait(1.2)

        # 4. 按第一列大写字母的顺序把这 13 行换位
        dest = [0] * ROWS
        for i, k in enumerate(PERM):
            dest[k] = i
        self.say("现在按第一列大写字母的顺序，把这 13 行重新排一遍")
        self.play(*[lines[k].animate.shift(DOWN * ((dest[k] - k) * ROW_STEP)) for k in range(ROWS)], run_time=2.6)
        self.wait(1.2)

        at = [rows[k] for k in PERM]  # 换位后自上而下的每一行
        self.say("第一列自上而下：? $ I G N O R A N C E u 1")
        self.play(*[Indicate(at[i][0], color=GOLD, scale_factor=1.8) for i in range(2, 11)], run_time=1.8)
        self.wait(0.8)
        self.say("最后一列自上而下正好是 DISPOSSESSION —— 两个词都回来了")
        self.play(*[Indicate(at[i][-1], color=CIPHER, scale_factor=1.8) for i in range(ROWS)], run_time=1.8)
        self.wait(0.6)
        self.say("这张 13 × 12 的表，就是下一步栅栏密码要用的矩阵", wait=2.0)
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
