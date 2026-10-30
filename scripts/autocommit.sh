#!/usr/bin/env bash
# 一次性提交：把当前工作区所有变更提交为一个 commit，并推送到 origin
# 用法：bash scripts/autocommit.sh [-v]
#       默认提交后自动 push；AUTO_PUSH=0 可临时关掉推送
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

if [ ! -d .git ]; then
  echo "[autocommit] 当前目录不是 git 仓库" >&2
  exit 1
fi

# 有本地领先的 commit 才推，避免空跑（默认推，AUTO_PUSH=0 关闭）
push_if_needed() {
  [ "${AUTO_PUSH:-1}" = "1" ] || return 0
  if ! git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
    echo "[autocommit] 当前分支没有上游，跳过 push" >&2
    return 0
  fi
  AHEAD=$(git rev-list --count '@{u}..HEAD' 2>/dev/null || echo 0)
  [ "${AHEAD:-0}" = "0" ] && return 0
  if git push -q origin HEAD 2>/dev/null; then
    echo "[autocommit] 已推送 ${AHEAD} 个 commit 到 origin"
  else
    echo "[autocommit] push 失败（检查网络或凭据）" >&2
    return 1
  fi
}

CHANGES=$(git -c core.quotepath=false status --porcelain)
if [ -z "$CHANGES" ]; then
  [ "${1:-}" = "-v" ] && echo "[autocommit] 无变更"
  push_if_needed
  exit $?
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

push_if_needed
