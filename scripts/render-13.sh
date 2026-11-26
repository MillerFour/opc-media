#!/bin/bash
# 13 篇 × 封面2 + 插图1 批量渲染（AI意识觉醒风格）
export PATH=/d/Environment/nvm/v24.9.0:$PATH
cd "E:/Writing/wx-mp" || exit 1
BASE="http://127.0.0.1:8323/专题_男性叙事之殇"
LOG="E:/Writing/wx-mp/.workbuddy/render-13.log"
: > "$LOG"
taskkill //F //IM msedge.exe >/dev/null 2>&1

shoot() {
  local url="$1" sel="$2" out="$3"
  rm -f .playwright-cli/element-*.png 2>/dev/null
  playwright-cli open "$url" >>"$LOG" 2>&1
  sleep 1
  playwright-cli screenshot "$sel" >>"$LOG" 2>&1
  local f=$(ls -t .playwright-cli/element-*.png 2>/dev/null | head -1)
  if [ -z "$f" ]; then echo "FAIL $url $sel" >>"$LOG"; playwright-cli close >>"$LOG" 2>&1; return 1; fi
  mv "$f" "$out" && echo "OK $out" >>"$LOG"
  playwright-cli close >>"$LOG" 2>&1
}

for dir in 专题_男性叙事之殇/*_2026.11.26; do
  name=$(basename "$dir")
  echo "=== $name ===" >>"$LOG"
  shoot "$BASE/$name/源文件/封面.html" "#paper" "$dir/封面_2.3白底.png"
  shoot "$BASE/$name/源文件/封面.html" "#sq" "$dir/封面_方版1x1.png"
  shoot "$BASE/$name/源文件/插图.html" "#fig" "$dir/_fig.png"
  if [ -f "$dir/_fig.png" ]; then
    fig=$(ls "$dir" | grep '^插图_1_' | head -1)
    ffmpeg -y -loglevel error -i "$dir/_fig.png" -q:v 3 "$dir/${fig:-插图_1_机制图.jpg}" >>"$LOG" 2>&1
    rm -f "$dir/_fig.png"
  fi
done
echo ALL_DONE >>"$LOG"
