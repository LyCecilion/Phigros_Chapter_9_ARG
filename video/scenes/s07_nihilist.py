"""s07 · Nihilist：把字母查表，再叠加会变化的数字密钥。

每个 Scene 都从 README / artifacts/stage_ii/DISORIENTATION/nihilist.py
中的真实数据计算结果；动画只负责把查表、加减和越界显示出来。
"""

from manim import *
from style import *

# --- 数据 ---------------------------------------------------------------------

RIGHT_SOURCE = "PSZLMYQEBJARTFCHNUGVKDOXIW"
SQUARE_TEXT = RIGHT_SOURCE[:-2] + RIGHT_SOURCE[-1]  # 按惯例删去倒数第二个 I
CIPHERTEXT = [56, 75, 65, 76, 35, 56, 75, 63, 97, 66, 67, 47, 72]
WRONG_KEY = "AROUSAL"
RIGHT_KEY = "AROUSL"
WRONG_EXPECTED = "JUSTEJ✗R✗ZBCH"
RIGHT_EXPECTED = "JUSTENGAGEWTH"

assert RIGHT_SOURCE[-2] == "I"
assert len(SQUARE_TEXT) == 25

POS = {ch: (i // 5 + 1, i % 5 + 1) for i, ch in enumerate(SQUARE_TEXT)}
REV = {value: key for key, value in POS.items()}


def number(ch: str) -> int:
    row, col = POS[ch]
    return 10 * row + col


def decrypt(key: str) -> list[str | None]:
    key_numbers = [number(ch) for ch in key]
    result = []
    for i, value in enumerate(CIPHERTEXT):
        coordinate = value - key_numbers[i % len(key_numbers)]
        result.append(REV.get(divmod(coordinate, 10)))
    return result


def display_result(result: list[str | None]) -> str:
    return "".join(ch if ch is not None else "✗" for ch in result)


WRONG_NUMBERS = [number(ch) for ch in WRONG_KEY]
RIGHT_NUMBERS = [number(ch) for ch in RIGHT_KEY]
WRONG_DIFFS = [
    value - WRONG_NUMBERS[i % len(WRONG_NUMBERS)]
    for i, value in enumerate(CIPHERTEXT)
]
RIGHT_DIFFS = [
    value - RIGHT_NUMBERS[i % len(RIGHT_NUMBERS)]
    for i, value in enumerate(CIPHERTEXT)
]
WRONG_RESULT = decrypt(WRONG_KEY)
RIGHT_RESULT = decrypt(RIGHT_KEY)

assert WRONG_DIFFS == [25, 43, 12, 33, 23, 25, 61, 32, 65, 13, 24, 35, 41]
assert RIGHT_DIFFS == [25, 43, 12, 33, 23, 42, 44, 31, 44, 23, 55, 33, 41]
assert display_result(WRONG_RESULT) == WRONG_EXPECTED
assert display_result(RIGHT_RESULT) == RIGHT_EXPECTED
assert [number(ch) for ch in "AROUSL"] == [31, 32, 53, 43, 12, 14]

# --- 构件 ---------------------------------------------------------------------

GRID_CELL = 0.66


def make_square(cell: float = GRID_CELL) -> tuple[VGroup, dict[str, VGroup]]:
    """返回带行列坐标的 5×5 方阵，以及按字母索引的单元格。"""
    cells = VGroup()
    by_letter: dict[str, VGroup] = {}
    for i, ch in enumerate(SQUARE_TEXT):
        row, col = divmod(i, 5)
        rect = Square(side_length=cell, stroke_color=MUTED, stroke_width=1.5)
        rect.set_fill(BG, opacity=0.72)
        label = mono(ch, 25).set_color(FG)
        item = VGroup(rect, label).move_to(
            np.array([(col - 2) * cell, (2 - row) * cell, 0])
        )
        cells.add(item)
        by_letter[ch] = item

    grid = VGroup(cells)
    col_labels = VGroup(
        *[mono(str(i), 18).set_color(MUTED).move_to(np.array([(i - 3) * cell, 3 * cell, 0])) for i in range(1, 6)]
    )
    row_labels = VGroup(
        *[mono(str(i), 18).set_color(MUTED).move_to(np.array([-3 * cell, (3 - i) * cell, 0])) for i in range(1, 6)]
    )
    return VGroup(grid, col_labels, row_labels), by_letter


def grid_caption(grid: Mobject, text: str) -> Text:
    return ui(text, 22).set_color(MUTED).next_to(grid, DOWN, buff=0.28)


def number_strip(values: list[int], y: float, color, x0: float = -0.35, step: float = 0.50):
    """右侧的数字序列；每一项独立可高亮。"""
    return VGroup(
        *[
            mono(str(value), 22).set_color(color).move_to([x0 + i * step, y, 0])
            for i, value in enumerate(values)
        ]
    )


def strip_label(text: str, y: float, color, x: float = -1.65) -> Text:
    return ui(text, 21).set_color(color).move_to([x, y, 0])


def key_strip(key: str, y: float, color=CIPHER, x0: float = -0.35, step: float = 0.50):
    return VGroup(
        *[
            mono(ch, 22).set_color(color).move_to([x0 + i * step, y, 0])
            for i, ch in enumerate(key)
        ]
    )


def result_strip(result: list[str | None], y: float, x0: float = -0.35, step: float = 0.50):
    return VGroup(
        *[
            mono(ch if ch is not None else "✗", 23).set_color(
                DANGER if ch is None else OK
            ).move_to([x0 + i * step, y, 0])
            for i, ch in enumerate(result)
        ]
    )


class NihilistSquare(Narrated):
    """从 Chaocipher 右盘得到 5×5 Polybius 方阵。"""

    def construct(self):
        source = mono(RIGHT_SOURCE, 29).set_color(FG).move_to(UP * 2.50)
        source_tag = ui("Chaocipher 右盘", 20).set_color(MUTED).next_to(source, UP, buff=0.18)
        self.say("提示把我们带回了 Chaocipher 的右盘")
        self.play(FadeIn(source_tag), FadeIn(source))
        self.wait(0.8)

        removed = glyphs(source, RIGHT_SOURCE, "I")
        self.say("但 Polybius 方阵只有 25 个格子：删掉倒数第二个 I")
        self.play(Indicate(removed, color=DANGER, scale_factor=1.25), run_time=0.8)
        cross = Cross(removed, stroke_color=DANGER, stroke_width=3)
        self.play(Create(cross), run_time=0.5)
        self.wait(0.6)

        square, cells = make_square()
        square.move_to([-3.9, 0.10, 0])
        caption = grid_caption(square, "I / J 合并：这里没有 I")
        self.play(FadeIn(square), FadeIn(caption), run_time=1.0)
        self.say("剩下 25 个字母，按行放进方阵")
        self.play(
            LaggedStart(
                *[Indicate(cells[ch], color=ACCENT, scale_factor=1.08) for ch in SQUARE_TEXT],
                lag_ratio=0.035,
            ),
            run_time=2.4,
        )

        right = VGroup(
            ui("行号", 22).set_color(MUTED),
            mono("1  2  3  4  5", 27).set_color(GOLD),
            ui("列号", 22).set_color(MUTED),
            mono("1  2  3  4  5", 27).set_color(GOLD),
            mono("A = 31", 32).set_color(OK),
            mono("R = 32", 32).set_color(OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.0, 0.25, 0])
        self.say("每个字母的位置，就是两位数：行号再接列号")
        self.play(FadeIn(right, shift=LEFT * 0.2))
        self.play(Indicate(cells["A"], color=GOLD), Indicate(cells["R"], color=GOLD), run_time=1.0)
        self.wait(1.8)
        self.hush()
        self.play(FadeOut(VGroup(source, source_tag, cross, square, caption, right)))


class NihilistArithmetic(Narrated):
    """展示 Nihilist 的加法，以及解密时的减法。"""

    def construct(self):
        left = VGroup(
            mono("明文", 25).set_color(OK),
            mono("24", 48).set_color(OK),
        ).arrange(DOWN, buff=0.25).move_to([-4.5, 1.2, 0])
        plus = mono("+", 40).set_color(MUTED).move_to([-2.7, 1.2, 0])
        middle = VGroup(
            mono("密钥", 25).set_color(GOLD),
            mono("35", 48).set_color(GOLD),
        ).arrange(DOWN, buff=0.25).move_to([-1.5, 1.2, 0])
        equals = mono("=", 40).set_color(MUTED).move_to([0.0, 1.2, 0])
        result = VGroup(
            mono("密文数字", 25).set_color(CIPHER),
            mono("59", 52).set_color(CIPHER),
        ).arrange(DOWN, buff=0.25).move_to([1.55, 1.2, 0])
        line = Line([-5.3, 0.25, 0], [3.2, 0.25, 0], color=MUTED, stroke_width=1.5)
        note = ui("每个位置都用一枚循环密钥", 25).set_color(MUTED).move_to([0, -0.25, 0])

        self.say("先把明文和密钥都查成两位坐标")
        self.play(FadeIn(left), FadeIn(plus), FadeIn(middle))
        self.wait(0.7)
        self.say("再相加，得到可能超过 55 的密文数字")
        self.play(FadeIn(equals), FadeIn(result), Circumscribe(result[1], color=CIPHER))
        self.play(Create(line), FadeIn(note))
        self.wait(1.5)

        decrypt = VGroup(
            mono("59", 42).set_color(CIPHER),
            mono("−", 38).set_color(MUTED),
            mono("35", 42).set_color(GOLD),
            mono("=", 38).set_color(MUTED),
            mono("24", 42).set_color(OK),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.15)
        self.say("解密就反过来：减掉同一枚密钥，再回方阵查字母")
        self.play(FadeIn(decrypt, shift=UP * 0.15))
        self.wait(1.6)
        self.hush()
        self.play(FadeOut(VGroup(left, plus, middle, equals, result, line, note, decrypt)))


class NihilistWrongKey(Narrated):
    """用 AROUSAL 解密，显出两个越界坐标。"""

    def construct(self):
        square, cells = make_square(0.58)
        square.move_to([-4.25, 0.40, 0])
        caption = grid_caption(square, "有效坐标：11、12、…、55")
        self.play(FadeIn(square), FadeIn(caption))

        ys = [2.65, 1.95, 1.25, 0.55]
        ct = number_strip(CIPHERTEXT, ys[0], CIPHER)
        key = key_strip(WRONG_KEY, ys[1], GOLD)
        diffs = number_strip(WRONG_DIFFS, ys[2], FG)
        output = result_strip(WRONG_RESULT, ys[3])
        labels = VGroup(
            strip_label("密文", ys[0], CIPHER),
            strip_label("密钥", ys[1], GOLD),
            strip_label("相减", ys[2], MUTED),
            strip_label("查表", ys[3], OK),
        )
        self.say("把密文逐项减去循环密钥 AROUSAL")
        self.play(FadeIn(labels), FadeIn(ct), FadeIn(key))
        self.wait(0.8)

        for i in range(len(CIPHERTEXT)):
            key_i = i % len(WRONG_KEY)
            self.play(
                Indicate(ct[i], color=CIPHER, scale_factor=1.12),
                Indicate(key[key_i], color=GOLD, scale_factor=1.15),
                FadeIn(diffs[i], shift=DOWN * 0.12),
                FadeIn(output[i], shift=UP * 0.12),
                run_time=0.42,
            )
            if WRONG_RESULT[i] is None:
                self.play(Circumscribe(diffs[i], color=DANGER, time_width=0.7), run_time=0.45)

        error = chip("61、65 不在方阵坐标里", DANGER, 23).move_to([2.7, -0.62, 0])
        self.say("结果出现 61 和 65：它们根本不是合法的行列坐标")
        self.play(FadeIn(error, shift=UP * 0.15))
        self.wait(1.4)
        self.say("提示说：得到的元素不能直接使用，要移除干扰")
        bad_a = key[5]
        self.play(Indicate(bad_a, color=DANGER, scale_factor=1.4), run_time=0.8)
        cross = Cross(bad_a, stroke_color=DANGER, stroke_width=3)
        self.play(Create(cross))
        self.wait(1.2)
        self.hush()
        self.play(FadeOut(VGroup(square, caption, labels, ct, key, diffs, output, error, cross)))


class NihilistCorrectKey(Narrated):
    """删除第二个 A 后，所有坐标都能查回方阵。"""

    def construct(self):
        square, cells = make_square(0.58)
        square.move_to([-4.25, 0.40, 0])
        caption = grid_caption(square, "每个差值都能查回一个字母")
        self.play(FadeIn(square), FadeIn(caption))

        ys = [2.65, 1.95, 1.25, 0.55]
        ct = number_strip(CIPHERTEXT, ys[0], CIPHER)
        key = key_strip(RIGHT_KEY, ys[1], GOLD)
        diffs = number_strip(RIGHT_DIFFS, ys[2], FG)
        output = result_strip(RIGHT_RESULT, ys[3])
        labels = VGroup(
            strip_label("密文", ys[0], CIPHER),
            strip_label("密钥", ys[1], GOLD),
            strip_label("相减", ys[2], MUTED),
            strip_label("查表", ys[3], OK),
        )
        self.say("去掉第二个 A，密钥变成 AROUSL")
        self.play(FadeIn(labels), FadeIn(ct), FadeIn(key), FadeIn(diffs), FadeIn(output))
        self.wait(0.7)

        for i in range(len(CIPHERTEXT)):
            key_i = i % len(RIGHT_KEY)
            self.play(
                Indicate(ct[i], color=CIPHER, scale_factor=1.1),
                Indicate(key[key_i], color=GOLD, scale_factor=1.12),
                Indicate(diffs[i], color=FG, scale_factor=1.1),
                Indicate(output[i], color=OK, scale_factor=1.12),
                Indicate(cells[RIGHT_RESULT[i]], color=OK, scale_factor=1.05),
                run_time=0.34,
            )

        answer = mono(RIGHT_EXPECTED, 36).set_color(OK).move_to([1.7, -0.70, 0])
        self.say("这次每一个差值都能回到方阵，读出 JUSTENGAGEWTH")
        self.play(TransformFromCopy(output, answer), run_time=1.5)
        self.wait(1.2)

        phrase = VGroup(
            mono("JUST ENGAGE W", 27).set_color(FG),
            mono("I", 27).set_color(DANGER),
            mono("TH", 27).set_color(FG),
        ).arrange(RIGHT, buff=0.03).move_to([1.55, -1.55, 0])
        note = ui("I 被方阵规则省略，所以 WITH 读成 WTH", 21).set_color(MUTED).next_to(phrase, DOWN, buff=0.16)
        self.say("最后的 I 也解释了：它正是被 5 × 5 方阵省略的字母", wait=1.8)
        self.play(FadeIn(phrase), FadeIn(note))
        self.wait(2.0)
        self.hush()
        self.play(FadeOut(VGroup(square, caption, labels, ct, key, diffs, output, answer, phrase, note)))
