"""s06 · 零宽字符与 Morse：看不见的字符也可以携带信息。"""

from pathlib import Path

from manim import *
from style import *

# --- 从 README 现场提取数据 --------------------------------------------------

README = Path(__file__).resolve().parents[2] / "README.md"
ZERO = frozenset("\u200b\u200c\u200d")
ZERO_COLORS = {"\u200b": ACCENT, "\u200c": GOLD, "\u200d": CIPHER}
ZERO_NAMES = {
    "\u200b": "U+200B  ZERO WIDTH SPACE",
    "\u200c": "U+200C  ZERO WIDTH NON-JOINER",
    "\u200d": "U+200D  ZERO WIDTH JOINER",
}


def read_quote(prefix: str) -> str:
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.startswith("> " + prefix):
            return line[2:]
    raise ValueError(f"README quote not found: {prefix}")


def hidden_part(text: str) -> str:
    return "".join(ch for ch in text if ch in ZERO)


def visible_part(text: str) -> str:
    return "".join(ch for ch in text if ch not in ZERO)


COGITO = read_quote("Technology can expand")
DISORIENTATION = read_quote("In what sense, exactly,")
HIDDEN_1 = hidden_part(COGITO)
HIDDEN_2 = hidden_part(DISORIENTATION)
VISIBLE_1 = visible_part(COGITO)
VISIBLE_2 = visible_part(DISORIENTATION)

assert len(HIDDEN_1) == 43
assert len(HIDDEN_2) == 26
assert VISIBLE_1 == "Technology can expand the boundaries of humanity,  it can also fabricate the semblance of reality."
assert VISIBLE_2 == 'In what sense, exactly, do we "truly" inhabit the "world"?'

# 标题 .Bravo _Charlie ␣Delta 给出的映射：B → 点，C → 横线，D → 分隔。
TO_MORSE = {"\u200b": ".", "\u200c": "_", "\u200d": " "}
MORSE = {
    "A": "._", "B": "_...", "C": "_._.", "D": "_..", "E": ".",
    "F": ".._.", "G": "__.", "H": "....", "I": "..", "J": ".___",
    "K": "_._", "L": "._..", "M": "__", "N": "_.", "O": "___",
    "P": ".__.", "Q": "__._", "R": "._.", "S": "...", "T": "_",
    "U": ".._", "V": "..._", "W": ".__", "X": "_.._", "Y": "_.__",
    "Z": "__..",
}


def to_morse(hidden: str) -> str:
    return "".join(TO_MORSE[ch] for ch in hidden)


def decode_morse(code: str) -> str:
    reverse = {value: key for key, value in MORSE.items()}
    return "".join(reverse[group] for group in code.split())


MORSE_1 = to_morse(HIDDEN_1)
MORSE_2 = to_morse(HIDDEN_2)
assert MORSE_1 == "_.. .. ... ___ ._. .. . _. _ ._ _ .. ___ _."
assert MORSE_2 == "._ ._. ___ .._ ... ._ ._.."
assert decode_morse(MORSE_1) == "DISORIENTATION"
assert decode_morse(MORSE_2) == "AROUSAL"


# --- 构件 ---------------------------------------------------------------------


def hidden_cells(hidden: str, per_row: int = 22, size: float = 0.22) -> VGroup:
    """把不可见字符画成可寻址的小色块。"""
    cells = VGroup()
    step = size + 0.065
    rows = (len(hidden) + per_row - 1) // per_row
    for i, ch in enumerate(hidden):
        col, row = i % per_row, i // per_row
        rect = Square(side_length=size, stroke_color=ZERO_COLORS[ch], stroke_width=1.2)
        rect.set_fill(ZERO_COLORS[ch], opacity=0.24)
        rect.move_to([(col - (min(per_row, len(hidden) - row * per_row) - 1) / 2) * step,
                      (rows - 1) / 2 * 0.42 - row * 0.42, 0])
        cells.add(rect)
    return cells


