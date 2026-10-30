# 自动提交（githook 方案）

## 先说清楚：git 没有"文件生成"事件钩子

`pre-commit` / `post-commit` 只在**你执行 git commit 时**触发，文件被写出来的那一刻它们收不到任何通知。
所以"每次生成完文件自动提交"= **监听进程 + git 命令**，钩子只负责守门（拦截不该入库的东西）和记账（写提交日志）。

本目录实现分三层：

| 文件 | 角色 | 触发时机 |
|---|---|---|
| `scripts/watch-commit.sh` | 监听器：轮询 `git status`，检测到变更且静默一个周期后提交 | 常驻后台 |
| `scripts/autocommit.sh` | 一次性提交：`git add -A` + 自动生成 commit message | 随时手动 / 被监听器调用 |
| `.githooks/pre-commit` | 拦截 >30MB 大文件和 `*.tmp` / `*.log` 临时文件 | git commit 前 |
| `.githooks/post-commit` | 把每次提交记到 `.git/autocommit.log` | git commit 后 |

钩子目录已通过 `git config core.hooksPath .githooks` 生效，随仓库一起版本管理，换机器 clone 后仍然有效（但需重新执行一次这条 config 命令）。

## 用法

```bash
# 手动提交一次（我每篇公众号做完会调用这个）
bash scripts/autocommit.sh
bash scripts/autocommit.sh -v      # 无变更时也打印提示

# 连 push 一起（默认就推，本地领先几个就推几个，无新变更也会补推）
AUTO_PUSH=0 bash scripts/autocommit.sh   # 临时只提交不推

# 常驻监听（默认 15 秒一轮，两轮无变化才提交，避免图片写一半就落库）
bash scripts/watch-commit.sh
INTERVAL=10 bash scripts/watch-commit.sh
AUTO_PUSH=0 bash scripts/watch-commit.sh   # 监听器只提交不推
```

Windows 双击启动 / 停止：

- `scripts/start-watch.bat` — 最小化窗口启动监听器
- `scripts/stop-watch.bat` — 按 `scripts/.watch.pid` 杀掉

**不开机自启**（用户 2026.10.30 明确要求）。监听器由 agent 在会话内手动拉起即可：

- 进程跟着当前会话活，会话结束即退出，所以别指望它跨会话值守
- 真正可靠的兜底是「每做完一篇就调一次 `autocommit.sh`」——不依赖任何常驻进程
- 想看监听是否在跑：`cat scripts/.watch.pid`，再 `kill -0 <pid>`

## commit message 长什么样

```
auto: 2026-10-30 10:35 · 16 项变更

- 2026.10.30_AI换装站技术拆解/ (6)
- 00-模板/ (4)
- .workbuddy/ (3)
```

## 注意

- 单文件 >30MB 会被 `pre-commit` 拦下；本仓库是图文项目，别让 4K 原图进来。确需入库：`git commit --no-verify`。
- `*.tmp` / `*.log` / `.tmp-*` 已在 `.gitignore` 里，正常情况下根本进不了暂存区，钩子是第二道保险。
- 监听器是轮询不是 inotify（Windows 下 Git Bash 没有 inotify），间隔越小越灵敏，代价是 CPU 唤醒更频繁。15 秒够用。
- **默认提交后自动 push**（2026.10.30 用户确认）。`AUTO_PUSH=0` 可临时只提交不推。
- push 前会看本地领先几个 commit：领先才推，工作区干净也会补推，不会空跑。
