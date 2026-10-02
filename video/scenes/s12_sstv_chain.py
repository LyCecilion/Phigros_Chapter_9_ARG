"""s12 · SSTV 音频从哪来：页面如何协商密钥并解开 PNG 里的音频。"""

from pathlib import Path
import wave

from manim import *
from style import *

DATA = Path(__file__).resolve().parents[2] / "artifacts/stage_ii/SSTV"
AUDIO = DATA / "solivault_song.wav"
with wave.open(str(AUDIO), "rb") as wav:
    AUDIO_RATE = wav.getframerate()
    AUDIO_CHANNELS = wav.getnchannels()
    AUDIO_SECONDS = wav.getnframes() / AUDIO_RATE
assert (AUDIO_RATE, AUDIO_CHANNELS) == (44100, 1)
assert 111.3 < AUDIO_SECONDS < 111.4


def block(text: str, width: float, color, size: float = 23, height: float = 0.7) -> VGroup:
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.07, stroke_color=color, stroke_width=1.6)
    rect.set_fill(color, opacity=0.14)
    return VGroup(rect, mono(text, size).set_color(color).move_to(rect))


def arrow_between(a: Mobject, b: Mobject, color=MUTED) -> Arrow:
    return Arrow(a.get_right(), b.get_left(), buff=0.15, color=color, stroke_width=2)


class SSTVHandshake(Narrated):
    """抽象展示 ECDH → HKDF → AES-GCM 的会话链路。"""

    def construct(self):
        browser = block("浏览器", 1.8, ACCENT, 24).move_to([-4.8, 1.75, 0])
        server = block("服务器", 1.8, CIPHER, 24).move_to([4.8, 1.75, 0])
        pub1 = Arrow(browser.get_right(), server.get_left(), color=ACCENT, stroke_width=2)
        pub2 = Arrow(server.get_left() + DOWN * 0.45, browser.get_right() + DOWN * 0.45, color=CIPHER, stroke_width=2)
        pub1_label = mono("公钥", 20).set_color(ACCENT).next_to(pub1, UP, buff=0.12)
        # pub2 的标签原本居中贴在 pub2 箭头下方，正好压在 ecdh 芯片上框上（读成 ECDH·公钥P-256）；
        # 左移让标签右缘与芯片左框拉开 ≥0.4 的间隙。
        pub2_label = mono("公钥", 20).set_color(CIPHER).next_to(pub2, DOWN, buff=0.12).shift(LEFT * 1.9)
        self.say("浏览器和服务器先交换临时公钥，双方都不直接发送共享密钥")
        self.play(FadeIn(browser), FadeIn(server), GrowArrow(pub1), GrowArrow(pub2), FadeIn(pub1_label), FadeIn(pub2_label))
        self.wait(1.0)

        ecdh = chip("ECDH · P-256", GOLD, 24).move_to([0, 0.85, 0])
        shared = block("共享秘密", 2.5, GOLD, 24).move_to([0, 0.05, 0])
        hkdf = block("HKDF-SHA256", 2.8, ACCENT, 24).move_to([-2.45, -1.05, 0])
        session = block("会话密钥", 2.5, OK, 24).move_to([2.45, -1.05, 0])
        self.say("ECDH 让双方各自算出同一份共享秘密")
        self.play(FadeIn(ecdh), FadeIn(shared), Create(Line(ecdh.get_bottom(), shared.get_top(), color=MUTED, stroke_width=2)))
        self.say("再经过 HKDF，得到这一次访问专用的会话密钥")
        self.play(FadeIn(hkdf), FadeIn(session), GrowArrow(Arrow(shared.get_bottom(), hkdf.get_top(), color=MUTED, stroke_width=2)), GrowArrow(Arrow(shared.get_bottom(), session.get_top(), color=MUTED, stroke_width=2)))
        self.wait(2)
        self.hush()
        self.play(FadeOut(VGroup(browser, server, pub1, pub2, pub1_label, pub2_label, ecdh, shared, hkdf, session)))


