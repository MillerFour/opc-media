# 风格卡 · Nvidia（GPU BRIEF）

> 写作时只读这一张卡 + `00-模板/style-Nvidia.html` 骨架，不要全量读 style-guide。

```yaml
style_id: nvidia
name: Nvidia
aliases: [英伟达, nv, 绿黑, GPU风, 快讯]
best_for: 科技公司快讯 / 财报 / 产品发布 / 人事变动 / 算力与芯片
cover_theme_id: terminal
added: 2026-11-15
baseline: 00-模板/style-Nvidia.html
cover_baseline: 00-模板/cover-Nvidia.html
cover_generator: 00-模板/gen_nvidia_cover.py

palette:
  bg: "#f7f9f3"        # 页面底，浅绿白（正文保持浅色，公众号可读）
  card: "#ffffff"
  wash: "#f1f6e9"      # 浅绿卡（诉求卡 / 口径说明）
  line: "#dfe8d2"
  dark: "#0d1509"      # 头部卡 / 数据卡 / WATCHLIST
  ink: "#1c2614"       # 浅底正文
  sub: "#35402b"
  mute: "#5a6650"
  faint: "#8b9780"
  brand: "#76b900"     # 眉标 / 编号 / 左竖线 / 深卡标题
  text_green: "#4c7a00" # 浅底强调字（#76b900 对比度不足，禁用）
  bright: "#a6e22e"    # 仅深卡内数字
  dark_text: "#eaf3dd"
  dark_sub: "#9fb08a"

skeleton:
  - 头部深卡：绿药丸 FLASH·快讯 + 右时间戳(Consolas) + 24px 白标题 + 灰绿副题 + 绿细线 `▦ NVIDIA BRIEF // DISPATCH NNN // FACTS ≠ CLAIMS`
  - 导语：加粗两句，直接点明公告与单方主张的边界
  - `// 01 CONFIRMED · 已确认`：白卡 + 3px 绿左竖线 + `NN ▸` 条目 + 等宽 `$ source:` 行
  - 深底数据卡：三格数字（Consolas + 亮绿首格）+ `$` 口径注
  - `// 02 CLAIMS · 单方主张`：浅绿卡三条诉求 + 白卡写核心论点与未获背书声明
  - `// 03 TWO SIDES · 口径对照`：官方 ▸ / 公开信 ▸，写明哪方具备确认效力
  - WATCHLIST 深卡：01/02/03，写清时间或判断标准
  - 口径说明卡 + 居中 `— 快讯完 · FLASH —`

rules:
  - 每个 section 显式写 text-align:left（报尾居中除外）
  - 章节编号统一 `// NN KEYWORD · 中文`，用 Consolas 12px / 字距 2.5px
  - 数据、日期、编号、命令行一律 Consolas
  - 数字卡片用 display:flex 三等分，深卡内 1px #2c3a1c 分隔
  - 视觉签名：GPU die 点阵只出现在封面/插图，正文用 `▦` 一行绿字符代替
  - 事实四个层级分开标：公司公告 / 监管文件 / 媒体转述 / 网站自报

tone:
  default: 短句、高密度、不铺垫、不抒情
  verdict: 不下结论、不站队，只把口径摆清楚
  warm_variant: |
    立场述评用（2026.11.15 补）。配色/封面不变，只换骨架与笔法：
    - 去机器编号、数据卡、表格、$ source: 注脚；章节改中文序数 + 绿短线
    - 宋体引语卡起手，允许第一人称、单句成段、明确站队与判断
    - 头部眉标可换「述评 · OPINION」，副标直写立场；数字只出现一次做大字
    - 仍须给事实标出处、写「本文是立场文，不伪装中立」的口径说明
    - 封面生成器 kicker / desk / foot_sig 可替换快讯文案；2.3 版副标题限宽 490px
    实例：2026.11.15_黄仁勋辞任与员工公开信/正文.html

forbidden:
  - 把单方主张写成陈述事实
  - 转述或评价个人事项、国安 / 出口管制类指控
  - 第二种强调色、渐变、阴影
  - 道德判断、投资建议、AI 生成封面图
```
