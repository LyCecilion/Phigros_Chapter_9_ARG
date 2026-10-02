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
        phrase = block("sentence / passcode", 4.2, CIPHER, 25, 0.78).move_to([-4.0, 1.9, 0])
        arrow = Arrow(phrase.get_right(), [-1.45, 1.9, 0], color=MUTED, stroke_width=2)
        hash_box = block("SHA-512", 2.2, ACCENT, 26, 0.78).move_to([0, 1.9, 0])
        arrow2 = Arrow(hash_box.get_right(), [1.4, 1.9, 0], color=MUTED, stroke_width=2)
        output = block("64 bytes", 2.0, GOLD, 25, 0.78).move_to([2.55, 1.9, 0])
        self.say("玩家输入的一句话，先经过 SHA-512")
        self.play(FadeIn(phrase), GrowArrow(arrow), FadeIn(hash_box), GrowArrow(arrow2), FadeIn(output))
        self.wait(1.0)

        digest = bytes_row(DIGEST[:16], ACCENT, 0.75, "hash 前 16")
        digest2 = bytes_row(DIGEST[16:32], ACCENT, 0.15, "hash 16–32")
        self.say("哈希的输出长度固定，不管输入句子多长，结果都是 64 字节")
        self.play(FadeIn(digest), FadeIn(digest2), run_time=1.3)
        self.wait(0.8)

        # 三块之间用同一个间隔排（原来第一个和第二个留 0.55、第二个和第三个贴死）
        row = VGroup(
            block("Key · 32 bytes", 3.0, GOLD, 25),
            block("IV · 16 bytes", 2.7, ACCENT, 25),
            block("剩余 16 bytes · 不使用", 3.7, MUTED, 22),
        ).arrange(RIGHT, buff=0.55).move_to([0, -1.15, 0])
        key, iv, unused = row
        self.say("前 32 字节作为 Key，接着 16 字节作为 IV，剩下的不用")
        self.play(FadeIn(key), FadeIn(iv), FadeIn(unused, shift=DOWN * 0.15))
        self.wait(1.8)
        self.hush()
        self.play(FadeOut(VGroup(phrase, arrow, hash_box, arrow2, output, digest, digest2, key, iv, unused)))


class AesGate(Narrated):
    """Key 和 IV 进入 AES 解密器，再用已知答案验证结果。"""

    def construct(self):
        # 一条竖着的流程图：密文 → AES 解密 → 明文 ⇕ 已知答案 → 放行 / 拒绝
        ciphertext = block("encrypted bundle", 3.2, CIPHER, 23).move_to([-4.3, 1.6, 0])
        aes = block("AES 解密", 2.6, GOLD, 26, 0.8).move_to([0, 1.6, 0])
        key = block("Key · 32 bytes", 2.9, GOLD, 24).move_to([-1.9, 2.95, 0])
        iv = block("IV · 16 bytes", 2.9, ACCENT, 24).move_to([1.9, 2.95, 0])
        in_arrow = Arrow(ciphertext.get_right(), aes.get_left(), buff=0.12, color=CIPHER, stroke_width=2)
        key_arrow = Arrow(key.get_bottom(), aes.get_top() + LEFT * 0.45, buff=0.12, color=GOLD, stroke_width=2)
        iv_arrow = Arrow(iv.get_bottom(), aes.get_top() + RIGHT * 0.45, buff=0.12, color=ACCENT, stroke_width=2)
        self.say("Key 和 IV 一起喂给 AES 解密器，吃进去的是一段加密资源")
        self.play(
            FadeIn(ciphertext), GrowArrow(in_arrow), FadeIn(aes),
            FadeIn(key), GrowArrow(key_arrow), FadeIn(iv), GrowArrow(iv_arrow),
        )
        self.wait(1.0)

        # 钥匙不对：AES 那一格的输出就是拒绝
        down = Arrow(aes.get_bottom(), [0, 0.78, 0], buff=0.12, color=MUTED, stroke_width=2)
        denied = chip("✗ ACCESS DENIED", DANGER, 25).move_to([0, 0.3, 0])
        self.say("钥匙不对，AES 解不出明文，验证不通过")
        self.play(GrowArrow(down), FadeIn(denied, shift=UP * 0.12), Indicate(aes, color=DANGER))
        self.wait(1.0)
        self.play(FadeOut(denied), run_time=0.4)

        # 钥匙正确：同一格冒出明文，再和已知答案比对
        plain = block('明文 = "pass"', 3.0, OK, 24, 0.8).move_to([0, 0.3, 0])
        answer = block("known answer: pass", 3.5, OK, 23).move_to([0, -1.35, 0])
        compare = DoubleArrow(plain.get_bottom(), answer.get_top(), buff=0.12, color=OK, stroke_width=2)
        out = Arrow(answer.get_bottom(), [0, -2.25, 0], buff=0.12, color=OK, stroke_width=2)
        granted = chip("✓ ACCESS GRANTED", OK, 25).move_to([0, -2.75, 0])
        self.say("钥匙正确时，解出的明文和已知答案一致，才放行")
        self.play(FadeIn(plain, shift=UP * 0.12))
        self.play(GrowArrow(compare), FadeIn(answer))
        self.play(GrowArrow(out), FadeIn(granted, shift=UP * 0.12), Indicate(aes, color=OK))
        self.wait(2)
        self.hush()
        self.play(
            FadeOut(
                VGroup(
                    ciphertext, aes, key, iv, in_arrow, key_arrow, iv_arrow,
                    down, plain, answer, compare, out, granted,
                )
            )
        )


class AesWhyKeyMatters(Narrated):
    """收束：解包得到密文，不等于得到了隐藏曲。"""

    def construct(self):
        package = block("拿到的文件", 2.4, CIPHER, 25).move_to([-4.1, 1.15, 0])
        impossible = ui("没有 Key，不能从密文直接恢复隐藏曲", 25).set_color(DANGER).move_to([1.35, 1.15, 0])
        self.say("即使已经把加密资源从包里找出来，它仍然只是密文")
        self.play(FadeIn(package), FadeIn(impossible), run_time=1.3)

        chain = VGroup(
            chip("正确 PASSCODE", GOLD, 23),
            mono("→ SHA-512", 25).set_color(ACCENT),
            mono("→ Key + IV", 25).set_color(ACCENT),
            mono("→ AES", 25).set_color(OK),
            chip("hidden song", OK, 23),
        ).arrange(RIGHT, buff=0.18).move_to([0, -0.75, 0])
        self.say("只有从谜题得到正确的通行密钥，才能走完这条链路")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in chain], lag_ratio=0.15), run_time=1.8)
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(package, impossible, chain)))
