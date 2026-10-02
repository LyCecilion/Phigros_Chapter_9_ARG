"""s01 · Chaocipher：两个字母盘如何在每一步「自我打乱」。

用法：
    ./render.sh -ql scenes/s01_chaocipher.py ChaocipherIntro     # 字母盘 + 第 1 个字母慢放
    ./render.sh -ql scenes/s01_chaocipher.py ChaocipherRun       # 跑完剩下 34 个字母 + 德语原句
    ./render.sh -ql scenes/s01_chaocipher.py ChaocipherWhyChaos  # 同一密文字母 → 不同明文

三个 Scene 前后衔接：Run 的开场状态 = Intro 的结束状态。
"""

from manim import *
from style import *

# --- 算法（解密方向）---------------------------------------------------------

CIPHERTEXT = "ZGJGDGTDNUIOSQQCLIWWCWIIADNOFQDAEMG"
LEFT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RIGHT_ALPHABET = "PSZLMYQEBJARTFCHNUGVKDOXIW"
EXPECTED = "WERJETZTALLEINISTWIRDESLANGEBLEIBEN"

N = 26
NADIR = 13  # 第 14 位（0 起）


def rotated(order: list[str], i: int) -> list[str]:
    """整体转动，使 order[i] 到达 zenith。"""
    return order[i:] + order[:i]


def extract_insert(order: list[str], take: int) -> list[str]:
    """取出 take 处字母，其后到 nadir 的一段左移一格，再插回 nadir。"""
    out = list(order)
    out.insert(NADIR, out.pop(take))
    return out


def decrypt_step(left: list[str], right: list[str], c: str):
    """返回 (明文字母, 命中位置, 新左盘, 新右盘)。"""
    i = left.index(c)
    p = right[i]
    new_left = extract_insert(rotated(left, i), 1)
    new_right = extract_insert(rotated(rotated(right, i), 1), 2)
    return p, i, new_left, new_right


def run_all():
    left, right = list(LEFT_ALPHABET), list(RIGHT_ALPHABET)
    states = []
    for c in CIPHERTEXT:
        p, i, left, right = decrypt_step(left, right, c)
        states.append((p, i, left, right))
    return states


STATES = run_all()
PLAINTEXT = "".join(s[0] for s in STATES)
assert PLAINTEXT == EXPECTED, PLAINTEXT
assert "".join(STATES[0][2]) == "ZBCDEFGHIJKLMANOPQRSTUVWXY"
assert "".join(STATES[0][3]) == "PSLMYQEBJARTFZCHNUGVKDOXIW"

# --- 版面 ---------------------------------------------------------------------

STEP = TAU / N
DISK_R = 1.95
LIFT = 0.62
DISK_Y = -0.55
LEFT_C = np.array([-3.3, DISK_Y, 0])
RIGHT_C = np.array([3.3, DISK_Y, 0])
TAPE_W = 0.3
CT_Y, PT_Y = 3.45, 2.92


def angle_of(i: float) -> float:
    """第 i 格的角度：0 在正上方，顺时针递增。"""
    return PI / 2 - i * STEP


