# -*- coding: utf-8 -*-
"""
档案（ARCHIVE）物料生成器 —— 按 cfg.json 生成 封面.html（2.3 横版 + 1:1 方版）与 插图.html（1200×780 机制图）
用法： python gen_档案物料.py <cfg.json 路径> [输出目录]
  cfg 说明见同目录 元数据.md；输出目录默认 = cfg 同目录下的 源文件/
与羊皮卷 gen_封面.py 统一接口：吃 JSON 文件路径，不走命令行参数拼字。
"""
import json
import os
import sys


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if isinstance(s, str) else s


def build_cover(c: dict) -> str:
    title_lines = c["title_lines"]          # 列表，paper 用 2 行、sq 可 2-3 行
    paper_h1 = "<br>".join(esc(t) for t in title_lines[:2])
    sq_h1 = "<br>".join(esc(t) for t in title_lines[:3])
    sub = esc(c.get("subtitle", ""))
    num = esc(c.get("num", "001"))
    stamp = esc(c.get("stamp", "01 / 14"))
    date = esc(c.get("date", "2026.11.23"))
    stage = esc(c.get("stage", "产生"))
    material = esc(c.get("material", "平台规则 · 公开事件 · 数据"))
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #d6d1c4; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }}
  .mono {{ font-family: Consolas, "Courier New", monospace; }}
  .serif {{ font-family: 'STSong','SimSun',serif; }}
  .board {{ position: relative; overflow: hidden; background: #f2efe6; color: #1f1d1a; }}
  .paper {{ width: 900px; height: 383px; }}
  .sq {{ width: 900px; height: 900px; }}
  .grid {{ position: absolute; inset: 0;
    background-image: repeating-linear-gradient(to right, transparent 0 44px, rgba(61,100,112,.05) 44px 45px),
                      repeating-linear-gradient(to bottom, transparent 0 44px, rgba(61,100,112,.05) 44px 45px); }}
  .rule {{ position: absolute; left: 52px; right: 52px; height: 2px; background: #1f1d1a; }}
  .thin {{ position: absolute; left: 52px; right: 52px; height: 1px; background: #cfc9ba; }}
  .tag {{ color: #3d6470; font-weight: 800; letter-spacing: .32em; }}
  .h1 {{ font-weight: 700; line-height: 1.35; letter-spacing: -.02em; }}
  .sub {{ color: #6b6659; line-height: 1.6; }}
  .foot {{ position: absolute; left: 52px; right: 52px; display: flex; justify-content: space-between;
    font-size: 11.5px; color: #8a8375; letter-spacing: .12em; }}
  .stamp {{ position: absolute; border: 2px solid #3d6470; color: #3d6470; border-radius: 4px;
    font-weight: 800; letter-spacing: .2em; }}
  .spacer {{ height: 40px; }}
</style>
</head>
<body>

<div class="board paper" id="paper">
  <div class="grid"></div>
  <div class="rule" style="top:42px;"></div>
  <div style="position:absolute;left:52px;top:58px;">
    <span class="tag mono" style="font-size:13px;">ARCHIVE · 档案 {num}</span>
    <span class="mono" style="margin-left:18px;font-size:12px;color:#8a8375;letter-spacing:.12em;">社会学观察 / SOCIAL OBSERVATION</span>
  </div>
  <div class="thin" style="top:104px;"></div>
  <div style="position:absolute;left:52px;right:52px;top:136px;">
    <div class="h1 serif" style="font-size:42px;">{paper_h1}</div>
    <div class="sub" style="font-size:16px;margin-top:12px;">{sub}</div>
  </div>
  <div class="stamp mono" style="right:56px;bottom:64px;font-size:20px;padding:8px 14px;">{stamp}</div>
  <div class="foot mono" style="bottom:28px;">
    <span>{date} · DISPATCH DESK</span><span>事实与观点分离 · 出处可见</span>
  </div>
</div>

<div class="spacer"></div>

<div class="board sq" id="sq">
  <div class="grid"></div>
  <div class="rule" style="top:64px;left:64px;right:64px;"></div>
  <div style="position:absolute;left:64px;top:82px;">
    <span class="tag mono" style="font-size:15px;">ARCHIVE · 档案 {num}</span>
    <span class="mono" style="margin-left:20px;font-size:13px;color:#8a8375;letter-spacing:.12em;">社会学观察</span>
  </div>
  <div class="thin" style="top:138px;left:64px;right:64px;"></div>
  <div style="position:absolute;left:64px;right:64px;top:180px;">
    <div class="h1 serif" style="font-size:56px;">{sq_h1}</div>
    <div class="sub" style="font-size:20px;margin-top:24px;">{sub}</div>
  </div>
  <div style="position:absolute;left:64px;right:64px;top:560px;border-top:1px solid #cfc9ba;padding-top:20px;">
    <div class="mono" style="font-size:13px;color:#3d6470;letter-spacing:.2em;margin-bottom:14px;">// 本期观察</div>
    <div style="font-size:18px;color:#33302a;line-height:2;">
      ▸ 阶段：{stage}<br>
      ▸ 材料：{material}<br>
      ▸ 立场：<span style="color:#3d6470;font-weight:700;">观察者，不是当事人代表</span>
    </div>
  </div>
  <div class="stamp mono" style="right:64px;bottom:112px;font-size:28px;padding:12px 20px;">{stamp}</div>
  <div class="foot mono" style="left:64px;right:64px;bottom:52px;">
    <span>事实与观点分离</span><span>出处可见 · 不站队</span>
  </div>
</div>

</body>
</html>
"""


def build_fig(c: dict) -> str:
    stages = c.get("fig_stages") or [["STAGE 01", "节点一", ""], ["STAGE 02", "节点二", ""], ["STAGE 03", "节点三", ""]]
    while len(stages) < 3:
        stages.append(["STAGE 0%d" % (len(stages) + 1), "节点", ""])
    s_html = ""
    for i, s in enumerate(stages[:3]):
        code, title, desc = esc(s[0]), esc(s[1]), s[2] if isinstance(s[2], str) else esc(s[2])
        left = 60 + i * 420
        s_html += f"""
  <div style="position:absolute;left:{left}px;top:262px;width:240px;text-align:center;">
    <div class="mono" style="font-size:12px;color:#3d6470;letter-spacing:.2em;">{code}</div>
    <div style="font-size:19px;font-weight:700;margin:8px 0;">{title}</div>
    <div style="font-size:13px;color:#6b6659;line-height:1.7;">{desc}</div>
  </div>"""
    notes = c.get("notes") or ["[1] 来源：待补", "[2] 单方陈述标“未经另一方证实”"]
    n_html = "<br>".join(esc(n) for n in notes[:3])
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #d6d1c4; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }}
  .mono {{ font-family: Consolas, "Courier New", monospace; }}
  .serif {{ font-family: 'STSong','SimSun',serif; }}
  #fig {{ position: relative; width: 1200px; height: 780px; overflow: hidden;
    background: #f2efe6; color: #1f1d1a; }}
  .grid {{ position: absolute; inset: 0;
    background-image: repeating-linear-gradient(to right, transparent 0 48px, rgba(61,100,112,.05) 48px 49px),
                      repeating-linear-gradient(to bottom, transparent 0 48px, rgba(61,100,112,.05) 48px 49px); }}
  .rule {{ position: absolute; left: 60px; right: 60px; height: 2px; background: #1f1d1a; }}
  .thin {{ position: absolute; left: 60px; right: 60px; height: 1px; background: #cfc9ba; }}
  .tag {{ color: #3d6470; font-weight: 800; letter-spacing: .3em; }}
  .node {{ position: absolute; width: 3px; height: 3px; background: #3d6470; border-radius: 50%; }}
  .conn {{ position: absolute; height: 1px; background: #3d6470; }}
</style>
</head>
<body>
<div id="fig">
  <div class="grid"></div>
  <div class="rule" style="top:52px;"></div>
  <div style="position:absolute;left:60px;top:68px;">
    <span class="tag mono" style="font-size:13px;">ARCHIVE · 机制图 {esc(c.get('fig_num', '01'))}</span>
    <span class="mono" style="margin-left:20px;font-size:12px;color:#8a8375;letter-spacing:.1em;">编辑部绘制 · 据公开资料整理</span>
  </div>
  <div class="thin" style="top:108px;"></div>

  <div style="position:absolute;left:60px;top:130px;">
    <div class="serif" style="font-size:30px;font-weight:700;">{esc(c.get('fig_title', '机制示意图'))}</div>
    <div style="font-size:15px;color:#6b6659;margin-top:8px;">{esc(c.get('fig_sub', ''))}</div>
  </div>

  <div class="conn" style="left:150px;top:372px;width:900px;"></div>
  <div class="node" style="left:148px;top:370px;width:6px;height:6px;"></div>
  <div class="node" style="left:598px;top:370px;width:6px;height:6px;"></div>
  <div class="node" style="left:1048px;top:370px;width:6px;height:6px;"></div>
{s_html}

  <div style="position:absolute;left:60px;right:60px;top:430px;background:#eae6da;border-left:3px solid #3d6470;padding:20px 24px;">
    <div class="mono" style="font-size:11px;color:#3d6470;letter-spacing:.2em;margin-bottom:10px;">{esc(c.get('quote_label', '引文 01 · 来源立场：待标注'))}</div>
    <div class="serif" style="font-size:18px;line-height:1.75;">“{esc(c.get('quote', '一句可核对的原文引语，带出处，带立场。'))}”</div>
  </div>

  <div class="thin" style="bottom:96px;"></div>
  <div style="position:absolute;left:60px;bottom:58px;font-size:12px;color:#8a8375;line-height:1.8;" class="mono">
    {n_html}
  </div>
  <div class="mono" style="position:absolute;right:60px;bottom:58px;font-size:12px;color:#3d6470;letter-spacing:.16em;">事实 ≠ 立场 · 出处可见</div>
</div>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python gen_档案物料.py <cfg.json> [输出目录]")
        sys.exit(1)
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(cfg_path)), "源文件")
    os.makedirs(out_dir, exist_ok=True)
    p1 = os.path.join(out_dir, "封面.html")
    p2 = os.path.join(out_dir, "插图.html")
    with open(p1, "w", encoding="utf-8") as f:
        f.write(build_cover(cfg))
    with open(p2, "w", encoding="utf-8") as f:
        f.write(build_fig(cfg))
    print("OK:", p1)
    print("OK:", p2)


if __name__ == "__main__":
    main()
