<!-- markdownlint-disable MD033 MD041 -->

<div align="center">

# Phigros 第九章「穹顶孤舟」ARG 纪实

</div>

## 前言

待完善。

## Stage I（9 月 5 日起）

[\@Phigros官方](https://space.bilibili.com/414149787/) 在 9 月 5 日晚间的 Phigros 七周年直播中公开了第九章的 PV，并于 9 月 7 日 21 时在哔哩哔哩平台发布了视频[【Phigros】4.0.0 主线第九章更新曲目预览](https://www.bilibili.com/video/BV16vbN6REhD/)。

![【Phigros】4.0.0 主线第九章更新曲目预览 的视频封面](/assets/stage_i/cover.jpg)

视频的简介如下：

> Phigros主线最终章——第九章【穹顶孤舟】将于2026年9月25日更新。
>
> 第九章的新曲目分别是：<br/>
>「Implexrough」 by: Silentroom × mommy<br/>
>「Evanescent」 by: LeaF<br/>
>「About The Universe」 by: SOTUI & MIssionary<br/>
>「?」ZGJGDGTDNUIOSQQCLIWWCWIIADNOFQDAEMG<br/>
>「?」left: A - Z. right: PSZLMYQEBJARTFCHNUGVKDOXIW<br/>
>「?」Lmob Xszlh xzm hszggvi gsv nriztv gszg koztfvh gsv rtmlizmg Ullo.
>
> 视频制作：Pigeon Animation Team (汉堡、AiLANE、海产)

对于简介「？」的前 2 行，注意到其使用了 Chaocipher（混沌密码），将第 1 行作密文，第 2 行作 left disk 和 right disk 的字母表，解密得到

> WERJETZTALLEINISTWIRDESLANGEBLEIBEN

分词后得到一串德语 „Wer jetzt allein ist, wird es lange bleiben“，意为「如今独自一人的人，将长久如此」。这句出自奥地利诗人 *Rainer Maria Rilke*（里尔克）的诗 [*Herbsttag*（《秋日》）](https://de.wikipedia.org/wiki/Herbsttag)。

而对于简介「？」的第 3 行，注意到使用了 Atbash Cipher（Atbash 密码），解密后可以得到：

> Only Chaos can shatter the mirage that plagues the ignorant Fool.

意为「唯有混沌，才能击碎那困扰无知愚者的幻象。」

同时，在该视频的 1:19 起、1:28 起、1:39 起分别出现了黑白色的三首隐藏曲的 PV。其中：

- 1:19 起，视频左上角显示「SIG : MIRAGE」，右上角显示「CH-7」，下方显示「FVB TBZA NV IF H DHF DOPJO PZ AOL DHF VM PNUVYHUJL」；
- 1:28 起，视频左上角显示「SIG : CHAOS」，右上角显示「CH-7」，下方显示「FVB TBZA NV IF H DHF DOPJO PZ AOL DHF VM PNUVYHUJL」；
- 1:39 起，视频左上角显示「SIG : TRUTH」，右上角显示「CH-3」，下方显示「BRX PXVW JR WKURXJK WKH ZDB LQ ZKLFK BRX DUH QRW」。

不难注意到这是 Caesar Cipher（凯撒密码），偏移量即 `CH-?` 中的数字。反向偏移后可以得到明文：

> YOU MUST GO BY A WAY WHICH IS THE WAY OF IGNORANCE<br/>
> YOU MUST GO BY THE WAY OF DISPOSSESSION<br/>
> YOU MUST GO THROUGH THE WAY IN WHICH YOU ARE NOT

意为：

> 你必须经由无知之途。<br/>
> 你必须经由舍弃占有之途。<br/>
> 你必须经由你并不存在之途。

这三句均出自 [T. S. Eliot（托马斯·斯特恩斯·艾略特）](https://en.wikipedia.org/wiki/T._S._Eliot)的诗 [*East Coker*（《东科克》）](https://en.wikipedia.org/wiki/East_Coker_(poem))，是其诗集 [*Four Quartets*《四个四重奏》](https://en.wikipedia.org/wiki/Four_Quartets) 的第二篇。

在视频公开的同时，D.O.M.E. 在林泊百科[「谜题保管所:孤舟」](https://wiki.pigeon-games.com/index.php?title=%E8%B0%9C%E9%A2%98%E4%BF%9D%E7%AE%A1%E6%89%80:%E5%AD%A4%E8%88%9F)中添加内容「Solivault」：

![林泊百科「谜题保管所:孤舟」](/assets/stage_i/solivault_limbo.png)

根据提示，经过尝试，将解谜得到的字符串 `WERJETZTALLEINISTWIRDESLANGEBLEIBEN` 拼接到林泊百科的 URL `https://wiki.pigeon-games.com` 之后，即

```text
https://wiki.pigeon-games.com/WERJETZTALLEINISTWIRDESLANGEBLEIBEN
```

访问这个页面，我们得到了一张名为 `Solivault` 的 `.png` 图片，随后这一解密进展被 D.O.M.E. 认可，D.O.M.E. 在林泊百科的「谜题保管所:孤舟」页面追加了解谜答案，并附

> 不要就此结束念想，你们还会回来的。

![Solivault.png](/assets/stage_i/Solivault.png)

页面的图片中隐约包含两个角色，其上半部分做了黑暗处理。查看该页面的 HTML 源码，我们发现了这样的 JavaScript 逻辑：

```javascript
const stage = document.getElementById('stage');

stage.addEventListener('click', () => {
  if (document.fullscreenElement) {
    document.exitFullscreen().catch(() => {});
  } else {
    document.documentElement.requestFullscreen().catch(() => {});
  }
});

stage.addEventListener('dblclick', (e) => {
  e.preventDefault();
  stage.classList.toggle('contain');
});
```

这使得页面能够响应用户的点击请求，在单击时，页面进入或退出全屏；在双击时，页面切换 `#stage` 的 `contain` 类，从而改变图片的 `object-fit`。但这也间接导致图片无法被拖拽或长按选择，常规方法难以保存。同时，访问该 URL 必须携带正确的 User-Agent，否则页面将返回错误码 HTTP 773。

![HTTP 773 错误](/assets/stage_i/http_773.png)

不难获得图片的来源地址：

```text
https://ch9.oss-cn-beijing.aliyuncs.com/Solivault.png
```

图片存放于阿里云的 OSS，且进行了防盗链处理，会对 Referer 非 `https://wiki.pigeon-games.com/` 的请求返回 403。图片的 `Last-Modified` 时间为 2026 年 9 月 10 日 18:21 CST，大小为 2,160,381 字节，约 2.06 MiB。第一部分的解谜到此结束。

另外，此时已经有玩家发现视频中「SIG : TRUTH」段的 BGM 疑似是 *816ThreeNumbers* 的歌曲 *True Home, True World*，但并没有确证。

## Stage II（9 月 25 日起）

### 第一部分歌曲解锁

### 对游戏本体的分析

在完成 2 首表魔王曲的解锁后，我们于「穹顶孤舟」的地图向上滑动，发现了一个闪烁的隐藏曲目占位符，点击后弹出「ACCESS DENIED」界面，显示

> 访问被拒绝 需要通行密钥来继续

同时，下方提供一个输入框可供输入通行密钥（PASSCODE）。玩家几乎尝试了绝大多数可能的密钥，均不能成功解密。事实上，这个密钥必须通过 [林泊百科的解密](#林泊百科的解密) 获得——有解包者尝试分析了游戏本体，并确认了这一点。

![隐藏曲目弹出的「ACCESS DENIED」界面](assets/stage_ii/phigros_4.0.0_analysis/access_denied.jpg)

> [!WARNING]
>
> 根据[《Phigros》同人创作及第三方项目规范（2026版）](https://www.bilibili.com/opus/1243010548197490696) 的「第六条 程序、资源、数据与网络服务」的相关规定，下文中的内容仅作为对该 ARG 解谜过程中玩家的一种解谜思路的记录。笔者遵守 Phigros 官方的规范，同时也不鼓励对游戏本体进行逆向工程等的行为。下文中所记录的内容经过了一定的混淆和修改。
>
> > 未经授权，不得提取、复制、上传、公开传播、重新打包、销售、交换或向第三方提供《Phigros》的游戏程序、资源文件、未公开数据及其他受保护内容。
> >
> > 不得以获取或传播游戏资源、复制游戏程序、制作替代性产品、提供作弊功能或实施其他侵害合法权益的行为为目的，通过拆包、破解、反编译、绕过技术保护措施、截取非公开通信、攻击或干扰网络服务、非法获取数据等方式，取得、还原或使用前述内容。

<details>
<summary>「ACCESS DENIED」页面的实际解密流程</summary>

「ACCESS DENIED」页面要求玩家输入正确的通行密钥（PASSCODE），在回车确认后，程序调用函数 `Submit`，取输入框 `inputField` 的值，校验其长度大于 0 后，将原始值直接传给 `SetPassword` 函数。函数对传入的值 `password` 计算 SHA-512 哈希（共 64 字节），切片其 `0..32` 的 32 字节作为 `aes.Key`、`32..48` 的 16 字节作为 `aes.IV`，并使用这对 AES 密钥尝试通过 Addressables 异步加载加密的 Unity bundle，确认回调函数 `b__6_0` 的校验情况。这里，回调函数 `b__6_0` 使用用户输入的密钥尝试解密名为 `c9s.test` 的 `TextAsset` 类型的加密资源，通过判断其值是否等于 `pass` 以校验用户输入的密钥是否正确。

若正确，则程序最终调用 `Decrypt` 函数解密出最后的游戏资源。
</details>

由于隐藏曲使用了 AES 加密，在没有密钥的情况下，加密的文件密码学上不能恢复。这也是为什么解包者不能通过单纯的解包获得隐藏曲目。

在后文我们得到了密钥后，可以复现这一解密过程。在解密后的文件中，我们得到了一段 68.5 s 的 `.wav` 文件，来自于 *816ThreeNumbers* 的歌曲 *True Home, True World*，印证了前文的猜想。这也说明了，在 Phigros 4.0.0 的游戏本体中，隐藏曲仅包含了前 68.5 s 的音频，并不包含完整曲目。

### 林泊百科的解密

玩家再次访问先前的林泊百科页 [WERJETZTALLEINISTWIRDESLANGEBLEIBEN](https://wiki.pigeon-games.com/WERJETZTALLEINISTWIRDESLANGEBLEIBEN) 后，可以发现该页面内容已经发生改变，背景是一张扭曲过后的星体图片，上方浮现了一个为期 7 天的倒计时。

![林泊百科页面 WER... 的截图](/assets/stage_ii/limbo_wiki/countdown_site.png)

archive.org 保留了一份 2026 年 9 月 25 日晚 7 点的 [网页快照](https://web.archive.org/web/20260925113526/https://wiki.pigeon-games.com/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/)。

#### WERJETZTALLEINISTWIRDESLANGEBLEIBEN

分析 [该页面的 HTML 源码](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/WERJETZTALLEINISTWIRDESLANGEBLEIBEN.html) 可知，页面倒计时的截止时间是 2026-10-02 17:00:00，页面先用内嵌的时间戳 `window.SV_EMBED_MS` 初始化时钟，然后尝试从 `ntp.php`、`timeapi.io` 和 Cloudflare `cdn-cgi/trace` 获取网络时间，同步之后每 10 分钟再同步一次。

页面从 `https://c9.gaoice.run/start.png` 加载背景图，随后用多个 canvas 分层渲染像素位移、红雾、噪点、火花粒子、CRT 扫描线、暗角、红蓝色差、畸变等。页面固定按照 1920x1080 设计，再用 CSS 缩放到当前屏幕。在移动端打开时，倒计时会竖排显示。

我们注意到该 HTML 的第 10 行和第 199 行分别有两个 `<script>` 块，其 JavaScript 代码进行了混淆。使用 [toolapi 的 JavaScript 反混淆器](https://www.toolapi.cc/jsreverse/) 可以反混淆这些代码，反混淆后的代码参见 [L10.js](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/L10.js) 和 [L199.js](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/L199.js)。

其中，第 199 行的代码是用来渲染页面效果的；而第 10 行的代码包含了这样的逻辑：脚本从 `c9.gaoice.run` 加载背景图后，通过

```javascript
if (
    a.length < 8 ||
    a[0] !== 137 ||
    a[1] !== 80 ||
    a[2] !== 78 ||
    a[3] !== 71
) {
    return 0;
}
```

校验 PNG 的魔数 `0x89 'P' 'N' 'G'`，之后通过

```javascript
let b = 8;
while (b + 8 <= a.length) {
    const c =
        ((a[b] << 24) | (a[b + 1] << 16) | (a[b + 2] << 8) | a[b + 3]) >>>
        0;
    const d = String.fromCharCode(a[b + 4], a[b + 5], a[b + 6], a[b + 7]);
    b += 12 + c;
    if (b > a.length) {
        return 0;
    }
    if (d === "IEND") {
        return b;
    }
}
```

遍历 PNG chunk，直到到达照片的 `IEND` 块后返回值，返回的即为第二张 PNG 的起始偏移。随后

```javascript
const f = URL.createObjectURL(
    new Blob([e.subarray(c(e))], {
        type: "image/png",
    }),
);
```

脚本截取第二个 PNG 起点到文件末尾的数据，取为 `"image/png"` 的 blob，并调用 `createObjectURL` 生成临时 `ObjectURL`。之后的 JavaScript 代码加载了第二张 PNG 作为 `bgImg.src`，即在页面上显示第二张 PNG；如果解析失败，则回滚到第一张 PNG。

我们下载得到 [`start.png`](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.png)，随后使用 `binwalk -a start.png` 确证 `start.png` 的确由两张图片合成，使用 `dd` 或脚本提取得到空间位置上前后的两张图片 `start.layer1.png` 和 `start.layer2.png`。WER... 页面上渲染的是 `start.layer2.png`。

![对 start.png 的 binwalk 结果](/assets/stage_ii/limbo_wiki/binwalk_start.png)

这是 `start.layer1.png`：

![start.layer1.png](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer1.png)

这是 `start.layer2.png`：

![start.layer2.png](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer2.png)

编写 Python 脚本，取两张照片的 diff，可以注意到两张照片的差异几乎 100% 集中在单个像素级的抖动上，低频内容（也就是「照片本身」）是同一张。脚本存放于 [diff_layers.py](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/diff_layers.py)。

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

from PIL import Image, ImageChops

here = Path(__file__).parent
l1, l2 = here / "start.layer1.png", here / "start.layer2.png"
a_path, b_path = ([Path(p) for p in sys.argv[1:3]] + [l1, l2])[:2]

a, b = (Image.open(p).convert("RGB") for p in (a_path, b_path))

ImageChops.difference(a, b).point(lambda v: min(255, v * 8)).save(
    here / "start.diff_x8.png"
)
```

![两张照片的 diff](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.diff_x8.png)

同时，用肉眼观察 `start.layer1.png`，我们也可以发现图片有细微而连续的波动，在四个角落尤其明显。这暗示我们需要对图片进行二维 Fourier 变换。

一般地，人们看一张图片，是按照像素坐标 $(x, y)$ 来看的，这是空域（Spatial Domain）。而 Fourier 变换会将一张图片拆解为无数个不同方向、不同波长（频率）、不同强度的正弦波纹理叠加，这就切换到了频域（Frequency Domain）。一张图片的低频部分通常是大片平滑渐变的背景、整体的明暗轮廓；而高频部分则通常是物体的边缘、文字轮廓、细碎的杂色和噪点等。

我们对 `start.layer1.png` 编写二维 Fourier 变换脚本：

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

here = Path(__file__).parent
p = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "start.layer1.png"

a = np.asarray(Image.open(p).convert("L"), dtype=float)
m = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(a))))
m = (255 * (m - m.min()) / (m.max() - m.min())).astype("uint8")
out = here / f"{p.stem}.fft.png"
Image.fromarray(m).save(out)
print(f"{p.name} {a.shape[1]}x{a.shape[0]} → {out.name}")
```

该脚本存放于 [fft_view.py](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/fft_view.py)。脚本读入图片并转为灰度图（L 模式），并转成 float 数组，随后对其作 2D 快速 Fourier 变换、中心化和对数压缩动态范围，归一化到 0\~255 并转成 8 位无符号整数，最终输出为 PNG 图片。这里：

1. `fft2` 计算出的结果默认将零频（直流分量，即图片的平均亮度）放在了数组的四个角落。默认情况下，低频在四个角落会使得输出的图片散乱。我们使用 `fftshift` 做一次象限对调，将零频移动到了图像的正中心，这样画出的频谱图将呈现出中心对称，使人能更容易看出隐藏的信息。
2. 最后，我们对输出作 `np.log1p(...)`，这即 $\ln(1 + x)$，它对输出做了一次动态范围对数压缩，将微弱的细节提亮，显露出隐藏在频域中的图案；随后再做一次线性归一化，将幅值映射到 $[0, 255]$ 并转成 8 位无符号整数，以便保存为 PNG 图片。

处理后我们得到了 `start.layer1.fft.png`：

![对 layer1 的 FFT](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer1.fft.png)

截取上半部分的隐藏信息，我们得到：

![对 layer 1 FFT 的截取](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer1.fft.band.png)

字符串 `outside_the_birdcage`。

事实上，更好的做法是对 diff 图片作二维 Fourier 变换。由于 `layer1` 图片是由

1. `layer2` 图片，作为底图；
2. `diff` 图片，是 ARG 出题人隐写字符串的图片

叠加而来，所以对 `diff` 图片作 Fourier 变换可使得得到的隐藏信息更加清晰。该脚本位于 [fft_view_diff.py](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/fft_view_diff.py)，得到的结果如下：

![对 diff 的 FFT](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer1-start.layer2.fft.png)

![对 diff FFT 的截取](/artifacts/stage_ii/WERJETZTALLEINISTWIRDESLANGEBLEIBEN/start.layer1-start.layer2.fft.band.png)

#### outside_the_birdcage

将 `outside_the_birdcage` 拼接到 `https://wiki.pigeon-games.com` 之后，访问得到了新的页面，一个格状背景图上方显示了一串字符串。

![outside_the_birdcage 网页截图](/assets/stage_ii/limbo_wiki/outside_the_birdcage.png)

下载该页面的 HTML，在 `<meta>` 块中，我们得到了鸽游官方的提示：

```html
<meta name="hint" content="To our non-Chinese players: during our review, we found an information gap between mainland China and overseas that may leave you stuck on the puzzles. 
If you've made it this far but have no idea how to proceed, visit Bilibili and browse the Phigros official account's past posts. Earlier puzzles may give you the inspiration you need.">
```

> 对于非中文的玩家：审查期间，我们发现中国大陆的玩家和海外玩家之间存在信息差，可能会让你们卡在谜题上。<br/>
> 如果走到这一步，但你不知道怎么办，可以去哔哩哔哩上看 Phigros 官方的历史投稿，早期的谜题或许会给你灵感。

并在后文中得到了一个 [JavaScript 脚本](/artifacts/stage_ii/outside_the_birdcage/711f2f61b954952722263a03-text.js)。分析后发现，该脚本的 `fingerprint()` 函数收集了大量的浏览器和环境信息，包括 User-Agent、语言、平台、硬件并发数、设备内存、触摸点数、屏幕尺寸、色彩深度、`devicePixelRatio`、时区、`Intl` 时区、Canvas 绘制文字后的 `toDataURL()` 尾部、WebGL 的 vendor/renderer 信息等，最后将这些内容拼成一个字符串，用不同的 seed 做四次 FNV 哈希（`fnv(str, seed)`），拼成 32 位十六进制字符串（`hex8(n)`）。

随后，网页从服务器同步文本：`syncFromServer()` 使用上面计算得到的指纹请求同源接口 `api.php?fp=<fingerprint>`，解析其得到的 JSON 并显示响应传回的字符串。例如，我们打开 F12 开发人员工具的 Network 标签页，可以看到一次请求：

![F12 开发人员工具中的响应](/assets/stage_ii/limbo_wiki/outside_the_birdcage_network.png)

这次对 `api.php` 的请求得到了响应

```json
{"ok":true,"index":12,"text":"1$R&fuH6AbuN","total":13}
```

其中的 `text` 就显示在了页面上。这里，`"index":12` 表明这是第 12 个字符串。经过玩家的枚举尝试，最终得到了 13 个字符串，经过 `sort` 排列后得到

```text
$6&Dj#f=6T+I
1$R&fuH6AbuN
ALes@K3@MtmE
?aT?~!4*jK^D
C4_tubAxU+/S
E&r%JaM/9_,I
G#TroCyuuH#P
IV7aN2emf9nS
N2riNdAuY~US
Nf9etodigrAO
OU/@ig=!9~VS
R#m6Aya#N=$S
u~D4wBeN3i_O
```

我们注意到，这 13 个字符串的末尾均为大写字母；`rev | sort` 后得到 7 个不重复的字母 `D`, `E`, `I`, `N`, `O`, `P`, `S`。注意到这 13 个尾字母恰好可以构成单词 `DISPOSSESSION`，我们在前文的 [Stage I](#stage-i9-月-5-日起) 中获得过这个单词——但由于有重复字母，顺序不能被唯一确定。再次注意到 13 个字符串的开头，共出现了 12 个不重复的字母：`$`, `1`, `A`, `?`, `C`, `E`, `G`, `I`, `N`, `O`, `R`, `u`，其中的大写字母恰好可以构成单词 `IGNORANCE`，我们按照这样的顺序排列 13 个字符串，最终得到了矩阵

```text
?aT?~!4*jK^D
$6&Dj#f=6T+I
IV7aN2emf9nS
G#TroCyuuH#P
Nf9etodigrAO
OU/@ig=!9~VS
R#m6Aya#N=$S
ALes@K3@MtmE
N2riNdAuY~US
C4_tubAxU+/S
E&r%JaM/9_,I
u~D4wBeN3i_O
1$R&fuH6AbuN
```

另一边，我们提取出该网页的背景图

```text
https://c9.gaoice.run/background-7-7.png
```

![background-7-7.png 背景图](/artifacts/stage_ii/outside_the_birdcage/background-7-7.png)

注意到背景图由若干三角形构成，多数三角形内皆无其他内容，为空三角形：

![空三角形](/assets/stage_ii/limbo_wiki/empty_triangle.png)

但存在这样的三角形，其中大的三角形内有一个略小的三角形描边，且三角形的中间位置还有小的实心三角形。这样的三角形共有 4 个，下面的这张图片展示了其中 2 个。图片拉高了 Gamma 值，使得这样的三角形更加清晰，这 2 个三角形位于图片的左侧和右侧：

![不同的三角形](/assets/stage_ii/limbo_wiki/filled_triangle.png)

为了使得图片更加清晰，我们可以对图片进行简要处理。使用下面的脚本：

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

here = Path(__file__).parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "background-7-7.png"
dst = (
    Path(sys.argv[2])
    if len(sys.argv) > 2
    else src.with_name(src.stem + "_enhanced.png")
)

im = Image.open(src).convert("RGB")
g = im.convert("L")
res = np.asarray(g, float) - np.asarray(
    g.filter(ImageFilter.GaussianBlur(6)), float
)  # 细节层（高通）
base = 255.0 * (np.asarray(im, float) / 255.0) ** (1 / 2.4)  # gamma 提亮中间调
w = np.exp(-np.abs(res) / 18.0)  # 强网格线权重小
out = np.clip(base + 6.0 * res[..., None] * w[..., None], 0, 255).astype("uint8")
Image.fromarray(out).save(dst)
print(f"{src.name} → {dst.name}")
```

脚本首先对图片进行高反差保留（High-Pass Filter），在原图基础上减去其半径为 6 的 Gauss 模糊，剔除了大面积平缓的渐变背景，只保留了白色的网格线和藏在暗处的微弱轮廓；紧接着，对图片进行 Gamma 校正，使用非线性提亮显现出原先暗蓝的背景；最终，脚本抑制了图片中的强线条。脚本使用负指数衰减函数

$$
e^{-\mid x \mid / \sigma}
$$

做权重分配，并将微弱的细节放大 6 倍后叠加在底图上，将像素截断在 $[0, 255]$ 内。最终得到了增强图片：

![background-7-7 增强图片](/artifacts/stage_ii/outside_the_birdcage/background-7-7_enhanced.png)

脚本位于 [enhance_background.py](/artifacts/stage_ii/outside_the_birdcage/enhance_background.py)。

考虑将上文中得到的 13 个字符串叠加在这张增强图片上。这里我们使用 Figma 完成，设置字体为 Cascadia Code 或其他等宽字体即可。对于 Cascadia Code：设置 Font Size 为 55、Line Height 为 Auto、Letter Spacing 为 148%。居中放置，即可使得字符大致位于三角形内。

![使用 Figma 完成叠加](/assets/stage_ii/limbo_wiki/figma.png)

将内含元素的四个三角形标注出来后，对每个三角形，分别作为六边形右上角的 1/6，向左下角绘制出整个六边形。随后，顺时针读取六边形中的 6 个字母，`sort` 后得到

```text
Cogito
fugium
sit_re
,_ubi_
```

这四个字符串可以拼接成

```text
Cogito,_ubi_sit_refugium
```

这是一句拉丁文，意为

> 我思，避难所何在？

拼接到 `https://wiki.pigeon-games.com/` 后，进入下一步解谜。

#### Cogito,_ubi_sit_refugium

访问页面，注意到页面上显示了一句话

> Technology can expand the boundaries of humanity,‌​​‍​​‍​​​‍‌‌‌‍​‌​‍​​‍​‍‌​‍‌‍​‌‍‌‍​​‍‌‌‌‍‌​  it can also fabricate the semblance of reality.

意为

> 科技可以拓展人类的疆界，但也能捏造出以假乱真的现实。

![Cogito 页面截图](/assets/stage_ii/limbo_wiki/cogito.png)

点击这句话可以复制到剪贴板。注意到页面上的两句话中间有间隔；事实上，这段文本隐写了 Unicode 零宽字符：在终端内粘贴这段文本便可以看到这些隐藏的字符，使用 `xxd` 也可以确证这一点。

![页面上的文本含有零宽字符](/assets/stage_ii/limbo_wiki/unicode-zero-width.png)

这段隐写包括三种字符：`U+200B` ZERO WIDTH SPACE、`U+200C` ZERO WIDTH NON-JOINER 和 `U+200D` ZERO WIDTH JOINER。不过与一般 Misc 题目的思路不同，这段隐写中的零宽字符解码后并不是纯文本。我们再次注意到该页面的标题

```text
.Bravo _Charlie ␣Delta
```

页面提示我们将 `U+200B`（`Bravo`）对应给 `.`，同理，将 `U+200C`（`Charlie`）和 `U+200D`（`Delta`）对应给 `_` 和 ` `（空格），这即提示我们使用 Morse 电码。转换那一段零宽字符，我们得到：

```text
-.. .. ... --- .-. .. . -. - .- - .. --- -.
```

解码后得到：

```text
DISORIENTATION
```

意为「迷失方向」。拼接后进行下一步解谜。

#### DISORIENTATION

访问该页面，得到一句话：

> In what sense, exactly,​‌‍​‌​‍‌‌‌‍​​‌‍​​​‍​‌‍​‌​​ do we "truly" inhabit the "world"?

意为

> 确切地说，在什么意义上，我们究竟才算是「真正地」栖居于「世界」之中？

![DISORIENTATION 页面截图](/assets/stage_ii/limbo_wiki/disorientation.png)

这段话中仍然存在零宽字符，仿照上例解谜后得到

```text
AROUSAL
```

意为「唤醒、激发、被唤起、被触动」。注意到页面的标题为 `nihilist`，这暗示我们使用 Nihilist Cipher（虚无主义密码）。下载该页面的 [HTML 源码](/artifacts/stage_ii/DISORIENTATION/DISORIENTATION.html)，在 `<meta>` 块中得到一串数字

```html
<meta name=" " content="56 75 65 76 35 56 75 63 97 66 67 47 72">
```

这串数字应当为 Nihilist Cipher 的密文。Nihilist Cipher 的密码表 Polybius 方阵是 $5 \times 5$ 的，即需要 $25$ 个字符。注意到 HTML 源码中 L63 的提示

> hint1: This hint has been destroyed by Chaos

意为

> 提示 1：这条提示被混沌（Chaos）摧毁

我们联想到 [Stage I 中 Chaocipher 的右表](#stage-i9-月-5-日起)

```text
PSZLMYQEBJARTFCHNUGVKDOXIW
```

但右表共 26 个字符，不能被全部填充进 Polybius 方阵（波利比奥斯方阵）。按照密码学的惯例操作，在这里，我们删除该字符串的倒数第二个字母 `I`。

事实上，在古罗马时期的拉丁字母中，原先并没有字母 `J`，它只是 `I` 的一种书写变体；直到文艺复兴后，`J` 才被正式拆分为独立字母。因此，在密码学的历史中，将 `I` 和 `J` 合并为同一个字母，或删去其中之一，是非常常见的操作。历史上所有基于 $5 \times 5$ 方阵的经典密码——如 Playfair Cipher（波雷费密码）、ADFGX Cipher、以及纯 Polybius 密码（波利比奥斯密码）等，全部都默认把 `I` 和 `J` 合并或省略一个。

如此操作我们得到了

```text
PSZLMYQEBJARTFCHNUGVKDOXW
```

将这串字符串行主序地置入 Polybius 方阵中，得到

| | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 1 | `P` | `S` | `Z` | `L` | `M` |
| 2 | `Y` | `Q` | `E` | `B` | `J` |
| 3 | `A` | `R` | `T` | `F` | `C` |
| 4 | `H` | `N` | `U` | `G` | `V` |
| 5 | `K` | `D` | `O` | `X` | `W` |

使用一个 [在线的 Nihilist Cipher 解密工具](https://converterfu.com/zh/cipher/nihilist/)，以密钥 `AROUSAL` 和上面的 Polybius 方阵解密 `<meta>` 块中的密文，我们得到了

```text
JUSTEJ✗R✗ZBCH
```

其中 `✗` 表明坐标越界。这显然不正确；再次注意到 HTML 源码 L222 的提示

> hint2: What elements you have obtained cannot be directly used. Observe encryption rules and remove any interference from them

意为：

> 提示 2：你所得到的元素并不能直接使用。观察加密规则，并移除全部干扰

我们考虑移除密钥中的第二个 `A`，密钥即作 `AROUSL`。再次解密后，得到了

```text
JUSTENGAGEWTH
```

这即 `JUSTENGAGEWITH`（just engage with）去掉字母 `I` 的结果。我们也可以自写 [Python 脚本](/artifacts/stage_ii/DISORIENTATION/nihilist.py) 复现 Nihilist Cipher 的解密。

```python
sq = "PSZLMYQEBJARTFCHNUGVKDOXW"
pos = {c: (i // 5 + 1, i % 5 + 1) for i, c in enumerate(sq)}
rev = {v: k for k, v in pos.items()}
ct = [56, 75, 65, 76, 35, 56, 75, 63, 97, 66, 67, 47, 72]
ks = [10 * pos[c][0] + pos[c][1] for c in "AROUSL"]
print("".join(rev[divmod(n - ks[i % len(ks)], 10)] for i, n in enumerate(ct)))
```

拼接后继续。

#### JUSTENGAGEWTH

访问页面，得到一句话：

> This is not something you were meant to know. It is, in truth, something you have known all along.

意为

> 这不是你本该知道的事。事实上，这是你一直以来就知道的事。

![JUSTENGAGEWTH 页面截图](/assets/stage_ii/limbo_wiki/justengagewth.png)

尝试点击页面中间的文本进行复制，但我们注意到，复制得到的文本并非显示的文本。

下载 [HTML 源码](/artifacts/stage_ii/JUSTENGAGEWTH/JUSTENGAGEWTH.html)，查看得到其中的第 2 行

```html
<!-- hint:just need 1 step -->
```

这暗示我们，这是解谜的最后一步。继续分析该 HTML 源码。页面中间的文本绑定了点击、回车和空格事件，触发后，页面使用 `handleCopy()` 将一个内容写入剪贴板，该内容优先使用本地变量 `pendingCopy`，初始值为 `eXcU`，该值会使用 `decodeCopy()` 函数解密。`decodeCopy()` 函数对密文进行了这样的操作：首先使用 URL-safe 的 Base64 解码；随后逐字节与 `0x37 + (i % 29)` 做 XOR；最后用 UTF-8 解码成字符串。

初始值的解密结果为

```text
NO-
```

不过，页面在加载时，`syncFromServer()` 就已经进行了一次，它会使用服务器下发的 `c` 重新赋值 `pendingCopy`，所以实际上第一次点击拿到的大概率已经是服务器版本。

`syncFromServer()` 在页面加载时调用 `api.php?fp=<fp>` 获得 JSON 响应体 `{ok, index, text, c, total}`，并在返回的 `text` 与页面上显示文本不同时替换掉页面上的内容，同时将 `pendingCopy` 的值设置为 `c`。在玩家点击文本时，`pendingCopy` 已经被使用并清空，页面则从 `api.php?act=copy&fp=<fp>` 获取一份 `c`。

`handleCopy()` 在复制时取 `pendingCopy` 的值，写入剪贴板成功后立刻清空；若 `pendingCopy` 本为空，就现取一份值，解密后写入剪贴板。

服务器端会随机返回 5 个 `c`。可以编写脚本穷举，也可以连续复制获得。解密后，可得内容分别为

| 密文 | 明文 |
| --- | --- |
| `eXcU` | `NO-` |
| `Gmt2` | `-SO` |
| `axdlFWcT` | `\/\/\/` |
| `RVdOABsIAh4Kfw` | `row: 4? 5?` |
| `Q0pAGl1TTx5GLzQwMCEpIA` | `try for yourself` |

可以使用这个 Python 片段复现解密过程，传入 `s` 为加密内容即可。

```python
import base64
def decode_copy(s):
    t = s.replace('-', '+').replace('_', '/'); t += '=' * (-len(t) % 4)
    b = base64.b64decode(t)
    return bytes(x ^ (0x37 + i % 29) for i, x in enumerate(b)).decode('utf-8')
```

解得结果后，注意到页面标题为 `Fence?`，且解密得到的一个明文为 `\/\/\/`，这暗示我们使用 Fence Cipher（栅栏密码）。注意到 `NO-` 和 `-SO` 暗示了栅栏的两端，我们使用 [outside_the_birdcage](#outside_the_birdcage) 中已有的矩阵，注意到矩阵的第一列和最后一列出现了（从上到下的）`NO` 和 `OS`（两个字母分别出现在第 5 行和第 6 行），`NO` 与 `NO-` 同向，而 `OS` 与 `SO-` 反向，所以该栅栏应当在 `NO` 侧自上而下，在 `OS` 侧自下而上。自然地，我们用箭头连接 `N` 所在三角形的左上角顶点和 `O` 所在三角形的右下角顶点。注意到明文 `row: 4? 5?`，这暗示我们「行的数量」是 4 或 5，我们考虑让箭头穿过 `O` 的右下角顶点；由图形的对称性，它连接到了 `2` 所在三角形的右下角顶点，这个长箭头恰好穿过了 **4** 个三角形和 **5** 行文本。在 `OS` 侧同理，使用反向的箭头穿过 `UmSO`，再由整个图形的对称性，使用 Zigzag 方法连接全部图形，恰好得到了下图：

![Fence Cipher 解密](/assets/stage_ii/limbo_wiki/fence.png)

蓝色箭头穿过的 24 个字符分别为

```text
NOL2re@etiKdA3!ig9t~UmSO
```

将其拼接在 `https://wiki.pigeon-games.com/` 之后，完成解密。

#### NOL2re@etiKdA3!ig9t~UmSO

访问后得到一句话

> Backward, go backward, turn back to the antemundane realm, go back to the -

这即为 [上文](#对游戏本体的分析) 中，需要在 Phigros 游戏内输入的通行密钥。页面仍然展示了许多三角形阵，但右上角的三角形已经几乎破碎，这或许暗示了剧情。同时，页面的标题为 `End`，这揭示本段解密的结束。

![End 页面截图](/assets/stage_ii/limbo_wiki/end.png)