class Disk:
    """一个字母盘：记录字母顺序与每个字母的半径，生成「换位」动画。"""

    def __init__(self, order, center, ring_color, title: str, role: str):
        self.order = list(order)
        self.center = np.array(center, dtype=float)
        self.glyphs = {ch: mono(ch, 26).set_color(FG) for ch in self.order}
        self.rad = {ch: DISK_R for ch in self.order}
        for i, ch in enumerate(self.order):
            self.glyphs[ch].move_to(self.point(i))

        rings = VGroup(
            Circle(radius=DISK_R + 0.36, color=ring_color, stroke_width=2),
            Circle(radius=DISK_R - 0.36, color=ring_color, stroke_width=1, stroke_opacity=0.5),
        ).move_to(self.center)
        label = VGroup(
            cn(title, 34).set_color(ring_color),
            cn(role, 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.12).move_to(self.center)

        top = self.center + UP * (DISK_R + 0.36)
        bottom = self.center + DOWN * (DISK_R + 0.36)
        zenith = VGroup(
            Triangle(color=GOLD, fill_opacity=1).scale(0.09).rotate(PI).next_to(top, UP, buff=0.05),
        )
        zenith.add(mono("zenith", 18).set_color(GOLD).next_to(zenith[0], RIGHT, buff=0.12))
        nadir = VGroup(
            Triangle(color=GOLD, fill_opacity=1).scale(0.09).next_to(bottom, DOWN, buff=0.05),
        )
        nadir.add(mono("nadir", 18).set_color(GOLD).next_to(nadir[0], RIGHT, buff=0.12))

        self.frame = VGroup(rings, label, zenith, nadir)
        self.letters = VGroup(*self.glyphs.values())

    def point(self, i: float, r: float = DISK_R) -> np.ndarray:
        a = angle_of(i)
        return self.center + r * np.array([np.cos(a), np.sin(a), 0])

    def slot(self, i: int, color=GOLD) -> Circle:
        return Circle(radius=0.27, color=color, stroke_width=3).move_to(self.point(i))

    def band(self, a: int, b: int, color=ACCENT) -> AnnularSector:
        """覆盖第 a..b 格的扇环，用于标出「整体左移」的那一段。"""
        return AnnularSector(
            inner_radius=DISK_R - 0.33,
            outer_radius=DISK_R + 0.33,
            angle=(b - a + 1) * STEP,
            start_angle=angle_of(b) - STEP / 2,
            fill_color=color,
            fill_opacity=0.16,
            stroke_width=0,
            arc_center=self.center,
        )

    def morph(self, new_order, radius=None, **kw) -> Animation:
        """沿圆周把每个字母移到新位置（走最短弧），同时可改半径。调用即提交新状态。"""
        radius = radius or {}
        old = {ch: i for i, ch in enumerate(self.order)}
        plan = []
        for j, ch in enumerate(new_order):
            i = old[ch]
            d = (j - i) % N
            if d > N // 2:
                d -= N
            r0 = self.rad[ch]
            r1 = radius.get(ch, r0)
            self.rad[ch] = r1
            if d or r0 != r1:
                plan.append((self.glyphs[ch], i, d, r0, r1))
        self.order = list(new_order)

        def update(_, a):
            for glyph, i, d, r0, r1 in plan:
                glyph.move_to(self.point(i + d * a, r0 + (r1 - r0) * a))

        return UpdateFromAlphaFunc(VGroup(*[p[0] for p in plan]), update, **kw)

    def lift(self, ch: str, **kw) -> Animation:
        return self.morph(self.order, radius={ch: DISK_R + LIFT}, **kw)

    def drop(self, ch: str, **kw) -> Animation:
        return self.morph(self.order, radius={ch: DISK_R}, **kw)


def tape(text: str, y: float, color) -> VGroup:
    """等距排开的一行字符（逐字可寻址）。"""
    x0 = -TAPE_W * (len(CIPHERTEXT) - 1) / 2
    return VGroup(*[mono(ch, 24).set_color(color).move_to([x0 + k * TAPE_W, y, 0]) for k, ch in enumerate(text)])


def tape_slot(k: int, y: float) -> np.ndarray:
    return np.array([-TAPE_W * (len(CIPHERTEXT) - 1) / 2 + k * TAPE_W, y, 0])


class ChaoBase(Narrated):
    def board(self, left_order, right_order, done: int):
        """直接摆出「已解 done 个字母」后的局面（无动画）。"""
        self.left = Disk(left_order, LEFT_C, CIPHER, "左盘", "读密文")
        self.right = Disk(right_order, RIGHT_C, OK, "右盘", "读明文")
        self.ct = tape(CIPHERTEXT, CT_Y, CIPHER)
        self.ct_tag = cn("密文", 22).set_color(MUTED).next_to(self.ct, LEFT, buff=0.35)
        self.pt_tag = cn("明文", 22).set_color(MUTED).move_to([self.ct_tag.get_x(), PT_Y, 0])
        self.pt = VGroup(*[mono(PLAINTEXT[k], 24).set_color(OK).move_to(tape_slot(k, PT_Y)) for k in range(done)])
        self.cursor = SurroundingRectangle(self.ct[done], color=GOLD, buff=0.06, stroke_width=2)

    def step(self, k: int, pace: str):
        """解第 k 个字母。pace: 'slow' 逐步讲解 / 'mid' 分步无字幕 / 'fast' 一步到位。"""
        c = CIPHERTEXT[k]
        p, i, new_left, new_right = STATES[k]
        L, R = self.left, self.right
        t = {"slow": 1.0, "mid": 0.45, "fast": 0.22}[pace]

        cursor = SurroundingRectangle(self.ct[k], color=GOLD, buff=0.06, stroke_width=2)
        hit_l, hit_r = L.slot(i, GOLD), R.slot(i, OK)
        link = DashedLine(L.point(i), R.point(i), color=ACCENT, stroke_width=2, dash_length=0.1)

        if pace == "slow":
            self.say("解密：先在左盘上找到密文字母")
        self.play(Transform(self.cursor, cursor), run_time=0.5 * t)
        self.play(Create(hit_l), run_time=0.6 * t)
        if pace == "slow":
            self.wait(0.6)
            self.say("右盘上同一位置的字母，就是明文")
        self.play(Create(link), Create(hit_r), run_time=0.6 * t)

        out = R.glyphs[p].copy().set_color(OK)
        self.add(out)
        self.play(out.animate.move_to(tape_slot(k, PT_Y)).scale(24 / 26), run_time=0.7 * t)
        self.pt.add(out)
        if pace == "slow":
            self.wait(1.0)

        if pace == "fast":
            self.play(
                FadeOut(VGroup(hit_l, hit_r, link)),
                L.morph(new_left),
                R.morph(new_right),
                run_time=0.55,
            )
            return

        # ① 两盘一起转，命中位置到 zenith
        if pace == "slow":
            self.say("接下来是「置换」：两盘一起转，把这个位置转到 zenith")
        self.play(
            FadeOut(link),
            L.morph(rotated(L.order, i)),
            R.morph(rotated(R.order, i)),
            hit_l.animate.move_to(L.point(0)),
            hit_r.animate.move_to(R.point(0)),
            run_time=1.4 * t,
        )
        self.play(FadeOut(hit_l), FadeOut(hit_r), run_time=0.3 * t)
        if pace == "slow":
            self.wait(0.6)

        # ② 左盘：取 zenith+1 → zenith+2..nadir 左移 → 插回 nadir
        self.permute(L, take=1, after=new_left, pace=pace, t=t, side="左盘")

        # ③ 右盘：整体再左移一格 → 取 zenith+2 → zenith+3..nadir 左移 → 插回 nadir
        if pace == "slow":
            self.say("右盘：先整体再左移一格")
        self.play(R.morph(rotated(R.order, 1)), run_time=0.9 * t)
        self.permute(R, take=2, after=new_right, pace=pace, t=t, side="右盘")

        assert L.order == new_left and R.order == new_right

    def permute(self, disk: Disk, take: int, after, pace: str, t: float, side: str):
        ch = disk.order[take]
        band = disk.band(take + 1, NADIR)
        if pace == "slow":
            self.say(f"{side}：取出 zenith+{take} 处的字母")
        self.play(disk.lift(ch), disk.glyphs[ch].animate.set_color(GOLD), run_time=0.7 * t)
        if pace == "slow":
            self.say(f"zenith+{take + 1} 到 nadir 这一段，整体左移一格")
        self.play(FadeIn(band), run_time=0.4 * t)
        self.play(disk.morph(extract_insert(disk.order, take)), run_time=1.2 * t)
        if pace == "slow":
            self.say("再把取出的字母插回 nadir")
        self.play(disk.drop(ch), FadeOut(band), run_time=0.7 * t)
        self.play(disk.glyphs[ch].animate.set_color(FG), run_time=0.3 * t)
        assert disk.order == after
        if pace == "slow":
            self.wait(0.8)


class ChaocipherIntro(ChaoBase):
    """字母盘登场 + 第 1 个字母完整慢放。"""

    def construct(self):
        self.board(LEFT_ALPHABET, RIGHT_ALPHABET, done=0)
        L, R = self.left, self.right

        # 简介里的两行 → 两个字母盘
        src_left = mono("left:  A - Z", 30).set_color(CIPHER)
        src_right = mono(f"right: {RIGHT_ALPHABET}", 30).set_color(OK)
        src = VGroup(src_left, src_right).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(src))
        self.wait(1.0)

        line_left = VGroup(*[L.glyphs[ch] for ch in LEFT_ALPHABET]).copy()
        line_right = VGroup(*[R.glyphs[ch] for ch in RIGHT_ALPHABET]).copy()
        line_left.arrange(RIGHT, buff=0.14).move_to(UP * 0.5)
        line_right.arrange(RIGHT, buff=0.14).move_to(DOWN * 0.5)
        self.play(
            ReplacementTransform(src_left, line_left),
            ReplacementTransform(src_right, line_right),
        )
        self.wait(0.5)
        self.play(
            ReplacementTransform(line_left, L.letters),
            ReplacementTransform(line_right, R.letters),
            Create(L.frame[0]),
            Create(R.frame[0]),
            run_time=2.0,
        )
        self.play(FadeIn(L.frame[1]), FadeIn(R.frame[1]))
        self.say("Chaocipher：两个各 26 格的字母盘", wait=1.0)
        self.play(FadeIn(L.frame[2:]), FadeIn(R.frame[2:]))
        self.say("第 1 格叫 zenith（天顶），第 14 格叫 nadir（天底）", wait=1.5)

        self.play(FadeIn(self.ct_tag), FadeIn(self.pt_tag), LaggedStart(*[FadeIn(g) for g in self.ct], lag_ratio=0.03))
        self.play(Create(self.cursor))
        self.wait(0.5)

        self.step(0, "slow")
        self.say("两张字母表都变了，下一个字母要用新的表来查", wait=2.0)


