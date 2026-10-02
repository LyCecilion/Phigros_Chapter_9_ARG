# ARG 网页 replay

这里保存了 Phigros 第九章「穹顶孤舟」ARG 的七个网页重放入口，供回看、解谜复盘、演示和录屏使用。它们是**本地可复现版本，不是官方实时页面，也不是官方站点的完整镜像**。

部署后访问 [`index.html`](index.html)，即可在导航页选择要进入的页面。页面对应的解谜背景见[根目录 README](../README.md)及其链接的 [ARG_explanation.md](../ARG_explanation.md)。本目录可独立部署；只部署本目录时，这两个上级目录链接不在部署范围内，不影响重放功能。

## 版权与使用声明

本目录所收录的 Phigros 原始网页、图片、文本及相关游戏素材，版权归 **南京鸽游网络有限公司** 所有；第三方字体等素材的权利归各自权利人所有，并仍受各自许可证约束。

本项目是非官方、非商业的玩家存档，仅用于解谜复盘、学习研究与交流展示，不代表南京鸽游网络有限公司的官方立场，也不暗示本项目获得了官方授权或背书。对原网页的本地化修改与重放演示，不改变原素材的版权归属。

仓库中由维护者编写的脚本及新增代码，按根目录说明采用 MIT 许可证；**该许可证不适用于收录的官方素材，也不构成对官方素材或第三方素材的再授权**。请勿将相关素材用于未经授权的商业用途；其他使用、转载或再分发，请遵守适用法律及权利人的授权要求。若权利人对收录内容有异议，可通过本仓库 Issue 联系维护者处理。

