# ARG 详析视频 · Manim 环境与使用说明

本目录用于制作 **Phigros 第九章 ARG 详析视频** 中「原理呈现」部分的动画。
本文档记录环境的**安装途径、安装位置、使用方法、故障排查**，目标是：**换台机器或重装后，照本文能完整复现**。

- 宿主环境：Fedora 44（kernel 7.2.7）+ Nix（Determinate Nix 3.21.1）
- 项目根：`/home/lycecilion/Workspace/active/Phigros_Chapter_9_ARG/`
- 本文档所在：`video/`

---

## 1. 最终环境清单

| 组件 | 版本 | 安装位置 | 安装途径 |
|---|---|---|---|
| Manim Community | **0.21.0** | `video/.venv/lib/python3.13/site-packages/manim` | `uv pip install manim` |
| Python | **3.13.7** | `~/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu` → `video/.venv` | `uv venv --python 3.13` |
| pycairo | 1.29.1 | `video/.venv` | **源码编译**（见 §2） |
| manimpango | 0.6.1 | `video/.venv` | **源码编译**（见 §2） |
| dvisvgm | **3.6** | `video/tools/dvisvgm`（nix out-link） | `nix build nixpkgs#texlive.bin.dvisvgm` |
| LaTeX | TeX Live 2026 (`pdfTeX 3.141592653-2.6-1.40.29`) | `/usr/bin/latex` → `/usr/share/texlive` | Fedora rpm（部分由你补装） |
| uv | — | `~/.nix-profile/bin/uv` | Nix profile |

字体（由系统 fontconfig 提供，manim 可见 373 个）：

| 用途 | 字体 | 来源 |
|---|---|---|
| 正文中文 | **LXGW WenKai**（霞鹜文楷） | copr `xuthus5/lxgw-wenkai-fonts` |
| 界面中文 | **Noto Sans CJK SC** | 系统 |
| 等宽中文/代码 | **Sarasa Mono SC**（更纱黑体） | 系统 |

> ⚠️ **别搞混两个 venv**：项目根目录那个 `.venv` 是 Python **3.14** 的**空**环境，与视频无关；
> manim 用的是 **`video/.venv`（3.13）**。

---

## 2. 为什么不能直接 `pip install manim`（三条坑）

这台机器是 Nix + Fedora 混合环境，装 manim 会连挂三次：

### 坑 1 —— Python 版本
`python3` 是 **Nix 的 3.14.7**，而 `pycairo` / `manimpango` 当时**没有 3.14 轮子** → 必须自己指定 3.13。

### 坑 2 —— 缺 cairo / pango 的 dev 头文件
系统只装了**运行时**（`/lib64/libpango-1.0.so.0` 等），没有 `-devel`（即没有 `pangocairo.pc`），
而 `pycairo` / `manimpango` 是**纯源码包**，必须编译 → 报
`RequiredDependencyException: pangocairo >= 1.30.0 is required`。

且本机**没有免密 sudo**，装不了 `dnf` 的 `*-devel`。

**解法**：借用 **Nix store 里的 `*-dev` 输出**来编译。
运气好的是 Nix 侧版本与 Fedora 运行时**完全一致**：

| 库 | Nix dev 输出版本 | Fedora 运行时版本 |
|---|---|---|
| cairo | 1.18.4 | `cairo-1.18.4-6.fc44` |
| pango | 1.57.1 | `pango-1.57.1-1.fc44` |
| glib2 | 2.88.3 | `glib2-2.88.3-1.fc44` |

于是可以「**编译期用 Nix 的头文件、运行期按 SONAME 命中 Fedora 的库**」——
产物 `.so` 里记的是 `libcairo.so.2` 这类 SONAME，loader 找不到 nix store 路径就回落到系统库，**完全兼容**。
副作用（好事）：**中文字体仍走系统 fontconfig，不会变豆腐块**。

### 坑 3 —— cairo.pc 不声明 X11 / xcb 依赖
`cairo-xlib.h`、`cairo-xcb.h` 会 `#include` 这些头，但它们**不在** `cairo.pc` 的 `Requires` 里：

