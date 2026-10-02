"""s03 · PNG 两图拼接：为什么一个 start.png 能装下两张图。

用法：
    ./render.sh -ql scenes/s03_png_polyglot.py PngSignature  # 8 字节签名 + 脚本里的 137/80/78/71
    ./render.sh -ql scenes/s03_png_polyglot.py PngChunk      # 块的四个字段，拿真实的 IHDR 拆
    ./render.sh -ql scenes/s03_png_polyglot.py PngWalk       # b += 12 + c，一路跳到 IEND
    ./render.sh -ql scenes/s03_png_polyglot.py PngPolyglot   # IEND 之后的第二张 PNG + binwalk + 拆图

所有偏移、长度都在加载时从仓库里的 start.png 现算，并与 README 中的数字断言一致。
"""

import struct
from pathlib import Path

from manim import *
from style import *

# --- 数据 ---------------------------------------------------------------------

DATA = Path(__file__).resolve().parents[2] / "artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN"
RAW = (DATA / "start.png").read_bytes()
SIGNATURE = bytes.fromhex("89504E470D0A1A0A")


def walk(off: int):
    """按 PNG 块结构从 off 处走到 IEND，返回 ([(偏移, 长度, 类型)], IEND 之后的偏移)。"""
    assert RAW[off : off + 8] == SIGNATURE
    b, out = off + 8, []
    while b + 8 <= len(RAW):
        c = struct.unpack(">I", RAW[b : b + 4])[0]
        d = RAW[b + 4 : b + 8].decode("latin1")
        out.append((b, c, d))
        b += 12 + c
        if d == "IEND":
            return out, b
    raise ValueError("no IEND")


CHUNKS_A, END_A = walk(0)
CHUNKS_B, END_B = walk(END_A)
SIZE = len(RAW)
IDAT_A = [ch for ch in CHUNKS_A if ch[2] == "IDAT"]

assert SIZE == 3_722_963
assert END_A == 3_139_459 == 0x2FE783
assert SIZE - END_A == 583_504 and END_B == SIZE
assert [ch[2] for ch in CHUNKS_B] == ["IHDR", "tEXt", "PLTE", "IDAT", "IEND"]
assert struct.unpack(">II", RAW[16:24]) == (1920, 1080)

# --- 构件 ---------------------------------------------------------------------

LEN_C, TYPE_C, DATA_C, CRC_C = ACCENT, GOLD, CIPHER, OK


def hex_cell(byte: int, color=FG, w: float = 0.62, size: float = 26) -> VGroup:
    rect = RoundedRectangle(width=w, height=0.62, corner_radius=0.06, stroke_color=color, stroke_width=1.5)
    rect.set_fill(color, opacity=0.08)
    return VGroup(rect, mono(f"{byte:02X}", size).set_color(color).move_to(rect))


def block(label: str, width: float, color, size: float = 22, height: float = 0.66) -> VGroup:
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.07, stroke_color=color, stroke_width=1.8)
    rect.set_fill(color, opacity=0.14)
    return VGroup(rect, mono(label, size).set_color(color).move_to(rect))


def tint(group: VGroup, color, opacity: float = 0.14):
    """把 block / hex_cell 整体换色。"""
    rect, text = group
    rect.set_stroke(color).set_fill(color, opacity=opacity)
    text.set_color(color)
    return group


def labeled_brace(mob, text: str, color, direction=DOWN, size: float = 22) -> VGroup:
    brace = Brace(mob, direction, buff=0.1, color=color)
    return VGroup(brace, cn(text, size).set_color(color).next_to(brace, direction, buff=0.1))


# --- 场景 ---------------------------------------------------------------------


