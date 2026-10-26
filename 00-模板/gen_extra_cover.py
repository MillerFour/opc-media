# -*- coding: utf-8 -*-
"""号外(EXTRA)风封面参数化生成：2.3 报头版 + 方版，输出单 HTML"""
import sys, io, json

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Inter", -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #55524a; }}
  .serif {{ font-family: 'STZhongsong','STSong','SimSun',serif; }}
  .paper {{ width: 900px; height: 383px; position: relative; overflow: hidden; background: #f7f4ec; }}
  .paper-sq {{ width: 900px; height: 900px; position: relative; overflow: hidden; background: #f7f4ec; }}
  .cols {{ position: absolute; inset: 0;
    background-image: repeating-linear-gradient(to right, transparent 0 118px, rgba(26,26,26,.07) 118px 119px); }}
  .topbar {{ position: absolute; top: 30px; left: 48px; right: 48px; border-top: 4px solid #1a1a1a; }}
  .midbar {{ position: absolute; bottom: 96px; left: 48px; right: 48px; border-bottom: 2px solid #1a1a1a; }}
  .stamp {{ position: absolute; border: 5px solid #c9342b; color: #c9342b; border-radius: 10px;
    font-weight: 900; letter-spacing: 8px; padding: 10px 20px; transform: rotate(-8deg); background: rgba(201,52,43,.04); }}
  .kicker {{ display: inline-block; background: #1a1a1a; color: #f7f4ec; font-size: 15px; font-weight: 800; letter-spacing: .5em; padding: 7px 18px 7px 22px; }}
  .datebar {{ position: absolute; font-size: 14px; color: #6b6552; letter-spacing: .35em; font-family: Consolas, monospace; }}
  .headline {{ color: #1a1a1a; font-weight: 900; line-height: 1.22; }}
  .hl-red {{ color: #c9342b; }}
  .subbar {{ color: #2b2b2b; font-size: 19px; font-weight: 600; letter-spacing: .04em; }}
  .lead {{ position: absolute; background: #1a1a1a; color: #f7f4ec; padding: 18px 22px; width: 300px; }}
  .lead .t {{ font-size: 12px; color: #c9a24b; letter-spacing: .3em; font-weight: 700; margin-bottom: 10px; }}
  .lead .l {{ font-size: 14px; line-height: 1.8; color: #e8e3d5; margin-bottom: 8px; }}
  .lead .l b {{ color: #f7f4ec; border-bottom: 2px solid #c9342b; }}
  .spacer {{ height: 40px; }}
</style>
</head>
<body>

<div class="paper" id="paper">
  <div class="cols"></div>
  <div class="topbar"></div>
  <div class="stamp" style="top:64px;right:64px;font-size:30px;">号外</div>
  <div style="position:absolute;top:58px;left:48px;">
    <span class="kicker">热点手记 · 快评</span>
  </div>
  <div style="position:absolute;left:48px;top:118px;width:640px;">
    <div class="headline serif" style="font-size:44px;">{title_main}<span class="hl-red">{title_red}</span></div>
    <div class="subbar" style="margin-top:14px;">{sub}</div>
  </div>
  <div class="midbar"></div>
  <div class="datebar" style="left:48px;bottom:62px;">{date} · EDITORIAL DESK</div>
  <div class="datebar" style="right:48px;bottom:62px;">{kw1} ｜ {kw2} ｜ {kw3}</div>
</div>

<div class="spacer"></div>

<div class="paper-sq" id="paper-sq">
  <div class="cols"></div>
  <div class="topbar" style="left:64px;right:64px;"></div>
  <div class="stamp" style="top:96px;right:80px;font-size:44px;">号外</div>
  <div style="position:absolute;top:92px;left:64px;">
    <span class="kicker" style="font-size:17px;">热点手记 · 快评</span>
  </div>
  <div style="position:absolute;left:64px;top:186px;width:720px;">
    <div class="headline serif" style="font-size:52px;">{title_main}<span class="hl-red">{title_red}</span></div>
    <div class="subbar" style="margin-top:20px;font-size:22px;">{sub}</div>
  </div>
  <div class="lead" style="left:64px;bottom:110px;">
    <div class="t">本期看点</div>
    <div class="l">▸ 事件：{p_event}</div>
    <div class="l">▸ 争议：<b>{p_conflict}</b></div>
    <div class="l">▸ 观点：{p_view}</div>
  </div>
  <div style="position:absolute;right:64px;bottom:110px;text-align:right;">
    <div style="font-size:88px;font-weight:900;color:#c9342b;line-height:1;font-family:Consolas,monospace;">{issue}<span style="font-size:30px;color:#1a1a1a;">/期</span></div>
    <div style="margin-top:10px;font-size:14px;color:#6b6552;letter-spacing:.3em;font-family:Consolas,monospace;">{date}</div>
  </div>
  <div class="midbar" style="left:64px;right:64px;bottom:64px;"></div>
</div>

</body>
</html>'''

cfg = json.loads(sys.argv[1])
html = TPL.format(**cfg)
with io.open(cfg["out"], "w", encoding="utf-8") as f:
    f.write(html)
print("written:", cfg["out"])
