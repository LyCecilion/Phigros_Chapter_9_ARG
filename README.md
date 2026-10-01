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

与视频公开同时地，D.O.M.E. 在林泊百科[「谜题保管所:孤舟」](https://wiki.pigeon-games.com/index.php?title=%E8%B0%9C%E9%A2%98%E4%BF%9D%E7%AE%A1%E6%89%80:%E5%AD%A4%E8%88%9F)中添加内容「Solivault」：

![林泊百科「谜题保管所:孤舟」](/assets/stage_i/solivault_limbo.png)

根据提示，经过尝试，将解谜得到的字符串 `WERJETZTALLEINISTWIRDESLANGEBLEIBEN` 拼接到林泊百科的 URL `https://wiki.pigeon-games.com` 之后，即

```text
https://wiki.pigeon-games.com/WERJETZTALLEINISTWIRDESLANGEBLEIBEN
```

访问这个页面，我们得到了一张名为 `Solivault` 的 `.png` 图片，随后这一解密进展被 D.O.M.E. 认可，D.O.M.E. 在林泊百科的「谜题保管所:孤舟」页面追加了解谜答案，并附

> 不要就此结束念想，你们还会回来的。

![Solivault.png](/assets/stage_i/Solivault.png)

也免得图片中隐约包含两个角色，其上半部分做了黑暗处理。查看该页面的 HTML 源码，我们发现了这样的 JavaScript 逻辑：

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

## WERJETZTALLEINISTWIRDESLANGEBLEIBEN

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
