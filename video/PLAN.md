# 第九章 ARG 原理篇 · Manim 制作计划

## 定位

B 站已经有不少全流程解谜视频，这一期不再复述流程，只讲原理：这些 cipher 到底在干什么，一张 PNG 为什么能装两张图，二维 Fourier 到底在“看”什么。

- 流程只用一两句话交代“在哪拿到了什么”，配上 DaVinci 的截图或录屏。
- Manim 负责动画，回答“为什么这样做能解出来”。
- 旁白稿以后从 `README.md` 衍生。现在先按慢讲节奏出片，DaVinci 里再切、再对齐。

## 统一规范

| 项 | 约定 |
| --- | --- |
| 底色 | 全部用深色底 `#0E1116`（`manim.cfg`），暂时不出透明版 |
| 画质 | 预览 `-ql`，定稿 `-qh`（1080p60） |
| 风格 | 只用 `scenes/style.py` 的配色和构件；新构件先加进 `style.py` |
| 色义 | 明文 `OK`，密文 `CIPHER`，密钥 `GOLD`，结构框 `MUTED`，强调 `ACCENT`，错误或越界 `DANGER` |
| 数学 | 讲直觉，公式只出现一下就淡出，不做推导 |
| 节奏 | 慢讲：每个关键状态停 1～2 s；重复的过程先慢演一遍，再加速 |
| 分段 | 一个原理一个 `Scene` 类，按“段落切点”多拆几个小 `Scene`，方便剪辑时替换 |
| 数据 | 所有字符串和结果都在代码里现算，再和 README 对照断言；不手抄结果 |
| 命名 | `scenes/sNN_<topic>.py`，`NN` 按视频顺序 |
| 抽帧 | 写完先 `-s` 看最后一帧，再 `-ql` 看整体节奏 |

## 场景清单

状态：⬜ 未开始 · 🟨 进行中 · ✅ 样片完成 · 🎬 定稿

### s01 · Chaocipher ★★★ ✅

文件：`scenes/s01_chaocipher.py`

已拆成三个 Scene：`ChaocipherIntro`（字母盘登场 + 第 1 个字母慢放，39 s）、`ChaocipherRun`（剩余 34 个字母逐渐加速 + 德语原句，69 s）、`ChaocipherWhyChaos`（同一个 G 解出 E/J/T/N，18 s）。

1. 两个 26 格字母环（左盘 `A-Z`，右盘 `PSZ…IW`），标出 zenith（第 1 位）和 nadir（第 14 位）。
2. 替换：在左盘找到密文 `Z`，从右盘同一位置读出明文 `W`。
3. 左盘置换，分步慢放：转到 zenith，取出 zenith+1，zenith+2～nadir 左移一位，再插回 nadir。
4. 右盘置换：转到 zenith，整体左移一位，取出 zenith+2，zenith+3～nadir 左移一位，再插回 nadir。
5. 对比“固定映射”和“每步都改字母表”：同一个密文字母先后解出不同的明文。
6. 加速跑完 35 个字母，明文逐字出现：`WERJETZTALLEINISTWIRDESLANGEBLEIBEN`。
7. 分词出现 „Wer jetzt allein ist, wird es lange bleiben“。

数据校验：解密结果等于 README 原文。第 1 步后左盘为 `ZBCDEFGHIJKLMANOPQRSTUVWXY`，右盘为 `PSLMYQEBJARTFZCHNUGVKDOXIW`。

### s02 · Atbash 与 Caesar ★ ✅

文件：`scenes/s02_atbash_caesar.py`

1. Atbash：字母带 `A…Z` 原地翻折成 `Z…A`，连线 A↔Z、B↔Y，强调“自己就是自己的逆”。
2. 解一个词作示范，然后整句直接给出。
3. Caesar：下方字母带滑动 3 格或 7 格，`CH-7` 的 7 就是平移格数；同样只演示一个词。
4. 收尾：这两种都是固定映射，对照 s01 的“混沌”。

### s03 · PNG 两图拼接 ★★ ✅

文件：`scenes/s03_png_polyglot.py`（取代旧样片 `s02_png_polyglot.py`）

