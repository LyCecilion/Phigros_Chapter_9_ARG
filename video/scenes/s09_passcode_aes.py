"""s09 · 通行密钥 → AES（抽象版）：只讲验证链路，不展示游戏内部细节。"""

import hashlib

from manim import *
from style import *

MESSAGE = "YOU MUST GO BY A WAY WHICH IS THE WAY OF IGNORANCE"
DIGEST = hashlib.sha512(MESSAGE.encode("utf-8")).digest()
HEX = DIGEST.hex().upper()
assert len(DIGEST) == 64
assert len(HEX) == 128
KEY_BYTES, IV_BYTES, UNUSED_BYTES = DIGEST[:32], DIGEST[32:48], DIGEST[48:]
assert (len(KEY_BYTES), len(IV_BYTES), len(UNUSED_BYTES)) == (32, 16, 16)


def title_block(title: str, subtitle: str | None = None) -> VGroup:
    items = [ui(title, 36).set_color(FG)]
    if subtitle:
        items.append(ui(subtitle, 20).set_color(MUTED))
    return VGroup(*items).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.32)


def block(text: str, width: float, color, size: float = 23, height: float = 0.7) -> VGroup:
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.07, stroke_color=color, stroke_width=1.6)
    rect.set_fill(color, opacity=0.14)
    return VGroup(rect, mono(text, size).set_color(color).move_to(rect))


def bytes_row(data: bytes, color, y: float, label: str) -> VGroup:
    cells = VGroup(*[
        block(f"{value:02X}", 0.48, color, 17, 0.52) for value in data
    ]).arrange(RIGHT, buff=0.04)
    tag = ui(label, 21).set_color(color).next_to(cells, LEFT, buff=0.22)
    return VGroup(tag, cells).move_to([0, y, 0])


class PasscodeHash(Narrated):
    """SHA-512 的 64 字节输出如何切成 Key 与 IV。"""

    def construct(self):
        title = title_block("通行密钥 · 先把一句话变成字节", "SHA-512 输出固定为 64 bytes")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        phrase = block("sentence / passcode", 4.2, CIPHER, 25, 0.78).move_to([-4.0, 1.4, 0])
        arrow = Arrow(phrase.get_right(), [-1.45, 1.4, 0], color=MUTED, stroke_width=2)
        hash_box = block("SHA-512", 2.2, ACCENT, 26, 0.78).move_to([0, 1.4, 0])
        arrow2 = Arrow(hash_box.get_right(), [1.4, 1.4, 0], color=MUTED, stroke_width=2)
        output = block("64 bytes", 2.0, GOLD, 25, 0.78).move_to([2.55, 1.4, 0])
        self.say("玩家输入的一句话，先经过 SHA-512")
        self.play(FadeIn(phrase), GrowArrow(arrow), FadeIn(hash_box), GrowArrow(arrow2), FadeIn(output))
        self.wait(1.0)

        digest = bytes_row(DIGEST[:16], ACCENT, 0.25, "hash 前 16")
        digest2 = bytes_row(DIGEST[16:32], ACCENT, -0.35, "hash 16–32")
        self.say("哈希的输出长度固定，不管输入句子多长，结果都是 64 字节")
        self.play(FadeIn(digest), FadeIn(digest2), run_time=1.3)
        self.wait(0.8)

        key = block("Key · 32 bytes", 3.0, GOLD, 25).move_to([-2.35, -1.65, 0])
        iv = block("IV · 16 bytes", 2.7, ACCENT, 25).move_to([1.05, -1.65, 0])
        unused = block("剩余 16 bytes · 不使用", 3.7, MUTED, 22).move_to([4.25, -1.65, 0])
        self.say("前 32 字节作为 Key，接着 16 字节作为 IV，剩下的不用")
        self.play(FadeIn(key), FadeIn(iv), FadeIn(unused, shift=DOWN * 0.15))
        self.wait(1.8)
        self.hush()
        self.play(FadeOut(VGroup(title, phrase, arrow, hash_box, arrow2, output, digest, digest2, key, iv, unused)))


