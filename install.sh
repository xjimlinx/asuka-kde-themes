#!/usr/bin/env bash
#
# OMEN Dark — KDE Plasma theme kit installer
# Installs every component into ~/.local/share (respects XDG_DATA_HOME).
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
VARIANT="${1:-Asuka}"
case "$VARIANT" in
  AsukaEmber) THEME_ID="com.omen.asukaember"; DECORATION="AsukaEmberRounded" ;;
  Asuka) THEME_ID="com.omen.asuka"; DECORATION="AsukaRounded" ;;
  OmenDark) THEME_ID="com.omen.dark"; DECORATION="OmenDark" ;;
  *) echo "用法: $0 [Asuka|AsukaEmber|OmenDark]" >&2; exit 2 ;;
esac
if [[ "$DATA_HOME" != /* || "$DATA_HOME" == / ]]; then
  echo "XDG_DATA_HOME 必须是非根目录的绝对路径。" >&2; exit 2
fi

echo "$VARIANT -> $DATA_HOME"

mkdir -p "$DATA_HOME/color-schemes"
mkdir -p "$DATA_HOME/aurorae/themes"
mkdir -p "$DATA_HOME/plasma/desktoptheme"
mkdir -p "$DATA_HOME/plasma/look-and-feel"
mkdir -p "$DATA_HOME/konsole"
mkdir -p "$DATA_HOME/wallpapers"

cp "$REPO_DIR/color-schemes/$VARIANT.colors" "$DATA_HOME/color-schemes/"
cp -r "$REPO_DIR/aurorae/$DECORATION" "$DATA_HOME/aurorae/themes/"
cp -r "$REPO_DIR/plasma/desktoptheme/$VARIANT" "$DATA_HOME/plasma/desktoptheme/"
cp -r "$REPO_DIR/plasma/look-and-feel/$THEME_ID" "$DATA_HOME/plasma/look-and-feel/"
cp "$REPO_DIR/konsole/$VARIANT.colorscheme" "$DATA_HOME/konsole/"
cp -r "$REPO_DIR/wallpapers/$VARIANT" "$DATA_HOME/wallpapers/"

# Retire the old decoration ID after its replacement is installed.
# Keep a legacy decoration that is still selected until the user switches.
if [[ "$VARIANT" == Asuka && -d "$DATA_HOME/aurorae/themes/Asuka" ]]; then
  CONFIG_READER="$(command -v kreadconfig6 || command -v kreadconfig5 || true)"
  if [[ -n "$CONFIG_READER" ]]; then
    CURRENT_DECORATION="$("$CONFIG_READER" --file kwinrc --group org.kde.kdecoration2 --key theme)"
    if [[ "$CURRENT_DECORATION" != __aurorae__svg__Asuka ]]; then
      rm -rf -- "$DATA_HOME/aurorae/themes/Asuka"
      echo "已清理旧版 Asuka 窗口装饰，保留 AsukaRounded。"
    else
      echo "旧版 Asuka 正在使用；切换到新版后再次安装即可清理重复项。"
    fi
  fi
fi

echo
echo "已安装。接下来在 系统设置 中应用："
echo "  颜色 / 全局主题 / Plasma 风格 / 窗口装饰 / 壁纸: $VARIANT"
echo "  Konsole: 配置文件 -> $VARIANT（单独选择）"
echo
echo "或直接整体应用（一次搞定）："
echo "  plasma-apply-lookandfeel -a $THEME_ID"
echo
echo "若列表里还没出现，可先刷新："
echo "  kbuildsycoca6 --noincremental"
