#!/usr/bin/env bash
# 文件变更监听 → 自动提交
# 原理：git 没有"文件生成"事件钩子，只能由外部轮询 git status 再提交。
#       本脚本每 INTERVAL 秒检查一次，检测到变更后等一个"静默周期"（无新变更）才提交，
#       避免一批图片写到一半就被提交成多个碎片 commit。
# 用法：bash scripts/watch-commit.sh            # 前台运行，Ctrl+C 退出
#       INTERVAL=10 bash scripts/watch-commit.sh
#       AUTO_PUSH=1 bash scripts/watch-commit.sh # 提交后顺带 push
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

INTERVAL=${INTERVAL:-15}
LOCK="scripts/.watch.pid"
LOG="scripts/.watch.log"

if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[watch] 已有实例在运行：pid=$(cat "$LOCK")" >&2
  exit 1
fi

echo $$ > "$LOCK"
trap 'rm -f "$LOCK"; echo "[watch] 已停止" >> "$LOG"' EXIT INT TERM

echo "[watch] 开始监听 · 间隔 ${INTERVAL}s · pid=$$" | tee -a "$LOG"

PREV=""
STABLE=0

while true; do
  CUR=$(git -c core.quotepath=false status --porcelain 2>/dev/null \
        | grep -v 'scripts/\.watch\.pid' | grep -v 'scripts/\.watch\.log')

  if [ -n "$CUR" ]; then
    H=$(printf '%s' "$CUR" | sha1sum | cut -d' ' -f1)
    if [ "$H" = "$PREV" ]; then
      STABLE=$((STABLE + 1))
    else
      STABLE=0
      PREV=$H
    fi
    # 静默一个周期后提交，保证一批文件写完再落库
    if [ "$STABLE" -ge 1 ]; then
      OUT=$(bash scripts/autocommit.sh 2>&1)
      [ -n "$OUT" ] && echo "$(date '+%Y-%m-%d %H:%M:%S') $OUT" >> "$LOG" && echo "$OUT"
      PREV=""
      STABLE=0
    fi
  else
    PREV=""
    STABLE=0
  fi

  sleep "$INTERVAL"
done