| 头文件 | 来自 |
|---|---|
| `X11/Xlib.h` | libX11 |
| `X11/X.h`、`X11/Xfuncproto.h` | **xorgproto**（注意：不在 libX11！） |
| `X11/extensions/Xrender.h` | libXrender |
| `X11/extensions/Xext.h` | libXext |
| `xcb/xcb.h` | libxcb |

必须手动把这些 include 根塞进 `CFLAGS`。

> 💣 **最阴的坑**：把 `*/include/**/*.h` 一律 `dirname` 剥两层，会把
> `mingw-w64-*-dev/include` 之类的无关目录也塞进 `CFLAGS`，
> 导致 **meson 的编译器自检失败**，报错是 `../meson.build:1:0: ERROR: Compiler cc cannot compile programs`
> —— **完全不提 CFLAGS**，极易误判成环境彻底坏了。
> 正确做法是用 `sed 's|/X11/.*||; s|/xcb/.*||'` **精确剥到 `include` 那一层**。

---

## 3. 复现步骤（从零）

### 3.1 一键脚本
```bash
cd video
./setup-deps.sh        # 重建 venv + 编译安装 manim（三条坑都在脚本注释里）
```

### 3.2 脚本做的事（手工等价）
```bash
# ① 让 pkg-config 看见 Nix store 里所有 .pc（约 997 个目录）
export PKG_CONFIG_PATH="$(find /nix/store -maxdepth 3 -type d -path '*/lib/pkgconfig' 2>/dev/null | sort -u | tr '\n' ':')"

# ② 补 X11 / xcb 的 include 根（精确剥到 include 层）
X_ROOTS="$(find /nix/store -maxdepth 5 \
    \( -path '*/include/X11/X.h' \
    -o -path '*/include/X11/Xlib.h' \
    -o -path '*/include/X11/extensions/Xrender.h' \
    -o -path '*/include/X11/extensions/Xext.h' \
    -o -path '*/include/xcb/xcb.h' \) 2>/dev/null \
  | sed 's|/X11/.*||; s|/xcb/.*||' | sort -u)"
export CFLAGS="$(echo "$X_ROOTS" | sed 's|^|-I|' | tr '\n' ' ')"

# ③ 用 3.13 建 venv 并安装
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python manim
.venv/bin/manim --version      # → Manim Community v0.21.0
```

### 3.3 MathTex 链路（两个额外依赖）
```bash
# ① dvisvgm：系统没有；从 nix 拉，并用 --out-link 落成 GC root（不会被 nix GC 回收）
nix build --out-link tools/dvisvgm nixpkgs#texlive.bin.dvisvgm
tools/dvisvgm/bin/dvisvgm --version     # → dvisvgm 3.6

# ② 关键：告诉 nix 的 dvisvgm 去哪找 kpathsea 配置（详见 §5）
export TEXMFCNF=/usr/share/texlive/texmf-dist/web2c
```

### 3.4 Fedora 侧补装的 LaTeX 宏包
Fedora 的 texlive 是**按 CTAN 包分包**安装的，manim 需要的类/宏包默认大都不在：

```bash
sudo dnf install \
  texlive-standalone texlive-preview texlive-amsmath texlive-babel-english \
  texlive-doublestroke texlive-setspace texlive-relsize texlive-jknapltx \
  texlive-ragged2e texlive-physics texlive-xcolor texlive-microtype \
  texlive-ctex          # 可选：想在 Tex/MathTex 里直接写中文才需要
```

对应的「谁需要谁」：

| 宏包 / 文件 | 谁需要 |
|---|---|
| `standalone.cls`、`preview.sty` | **所有** `Tex` / `MathTex`（模板是 `\documentclass[preview]{standalone}`） |
| `babel`(+english)、`amsmath`、`amssymb` | manim **默认模板** |
| `dsfont`、`setspace`、`tipa`、`relsize`、`textcomp`、`mathrsfs`、`calligra`、`wasysym`、`ragged2e`、`physics`、`xcolor`、`microtype`、`lmodern` | `_3b1b_preamble` / `TexTemplateLibrary` 的 3b1b 风格模板 |
| `ctex` | `TexTemplateLibrary` 里的 ctex 模板（Tex 里写中文） |