class ChaocipherRun(ChaoBase):
    """承接 Intro：跑完剩下的字母，逐渐加速，得到德语原句。"""

    def construct(self):
        _, _, left0, right0 = STATES[0]
        self.board(left0, right0, done=1)
        self.add(self.left.frame, self.left.letters, self.right.frame, self.right.letters)
        self.add(self.ct_tag, self.pt_tag, self.ct, self.pt, self.cursor)
        self.say("每解一个字母，就做一次同样的替换 + 置换")

        for k in range(1, 4):
            self.step(k, "mid")
        self.say("越往后越快：规则不变，只是字母表一直在变")
        for k in range(4, len(CIPHERTEXT)):
            self.step(k, "fast")
        self.play(FadeOut(self.cursor))
        self.wait(0.8)

        # 收束到明文
        disks = VGroup(self.left.frame, self.left.letters, self.right.frame, self.right.letters)
        self.play(FadeOut(disks), FadeOut(self.caption), FadeOut(self.ct), FadeOut(self.ct_tag), FadeOut(self.pt_tag))
        self.caption = None
        self.play(self.pt.animate.scale(1.1).move_to(UP * 1.2))
        self.wait(0.8)

        words = ["WER", "JETZT", "ALLEIN", "IST", "WIRD", "ES", "LANGE", "BLEIBEN"]
        groups, k = [], 0
        for w in words:
            groups.append(VGroup(*self.pt[k : k + len(w)]))
            k += len(w)
        spaced = VGroup(*[g.copy() for g in groups]).arrange(RIGHT, buff=0.36).move_to(UP * 1.2)
        self.play(*[g.animate.move_to(s) for g, s in zip(groups, spaced)], run_time=1.2)
        self.wait(0.8)

        german = cn("„Wer jetzt allein ist, wird es lange bleiben“", 40).set_color(FG).move_to(DOWN * 0.1)
        zh = cn("如今独自一人的人，将长久如此", 32).set_color(MUTED).next_to(german, DOWN, buff=0.35)
        src = cn("—— Rainer Maria Rilke《秋日》(Herbsttag)", 26).set_color(GOLD).next_to(zh, DOWN, buff=0.45)
        self.play(Write(german), run_time=2.0)
        self.play(FadeIn(zh, shift=UP * 0.1))
        self.play(FadeIn(src, shift=UP * 0.1))
        self.wait(2.5)


