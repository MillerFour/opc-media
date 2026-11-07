# -*- coding: utf-8 -*-
"""哲人档案 · 维特根斯坦系列 白色封面生成器（锌白 light 版，2.35:1 + 1:1）
用法：python gen_cover.py cfg.json
cfg 字段：out, vol, title, title2, sub_pre, sub_post, lines[[year,text],...], cmd, foot, slogan
"""
import sys, io, json

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Inter", -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #52525b; -webkit-font-smoothing: antialiased; }}
  .cover {{ width: 900px; height: 383px; position: relative; overflow: hidden; display: flex; align-items: center; background: #fafafa; }}
  .cover-square {{ width: 900px; height: 900px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; background: #fafafa; }}
  .grid-bg {{ position: absolute; inset: 0;
    background-image: linear-gradient(to right, rgba(9,9,11,.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(9,9,11,.05) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: radial-gradient(720px 420px at 30% 40%, #000 30%, transparent 100%);
    -webkit-mask-image: radial-gradient(720px 420px at 30% 40%, #000 30%, transparent 100%); }}
  .cover-square .grid-bg {{ mask-image: radial-gradient(860px 620px at 50% 42%, #000 30%, transparent 100%);
    -webkit-mask-image: radial-gradient(860px 620px at 50% 42%, #000 30%, transparent 100%); }}
  .glow {{ position: absolute; width: 560px; height: 560px; border-radius: 50%;
    background: radial-gradient(circle, rgba(24,24,27,.06) 0%, transparent 65%); top: -280px; right: -120px; }}
  .content {{ position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: space-between; padding: 0 48px; }}
  .content-col {{ position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; padding: 0 64px; }}
  .left {{ max-width: 470px; }}
  .tag {{ display: inline-flex; align-items: center; gap: 8px; border: 1px solid #e4e4e7; border-radius: 9999px;
    padding: 4px 14px; font-size: 11.5px; font-weight: 600; letter-spacing: .14em; color: #3f3f46; margin-bottom: 18px; }}
  .tag .dot {{ width: 6px; height: 6px; border-radius: 50%; background: #09090b; }}
  h1 {{ font-size: 54px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.14; color: #09090b; margin-bottom: 14px; }}
  .sub {{ font-size: 17px; line-height: 1.6; color: #52525b; }}
  .sub b {{ color: #09090b; font-weight: 600; }}
  .foot {{ position: absolute; left: 48px; bottom: 26px; font-size: 11.5px; letter-spacing: .1em; color: #a1a1aa;
    display: flex; align-items: center; gap: 10px; }}
  .cover-square .foot {{ left: 64px; bottom: 36px; }}
  .foot::before {{ content: ""; width: 26px; height: 1px; background: #d4d4d8; }}
  .slogan {{ position: absolute; left: 64px; bottom: 68px; font-size: 13.5px; font-weight: 600; letter-spacing: .02em; color: #52525b; }}
  .slogan b {{ color: #09090b; }}
  .term {{ width: 336px; flex: none; border: 1px solid #e4e4e7; border-radius: 14px; background: #ffffff;
    box-shadow: 0 20px 50px rgba(9,9,11,.10); overflow: hidden; }}
  .term-wide {{ width: 100%; max-width: 772px; }}
  .term-bar {{ display: flex; align-items: center; gap: 6px; padding: 10px 14px; border-bottom: 1px solid #e4e4e7; }}
  .term-bar i {{ width: 9px; height: 9px; border-radius: 50%; background: #d4d4d8; display: block; }}
  .term-bar .ttl {{ margin-left: 8px; font-size: 10.5px; color: #a1a1aa; letter-spacing: .04em; font-family: Consolas, monospace; }}
  .term-body {{ padding: 14px 16px 16px; font-family: Consolas, "Courier New", monospace; }}
  .cmd {{ color: #a1a1aa; margin-bottom: 10px; font-size: 10.5px; }}
  .cmd .p {{ color: #09090b; }}
  .line {{ display: grid; grid-template-columns: 52px 1fr; gap: 10px; align-items: baseline; margin-bottom: 7px; }}
  .line:last-child {{ margin-bottom: 0; }}
  .line .y {{ font-size: 11.5px; font-weight: 600; color: #09090b; }}
  .line .tx {{ font-size: 11.5px; color: #71717a; line-height: 1.5; }}
  .cover-square .line {{ grid-template-columns: 86px 1fr; margin-bottom: 9px; }}
  .cover-square .line .y {{ font-size: 13px; }}
  .cover-square .line .tx {{ font-size: 13px; }}
  .spacer {{ height: 40px; }}
</style>
</head>
<body>

<div class="cover" id="light">
  <div class="grid-bg"></div>
  <div class="glow"></div>
  <div class="content">
    <div class="left">
      <div class="tag"><span class="dot"></span>{tag}</div>
      <h1>{title}{title2}</h1>
      <div class="sub"><b>{sub_pre}</b>{sub_post}</div>
    </div>
    <div class="term">
      <div class="term-bar"><i></i><i></i><i></i><span class="ttl">{cmd}</span></div>
      <div class="term-body">
        <div class="cmd"><span class="p">$</span> {cmdline}</div>
        {lines23}
      </div>
    </div>
  </div>
  <div class="foot">{foot}</div>
</div>

<div class="spacer"></div>

<div class="cover-square" id="sq">
  <div class="grid-bg"></div>
  <div class="glow"></div>
  <div class="content-col">
    <div class="tag" style="margin-bottom:26px;"><span class="dot"></span>{tag}</div>
    <h1 style="font-size:76px;margin-bottom:18px;">{title}{title2}</h1>
    <div class="sub" style="font-size:20px;margin-bottom:34px;"><b>{sub_pre}</b>{sub_post}</div>
    <div class="term term-wide">
      <div class="term-bar"><i></i><i></i><i></i><span class="ttl">{cmd}</span></div>
      <div class="term-body">
        <div class="cmd"><span class="p">$</span> {cmdline}</div>
        {lines11}
      </div>
    </div>
    <div class="slogan">{slogan}</div>
  </div>
  <div class="foot">{foot}</div>
</div>

</body>
</html>'''


def make(cfg):
    lines23 = "\n        ".join(
        f'<div class="line"><span class="y">{y}</span><span class="tx">{t}</span></div>' for y, t in cfg["lines"])
    lines11 = "\n        ".join(
        f'<div class="line"><span class="y">{y}</span><span class="tx">{t}</span></div>' for y, t in cfg["lines"])
    html = TPL.format(
        tag=cfg["tag"], title=cfg["title"], title2=cfg.get("title2", ""),
        sub_pre=cfg["sub_pre"], sub_post=cfg["sub_post"],
        cmd=cfg["cmd"], cmdline=cfg["cmdline"],
        lines23=lines23, lines11=lines11,
        foot=cfg["foot"], slogan=cfg["slogan"])
    with io.open(cfg["out"], "w", encoding="utf-8") as f:
        f.write(html)
    print("written:", cfg["out"])


if __name__ == "__main__":
    with io.open(sys.argv[1], encoding="utf-8") as f:
        make(json.load(f))
