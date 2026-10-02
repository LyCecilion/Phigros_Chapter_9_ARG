#!/usr/bin/env bash
# 出片：把全部 Scene 渲染成 1080p60 的「无字幕」版本 —— 字幕交给旁白，不烧进画面。
#
#   ./render_final.sh                  # 全部 Scene
#   ./render_final.sh 's06*'           # 只出 s06 这一支（记得加引号）
#
# 输出：media/videos/<文件名>/1080p60/<Scene>.mp4
# 说明：
#   * 带字幕的低清预览版仍在 480p15/，两者**总时长完全一致**
#     （style.py 里 OMP_NO_CAPTION=1 时只把字幕换成看不见的占位，时长照旧）；
#   * 所以配音时可以先对 480p15 找节奏，最后直接换 1080p60 的画面。

set -euo pipefail
cd "$(dirname "$0")"

export OMP_NO_CAPTION=1
pattern="${1:-s[0-9][0-9]_*.py}"

# 用 find 列文件：不依赖 shell 的 glob 展开
while IFS= read -r src; do
    [ -n "$src" ] || continue
    # 能渲染的 Scene = 定义了 construct 的类（ChaoBase / Disk 这类抽象基类没有 construct，
    # 而且 s01 的三个 Scene 继承的是 ChaoBase 而不是 Narrated，不能只按基类名筛）
    scenes=$(awk '/^class /{name=$2; sub(/\(.*/,"",name)} /^    def construct\(/ && name != "" {print name; name=""}' "$src" | tr '\n' ' ')
    [ -n "$scenes" ] || continue
    echo "### $(basename "$src"): $scenes"
    ./render.sh -qh "$src" $scenes
done < <(find scenes -maxdepth 1 -name "$pattern" -print | sort)

echo "=== 出片完成：media/videos/*/1080p60/ ==="