class ChaocipherWhyChaos(ChaoBase):
    """同一个密文字母在不同位置解出不同明文：对照固定映射。"""

    def construct(self):
        ct = tape(CIPHERTEXT, 1.6, CIPHER)
        pt = tape(PLAINTEXT, 0.9, OK)
        ct_tag = cn("密文", 24).set_color(MUTED).next_to(ct, LEFT, buff=0.35)
        pt_tag = cn("明文", 24).set_color(MUTED).next_to(pt, LEFT, buff=0.35)
        VGroup(ct_tag, ct, pt_tag, pt).scale(1.1).set_x(0)
        self.play(FadeIn(VGroup(ct_tag, ct, pt_tag, pt)))
        self.wait(0.6)

        hits = [k for k, c in enumerate(CIPHERTEXT) if c == "G"]
        boxes = VGroup(*[SurroundingRectangle(VGroup(ct[k], pt[k]), color=GOLD, buff=0.07, stroke_width=2) for k in hits])
        self.say("同一个密文字母 G，出现了 4 次")
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25))
        self.wait(1.0)

        mapping = VGroup(
            mono("G", 40).set_color(CIPHER),
            mono("→", 40).set_color(MUTED),
            VGroup(*[mono(PLAINTEXT[k], 40).set_color(OK) for k in hits]).arrange(RIGHT, buff=0.5),
        ).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.7)
        self.say("每次解出来的明文都不一样")
        self.play(FadeIn(mapping[:2]))
        self.play(LaggedStart(*[TransformFromCopy(pt[k], m) for k, m in zip(hits, mapping[2])], lag_ratio=0.3))
        self.wait(1.2)

        fixed = VGroup(
            cn("凯撒、Atbash：一个字母永远对应同一个字母", 28).set_color(MUTED),
            cn("Chaocipher：字母表每一步都在变", 28).set_color(GOLD),
            cn("字母频率被打散，统计分析几乎无从下手", 28).set_color(FG),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 2.3)
        self.play(FadeOut(self.caption))
        self.caption = None
        for line in fixed:
            self.play(FadeIn(line, shift=UP * 0.1))
            self.wait(0.8)
        self.wait(1.5)