def symbol_cells(hidden: str, per_row: int = 22) -> VGroup:
    cells = VGroup()
    step = 0.285
    rows = (len(hidden) + per_row - 1) // per_row
    for i, ch in enumerate(hidden):
        col, row = i % per_row, i // per_row
        symbol = "·" if TO_MORSE[ch] == " " else TO_MORSE[ch]
        mob = mono(symbol, 24).set_color(ZERO_COLORS[ch])
        mob.move_to([(col - (min(per_row, len(hidden) - row * per_row) - 1) / 2) * step,
                     (rows - 1) / 2 * 0.42 - row * 0.42, 0])
        cells.add(mob)
    return cells


def morse_groups(code: str, size: float = 25) -> VGroup:
    return VGroup(*[
        mono(group, size).set_color(ACCENT if i % 2 == 0 else GOLD)
        for i, group in enumerate(code.split())
    ]).arrange(RIGHT, buff=0.22)


def split_visible(text: str) -> tuple[str, str]:
    parts = text.split("  ", 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (text, "")


def sentence_lines(text: str, size: float = 25) -> VGroup:
    left, right = split_visible(text)
    items = [mono(left, size).set_color(FG)]
    if right:
        items.append(mono(right, size).set_color(FG))
    return VGroup(*items).arrange(DOWN, buff=0.28, aligned_edge=LEFT)


# 卡片：方块 + 三行文字。三行用基线定位，卡片之间才对得齐
# （`.` / `_` / `space` 的墨迹高低不同，按包围盒中心排会让它们各浮一截）
CARD_Y = 1.15
CARD_PITCH = 3.02
CARD_SQ_Y = 0.0
CARD_CODE_Y = -0.62
CARD_MAP_Y = -1.12
CARD_NOTE_Y = -1.55


def mapping_card(ch: str, symbol: str, name: str, color) -> VGroup:
    square = Square(side_length=0.52, stroke_color=color, stroke_width=1.8)
    square.set_fill(color, opacity=0.18)
    square.move_to([0, CARD_SQ_Y, 0])
    code_text = f"U+{ord(ch):04X}"
    map_text = symbol if symbol != " " else "space"
    code = mono(code_text, 19).set_color(color)
    mapping = mono(map_text, 25).set_color(OK)
    note = ui(name, 18).set_color(MUTED)
    place_baseline(code, code_text, 19, CARD_CODE_Y)
    place_baseline(mapping, map_text, 25, CARD_MAP_Y)
    place_baseline(note, name, 18, CARD_NOTE_Y, CJK_SANS)
    return VGroup(square, code, mapping, note)


# --- 场景 ---------------------------------------------------------------------


class ZeroWidthReveal(Narrated):
    """先证明文本看起来正常，但复制内容里有隐藏字符。"""

    def construct(self):
        lines = sentence_lines(VISIBLE_1, 28).move_to([0, 2.45, 0])
        self.say("页面上看起来只是一句普通英文")
        self.play(FadeIn(lines, shift=DOWN * 0.12))
        self.wait(1.0)

        # 隐藏字符夹在第一行的逗号之后，用一小段红虚线点出这个缝
        gap = DashedLine(ORIGIN, RIGHT * 0.85, color=DANGER, dash_length=0.09)
        gap.next_to(lines[0], RIGHT, buff=0.16)
        gap_tag = ui("复制时，这里多了东西", 22).set_color(DANGER)
        gap_tag.next_to(lines, DOWN, buff=0.3).align_to(gap, RIGHT)
        self.say("但复制这段文本，就会发现逗号后面多了一段完全不占宽度的内容")
        self.play(Create(gap), FadeIn(gap_tag, shift=UP * 0.1))
        self.wait(0.8)

        cells = hidden_cells(HIDDEN_1, size=0.40).move_to([0, -1.15, 0])
        cell_tag = ui(f"隐藏字符：{len(HIDDEN_1)} 个", 24).set_color(ACCENT).next_to(cells, UP, buff=0.34)
        self.play(FadeIn(cell_tag), LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.035), run_time=1.8)
        self.wait(1.6)
        self.hush()
        self.play(FadeOut(VGroup(lines, gap, gap_tag, cells, cell_tag)))


