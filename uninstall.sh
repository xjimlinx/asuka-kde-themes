#!/usr/bin/env bash
#
# OMEN Dark — remove all components installed by install.sh
#
set -euo pipefail

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

echo "Removing $VARIANT components from $DATA_HOME ..."

rm -f  "$DATA_HOME/color-schemes/$VARIANT.colors"
rm -rf "$DATA_HOME/aurorae/themes/$DECORATION"
rm -rf "$DATA_HOME/plasma/desktoptheme/$VARIANT"
rm -rf "$DATA_HOME/plasma/look-and-feel/$THEME_ID"
rm -f  "$DATA_HOME/konsole/$VARIANT.colorscheme"
rm -rf "$DATA_HOME/wallpapers/$VARIANT"

if [[ "$VARIANT" == Asuka ]]; then
  rm -rf "$DATA_HOME/aurorae/themes/Asuka" # Previous decoration identifier
fi

echo "完成。若当前正在使用该主题，请在 系统设置 中切换回其他主题。"
