"""s02 · Atbash 与 Caesar：固定映射密码的两个例子。"""

import string

from manim import *
from style import *

ALPHABET = string.ascii_uppercase
ATBASH_PLAIN = "ONLY CHAOS CAN SHATTER THE MIRAGE THAT PLAGUES THE IGNORANT FOOL."
CAESAR_ITEMS = [
    (
        7,
        "FVB TBZA NV IF H DHF DOPJO PZ AOL DHF VM PNUVYHUJL",
        "YOU MUST GO BY A WAY WHICH IS THE WAY OF IGNORANCE",
    ),
    (
        3,
        "BRX PXVW JR WKURXJK WKH ZDB LQ ZKLFK BRX DUH QRW",
        "YOU MUST GO THROUGH THE WAY IN WHICH YOU ARE NOT",
    ),
]


def atbash(text: str) -> str:
    return "".join(
        ALPHABET[25 - ALPHABET.index(ch)] if ch in ALPHABET else ch
        for ch in text.upper()
    )


def caesar(text: str, shift: int) -> str:
    return "".join(
        ALPHABET[(ALPHABET.index(ch) + shift) % 26] if ch in ALPHABET else ch
        for ch in text.upper()
    )


ATBASH_CIPHER = atbash(ATBASH_PLAIN)
assert atbash(ATBASH_CIPHER) == ATBASH_PLAIN
assert caesar(CAESAR_ITEMS[0][1], -CAESAR_ITEMS[0][0]) == CAESAR_ITEMS[0][2]
assert caesar(CAESAR_ITEMS[1][1], -CAESAR_ITEMS[1][0]) == CAESAR_ITEMS[1][2]


def band(text: str, color, y: float, size: float = 29) -> VGroup:
    cells = VGroup()
    for i, ch in enumerate(text):
        rect = Rectangle(width=0.42, height=0.62, stroke_color=color, stroke_width=1.2)
        rect.set_fill(color, opacity=0.10)
        cells.add(VGroup(rect, mono(ch, size).set_color(color).move_to(rect)))
    cells.arrange(RIGHT, buff=0.02).move_to([0, y, 0])
    return cells


def title_block(title: str, subtitle: str | None = None) -> VGroup:
    items = [ui(title, 36).set_color(FG)]
    if subtitle:
        items.append(ui(subtitle, 20).set_color(MUTED))
    return VGroup(*items).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.32)


def word_letters(text: str, color, size: float = 38) -> VGroup:
    return VGroup(*[mono(ch, size).set_color(color) for ch in text]).arrange(RIGHT, buff=0.16)


class AtbashAlphabet(Narrated):
    """字母表翻折：A↔Z，且操作两次会回到原文。"""

    def construct(self):
        title = title_block("Atbash · 把字母表原地翻折", "A ↔ Z，B ↔ Y，C ↔ X ……")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        top = band(ALPHABET, ACCENT, 1.35, 25)
        bottom = band(ALPHABET[::-1], GOLD, -0.05, 25)
        self.say("Atbash 不需要密钥：把正向字母表和反向字母表对齐")
        self.play(FadeIn(top), FadeIn(bottom))

        lines = VGroup()
        for i in range(26):
            line = Line(top[i].get_bottom(), bottom[i].get_top(), color=MUTED, stroke_width=1, stroke_opacity=0.45)
            lines.add(line)
        self.play(LaggedStart(*[Create(line) for line in lines], lag_ratio=0.025), run_time=2.0)

        for i in (0, 1, 2, 12, 25):
            self.play(Indicate(top[i], color=ACCENT), Indicate(bottom[i], color=GOLD), run_time=0.35)
        note = chip("固定映射 · 自己就是自己的逆", OK, 24).move_to([0, -1.35, 0])
        self.say("同一个位置永远对应同一个字母；再做一次 Atbash 就能还原", wait=1.8)
        self.play(FadeIn(note, shift=UP * 0.15))
        self.hush()
        self.play(FadeOut(VGroup(title, top, bottom, lines, note)))


