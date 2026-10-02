#!/usr/bin/env bash
# 一键重建 manim 环境。本机是 Nix + Fedora 混合环境，下面三个坑都已填好。
#
# 坑 1  本机 python3 是 Nix 的 3.14，pycairo / manimpango 还没有 3.14 轮子，
#       → 固定用 python 3.13 建 venv。
# 坑 2  pycairo / manimpango 必须从源码编译，需要 cairo / pango 的 dev 头文件；
#       本机没装 dnf 的 *-devel（且无免密 sudo），于是借用 Nix store 里的 dev 输出。
#       版本与 Fedora 运行时一致（cairo 1.18.4 / pango 1.57.1 / glib 2.88.3），
#       编译期用 Nix 的头文件，运行期按 SONAME 命中 Fedora 的库 —— 因此中文字体
#       仍然走系统 fontconfig，不会变成方块。
# 坑 3  cairo.pc 不声明 X11 / xcb 依赖，但 cairo-xlib.h、cairo-xcb.h 会 include 它们，
#       所以要手动把 X11 / xcb 的 include 根目录塞进 CFLAGS。
#       注意 sed 要剥到 include 根：多剥一层变成 .../include/X11 尚可，
#       若混进 mingw 的 include 目录，meson 的编译器自检会直接失败。

set -euo pipefail
cd "$(dirname "$0")"

export PKG_CONFIG_PATH="$(find /nix/store -maxdepth 3 -type d -path '*/lib/pkgconfig' 2>/dev/null | sort -u | tr '\n' ':')"

X_ROOTS="$(find /nix/store -maxdepth 5 \
      \( -path '*/include/X11/X.h' \
      -o -path '*/include/X11/Xlib.h' \
      -o -path '*/include/X11/extensions/Xrender.h' \
      -o -path '*/include/X11/extensions/Xext.h' \
      -o -path '*/include/xcb/xcb.h' \) 2>/dev/null \
    | sed 's|/X11/.*||; s|/xcb/.*||' | sort -u)"
export CFLAGS="$(echo "$X_ROOTS" | sed 's|^|-I|' | tr '\n' ' ')"

uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python manim

echo
echo "== 完成 =="
.venv/bin/manim --version
