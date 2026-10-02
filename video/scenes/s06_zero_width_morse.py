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


def title_block(title: str, subtitle: str | None = None) -> VGroup:
    items = [ui(title, 36).set_color(FG)]
    if subtitle:
        items.append(ui(subtitle, 20).set_color(MUTED))
    return VGroup(*items).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.32)


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


def mapping_card(ch: str, symbol: str, name: str, color) -> VGroup:
    square = Square(side_length=0.52, stroke_color=color, stroke_width=1.8)
    square.set_fill(color, opacity=0.18)
    code = mono(f"U+{ord(ch):04X}", 19).set_color(color)
    mapping = mono(symbol if symbol != " " else "space", 25).set_color(OK)
    note = ui(name, 18).set_color(MUTED)
    return VGroup(square, code, mapping, note).arrange(DOWN, buff=0.12)


# --- 场景 ---------------------------------------------------------------------


class ZeroWidthReveal(Narrated):
    """先证明文本看起来正常，但复制内容里有隐藏字符。"""

    def construct(self):
        title = title_block("零宽字符 · 文字里藏着看不见的字符", "肉眼看到的文本，不一定等于复制出来的文本")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        lines = sentence_lines(VISIBLE_1, 23).move_to([0, 1.55, 0])
        tag = chip("看起来只是普通句子", MUTED, 22).move_to([0, 0.45, 0])
        self.say("页面上看起来只是一句普通英文")
        self.play(FadeIn(lines), FadeIn(tag))
        self.wait(1.2)

        gap = DashedLine([-0.5, 1.25, 0], [0.5, 1.25, 0], color=DANGER, dash_length=0.08)
        gap_tag = ui("复制时，两个词之间其实多了东西", 23).set_color(DANGER).next_to(gap, DOWN, buff=0.18)
        self.say("但复制文本、查看 Unicode 码点，就能发现一段完全不占宽度的内容")
        self.play(FadeOut(tag), Create(gap), FadeIn(gap_tag))

        cells = hidden_cells(HIDDEN_1).move_to([0, -0.75, 0])
        cell_tag = ui(f"隐藏字符：{len(HIDDEN_1)} 个", 22).set_color(ACCENT).next_to(cells, UP, buff=0.3)
        self.play(FadeIn(cell_tag), LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.035), run_time=1.8)
        self.wait(1.2)

        note = ui("它们没有可见字形，但仍然会被复制、存储和传输", 24).set_color(FG).move_to([0, -1.75, 0])
        self.play(FadeIn(note))
        self.say("零宽，不等于不存在", wait=1.8)
        self.hush()
        self.play(FadeOut(VGroup(title, lines, tag, gap, gap_tag, cells, cell_tag, note)))


class ZeroWidthAlphabet(Narrated):
    """解释三种码点，以及标题给出的映射。"""

    def construct(self):
        title = title_block("零宽字符 · 先认出三种码点", "标题：.Bravo  _Charlie  ␣Delta")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        cards = VGroup(*[
            mapping_card(ch, TO_MORSE[ch], ZERO_NAMES[ch].split("  ", 1)[1], ZERO_COLORS[ch])
            for ch in ("\u200b", "\u200c", "\u200d")
        ]).arrange(RIGHT, buff=0.8).move_to([0, 0.75, 0])
        self.say("一共只有三种字符，先把它们的 Unicode 码点认出来")
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in cards], lag_ratio=0.2), run_time=1.6)

        hint = VGroup(
            mono(".Bravo", 28).set_color(ACCENT),
            mono("_Charlie", 28).set_color(GOLD),
            mono("␣Delta", 28).set_color(CIPHER),
        ).arrange(RIGHT, buff=0.75).move_to([0, -0.7, 0])
        arrow = Arrow(hint.get_bottom(), [0, -1.45, 0], color=MUTED, stroke_width=2)
        answer = VGroup(
            mono(".  →  点", 26).set_color(ACCENT),
            mono("_  →  横线", 26).set_color(GOLD),
            mono("␣  →  分隔字母", 26).set_color(CIPHER),
        ).arrange(RIGHT, buff=0.42).move_to([0, -1.95, 0])
        self.say("Bravo、Charlie、Delta 的开头，给出了点、横线和字母间隔")
        self.play(FadeIn(hint), GrowArrow(arrow), FadeIn(answer, shift=UP * 0.15))
        self.wait(1.8)
        self.say("这已经不是普通的二进制了：它在提示 Morse 电码", wait=1.5)
        self.hush()
        self.play(FadeOut(VGroup(title, cards, hint, arrow, answer)))


class ZeroWidthMorse(Narrated):
    """第一句慢讲：零宽字符逐个翻成 Morse，再查表。"""

    def construct(self):
        title = title_block("零宽字符 · 翻译成 Morse", "第一句：DISORIENTATION")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        hidden = hidden_cells(HIDDEN_1).move_to([0, 2.0, 0])
        symbols = symbol_cells(HIDDEN_1).move_to(hidden)
        self.say("把第一段隐藏字符逐个替换成点、横线或字母间隔")
        self.play(FadeIn(hidden))
        self.play(*[ReplacementTransform(hidden[i], symbols[i]) for i in range(len(hidden))], run_time=2.4)

        code = morse_groups(MORSE_1, 24).move_to([0, 0.65, 0])
        code_tag = ui("按空格分组，每组就是一个 Morse 字母", 22).set_color(MUTED).next_to(code, UP, buff=0.25)
        self.say("连续的点和横线，按空格分成一个个 Morse 字母")
        self.play(FadeIn(code_tag), LaggedStart(*[FadeIn(group) for group in code], lag_ratio=0.12), run_time=2.0)

        letters = VGroup(*[
            mono(ch, 34).set_color(OK) for ch in decode_morse(MORSE_1)
        ]).arrange(RIGHT, buff=0.15).move_to([0, -0.65, 0])
        self.say("再查 Morse 表，明文逐字出现")
        for letter in letters:
            self.play(FadeIn(letter, shift=UP * 0.12), run_time=0.18)
        result = chip("DISORIENTATION · 迷失方向", OK, 24).move_to([0, -1.65, 0])
        self.play(FadeIn(result, shift=UP * 0.15))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, hidden, symbols, code, code_tag, letters, result)))


class ZeroWidthSecond(Narrated):
    """第二句快速复用同一规则，得到 AROUSAL。"""

    def construct(self):
        title = title_block("零宽字符 · 同样的规则再来一次", "第二句：页面标题指向 Nihilist")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        lines = sentence_lines(VISIBLE_2, 24).move_to([0, 1.55, 0])
        self.say("第二个页面也有一段零宽字符")
        self.play(FadeIn(lines))

        cells = hidden_cells(HIDDEN_2, per_row=26).move_to([0, 0.25, 0])
        self.play(LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.04), run_time=1.0)
        morse = mono(MORSE_2, 30).set_color(ACCENT).move_to([0, -0.65, 0])
        self.say("快速映射成 Morse")
        self.play(FadeIn(morse), run_time=0.8)

        output = VGroup(*[
            mono(ch, 43).set_color(OK) for ch in decode_morse(MORSE_2)
        ]).arrange(RIGHT, buff=0.2).move_to([0, -1.65, 0])
        self.say("得到 AROUSAL：唤醒", wait=1.2)
        self.play(LaggedStart(*[FadeIn(ch, shift=UP * 0.15) for ch in output], lag_ratio=0.16), run_time=1.2)
        self.wait(1.8)
        self.hush()
        self.play(FadeOut(VGroup(title, lines, cells, morse, output)))