> 📌 `mathrsfs.sty` **属于 `texlive-jknapltx`** —— Fedora **没有** `texlive-mathrsfs` 这个包名。
> 📌 还差一个可选包：`sudo dnf install texlive-calligra`（仅 3b1b 字体风格需要，**不影响 MathTex**）。
> 📌 本机 `tipa` / `wasysym` / `amssymb` / `babel` / `lmodern` **本来就有**。

自检命令：
```bash
for f in standalone.cls preview.sty amsmath.sty dsfont.sty setspace.sty relsize.sty \
         mathrsfs.sty calligra.sty ragged2e.sty physics.sty xcolor.sty microtype.sty; do
  printf '%-14s %s\n' "$f" "$(kpsewhich "$f" 2>/dev/null || echo '★缺失')"
done
```

---

## 4. 目录结构

```
video/
├── README.md            # 本文档
├── render.sh            # ★ 渲染入口（统一环境变量，日常只用它）
├── setup-deps.sh        # 一键重建环境（§3.2）
├── manim.cfg            # 项目级配置：背景色 #0E1116、1080p60
├── .gitignore           # .venv/ media/ __pycache__/
├── tools/
│   └── dvisvgm ->       # nix out-link（GC root，勿删；删了重跑 §3.3）
├── scenes/              # ★ 所有场景代码
│   ├── style.py         # 共享风格：配色 / 字体 / 常用构件
│   ├── smoke.py         # 冒烟：中文 + 出片
│   └── smoke_tex.py     # 冒烟：MathTex 公式
└── media/               # 渲染产物（已 gitignore）
    ├── videos/<场景名>/<画质>/<Scene>.mp4
    ├── Tex/             # LaTeX 中间产物 + .log（排查 MathTex 时用）
    └── images/
```

---

## 5. 使用方法

### 5.1 渲染（统一走 `render.sh`）
```bash
cd video

./render.sh -ql scenes/smoke.py Smoke            # 低清快速预览：854×480 @15fps
./render.sh -qm scenes/xxx.py Xxx                # 中清：1280×720 @30fps
./render.sh -qh scenes/xxx.py Xxx                # 高清出片：1920×1080 @60fps
./render.sh -qk scenes/xxx.py Xxx                # 4K：3840×2160 @60fps

./render.sh -s scenes/xxx.py Xxx                 # 只存最后一帧（快速看排版）
./render.sh -p scenes/xxx.py Xxx                 # 渲染完自动播放
./render.sh -n 3,5 scenes/xxx.py Xxx             # 只渲第 3~5 号动画（调试分段用）
```

> `render.sh` 会自动设置：`PYTHONPATH=$PWD/scenes`、`PYTHONWARNINGS=ignore`、
> `PATH += tools/dvisvgm/bin`、`TEXMFCNF=/usr/share/texlive/texmf-dist/web2c`。
> **不要直接调 `.venv/bin/manim`**，否则 MathTex 会失败。

产物路径：
```
media/videos/<场景文件名>/<画质代号>/<Scene 类名>.mp4
例：media/videos/smoke_tex/480p15/SmokeTex.mp4
```

### 5.2 写一个新场景
```python
# video/scenes/s01_overview.py
from manim import *
from style import *          # 靠 render.sh 设置的 PYTHONPATH 生效

class Overview(Scene):
    def construct(self):
        title = cn("穹顶孤舟 · 全流程", 54).set_color(FG)
        note = cn("Stage I → Stage II → 隐藏曲", 26).set_color(MUTED)
        head = VGroup(title, note).arrange(DOWN, buff=0.24).to_edge(UP, buff=0.7)

        step = VGroup(
            mono("SHA512(pw)", 30).set_color(ACCENT),
            mono("→ AES-256-CBC", 30).set_color(OK),
        ).arrange(RIGHT, buff=0.6)
        step.add(box(step, color=MUTED)).shift(DOWN * 0.4)

        formula = MathTex(r"K = h[0:32],\quad IV = h[32:48]", font_size=54).set_color(OK)
        formula.next_to(step, DOWN, buff=0.8)

        self.play(FadeIn(head))
        self.play(FadeIn(step), Write(formula))
        self.wait(1)
```
渲染：`./render.sh -ql scenes/s01_overview.py Overview`

