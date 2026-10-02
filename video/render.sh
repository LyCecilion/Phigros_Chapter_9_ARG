#!/usr/bin/env bash
# 渲染封装：固定环境变量，避免每次重装依赖 / 反复踩环境坑。
#
# 用法:
#   ./render.sh -ql scenes/smoke.py Smoke          # 低清快速预览（480p15）
#   ./render.sh -qh scenes/s01_overview.py        # 高清出片（1080p60，见 manim.cfg）
#   ./render.sh -s scenes/smoke.py Smoke           # 只存最后一帧（省时间）

set -euo pipefail
cd "$(dirname "$0")"

export PYTHONWARNINGS=ignore
export PYTHONPATH="$PWD/scenes${PYTHONPATH:+:$PYTHONPATH}"

# ---- MathTex / Tex 链路 ----------------------------------------------------
# dvisvgm 系统里没有，用 nix 拉进 tools/ 的那份（out-link 是 GC root，不会被回收）。
if [ -d "$PWD/tools/dvisvgm/bin" ]; then
  export PATH="$PWD/tools/dvisvgm/bin:$PATH"
fi
# nix 的 dvisvgm 用 kpathsea 找 texmf.cnf，默认只搜自己的 prefix；
# 指向 Fedora 的 texmf 树，否则它会以 rc=254 静默失败（manim 只会报
# "does not support converting .dvi files to SVG"，极具误导性）。
if [ -f /usr/share/texlive/texmf-dist/web2c/texmf.cnf ]; then
  export TEXMFCNF="/usr/share/texlive/texmf-dist/web2c${TEXMFCNF:+:$TEXMFCNF}"
fi

exec "$PWD/.venv/bin/manim" "$@"