导航页的「使用说明」和「文件、操作与部署说明」均指向 [GitHub 上的本说明](https://github.com/LyCecilion/Phigros_Chapter_9_ARG/blob/main/replay/README.md)，便于直接阅读渲染后的 Markdown。

## 文件与页面含义

| 路径 / 入口 | 含义与重放内容 |
| --- | --- |
| [`index.html`](index.html) | 总导航：三个 WER 版本、正常版起始时间选择、四个解谜链页面。 |
| [`WERJETZTALLEINISTWIRDESLANGEBLEIBEN/index.html`](WERJETZTALLEINISTWIRDESLANGEBLEIBEN/index.html) | Stage II 的 Solivault 七日倒计时页面。路径来自里尔克《秋日》的德语句子「如今独自一人的人，将长久如此」。保留背景像素位移、红雾、火花、扫描线、暗角等视觉效果。 |
| [`WERJETZTALLEINISTWIRDESLANGEBLEIBEN_2026-10-02_garble/index.html`](WERJETZTALLEINISTWIRDESLANGEBLEIBEN_2026-10-02_garble/index.html) | 2026 年 10 月 2 日 16:00 换页后的 Stage III 状态：倒计时消失，画面中央改为持续变化的随机乱码。与正常版独立保存。 |
| [`WER_3D/index.html`](WER_3D/index.html) | 基于旧版制作的 **CSS 3D 分层演示**，不是官方第三种页面状态。把背景位移、红雾、顶部染色、雾层、暗角、火花沿 Z 轴展开，适合说明渲染管线。 |
| [`outside_the_birdcage/index.html`](outside_the_birdcage/index.html) | 「鸟笼之外」。从 WER 背景图的频域隐藏信息进入此页；显示格状背景和字符串碎片。重放版每次打开从已收集的 13 个样本中随机显示一个，点击可复制。 |
| [`Cogito,_ubi_sit_refugium/index.html`](Cogito,_ubi_sit_refugium/index.html) | 「我思，避难所何在？」。由上一页的矩阵与背景图得到的入口；保留有关技术、现实的句子及其零宽字符，点击可复制。 |
| [`DISORIENTATION/index.html`](DISORIENTATION/index.html) | 「迷失方向」。保留可复制的零宽字符文本、`nihilist` 标题以及源码中的数字提示。 |
| [`JUSTENGAGEWTH/index.html`](JUSTENGAGEWTH/index.html) | 「just engage with」去掉 `I` 后的路径。保留 `Fence?` 标题和点击复制交互；复制结果并非屏幕上那句话，而是从已收集的五个编码样本中随机抽取并解码后的内容。 |
| `README.md` | 本说明。静态服务器一般直接提供 Markdown 原文，不一定渲染为网页。 |

四个解谜链页面按上表顺序访问。有关文本、零宽字符、密码、排序和最终去向的完整解释请看 `ARG_explanation.md`；本导航不会自动解谜或跳转到下一关。

### 随页面打包的素材

- `SairaCondensed-Regular.ttf`：各重放页面使用的本地字体。
- 三个 WER 目录中的 `start.png`：原始打包背景文件，包含两段 PNG 图像数据；乱码版会用 `fetch()` 读取并自行提取。
- 三个 WER 目录中的 `start.layer2.png`：已提取的第二张背景图；正常版、3D 版直接读取，总导航也用它作预览图。
- `outside_the_birdcage/background-7-7.png`：鸟笼页背景。
- `Cogito,_ubi_sit_refugium/background_Cogito,_ubi_sit_refugium.png`、`DISORIENTATION/background_DISORIENTATION.png`、`JUSTENGAGEWTH/background_JUSTENGAGEWTH.png`：对应页面的背景。

部署时保留这些文件及其目录结构，不要只上传 HTML，也不要随意改名（包括路径中的大小写、逗号和下划线）。

## 正常版：选择倒计时起始时间

1. 打开总导航，找到「七日倒计时」。
2. 选择 **2026-09-25 17:00 至 2026-10-02 16:00** 之间的时间，精度为分钟，包含两个端点。
3. 日期框里的时间统一解释为 **UTC+8 / 北京时间**，不随浏览器时区改变；日期显示格式由浏览器语言决定。
4. 页面会预览起始剩余时长。点击「从此刻开始重放」进入正常版。

倒计时的固定终点是 **2026-10-02 17:00:00+08:00**：

- 从 9 月 25 日 17:00 开始，起始剩余七天。
- 从 10 月 2 日 16:00 开始，起始剩余一小时。
- 进入页面后，用 `performance.now()` 累加真实经过的时间，按一倍速推进，不请求原站时间接口，也不取决于电脑当前日期。
- 刷新会从 URL 中选择的起始时间重新开始；直接打开正常版入口，或 `start` 参数无效、超出范围时，默认从 9 月 25 日 17:00 开始。
- 倒计时到零后停在零，不会自动跳转到乱码版；要看新状态，请返回导航选择乱码版。
- 显示会向下取整到秒，因此七天起点在页面绘制时通常已显示为 `6:23:59:59`。

选择结果保存在 `start` 查询参数中，可以收藏或分享链接。例如从 10 月 2 日 16:00 重放：

```text
WERJETZTALLEINISTWIRDESLANGEBLEIBEN/index.html?start=2026-10-02T16%3A00%2B08%3A00
```

手动构造链接时应明确带上时区，并把 `+` 编码为 `%2B`，不要让它被查询参数解析成空格。起始时间选择仅影响正常版；乱码版和 3D 演示保持各自行为，3D 版仍每次打开从剩余七天开始计时。

## 3D 分层演示与录屏

建议在桌面浏览器、横屏窗口中使用。默认进入后约 850 ms 自动开始展开，动画约 5.2 秒。

| 操作 | 用途 |
| --- | --- |
| `PLAY EXPLODE` 按钮 / 空格 | 播放展开动画；完全展开后再播放会从头开始。 |
| `RESET` 按钮 / `R` | 重置为未展开状态。 |
| 拖动滑块 | 手动控制展开进度，并停止自动播放。 |
| `H` | 隐藏 / 显示控制面板。 |

已有查询参数可组合使用：

| 参数 | 效果 |
| --- | --- |
| `manual` | 不自动开始播放。 |
| `progress=0.65` | 设置初始展开进度（0～1）；若希望停在此处，同时加 `manual`。 |
| `hide` | 初始隐藏控制面板；仍可用 `H` 显示。 |
| `nocountdown` | 隐藏倒计时，保留背景渲染层。 |

例如，固定在完全展开状态并隐藏面板和倒计时，适合截图：

```text
WER_3D/index.html?manual&progress=1&hide&nocountdown
```

或从折叠状态自动播放、隐藏控制面板及倒计时，适合录屏：

```text
WER_3D/index.html?hide&nocountdown
```

## 本地访问

推荐在仓库根目录启动一个 HTTP 静态服务器：

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

然后打开：

```text
http://127.0.0.1:8000/replay/
```

也可以只服务本目录，在仓库根目录运行：

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory replay
```

此时入口是 `http://127.0.0.1:8000/`。用 `Ctrl+C` 停止服务器；端口被占用时换一个端口即可。

**不要用直接双击 HTML 作为统一访问方式。** 部分页面可以通过 `file://` 打开，但乱码版使用 `fetch()` 读取背景，浏览器的本地文件限制可能阻止它加载。使用 HTTP 服务可以避开这类差异。

## 静态部署

不需要 Node.js、构建步骤、PHP、数据库或后端 API。

- **任意静态托管（Nginx、Caddy、静态站点平台等）**：把整个 `replay/` 目录作为站点内容发布，默认文档设置为 `index.html`。如果只部署本目录，入口位于站点根路径。
- **与仓库其他文件一同部署**：保持 `replay/` 子目录不变，访问 `/replay/`。
- **GitHub Pages**：若发布源是仓库根目录，访问 `https://<用户名>.github.io/<仓库名>/replay/`；也可以通过 Pages 工作流仅发布 `replay/` 目录，此时入口为该项目站点根路径。根目录发布方式若启用了 Jekyll，可在发布根放置 `.nojekyll` 使用原样静态发布。

所有页面入口和素材都使用相对路径，支持项目子路径部署。不需要配置 SPA 回退；应直接提供对应目录中的 HTML、PNG 和 TTF 文件。自定义服务器需正确提供字体和 PNG 的 MIME 类型。

线上部署推荐 HTTPS：复制按钮优先使用 Clipboard API；在不满足安全上下文时，页面会尝试浏览器的传统复制方式，其是否可用仍取决于浏览器权限与策略。四个解谜链页面也支持先聚焦文本，再按回车或空格复制。

## 与官方原站的区别

- 背景、字体已本地化，绕过原素材站的防盗链与在线依赖。
- 正常版采用可选历史起点，不同步服务器时间；它只重放视觉倒计时，不恢复与倒计时绑定的实时换页、播歌或其他服务器状态。
- `outside_the_birdcage` 与 `JUSTENGAGEWTH` 使用已收集的响应样本代替原站的浏览器指纹和 API 分发。刷新或复制可以随机抽到重复样本，不能据此推断原服务器当时的发放顺序。
- 乱码字符是动画运行时随机生成的，不是固定截图或固定待解密文本。
- 3D 分层是为复盘和视频制作添加的演示效果；正常版与乱码版没有被它覆盖。