class AesGate(Narrated):
    """Key 和 IV 打开 AES 盒子，再用已知答案验证结果。"""

    def construct(self):
        title = title_block("AES · 有钥匙才能打开加密资源", "动画只保留密码学上的抽象流程")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        key = block("Key", 1.7, GOLD, 25).move_to([-4.25, 1.0, 0])
        iv = block("IV", 1.7, ACCENT, 25).move_to([-4.25, -0.05, 0])
        key_arrow = Arrow(key.get_right(), [-2.8, 1.0, 0], color=GOLD, stroke_width=2)
        iv_arrow = Arrow(iv.get_right(), [-2.8, -0.05, 0], color=ACCENT, stroke_width=2)
        lock = VGroup(
            RoundedRectangle(width=2.4, height=2.0, corner_radius=0.16, stroke_color=GOLD, stroke_width=2.5),
            mono("AES", 38).set_color(GOLD),
            ui("解密", 22).set_color(MUTED),
        ).arrange(DOWN, buff=0.12).move_to([-1.45, 0.45, 0])
        ciphertext = block("encrypted bundle", 3.0, CIPHER, 23).move_to([1.5, 0.45, 0])
        arrow2 = Arrow(ciphertext.get_left(), lock.get_right(), color=CIPHER, stroke_width=2)
        self.say("Key 和 IV 一起进入 AES 解密器，面对的是锁住的资源")
        self.play(FadeIn(key), FadeIn(iv), GrowArrow(key_arrow), GrowArrow(iv_arrow), FadeIn(lock), FadeIn(ciphertext), GrowArrow(arrow2))
        self.wait(1.0)

        denied = chip("错误的 Key  →  ACCESS DENIED", DANGER, 25).move_to([0, -1.45, 0])
        self.say("钥匙不对，输出无法通过验证")
        self.play(FadeIn(denied, shift=UP * 0.15), Indicate(lock, color=DANGER))
        self.wait(1.0)
        self.play(FadeOut(denied))

        answer = block("known answer: pass", 3.2, OK, 24).move_to([3.7, -1.15, 0])
        granted = chip("正确的 Key  →  ACCESS GRANTED", OK, 25).move_to([0, -1.45, 0])
        check_arrow = Arrow(lock.get_right() + DOWN * 0.35, answer.get_left(), color=OK, stroke_width=2)
        self.say("钥匙正确，解密结果和已知答案一致，才放行")
        self.play(FadeIn(answer), GrowArrow(check_arrow), FadeIn(granted, shift=UP * 0.15), Indicate(lock, color=OK))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, key, iv, key_arrow, iv_arrow, lock, ciphertext, arrow2, answer, check_arrow, granted)))


class AesWhyKeyMatters(Narrated):
    """收束：解包得到密文，不等于得到了隐藏曲。"""

    def construct(self):
        title = title_block("AES · 为什么光有资源文件还不够？", "加密不是压缩：没有 Key，不能直接还原明文")
        self.play(FadeIn(title, shift=DOWN * 0.15))

        package = block("拿到的文件", 2.4, CIPHER, 25).move_to([-4.1, 0.65, 0])
        locked = VGroup(
            Circle(radius=0.72, color=DANGER, stroke_width=3),
            Line([-0.35, -0.22, 0], [0.35, 0.22, 0], color=DANGER, stroke_width=3),
            Line([-0.35, 0.22, 0], [0.35, -0.22, 0], color=DANGER, stroke_width=3),
        ).move_to([-1.55, 0.65, 0])
        impossible = ui("没有 Key，不能从密文直接恢复隐藏曲", 25).set_color(DANGER).move_to([1.35, 0.65, 0])
        self.say("即使已经把加密资源从包里找出来，它仍然只是密文")
        self.play(FadeIn(package), FadeIn(locked), FadeIn(impossible), run_time=1.3)

        chain = VGroup(
            chip("正确 PASSCODE", GOLD, 23),
            mono("→ SHA-512", 25).set_color(ACCENT),
            mono("→ Key + IV", 25).set_color(ACCENT),
            mono("→ AES", 25).set_color(OK),
            chip("hidden song", OK, 23),
        ).arrange(RIGHT, buff=0.18).move_to([0, -1.25, 0])
        self.say("只有从谜题得到正确的通行密钥，才能走完这条链路")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in chain], lag_ratio=0.15), run_time=1.8)
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(title, package, locked, impossible, chain)))