class AtbashSentence(Narrated):
    """从一个词推广到 README 中的完整 Atbash 句子。"""

    def construct(self):
        title = title_block("Atbash · 从一个词到整句话", "固定映射的查表过程")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        cipher_word = atbash("ONLY")
        plain_word = "ONLY"
        cipher = word_letters(cipher_word, CIPHER, 42).move_to([-2.1, 1.25, 0])
        arrow = Arrow(cipher.get_right() + RIGHT * 0.25, [0.3, 1.25, 0], color=MUTED, stroke_width=2)
        plain = word_letters(plain_word, OK, 42).move_to([1.35, 1.25, 0])
        self.say("例如密文 L M O B，逐字翻折就得到 ONLY")
        self.play(FadeIn(cipher), GrowArrow(arrow))
        self.play(FadeIn(plain, shift=RIGHT * 0.15))
        self.wait(1.0)

        full_cipher = mono(ATBASH_CIPHER, 23).set_color(CIPHER).move_to([0, 0.15, 0])
        full_plain = mono(ATBASH_PLAIN, 23).set_color(OK).move_to([0, -0.65, 0])
        self.say("对整句做同样的操作，直接得到明文")
        self.play(FadeIn(full_cipher))
        self.play(TransformFromCopy(full_cipher, full_plain), run_time=1.8)
        self.wait(1.2)
        self.say("唯有混沌，才能击碎困扰无知愚者的幻象", wait=1.5)
        self.hush()
        self.play(FadeOut(VGroup(title, cipher, arrow, plain, full_cipher, full_plain)))


class CaesarShift(Narrated):
    """用字母带滑动演示 Caesar，并展示 README 的两段真实密文。"""

    def construct(self):
        title = title_block("Caesar · 整条字母带平移", "CH-7 的 7，就是向前移动 7 格")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        upper = band(ALPHABET, MUTED, 1.7, 25)
        lower = band(caesar(ALPHABET, CAESAR_ITEMS[0][0]), ACCENT, 0.7, 25)
        upper_tag = ui("原字母表", 21).set_color(MUTED).move_to([-6.15, 1.7, 0])
        lower_tag = ui("平移 7 格", 21).set_color(ACCENT).move_to([-6.15, 0.7, 0])
        self.say("Caesar 则更直接：整条字母带统一平移")
        self.play(FadeIn(upper), FadeIn(lower), FadeIn(upper_tag), FadeIn(lower_tag))

        for i in range(7):
            self.play(upper[i].animate.set_color(GOLD), lower[i].animate.set_color(GOLD), run_time=0.18)
        marker = chip("CH-7", GOLD, 25).move_to([0, -0.15, 0])
        self.play(FadeIn(marker))
        self.say("解密时反向移动 7 格")
        self.wait(1.2)

        rows = VGroup()
        for shift, cipher, plain in CAESAR_ITEMS:
            c = mono(f"CH-{shift}:  {cipher}", 20).set_color(CIPHER)
            p = mono(plain, 20).set_color(OK)
            rows.add(VGroup(c, p).arrange(DOWN, buff=0.16, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([0, -1.3, 0])
        self.say("README 中的两段密文也分别用 CH-7 和 CH-3 反向解出")
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.12) for row in rows], lag_ratio=0.25), run_time=1.8)
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, upper, lower, upper_tag, lower_tag, marker, rows)))


class FixedMappingSummary(Narrated):
    """把 Atbash、Caesar 和 Chaocipher 放在同一张对照图上。"""

    def construct(self):
        title = title_block("固定映射 · 和 Chaocipher 有什么不同？", "每次查表是否使用同一张表")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        fixed = VGroup(
            chip("Atbash", ACCENT, 24),
            mono("A → Z   A → Z   A → Z", 27).set_color(ACCENT),
            ui("同一字母永远得到同一结果", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.22).move_to([-3.35, 0.55, 0])
        caesar = VGroup(
            chip("Caesar", GOLD, 24),
            mono("A → D   A → D   A → D", 27).set_color(GOLD),
            ui("偏移量固定不变", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.22).move_to([0, 0.55, 0])
        chaos = VGroup(
            chip("Chaocipher", CIPHER, 24),
            mono("G → E   G → J   G → T", 27).set_color(CIPHER),
            ui("每一步都要换一张表", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.22).move_to([3.35, 0.55, 0])
        self.say("Atbash 和 Caesar 都是固定映射")
        self.play(FadeIn(fixed), FadeIn(caesar))
        self.say("Chaocipher 不一样：字母表会随着过程改变")
        self.play(FadeIn(chaos), Circumscribe(chaos[1], color=CIPHER))
        conclusion = chip("固定映射：简单、可逆、但没有“混沌状态”", OK, 24).move_to([0, -1.65, 0])
        self.play(FadeIn(conclusion, shift=UP * 0.15))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, fixed, caesar, chaos, conclusion)))