### 5.3 `style.py` 提供的 API

**配色**（都在 `from style import *` 里）：

| 常量 | 色值 | 用途 |
|---|---|---|
| `BG` | `#0E1116` | 背景 |
| `FG` | `#E8EAED` | 正文 |
| `MUTED` | `#8B93A7` | 次要说明 |
| `ACCENT` | `#4CC2FF` | 主题青 |
| `CIPHER` | `#C792EA` | 密文 / 未知 |
| `DANGER` | `#FF5C7A` | 拒绝 / 错误 |
| `OK` | `#59D9A4` | 通过 / 校验成功 |
| `GOLD` | `#FFC857` | 关键高亮 |

**字体**：`CJK`（霞鹜文楷）、`CJK_SANS`（Noto CJK）、`CJK_MONO`（更纱等宽）——
由 `pick_font()` 在启动时从 `manimpango.list_fonts()` 里挑第一个**真实存在**的，缺字体自动降级，不会硬崩。

**构件**：
```python
cn("中文正文", 32)          # 霞鹜文楷
ui("界面中文", 32)          # 黑体
mono("password", 26)        # 等宽（伪代码 / hex）
box(mob, color=OK)          # 圆角边框
chip("解锁", color=GOLD)    # 小标签（文字 + 同色细框，框高固定）
```

**基线对齐**（`Text` 的包围盒是墨迹范围，降部会把一行撑高、纯大写又更矮，
按中心摆放会让同一排 / 同一列的文字各自浮一截，所以要排整齐就得对齐基线）：

```python
baseline_offset("pHYs", 24)                  # 该行基线相对墨迹中心的偏移
place_baseline(mob, "pHYs", 24, -1.05)       # 把这一行的基线摆到 y = -1.05
baseline_row((".Bravo", "_Charlie"), 28, buff=0.75, baseline_y=-0.2)   # 一排共享基线
```

`chip()` 内部就是按这个来的：框高用固定行框 `CHIP_REF = "Hg字"`（升部 + 降部 + 汉字，
盖住项目里所有标签），文字统一坐在同一条基线上——`tEXt` / `pHYs` / `gAMA` 三个标签
不会再一个高一个矮、字也不会错行。

### 5.4 检查中文字体是否可见
```bash
PYTHONWARNINGS=ignore video/.venv/bin/python -c "
from manimpango import list_fonts
f = list_fonts()
print(len(f), 'fonts')
print([x for x in f if any(k in x for k in ('CJK','LXGW','Sarasa'))])
"
```

### 5.5 抽帧检查画面（写完场景先抽帧看，比渲全片快）
```bash
ffmpeg -v error -ss 3 -i media/videos/smoke_tex/480p15/SmokeTex.mp4 -frames:v 1 /tmp/f.png -y
```

### 5.6 背景：纯色 / 图片 / 视频

**纯色**（三种改法，作用域不同）：

| 做法 | 生效范围 |
|---|---|
| `manim.cfg` 的 `background_color = #0E1116` | 整个项目 |
| CLI `--background_color "#0b0e13"` | 单次渲染 |
| 代码 `self.camera.background_color = "#0b0e13"` | 当前场景（**其 setter 会立刻 `init_background()`**，所以中途改也生效） |

另有 `background_opacity`（`0.0`~`1.0`）控制背景色自身的 alpha。

**图片背景 · 方式 A：`Camera.background_image`**

```python
class MyScene(Scene):
    def construct(self):
        self.camera.background_image = "assets/bg.png"
        self.camera.init_background()   # ★ 必须手动调用
        ...
```

三个硬坑（**全部实测确认**）：

1. **只赋值不生效**。`init_background()` 只在 `Camera.__init__`、`background_color` setter、`background_opacity` setter、`reset_pixel_shape` 里被调用；`background_image` 本身**没有** setter 触发器 → 必须手动补 `init_background()`。
2. **路径只从 cwd 解析**（不叠加 `assets_dir`）。写 `"bg.png"` 会直接报
   `OSError: From: <cwd>, could not find bg.png at either of these locations: ['bg.png', ...]`
   → 要写 `"assets/bg.png"` 或**绝对路径**。