class SSTVTextChunk(Narrated):
    """呼应 s03：封面图正常显示，但辅助 tEXt 块携带了音频密文。"""

    def construct(self):
        image = block("封面图\n正常显示", 2.8, ACCENT, 24, 1.45).move_to([-4.1, 1.2, 0])
        arrow = arrow_between(image, block("PNG chunks", 2.0, MUTED, 22))
        chunks = VGroup(
            block("IHDR", 1.15, ACCENT, 20),
            block("IDAT", 1.15, MUTED, 20),
            block("tEXt", 1.15, GOLD, 20),
            block("IEND", 1.15, MUTED, 20),
        ).arrange(RIGHT, buff=0.12).move_to([0.7, 1.2, 0])
        arrow2 = Arrow(chunks[2].get_bottom(), [0.7, -0.05, 0], color=GOLD, stroke_width=2)
        payload = block("Comment…\n音频密文", 2.6, CIPHER, 23, 1.0).move_to([0.7, -0.8, 0])
        self.say("服务器返回的封面图可以正常显示，因为 tEXt 是合法的 PNG 辅助块")
        self.play(FadeIn(image), FadeIn(chunks), Create(arrow2), FadeIn(payload, shift=DOWN * 0.15))
        self.wait(1.0)
        self.say("页面脚本遍历 PNG，在 tEXt 块里收集 Comment 开头的内容")
        self.play(Indicate(chunks[2], color=GOLD, scale_factor=1.15), Indicate(payload, color=CIPHER))

        key = block("会话密钥", 2.2, OK, 23).move_to([-2.0, -0.8, 0])
        decrypt = chip("AES-GCM 解密", OK, 24).move_to([-2.0, -1.75, 0])
        self.play(FadeIn(key), GrowArrow(Arrow(key.get_right(), payload.get_left(), color=OK, stroke_width=2)), FadeIn(decrypt, shift=UP * 0.15))
        self.say("只有刚刚协商出的会话密钥，才能解开这段音频密文", wait=1.8)
        self.hush()
        self.play(FadeOut(VGroup(image, chunks, arrow2, payload, key, decrypt)))


class SSTVAudioCapture(Narrated):
    """从 AES-GCM 明文到 AudioContext：指出可截获的音频边界。"""

    def construct(self):
        encrypted = block("PNG tEXt\n密文", 2.0, CIPHER, 23, 1.0).move_to([-5.0, 0.95, 0])
        key = block("会话密钥", 2.0, GOLD, 23).move_to([-5.0, -0.5, 0])
        aes = block("AES-GCM", 2.0, OK, 24).move_to([-2.25, 0.5, 0])
        pcm = block("解密后的音频\nPCM / WAV", 2.8, OK, 23, 1.0).move_to([0.8, 0.5, 0])
        decode = block("decodeAudioData", 3.0, ACCENT, 23).move_to([4.25, 0.5, 0])
        player = chip("AudioBuffer → 播放", ACCENT, 24).move_to([4.25, -0.85, 0])

        self.say("音频密文和会话密钥一起进入 AES-GCM")
        self.play(FadeIn(encrypted), FadeIn(key), FadeIn(aes), GrowArrow(Arrow(encrypted.get_right(), aes.get_left(), color=CIPHER, stroke_width=2)), GrowArrow(Arrow(key.get_right(), aes.get_left() + DOWN * 0.25, color=GOLD, stroke_width=2)))
        self.say("解密完成后，得到真正的 PCM / WAV 字节流")
        self.play(FadeIn(pcm), GrowArrow(Arrow(aes.get_right(), pcm.get_left(), color=OK, stroke_width=2)))
        self.say("最后交给浏览器的 decodeAudioData，才变成可以播放的 AudioBuffer")
        self.play(FadeIn(decode), GrowArrow(Arrow(pcm.get_right(), decode.get_left(), color=ACCENT, stroke_width=2)), FadeIn(player, shift=UP * 0.15))

        # 「截获点」原本右上角压在 player 芯片左下角；下移 0.55、左移到 player 外框左侧，
        # 与 player 留出 ≥0.3 的间隙。箭头从芯片顶部指向 decodeAudioData 的左侧，避开 player。
        # 下移后与底部的 duration 会相压，duration 一并下移让位。
        capture = chip("截获点", GOLD, 23).move_to([2.4, -1.8, 0])
        capture_arrow = Arrow(capture.get_top(), decode.get_left(), color=GOLD, stroke_width=2)
        duration = mono(f"真实音频：44.1 kHz · 单声道 · {AUDIO_SECONDS:.3f} s", 23).set_color(MUTED).move_to([0, -2.5, 0])
        self.play(FadeIn(capture), GrowArrow(capture_arrow), FadeIn(duration))
        self.say("所以最稳妥的抓取位置，是解密后的 decodeAudioData 输入", wait=2)
        self.hush()
        self.play(FadeOut(VGroup(encrypted, key, aes, pcm, decode, player, capture, capture_arrow, duration)))