1. 8 字节签名逐字节出现：`89 50 4E 47 0D 0A 1A 0A`。
2. chunk 的四个字段：长度、类型、数据、CRC。
3. 指针逐块跳跃，`b += 12 + c`，12 拆成 4 + 4 + 4。
4. 解码器读到 `IEND` 就停，后面的字节全部忽略，画成后段变灰。
5. 后面接第二张 PNG，看图软件只认前一张，页面脚本取后一张。
6. binwalk 的两个偏移：`3,139,459 + 583,504 = 3,722,963`，等于文件大小。
7. 拆出 layer1 和 layer2，两张图并排（沿用现有样片的结尾）。

### s04 · 二维 Fourier ★★★ ⬜

文件：`scenes/s04_fourier.py`

1. 一维热身：几条正弦波叠加成一条曲线，再拆回去，引出“频谱就是每种波有多强”。
2. 二维条纹模板：方向和疏密不同的条纹，每一种对应频谱上一对对称的点（距中心越远越密，方向就是条纹走向）。
3. 合成图：几种条纹相加，频谱上就多出几对亮点。
4. 照片的频谱是一团弥散的云；周期性隐写在上面是格外整齐的亮点或文字。
5. `fftshift`：四个象限对调，零频移到正中心。
6. `log1p`：线性显示几乎全黑，取对数后细节出来。
7. 真图：layer1 → FFT → 截取出 `outside_the_birdcage`；再用 diff 做 FFT，对比之下更清楚。

公式只出现一下：$F(u,v)=\sum_{x,y} f(x,y)\,e^{-2\pi i(ux/W+vy/H)}$。

素材：用 `numpy` 在场景里现算合成条纹和频谱；真图用 `artifacts/.../start.layer1.fft.png` 等现成结果。

### s05 · 13 个字符串 ★★★ 🎬

文件：`scenes/s05_birdcage_matrix.py`

三角形网格与六边形那一段（Figma 叠加、顺时针读 6 格）改为**录屏手动演示**，Manim 只保留两部分：

1. `BirdcageOrder`：13 个字符串排开，第一列从上到下读成 `? $ I G N O R A N C E u 1`，中间 9 行是 IGNORANCE（前面 2 个与最后 2 个是干扰项）；尾字母连起来是 DISPOSSESSION。
2. `BirdcagePhrase`：四个片段 `Cogito` / `,_ubi_` / `sit_re` / `fugium` 接成 `Cogito,_ubi_sit_refugium`，并给出中文与词根。

录屏时用得到的参照（代码里已断言）：

| 六边形左上角（行列） | 读出的词 |
| --- | --- |
| (3, 4) | `Cogito` |
| (2, 7) | `fugium` |
| (7, 2) | `sit_re` |
| (10, 9) | `,_ubi_` |

顺时针读序：右上 → 右中 → 右下 → 左下 → 左中 → 左上（先读右列自上而下，再读左列自下而上）。

数据校验：第 3..11 行的首字符等于 IGNORANCE；13 个尾字母等于 DISPOSSESSION；四个位置按顺时针读出的词与上表逐一相符。

### s06 · 零宽字符与 Morse ★★ ✅

文件：`scenes/s06_zero_width_morse.py`

1. 一句话看上去只是普通文本，中间“拉开”一道缝，露出一排不可见字符方块。
2. 三种码点：`U+200B`、`U+200C`、`U+200D`，以及 UTF-8 字节 `E2 80 8B` 等。
3. 页面标题 `.Bravo _Charlie ␣Delta` 给出映射：B→`.`，C→`_`，D→空格。
4. 方块翻成 Morse，再查表成 `DISORIENTATION`。
5. 第二句同理，快速出 `AROUSAL`。

数据校验：从 README 原句里提取零宽字符，现场解码，断言结果。

### s07 · Nihilist ★★★ ✅

文件：`scenes/s07_nihilist.py`

1. Polybius 方阵：右盘字母表删掉倒数第二个 `I`，按行填进 5×5。顺带一句 I/J 合并的历史。
2. 字母变坐标：一个字母变成两位数（行、列）。
3. 加密：明文坐标加上循环密钥坐标，`24 + 35 = 59` 的例子。
4. 解密：密文减密钥，用 `AROUSAL` 时出现越界 ✗（`DANGER`）。
5. 删掉第二个 A，用 `AROUSL` 重算，每一格都落进方阵，得到 `JUSTENGAGEWTH`。