class PngSignature(Narrated):
    """文件开头的 8 字节签名，以及页面脚本里的那句校验。"""

    def construct(self):
        name = mono("start.png", 36).set_color(ACCENT)
        size = cn(f"{SIZE:,} 字节", 26).set_color(MUTED)
        head = VGroup(name, size).arrange(DOWN, buff=0.18).move_to(UP * 2.7)
        self.play(FadeIn(head, shift=DOWN * 0.15))

        stream = VGroup(*[hex_cell(x, MUTED, w=0.5, size=20) for x in RAW[:22]]).arrange(RIGHT, buff=0.08)
        stream.move_to(UP * 0.9)
        fade = mono("…", 30).set_color(MUTED).next_to(stream, RIGHT, buff=0.15)
        self.say("一张 PNG，打开来看就是一长串字节")
        self.play(LaggedStart(*[FadeIn(c) for c in stream], lag_ratio=0.04), FadeIn(fade))
        self.wait(1.0)

        sig = VGroup(*[hex_cell(x, FG) for x in SIGNATURE]).arrange(RIGHT, buff=0.14).move_to(UP * 0.9)
        self.say("开头 8 个字节永远相同，这是 PNG 的「签名」")
        self.play(
            *[ReplacementTransform(stream[k], sig[k]) for k in range(8)],
            *[FadeOut(c) for c in stream[8:]],
            FadeOut(fade),
            run_time=1.2,
        )
        meaning = ["0x89", "P", "N", "G", "CR", "LF", "1A", "LF"]
        labels = VGroup(*[mono(m, 22).set_color(MUTED).next_to(c, DOWN, buff=0.18) for m, c in zip(meaning, sig)])
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels], lag_ratio=0.1))
        self.wait(0.6)

        self.say("中间三个字节，正好是字母 P、N、G 的 ASCII 码")
        self.play(*[sig[k].animate.set_color(GOLD) for k in (1, 2, 3)], *[labels[k].animate.set_color(GOLD) for k in (1, 2, 3)])
        self.wait(1.2)

        src = "a[0] !== 137 || a[1] !== 80 || a[2] !== 78 || a[3] !== 71"
        code = mono(src, 26).set_color(FG).move_to(DOWN * 1.5)
        tag = cn("页面脚本 L10.js", 22).set_color(MUTED).next_to(code, UP, buff=0.25).align_to(code, LEFT)
        self.say("页面脚本加载背景图时，先检查的就是这前 4 个字节")
        self.play(FadeIn(tag), Write(code), run_time=1.6)
        self.wait(0.6)

        nums = [glyphs(code, src, str(RAW[k])) for k in range(4)]
        decs = VGroup(
            *[mono(f"{RAW[k]} = 0x{RAW[k]:02X}", 22).set_color(GOLD) for k in range(4)]
        ).arrange(RIGHT, buff=0.7).move_to(DOWN * 2.55)
        self.say("十进制的 137、80、78、71，就是十六进制的 89、50、4E、47")
        for k in range(4):
            self.play(
                nums[k].animate.set_color(GOLD),
                TransformFromCopy(nums[k], decs[k]),
                Indicate(sig[k], color=GOLD, scale_factor=1.15),
                run_time=0.8,
            )
        self.wait(1.5)
        self.hush()
        self.play(FadeOut(VGroup(head, sig, labels, code, tag, decs)))


