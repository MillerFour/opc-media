#!/bin/bash
# 档案专题物料批量渲染：封面 #paper/#sq + 插图 #fig → 各文章文件夹
export PATH=/d/Environment/nvm/v24.9.0:$PATH
cd "E:/Writing/wx-mp" || exit 1
BASE="http://127.0.0.1:8321/专题_男性叙事之殇"
LOG="E:/Writing/wx-mp/.workbuddy/render-专题.log"
: > "$LOG"

taskkill //F //IM msedge.exe >/dev/null 2>&1

# 自起静态服务（此前外部起的会随会话死掉）
if ! curl -s -o /dev/null "http://127.0.0.1:8321/"; then
  (python -m http.server 8321 >/dev/null 2>&1 &)
  sleep 1
fi

shoot() { # $1=url $2=selector $3=outfile
  local url="$1" sel="$2" out="$3"
  rm -f .playwright-cli/element-*.png 2>/dev/null
  playwright-cli open "$url" >>"$LOG" 2>&1
  sleep 1
  playwright-cli screenshot "$sel" >>"$LOG" 2>&1
  local f
  f=$(ls -t .playwright-cli/element-*.png 2>/dev/null | head -1)
  if [ -z "$f" ] || [ ! -f "$f" ]; then echo "FAIL shot: $url $sel" >>"$LOG"; playwright-cli close >>"$LOG" 2>&1; return 1; fi
  mv "$f" "$out" && echo "OK $out" >>"$LOG"
  playwright-cli close >>"$LOG" 2>&1
}

# 子夹名|插图文件名
ITEMS='产生1_热搜入场_2026.11.23|插图_1_情绪正反馈环.jpg
产生2_算法改写_2026.11.23|插图_1_四因子排序.jpg
产生3_小作文_2026.11.23|插图_1_自述文体结构.jpg
演变1_微博机制_2026.11.23|插图_1_三条杠杆.jpg
演变2_小红书机制_2026.11.23|插图_1_CES与搜索.jpg
演变3_制度错位_2026.11.23|插图_1_两条时间轴.jpg
演变4_语言贬值_2026.11.23|插图_1_贬值曲线.jpg
常态1_默认设定_2026.11.23|插图_1_默认前提相变.jpg
常态2_对轰兴起_2026.11.23|插图_1_对轰回路.jpg
常态3_对轰代价_2026.11.23|插图_1_四张账单.jpg
常态4_标本复盘上_2026.11.23|插图_1_标本时间线.jpg
常态5_标本复盘下_2026.11.23|插图_1_双口径对照.jpg
收束1_第三种位置_2026.11.23|插图_1_三种位置.jpg
收束2_方法论_2026.11.23|插图_1_五步工具.jpg'

echo "$ITEMS" | while IFS='|' read -r folder fig; do
  [ -z "$folder" ] && continue
  dir="专题_男性叙事之殇/$folder"
  echo "=== $folder ===" >>"$LOG"
  shoot "$BASE/$folder/源文件/封面.html" "#paper" "$dir/封面_2.3档案.png"
  shoot "$BASE/$folder/源文件/封面.html" "#sq" "$dir/封面_方版1x1.png"
  shoot "$BASE/$folder/源文件/插图.html" "#fig" "$dir/_fig.png"
  if [ -f "$dir/_fig.png" ]; then
    ffmpeg -y -loglevel error -i "$dir/_fig.png" -q:v 3 "$dir/$fig" >>"$LOG" 2>&1 && rm -f "$dir/_fig.png" && echo "OK $dir/$fig" >>"$LOG"
  fi
done
echo "ALL DONE" >>"$LOG"