3. **它是「裁切」不是「缩放」**。源码是 `np.array(image)[:pixel_height, :pixel_width]` —— 取**左上角**、**不缩放**。
   → 图必须 ≥ 输出分辨率，最好**直接按输出分辨率出图**（1080p 就出 1920×1080），否则会被截掉。

**图片背景 · 方式 B（推荐）：`ImageMobject`**

```python
bg = ImageMobject("assets/bg.png").scale_to_fit_height(config.frame_height)
dim = Rectangle(width=config.frame_width, height=config.frame_height,
                fill_color=BG, fill_opacity=0.72, stroke_width=0)   # 压暗，保证文字可读
self.add(bg, dim)          # 先背景、后遮罩
```

好处：**会自动缩放**、可做动画（推拉摇移）、可加遮罩。绝大多数场景用这个。

**视频背景：manim 没有内建**。标准做法是**导出透明底 → 后期合成**（见 §5.7）；
若只是想要"会动的背景"，用 `ImageMobject` + 动画同样能实现。

### 5.7 导出透明底视频（叠加层）

```bash
./render.sh -t -ql scenes/xxx.py Xxx        # -t / --transparent
```

实测结果（本机 manim 0.21.0）：

| 命令 | 产物 | 编码 | 像素格式 | alpha |
|---|---|---|---|---|
| `./render.sh -t ...` | `Xxx.mov` | `qtrle` | `argb` | ✅ **有**（实测角像素 `(14,17,22, 0)`）|
| `./render.sh -t --format=webm ...` | `Xxx.webm` | `vp9` | `yuv420p` | ❌ **被丢掉** |

- `-t` 会**自动把扩展名切成 `.mov`**（`config.resolve_movie_file_extension()` 联动）——mp4 装不下 alpha。
- ⚠️ **别指望 `--format=webm` 保透明**：实测 manim 出的 webm 是 `yuv420p`，alpha 已经没了。
- ⚠️ **体积警告**：`qtrle` 是无损 RLE，480p / 5.8 s 就有 **1.4 MB**（同内容 mp4 仅 0.1 MB）。
  高分辨率下会非常大 → **合成完记得再压一遍**（见下）。
- 透明层里，无内容处的像素是「alpha=0 但 RGB 保留背景色」，这是正常的，合成时不可见。

用法二选一：

```bash
# ① 直接拖进剪映 / Premiere / 达芬奇 当叠加层（推荐，方便调色对齐）
# ② 命令行合成（已验证）
ffmpeg -i bg.mp4 -i Xxx.mov \
  -filter_complex "[0:v]scale=854:480[bg];[bg][1:v]overlay=shortest=1,format=yuv420p" \
  -c:v libx264 -crf 18 out.mp4
```

需要一张测试背景图时（`testsrc2` 自带色带 + 时间码，便于看裁切/缩放行为）：

```bash
ffmpeg -v error -f lavfi -i "testsrc2=size=1920x1080:duration=1:rate=1" \
       -frames:v 1 assets/bg_test.png -y
```

---

### 5.8 出片：1080p60 + 去掉底部字幕

预览版（`480p15/`）里底部那句字幕只是**旁白占位**。正式出片用：

```bash
cd video
./render_final.sh            # 全部 Scene → media/videos/<文件名>/1080p60/<Scene>.mp4
./render_final.sh 's06*'     # 只出一支（文件名的模式，记得加引号）
```

它做两件事：

1. `export OMP_NO_CAPTION=1` —— `Narrated.say()` 会把字幕换成**看不见的占位**（时长照旧），
   所以**画面里没有字幕，但每一幕的总时长与预览版完全一致**，配音时先对预览找节奏、最后换成片即可；
2. 用 `-qh` 渲染（`manim.cfg` 里 `pixel_width/height = 1920/1080`、`frame_rate = 60`）。

配套：**`SCRIPT.md`** 是全片配音稿（按「拍」给出每一幕的台词、时长，并标出哪些段落是 Manim、哪些是实录 / 口播）。

