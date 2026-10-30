#!/usr/bin/env bash
# 一次性提交：把当前工作区所有变更提交为一个 commit
# 用法：bash scripts/autocommit.sh [-v]
#       可选环境变量 AUTO_PUSH=1 提交后自动 push
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

if [ ! -d .git ]; then
  echo "[autocommit] 当前目录不是 git 仓库" >&2
  exit 1
fi

CHANGES=$(git -c core.quotepath=false status --porcelain)
if [ -z "$CHANGES" ]; then
  [ "${1:-}" = "-v" ] && echo "[autocommit] 无变更，跳过"
  exit 0
fi

# 排除 watcher 自身产生的临时文件
COUNT=$(printf '%s\n' "$CHANGES" | grep -v 'scripts/\.watch\.pid' | wc -l | tr -d ' ')
[ "$COUNT" = "0" ] && exit 0

TS=$(date '+%Y-%m-%d %H:%M')

# 变更摘要：按顶层目录/文件分组统计（最多 8 行）
SUMMARY=$(printf '%s\n' "$CHANGES" \
  | cut -c4- \
  | sed 's/.* -> //' \
  | while IFS= read -r p; do
      case "$p" in
        */*) printf '%s/\n' "${p%%/*}" ;;
        *)   printf '%s\n' "$p" ;;
      esac
    done \
  | sort | uniq -c | sort -rn | head -8 \
  | awk '{ printf "- %s (%s)\n", $2, $1 }')

git add -A -- . ':!scripts/.watch.pid' >/dev/null 2>&1 || git add -A >/dev/null 2>&1

if git diff --cached --quiet; then
  exit 0
fi

git commit -q -m "auto: ${TS} · ${COUNT} 项变更" -m "${SUMMARY}" || {
  echo "[autocommit] 提交失败（可能是 pre-commit 拦截）" >&2
  exit 1
}

echo "[autocommit] 已提交 ${COUNT} 项变更 · ${TS}"

if [ "${AUTO_PUSH:-0}" = "1" ]; then
  if git push -q origin HEAD 2>/dev/null; then
    echo "[autocommit] 已推送到 origin"
  else
    echo "[autocommit] push 失败（检查网络或凭据）" >&2
  fi
fi
