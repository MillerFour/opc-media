# -*- coding: utf-8 -*-
"""风格 E · Nvidia 封面参数化生成器：2.3 深绿快讯版 + 方版，输出单 HTML。

用法：
  python 00-模板/gen_nvidia_cover.py config.json
config.json 字段见文件末尾 __main__ 的 SAMPLE。
输出两个画板 id：#paper（900x383）、#sq（900x900）。
"""
import sys, io, json

# GPU die 点阵：10x10，按固定伪随机图案点亮，作为风格视觉签名
LIT = {
    (0, 3), (0, 6), (1, 1), (1, 4), (1, 7), (2, 2), (2, 5), (2, 8),
    (3, 0), (3, 3), (3, 6), (3, 9), (4, 1), (4, 4), (4, 7), (5, 2),
    (5, 5), (5, 8), (6, 0), (6, 3), (6, 6), (7, 1), (7, 4), (7, 7),
    (8, 2), (8, 5), (8, 9), (9, 3), (9, 6),
}


def die_grid(cell=11, gap=4, bright="#76b900", dim="#243318"):
    out = []
    for r in range(10):
        for c in range(10):
            color = bright if (r, c) in LIT else dim
            left = c * (cell + gap)
            top = r * (cell + gap)
            out.append(
                '<i style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;'
                'background:%s;border-radius:1px;"></i>' % (left, top, cell, cell, color)
            )
    return "".join(out)


TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #5c6650; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }}
  .mono {{ font-family: Consolas, "Courier New", monospace; }}
  .board {{ position: relative; overflow: hidden; background: #0d1509; color: #f0f6e6; }}
  .paper {{ width: 900px; height: 383px; }}
  .sq {{ width: 900px; height: 900px; }}
  .grid {{ position: absolute; inset: 0;
    background-image: repeating-linear-gradient(to right, transparent 0 44px, rgba(118,185,0,.065) 44px 45px),
                      repeating-linear-gradient(to bottom, transparent 0 44px, rgba(118,185,0,.065) 44px 45px); }}
  .glow {{ position: absolute; width: 620px; height: 620px; border-radius: 50%;
    background: radial-gradient(circle, rgba(118,185,0,.16) 0%, rgba(118,185,0,0) 68%); }}
  .kicker {{ display: inline-block; background: #76b900; color: #0d1509;
    font-weight: 800; letter-spacing: .28em; padding: 6px 14px 6px 18px; }}
  .hl {{ font-weight: 900; line-height: 1.25; letter-spacing: -.03em; color: #f0f6e6; }}
  .hl em {{ font-style: normal; color: #a6e22e; }}
  .sub {{ color: #9fb08a; font-weight: 500; letter-spacing: .02em; }}
  .term {{ background: #131c0d; border: 1px solid #33501a; border-radius: 10px; overflow: hidden; }}
  .termbar {{ height: 30px; background: #1b2710; border-bottom: 1px solid #33501a;
    display: flex; align-items: center; padding: 0 12px; }}
  .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; background: #76b900; }}
  .termbody {{ padding: 12px 14px 14px; }}
  .cmd {{ color: #76b900; font-size: 12px; letter-spacing: .02em; margin-bottom: 10px; }}
  .row {{ display: flex; justify-content: space-between; align-items: baseline;
    font-size: 12.5px; color: #9fb08a; padding: 5px 0; border-top: 1px solid #223213; }}
  .row b {{ color: #eaf3dd; font-size: 15px; font-weight: 700; }}
  .foot {{ position: absolute; left: 48px; right: 48px; bottom: 30px;
    border-top: 1px solid #33501a; padding-top: 12px; display: flex;
    justify-content: space-between; font-size: 12px; color: #8fa37a; letter-spacing: .12em; }}
  .lead {{ background: #131c0d; border: 1px solid #33501a; border-radius: 10px; padding: 18px 20px; }}
  .lead .t {{ color: #76b900; font-size: 12px; font-weight: 800; letter-spacing: .28em; margin-bottom: 12px; }}
  .lead .l {{ color: #d6e4c4; font-size: 15px; line-height: 1.9; }}
  .lead .l b {{ color: #a6e22e; }}
  .spacer {{ height: 40px; }}
</style>
</head>
<body>

<div class="board paper" id="paper">
  <div class="grid"></div>
  <div class="glow" style="right:-180px;top:-230px;"></div>
  <div style="position:absolute;right:56px;top:26px;opacity:.85;">{die}</div>
  <div style="position:absolute;left:48px;top:44px;">
    <span class="kicker">{kicker}</span>
    <span class="mono" style="margin-left:14px;font-size:12px;color:#8fa37a;letter-spacing:.2em;">NO.{flash}</span>
  </div>
  <div style="position:absolute;left:48px;top:112px;width:560px;">
    <div class="hl" style="font-size:42px;">{title_main}<em>{title_hl}</em></div>
    <div class="sub" style="font-size:17px;margin-top:14px;width:490px;line-height:1.5;">{sub}</div>
  </div>
  <div class="term" style="position:absolute;right:48px;top:104px;width:290px;">
    <div class="termbar"><i class="dot"></i><i class="dot" style="background:#4f7118"></i><i class="dot" style="background:#2c3a1c"></i>
      <span class="mono" style="margin-left:8px;font-size:11px;color:#8fa37a;">nvidia-smi --brief</span></div>
    <div class="termbody">
      <div class="cmd mono">$ query --status</div>
      <div class="row mono"><span>{m1_label}</span><b>{m1_value}</b></div>
      <div class="row mono"><span>{m2_label}</span><b>{m2_value}</b></div>
      <div class="row mono"><span>{m3_label}</span><b>{m3_value}</b></div>
    </div>
  </div>
  <div class="foot mono"><span>{date} · {desk}</span><span>{kw1} ｜ {kw2} ｜ {kw3}</span></div>
</div>

<div class="spacer"></div>

<div class="board sq" id="sq">
  <div class="grid"></div>
  <div class="glow" style="right:-210px;top:-160px;"></div>
  <div style="position:absolute;right:64px;top:64px;opacity:.8;">{die}</div>
  <div style="position:absolute;left:64px;top:88px;">
    <span class="kicker" style="font-size:15px;">{kicker}</span>
    <span class="mono" style="margin-left:16px;font-size:13px;color:#8fa37a;letter-spacing:.2em;">NO.{flash}</span>
  </div>
  <div style="position:absolute;left:64px;top:190px;width:760px;">
    <div class="hl" style="font-size:54px;">{title_main}<em>{title_hl}</em></div>
    <div class="sub" style="font-size:21px;margin-top:20px;">{sub}</div>
  </div>
  <div class="term" style="position:absolute;left:64px;right:64px;top:390px;">
    <div class="termbar" style="height:34px;"><i class="dot"></i><i class="dot" style="background:#4f7118"></i><i class="dot" style="background:#2c3a1c"></i>
      <span class="mono" style="margin-left:8px;font-size:12px;color:#8fa37a;">nvidia-smi --brief</span></div>
    <div class="termbody" style="padding:16px 20px 18px;">
      <div class="cmd mono" style="font-size:13px;">$ query --status</div>
      <div class="row mono" style="font-size:14px;"><span>{m1_label}</span><b style="font-size:17px;">{m1_value}</b></div>
      <div class="row mono" style="font-size:14px;"><span>{m2_label}</span><b style="font-size:17px;">{m2_value}</b></div>
      <div class="row mono" style="font-size:14px;"><span>{m3_label}</span><b style="font-size:17px;">{m3_value}</b></div>
    </div>
  </div>
  <div class="lead" style="position:absolute;left:64px;bottom:120px;width:470px;">
    <div class="t mono">// 本期看点</div>
    <div class="l">▸ 事件：{p_event}</div>
    <div class="l">▸ 焦点：<b>{p_conflict}</b></div>
    <div class="l">▸ 下一步：{p_view}</div>
  </div>
  <div style="position:absolute;right:64px;bottom:120px;text-align:right;">
    <div class="mono" style="font-size:76px;font-weight:800;color:#a6e22e;line-height:1;">{flash}<span style="font-size:26px;color:#8fa37a;">/期</span></div>
    <div class="mono" style="margin-top:12px;font-size:13px;color:#8fa37a;letter-spacing:.24em;">{date}</div>
  </div>
  <div class="foot mono" style="left:64px;right:64px;bottom:44px;"><span>{foot_sig}</span><span>{kw1} ｜ {kw2} ｜ {kw3}</span></div>
</div>

</body>
</html>'''

SAMPLE = {
    "out": "cover.html",
    "title_main": "黄仁勋辞任 CEO，",
    "title_hl": "员工公开信要答案",
    "sub": "官方公告已确认 · 一封要求「正当程序」的公开信正在集结签名",
    "date": "2026.11.15",
    "flash": "001",
    "kicker": "FLASH / 快讯",
    "desk": "DISPATCH DESK",
    "foot_sig": "GPU BRIEF · FACTS ≠ CLAIMS",
    "kw1": "CEO 交接", "kw2": "独立调查", "kw3": "公开信",
    "m1_label": "confirmed", "m1_value": "11.12",
    "m2_label": "signatures", "m2_value": "7,250+",
    "m3_label": "status", "m3_value": "OPEN",
    "p_event": "11-12 宣布辞任，CFO 任临时 CEO",
    "p_conflict": "公开信要求恢复职务与公开解释",
    "p_view": "11-17 财报与董事会调查结果",
}


def build(cfg):
    data = dict(SAMPLE)
    data.update(cfg)
    data["die"] = die_grid()
    html = TPL.format(**data)
    with io.open(cfg.get("out", "cover.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("written:", cfg.get("out", "cover.html"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        build({"out": "cover-Nvidia.html"})
    else:
        with io.open(sys.argv[1], encoding="utf-8") as f:
            build(json.load(f))