class PngChunk(Narrated):
    """块的四个字段：拿 start.png 里真实的 IHDR 逐字节拆开。"""

    def construct(self):
        ihdr = RAW[8:33]
        colors = [LEN_C] * 4 + [TYPE_C] * 4 + [DATA_C] * 13 + [CRC_C] * 4
        cells = VGroup(*[hex_cell(x, FG, w=0.46, size=19) for x in ihdr]).arrange(RIGHT, buff=0.05)
        cells.move_to(UP * 1.4)
        title = cn("签名之后的第一个块", 26).set_color(MUTED).next_to(cells, UP, buff=0.5)
        self.say("签名之后，文件由一个个「块」（chunk）首尾相接组成")
        self.play(FadeIn(title), LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cells], lag_ratio=0.03))
        self.wait(0.6)

        self.say("每个块都分成四段：长度、类型、数据、CRC")
        self.play(*[c[0].animate.set_stroke(col).set_fill(col, 0.1) for c, col in zip(cells, colors)],
                  *[c[1].animate.set_color(col) for c, col in zip(cells, colors)])
        parts = [cells[0:4], cells[4:8], cells[8:21], cells[21:25]]
        names = ["长度", "类型", "数据", "CRC"]
        braces = VGroup(*[labeled_brace(p, n, col) for p, n, col in zip(parts, names, (LEN_C, TYPE_C, DATA_C, CRC_C))])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in braces], lag_ratio=0.3))
        self.wait(1.0)

        length = struct.unpack(">I", ihdr[0:4])[0]
        w, h = struct.unpack(">II", ihdr[8:16])
        notes = VGroup(
            mono(f"= {length}", 24).set_color(LEN_C),
            mono(f"= \"{ihdr[4:8].decode()}\"", 24).set_color(TYPE_C),
            cn(f"宽 {w} · 高 {h} · 位深 · 色彩类型…", 22).set_color(DATA_C),
            cn("校验值", 22).set_color(CRC_C),
        )
        for n, b in zip(notes, braces):
            n.next_to(b, DOWN, buff=0.15)
        self.say(f"长度写着 {length}：后面的数据正好 {length} 个字节")
        self.play(FadeIn(notes[0]), Indicate(parts[0], color=LEN_C))
        self.play(Circumscribe(parts[2], color=DATA_C, time_width=0.8))
        self.say("类型是 4 个字母：IHDR，图像头")
        self.play(FadeIn(notes[1]), Indicate(parts[1], color=TYPE_C))
        self.say("它的数据里写着这张图的宽和高：1920 × 1080")
        self.play(FadeIn(notes[2]))
        self.wait(0.6)
        self.say("最后 4 字节是 CRC，用来检查这一块有没有损坏")
        self.play(FadeIn(notes[3]))
        self.wait(1.0)

        self.play(FadeOut(VGroup(title, cells, braces, notes)))
        anatomy = VGroup(
            block("长度 4", 1.8, LEN_C),
            block("类型 4", 1.8, TYPE_C),
            block("数据 c 字节", 4.4, DATA_C),
            block("CRC 4", 1.8, CRC_C),
        ).arrange(RIGHT, buff=0.08).move_to(UP * 1.5)
        self.say("一般地说：「长度」c 只数数据本身，不含另外三段")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in anatomy], lag_ratio=0.2))
        fixed = VGroup(*[mono("4", 30).set_color(col).next_to(anatomy[k], DOWN, buff=0.3) for k, col in ((0, LEN_C), (1, TYPE_C), (3, CRC_C))])
        cval = mono("c", 30).set_color(DATA_C).next_to(anatomy[2], DOWN, buff=0.3)
        self.play(FadeIn(fixed), FadeIn(cval))
        self.wait(0.8)

        formula = VGroup(
            cn("一块总长 =", 30).set_color(FG),
            mono("4 + 4 + 4", 32).set_color(MUTED),
            mono("+ c", 32).set_color(DATA_C),
            mono("= 12 + c", 32).set_color(GOLD),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.6)
        self.say("所以从一块的开头，跳 12 + c 个字节，就到了下一块")
        self.play(FadeIn(formula[0]), TransformFromCopy(fixed, formula[1]), TransformFromCopy(cval, formula[2]))
        self.play(Write(formula[3]))
        self.play(Circumscribe(formula[3], color=GOLD))
        self.wait(1.2)

        crit = VGroup(*[chip(t, ACCENT, 24) for t in ("IHDR", "IDAT", "IEND")]).arrange(RIGHT, buff=0.3)
        anc = VGroup(*[chip(t, MUTED, 24) for t in ("tEXt", "pHYs", "gAMA")]).arrange(RIGHT, buff=0.3)
        crit_tag = cn("大写开头 · 关键块：必须认得", 22).set_color(ACCENT)
        anc_tag = cn("小写开头 · 辅助块：不认识就跳过", 22).set_color(MUTED)
        kinds = VGroup(
            VGroup(crit, crit_tag).arrange(DOWN, buff=0.25),
            VGroup(anc, anc_tag).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=1.2).move_to(DOWN * 2.3)
        self.say("块的类型首字母大写是关键块，小写是辅助块")
        self.play(FadeIn(kinds[0], shift=UP * 0.1))
        self.play(FadeIn(kinds[1], shift=UP * 0.1))
        self.wait(0.6)
        self.say("IDAT 装像素，而 IEND 表示「图片到此结束」")
        self.play(Indicate(crit[1], color=ACCENT), run_time=0.8)
        self.play(Indicate(crit[2], color=GOLD, scale_factor=1.3), crit[2].animate.set_color(GOLD))
        self.wait(1.5)
        self.hush()
        self.play(FadeOut(VGroup(anatomy, fixed, cval, formula, kinds)))