数据校验：两套密钥的结果分别等于 README 中的 `JUSTEJ✗R✗ZBCH` 和 `JUSTENGAGEWTH`。

### s08 · Fence ★★ ⬜

文件：`scenes/s08_fence.py`（复用 s05 的矩阵和三角形构件，构件抽进 `style.py` 或公共模块）

1. 先讲栅栏密码本身：一串字按 zigzag 写成几行，再逐行读出（用一个短例子）。
2. 提示 `NO-`、`-SO`、`\/\/\/`、`row: 4? 5?` 依次出现，各自对应路径的起点、终点、形状和行数。
3. 在矩阵上画 zigzag 箭头，逐字点亮。
4. 读出 `NOL2re@etiKdA3!ig9t~UmSO`。

### s09 · 通行密钥 → AES（抽象版）★ ✅

文件：`scenes/s09_passcode_aes.py`

只画抽象流程，不出现函数名、资源名或游戏内部细节。

1. 一句话 → SHA-512 → 64 字节，切成 Key（32 字节）和 IV（16 字节），剩下的不用。
2. Key + IV 去解一个“锁着的盒子”，打开后对照一个已知答案：对了就放行，不对就是 ACCESS DENIED。
3. 一句话说明：没有密钥，AES 在密码学上不可逆，所以光解包拿不到隐藏曲。

### s10 · Base64 长度约束 ★★ ⬜

文件：`scenes/s10_base64_length.py`

1. 3 字节 = 24 位 → 切成 4 个 6 位 → 4 个字符。
2. 剩 1 字节或 2 字节时，只能编成 2 或 3 个字符，所以长度除以 4 只会余 0、2、3。
3. 星空留言的长度：25、29 都余 1，所以不可能是 Base64。
4. 末位对齐：余 2 时最后一个字符只能落在前 16 个，余 3 时只能落在前 4 个。实测 28% / 7%，对比随机 25% / 6%，真 Base64 应接近 100%。
5. 结论一句话：它看起来像密文，但从结构上说就不是 Base64。

### s11 · SSTV ★★★ ✅

文件：`scenes/s11_sstv.py`

不涉及“旋律之争”，等隐藏曲公开后再说。

1. 亮度 = 频率：灰度条对应 1500～2300 Hz，越亮音越高。
2. 一行像素 → 一段滑动的音调，配上频率曲线。
3. 每行开头的 1200 Hz 同步脉冲，也就是听到的“咯噔”。
4. Scottie S1 一行切成 G、B、R 三段，所以“旋律”的节奏是“咯噔”的三倍。
5. VIS 头逐段出现，按低位在前读 7 个数据位，得到 60，对应 Scottie S1。
6. 256 行逐行“唱”出来，图像从上往下长出 `sstv_img_0.png`。

素材：频谱图 `artifacts/stage_ii/SSTV/spectrogram.png`，解码图 `sstv_img_0.png`。

### s12 · SSTV 的音频从哪来（粗略版）★ ✅

文件：`scenes/s12_sstv_chain.py`

1. 浏览器和服务器交换公钥（ECDH）→ 共享秘密 → HKDF → 会话密钥 → AES-GCM。只画方块和箭头，不展开参数。
2. 真正的音频密文藏在封面图的 `tEXt` 块里，呼应 s03：PNG 的辅助块可以夹带任意数据，看图软件照常显示。
3. 解密后的音频送进 `decodeAudioData`，这里就是截获点。

## 制作顺序

1. s01 Chaocipher：作为风格样片，元素最多。配色、字体、节奏在这里定下来。
2. s03 PNG：按 s01 定下的标准翻修现有样片。
3. s04 Fourier、s07 Nihilist、s05 矩阵、s11 SSTV：★★★ 的主体部分。
4. s06、s08、s10：★★。
5. s02、s09、s12：★，最后做。

每个场景完成后：低清预览 → 你确认 → 标记 ✅；整体旁白稿定下后，统一调节奏，再 `-qh` 定稿 🎬。