> 只想渲一幕做对比、又不覆盖预览版：
> ```bash
> OMP_NO_CAPTION=1 ./render.sh -ql --media_dir /tmp/nocap scenes/s06_zero_width_morse.py ZeroWidthReveal
> ```

## 6. 故障排查

| 现象 | 真因 | 解法 |
|---|---|---|
| `pangocairo >= 1.30.0 is required` | 缺 cairo/pango dev 头文件 | 见 §3.2，设 `PKG_CONFIG_PATH` + `CFLAGS` |
| `fatal error: 'xcb/xcb.h' not found` / `'X11/Xlib.h' not found` | cairo.pc 不声明 X11/xcb | 同上，补 include 根 |
| `ERROR: Compiler cc cannot compile programs` | `CFLAGS` 里混进了无关 include（如 mingw） | **只**用 `sed 's\|/X11/.*\|\|; s\|/xcb/.*\|\|'` 剥出的根 |
| `! LaTeX Error: File 'standalone.cls' not found.` | Fedora texlive 分包缺包 | §3.4 装宏包 |
| `Your installation does not support converting .dvi files to SVG`（**误导！**） | nix 的 dvisvgm 找不到 `texmf.cnf`，**rc=254 静默失败**，manim 把它翻译成"dvisvgm 太旧" | 设 `TEXMFCNF=/usr/share/texlive/texmf-dist/web2c`（`render.sh` 已内置） |
| MathTex 改了却没变化 | manim 命中 `media/Tex/` 旧缓存 / 旧 `.log` | `rm -rf media/Tex` 再渲 |
| `ModuleNotFoundError: style` | 没走 `render.sh`，`PYTHONPATH` 没带上 `scenes/` | 用 `./render.sh`，或自己 `export PYTHONPATH=$PWD/scenes` |

**排查 MathTex 的标准动作**（manim 把 dvisvgm 的 stdout 丢进 `DEVNULL`，必须手动复现）：
```bash
cd video
rm -rf media/Tex
./render.sh -ql scenes/smoke_tex.py SmokeTex     # 让它失败并留下 .tex/.dvi/.log
cat media/Tex/*.log                              # 看 LaTeX 报错
dvi=$(ls media/Tex/*.dvi | head -1)
TEXMFCNF=/usr/share/texlive/texmf-dist/web2c \
  tools/dvisvgm/bin/dvisvgm --page=1 --no-fonts --output=/tmp/t.svg "$dvi"   # 去掉 --verbosity=0 才看得见真因
```
正常输出应形如：
```
pre-processing DVI file (format version 2)
processing page 1
  computing extents based on data set by preview package (version 14.0.6)
  width=75.06716pt, height=10pt, depth=0pt
  output written to /tmp/t.svg
```

---

## 7. 已知取舍与备注

- **渲染器**：manim 默认走 **cairo**，**不需要 GPU / GL 上下文**（`moderngl` 已装但用不到）。
- **ManimCE vs ManimGL**：本项目用 **Manim Community（`manim`）**，不是 3b1b 的 ManimGL。
  选它是因为社区活跃、文档全、`Scene`/`Mobject` API 稳定，适合做技术讲解片。
- **不碰系统**：
  - dvisvgm 用 `--out-link` 落在 `video/tools/`，**没有写进 nix profile**（不会污染你的 PATH）。
  - 唯一对系统的改动是 §3.4 那几个 `texlive-*` rpm。
- **`media/` 可随时删**：所有中间产物（含 `Tex/`、`partial_movie_files/`）都在里面。
- **换机器复现顺序**：§3.2 → §3.3 → §3.4，然后 `./render.sh -ql scenes/smoke_tex.py SmokeTex` 验证。

---

## 8. 冒烟测试基线（当前状态）

| 场景 | 命令 | 结果 |
|---|---|---|
| 中文 + 出片 | `./render.sh -ql scenes/smoke.py Smoke` | 854×480 / h264 / 5.8s / 渲染 12s |
| MathTex 公式 | `./render.sh -ql scenes/smoke_tex.py SmokeTex` | 854×480 / h264 / 6.0s / 渲染 2.5s |

两条都通过即代表环境完好；任一失败，按 §6 排查。