class PngWalk(Narrated):
    """页面脚本的循环：b += 12 + c，一块一块跳到 IEND。"""

    def construct(self):
        src = [
            (0, "let b = 8;"),
            (0, "while (…) {"),
            (1, "c = 长度;  d = 类型;"),
            (1, "b += 12 + c;"),
            (1, "if (d === \"IEND\") return b;"),
            (0, "}"),
        ]
        # Text 会吞掉行首空格，缩进改成手动右移
        code = VGroup(*[mono(s, 22).set_color(FG) for _, s in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for line, (indent, _) in zip(code, src):
            line.shift(RIGHT * 0.45 * indent)
        code.to_corner(UL, buff=0.55).shift(DOWN * 0.2)
        code_tag = cn("页面脚本 L10.js（简化）", 20).set_color(MUTED).next_to(code, UP, buff=0.18).align_to(code, LEFT)

        n_idat = len(IDAT_A)
        middle = n_idat - 4
        layout = [
            ("签名", 0.9, ACCENT),
            ("IHDR", 1.05, MUTED),
            ("IDAT", 1.05, CIPHER),
            ("IDAT", 1.05, CIPHER),
            ("IDAT", 1.05, CIPHER),
            (f"… {middle} 个 IDAT …", 2.9, CIPHER),
            ("IDAT", 1.05, CIPHER),
            ("IEND", 1.05, GOLD),
        ]
        strip = VGroup(*[block(t, w, col, 20) for t, w, col in layout]).arrange(RIGHT, buff=0.05)
        strip.move_to(DOWN * 0.3)
        tint(strip[5], CIPHER, 0.06)

        self.say("页面脚本要找到第二张图从哪开始，做法就是一块一块往后跳")
        self.play(FadeIn(code_tag), FadeIn(code), FadeIn(strip, shift=UP * 0.1))
        self.wait(0.6)

        b = ValueTracker(8)
        pointer = Triangle(color=GOLD, fill_opacity=1).scale(0.13).rotate(PI)
        pointer.next_to(strip[1].get_corner(UL), UP, buff=0.08)
        readout = always_redraw(
            lambda: mono(f"b = {int(round(b.get_value())):,}", 30).set_color(GOLD).next_to(pointer, UP, buff=0.15)
        )
        self.say("签名固定 8 字节，所以 b 从 8 开始")
        self.play(Indicate(code[0], color=GOLD), FadeIn(pointer), FadeIn(readout))
        self.wait(0.8)

        calc_pos = DOWN * 1.8

        def hop(target: Mobject, start: int, c: int) -> Mobject:
            nb = start + 12 + c
            calc = mono(f"{start:,} + 12 + {c:,} = {nb:,}", 30).set_color(FG).move_to(calc_pos)
            self.play(FadeIn(calc, shift=UP * 0.1), Indicate(code[3], color=GOLD), run_time=0.6)
            self.play(b.animate.set_value(nb), pointer.animate.next_to(target.get_corner(UL), UP, buff=0.08), run_time=1.2)
            return calc

        (o0, c0, _), (o1, c1, _), (o2, c2, _), (o3, c3, _) = CHUNKS_A[:4]
        assert o0 == 8 and c0 == 13

        self.say(f"IHDR 的长度 c = {c0}：跳 12 + {c0}，到下一块")
        calc = hop(strip[2], o0, c0)
        self.wait(0.8)
        for k, (o, c) in enumerate(((o1, c1), (o2, c2))):
            if k == 0:
                self.say(f"IDAT 装像素，这张图每块 {c:,} 字节，照样跳 12 + c")
            new_calc = mono(f"{o:,} + 12 + {c:,} = {o + 12 + c:,}", 30).set_color(FG).move_to(calc_pos)
            self.play(ReplacementTransform(calc, new_calc), Indicate(code[3], color=GOLD), run_time=0.6)
            calc = new_calc
            self.play(b.animate.set_value(o + 12 + c), pointer.animate.next_to(strip[3 + k].get_corner(UL), UP, buff=0.08), run_time=0.9)
            self.wait(0.3)

        o_last, c_last, t_last = CHUNKS_A[-2]
        assert t_last == "IDAT" and o3 == o2 + 12 + c2
        self.say(f"中间还有 {middle} 块 IDAT，一样地跳")
        new_calc = mono("b += 12 + c", 30).set_color(MUTED).move_to(calc_pos)
        self.play(ReplacementTransform(calc, new_calc), run_time=0.5)
        calc = new_calc
        self.play(b.animate.set_value(CHUNKS_A[4][0]), pointer.animate.next_to(strip[5].get_corner(UL), UP, buff=0.08), run_time=0.6)
        self.play(
            b.animate.set_value(o_last),
            pointer.animate.next_to(strip[6].get_corner(UL), UP, buff=0.08),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=3.0,
        )
        self.wait(0.4)

        self.say(f"最后一块 IDAT 只剩 {c_last:,} 字节")
        new_calc = mono(f"{o_last:,} + 12 + {c_last:,} = {o_last + 12 + c_last:,}", 30).set_color(FG).move_to(calc_pos)
        self.play(ReplacementTransform(calc, new_calc), Indicate(code[3], color=GOLD), run_time=0.6)
        calc = new_calc
        self.play(b.animate.set_value(o_last + 12 + c_last), pointer.animate.next_to(strip[7].get_corner(UL), UP, buff=0.08), run_time=0.9)
        self.wait(0.6)

        o_end, c_end, t_end = CHUNKS_A[-1]
        assert t_end == "IEND" and c_end == 0 and o_end + 12 == END_A
        self.say("IEND 没有数据，c = 0，只跳 12 字节")
        new_calc = mono(f"{o_end:,} + 12 + 0 = {END_A:,}", 30).set_color(FG).move_to(calc_pos)
        self.play(ReplacementTransform(calc, new_calc), Indicate(code[3], color=GOLD), run_time=0.6)
        calc = new_calc
        self.play(b.animate.set_value(END_A), pointer.animate.next_to(strip[7].get_corner(UR), UP, buff=0.08), run_time=0.9)
        self.wait(0.4)

        self.say(f"读到 IEND 就返回：b = {END_A:,}")
        self.play(Indicate(code[4], color=GOLD), code[4].animate.set_color(GOLD))
        result = VGroup(
            mono(f"return {END_A:,}", 32).set_color(GOLD),
            cn("= 第一张图的末尾 = 第二张图的起点", 26).set_color(FG),
        ).arrange(DOWN, buff=0.2).move_to(calc_pos + DOWN * 0.35)
        self.play(ReplacementTransform(calc, result))
        self.wait(2.0)
        self.hush()
        self.play(FadeOut(VGroup(code_tag, code, strip, pointer, readout, result)))


class PngPolyglot(Narrated):
    """IEND 之后：看图软件忽略的部分，正是第二张完整的 PNG。"""

    def construct(self):
        bar_w = 12.0
        wa = bar_w * END_A / SIZE
        wb = bar_w - wa
        seg_a = block("第一张 PNG", wa, ACCENT, 24, height=0.8)
        seg_b = block("？", wb, MUTED, 24, height=0.8)
        bar = VGroup(seg_a, seg_b).arrange(RIGHT, buff=0).move_to(UP * 1.6)
        size_tag = cn(f"start.png · {SIZE:,} 字节（按比例画）", 22).set_color(MUTED).next_to(bar, UP, buff=0.35)

        iend_x = seg_a.get_right()[0]
        iend = VGroup(
            Line([iend_x, bar.get_top()[1] + 0.05, 0], [iend_x, bar.get_bottom()[1] - 0.05, 0], color=GOLD, stroke_width=4),
        )
        iend.add(mono("IEND", 22).set_color(GOLD).next_to(iend[0], DOWN, buff=0.12))

        self.say("把整个文件按比例画出来")
        self.play(FadeIn(size_tag), FadeIn(seg_a), FadeIn(seg_b))
        self.play(Create(iend[0]), FadeIn(iend[1]))
        self.wait(0.6)

        ignored = cn("这里的字节一律忽略", 22).set_color(MUTED).next_to(seg_b, DOWN, buff=0.55)
        self.say("看图软件读到 IEND，就认为图片结束了")
        reader = Triangle(color=FG, fill_opacity=1).scale(0.12).rotate(PI).next_to(seg_a.get_corner(UL), UP, buff=0.06)
        self.play(FadeIn(reader))
        self.play(reader.animate.next_to([iend_x, bar.get_top()[1], 0], UP, buff=0.06), run_time=1.6)
        self.play(seg_b.animate.set_opacity(0.35), FadeIn(ignored, shift=UP * 0.1))
        self.wait(1.0)

        self.say(f"可 IEND 后面还有 {SIZE - END_A:,} 字节：它们恰好是另一张完整的 PNG")
        names = [ch[2] for ch in CHUNKS_B]
        inner = VGroup(
            block("签名", 1.2, OK, 20),
            *[block(n, 1.25 if n != "IDAT" else 2.4, OK if n != "tEXt" else MUTED, 20) for n in names],
        ).arrange(RIGHT, buff=0.06).move_to(DOWN * 0.9)
        zoom = VGroup(
            DashedLine(seg_b.get_corner(DL), inner.get_corner(UL), color=OK, stroke_width=1.5, dash_length=0.08),
            DashedLine(seg_b.get_corner(DR), inner.get_corner(UR), color=OK, stroke_width=1.5, dash_length=0.08),
        )
        self.play(FadeOut(ignored), FadeOut(reader))
        self.play(seg_b.animate.set_opacity(1), run_time=0.4)
        new_b = tint(block("第二张", wb, OK, 22, height=0.8).move_to(seg_b), OK)
        self.play(ReplacementTransform(seg_b, new_b), Create(zoom))
        seg_b = new_b
        bar = VGroup(seg_a, seg_b)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in inner], lag_ratio=0.15))
        self.wait(0.8)
        self.say("同样是签名开头、IEND 结尾，中间一个块都不缺")
        self.play(Indicate(inner[0], color=OK), Indicate(inner[-1], color=OK))
        self.wait(1.2)

        self.play(FadeOut(VGroup(inner, zoom)))
        term_lines = [
            "$ binwalk -a start.png",
            "0        0x0       PNG image, total size: 3139459 bytes",
            "3139459  0x2FE783  PNG image, total size: 583504 bytes",
        ]
        term = VGroup(*[mono(s, 22).set_color(FG if k else MUTED) for k, s in enumerate(term_lines)])
        term.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 0.65)
        term_box = box(term, MUTED, buff=0.3)
        self.say("binwalk 按「文件头」逐字节扫描，-a 让它把每一处都报出来")
        self.play(FadeIn(term_box), FadeIn(term[0]))
        self.play(FadeIn(term[1], shift=UP * 0.1))
        self.play(FadeIn(term[2], shift=UP * 0.1))
        self.wait(0.6)

        off_b = glyphs(term[2], term_lines[2], "3139459")
        self.say(f"第二张 PNG 的起点 0x2FE783，正是刚才算出的 {END_A:,}")
        self.play(off_b.animate.set_color(GOLD), Indicate(iend, color=GOLD))
        self.wait(0.8)

        s_a = glyphs(term[1], term_lines[1], "3139459")
        s_b = glyphs(term[2], term_lines[2], "583504")
        eq_src = f"{END_A:,} + {SIZE - END_A:,} = {SIZE:,}"
        eq = mono(eq_src, 34).set_color(FG).move_to(DOWN * 2.6)
        ok = cn("= 整个文件的大小", 26).set_color(OK).next_to(eq, RIGHT, buff=0.3)
        VGroup(eq, ok).move_to(DOWN * 2.6)
        self.say("两段长度加起来，刚好是整个文件：两张图首尾相接，一个字节不多")
        self.play(s_a.animate.set_color(ACCENT), s_b.animate.set_color(OK))
        self.play(
            TransformFromCopy(s_a, glyphs(eq, eq_src, f"{END_A:,}")),
            TransformFromCopy(s_b, glyphs(eq, eq_src, f"{SIZE - END_A:,}")),
        )
        self.play(FadeIn(glyphs(eq, eq_src, "+")), FadeIn(glyphs(eq, eq_src, "=")), FadeIn(glyphs(eq, eq_src, f"{SIZE:,}", 0)))
        self.play(FadeIn(ok, shift=LEFT * 0.1))
        self.wait(1.5)

        self.hush()
        self.play(FadeOut(VGroup(term, term_box, eq, ok, size_tag, iend)), bar.animate.move_to(UP * 2.9).scale(0.85))
        panels = Group()
        for path, title, who, col in (
            ("start.layer1.png", "start.layer1.png", "看图软件 · <img> 显示的", ACCENT),
            ("start.layer2.png", "start.layer2.png", "页面脚本 subarray(b) 取出的", OK),
        ):
            img = ImageMobject(str(DATA / path)).set(height=2.85)
            frame = SurroundingRectangle(img, color=col, buff=0.06, stroke_width=2)
            label = VGroup(mono(title, 22).set_color(col), cn(who, 20).set_color(MUTED)).arrange(DOWN, buff=0.1)
            label.next_to(frame, DOWN, buff=0.18)
            panels.add(Group(img, frame, label))
        panels.arrange(RIGHT, buff=0.7).move_to(DOWN * 0.45)

        arrows = VGroup(
            Arrow(bar[0].get_bottom(), panels[0].get_top(), color=ACCENT, buff=0.1, stroke_width=3),
            Arrow(bar[1].get_bottom(), panels[1].get_top(), color=OK, buff=0.1, stroke_width=3),
        )
        self.say("于是同一个文件，看图软件只看得到前一张")
        self.play(GrowArrow(arrows[0]), FadeIn(panels[0], shift=DOWN * 0.15))
        self.wait(0.6)
        self.say("而页面脚本跳过前一张，把后一张显示在网页上")
        self.play(GrowArrow(arrows[1]), FadeIn(panels[1], shift=DOWN * 0.15))
        self.wait(1.0)
        self.say("两张图乍看一样——差别藏在哪里，是下一段的事")
        self.wait(2.0)
        self.hush()
        self.play(FadeOut(Group(bar, arrows, panels)))