class ZeroWidthAlphabet(Narrated):
    """解释三种码点，以及标题给出的映射。"""

    def construct(self):
        cards = VGroup(*[
            mapping_card(ch, TO_MORSE[ch], ZERO_NAMES[ch].split("  ", 1)[1], ZERO_COLORS[ch])
            for ch in ("\u200b", "\u200c", "\u200d")
        ])
        for i, card in enumerate(cards):  # 按同一套基线排版，直接按列摆就是齐的
            card.move_to([(i - 1) * CARD_PITCH, CARD_Y, 0])
        self.say("一共只有三种字符，先把它们的 Unicode 码点认出来")
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in cards], lag_ratio=0.2), run_time=1.6)

        hint = baseline_row((".Bravo", "_Charlie", "␣Delta"), 28, buff=0.75, baseline_y=-0.2)
        for item, color in zip(hint, (ACCENT, GOLD, CIPHER)):
            item.set_color(color)
        arrow = Arrow(hint.get_bottom(), [0, -0.95, 0], color=MUTED, stroke_width=2)
        answer = baseline_row((".  →  点", "_  →  横线", "␣  →  分隔字母"), 26, buff=0.42, baseline_y=-1.45)
        for item, color in zip(answer, (ACCENT, GOLD, CIPHER)):
            item.set_color(color)
        self.say("Bravo、Charlie、Delta 的开头，给出了点、横线和字母间隔")
        self.play(FadeIn(hint), GrowArrow(arrow), FadeIn(answer, shift=UP * 0.15))
        self.wait(1.8)
        self.say("这已经不是普通的二进制了：它在提示 Morse 电码", wait=1.5)
        self.hush()
        self.play(FadeOut(VGroup(cards, hint, arrow, answer)))


class ZeroWidthMorse(Narrated):
    """第一句慢讲：零宽字符逐个翻成 Morse，再查表。"""

    def construct(self):
        hidden = hidden_cells(HIDDEN_1).move_to([0, 2.5, 0])
        symbols = symbol_cells(HIDDEN_1).move_to(hidden)
        self.say("把第一段隐藏字符逐个替换成点、横线或字母间隔")
        self.play(FadeIn(hidden))
        self.play(*[ReplacementTransform(hidden[i], symbols[i]) for i in range(len(hidden))], run_time=2.4)

        code = morse_groups(MORSE_1, 24).move_to([0, 1.15, 0])
        code_tag = ui("按空格分组，每组就是一个 Morse 字母", 22).set_color(MUTED).next_to(code, UP, buff=0.25)
        self.say("连续的点和横线，按空格分成一个个 Morse 字母")
        self.play(FadeIn(code_tag), LaggedStart(*[FadeIn(group) for group in code], lag_ratio=0.12), run_time=2.0)

        letters = VGroup(*[
            mono(ch, 34).set_color(OK) for ch in decode_morse(MORSE_1)
        ]).arrange(RIGHT, buff=0.15).move_to([0, -0.15, 0])
        self.say("再查 Morse 表，明文逐字出现")
        for letter in letters:
            self.play(FadeIn(letter, shift=UP * 0.12), run_time=0.18)
        result = chip("DISORIENTATION · 迷失方向", OK, 24).move_to([0, -1.15, 0])
        self.play(FadeIn(result, shift=UP * 0.15))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(hidden, symbols, code, code_tag, letters, result)))


class ZeroWidthSecond(Narrated):
    """第二句快速复用同一规则，得到 AROUSAL。"""

    def construct(self):
        lines = sentence_lines(VISIBLE_2, 24).move_to([0, 2.05, 0])
        self.say("第二个页面也藏着零宽字符，它的标题还指向 Nihilist")
        self.play(FadeIn(lines))

        cells = hidden_cells(HIDDEN_2, per_row=26).move_to([0, 0.75, 0])
        self.play(LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.04), run_time=1.0)
        morse = mono(MORSE_2, 30).set_color(ACCENT).move_to([0, -0.15, 0])
        self.say("快速映射成 Morse")
        self.play(FadeIn(morse), run_time=0.8)

        output = VGroup(*[
            mono(ch, 43).set_color(OK) for ch in decode_morse(MORSE_2)
        ]).arrange(RIGHT, buff=0.2).move_to([0, -1.15, 0])
        self.say("得到 AROUSAL：唤醒", wait=1.2)
        self.play(LaggedStart(*[FadeIn(ch, shift=UP * 0.15) for ch in output], lag_ratio=0.16), run_time=1.2)
        self.wait(1.8)
        self.hush()
        self.play(FadeOut(VGroup(lines, cells, morse, output)))
