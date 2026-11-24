# -*- coding: utf-8 -*-
"""
按「AI意识觉醒」风格生成 28 篇的封面.html（2.3 + 1:1）与 插图.html（1200×780）
用法: python gen_物料.py <cfg.json>
cfg 字段见 专题说明/元数据.md
"""
import json, os, sys


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if isinstance(s, str) else s


CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #e8e8e8; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; }
  .mono { font-family: Consolas, "Courier New", monospace; }
  .board { position: relative; overflow: hidden; background: #fff; }
  .wide { width: 900px; height: 383px; }
  .sq { width: 900px; height: 900px; }
  .bar { position: absolute; left: 48px; width: 4px; background: #1a6fb5; }
  .tag { color: #1a6fb5; font-weight: 700; letter-spacing: .2em; }
  .h1 { color: #111; font-weight: 700; line-height: 1.35; }
  .sub { color: #888; line-height: 1.6; }
  .foot { position: absolute; left: 48px; right: 48px; display: flex; justify-content: space-between;
    font-size: 11px; color: #bbb; letter-spacing: .08em; }
  .stamp { position: absolute; border: 2px solid #1a6fb5; color: #1a6fb5; border-radius: 3px;
    font-weight: 800; letter-spacing: .12em; }
"""


def cover(c):
    title = c["title_lines"]
    wide_h1 = "<br>".join(esc(x) for x in title[:2])
    sq_h1 = "<br>".join(esc(x) for x in title[:3])
    num = esc(c.get("num", "01"))
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><style>{CSS}</style></head><body>
<div class="board wide" id="paper">
  <div style="position:absolute;left:48px;top:34px;" class="mono tag" style="font-size:12px;">社会观察 · {num}/28</div>
  <div class="bar" style="top:34px;height:20px;"></div>
  <div style="position:absolute;left:48px;right:48px;top:92px;">
    <div class="h1" style="font-size:38px;">{wide_h1}</div>
    <div class="sub" style="font-size:15px;margin-top:12px;">{esc(c.get('sub',''))}</div>
  </div>
  <div class="stamp mono" style="right:48px;bottom:56px;font-size:17px;padding:7px 12px;">{num} / 28</div>
  <div class="foot mono" style="bottom:22px;"><span>2026.11.24</span><span>事实与观点分离 · 出处可见</span></div>
</div>
<div style="height:36px;"></div>
<div class="board sq" id="sq">
  <div style="position:absolute;left:56px;top:52px;" class="mono tag" style="font-size:14px;">社会观察 · {num}/28</div>
  <div class="bar" style="left:56px;top:52px;height:24px;"></div>
  <div style="position:absolute;left:56px;right:56px;top:124px;">
    <div class="h1" style="font-size:52px;">{sq_h1}</div>
    <div class="sub" style="font-size:19px;margin-top:20px;">{esc(c.get('sub',''))}</div>
  </div>
  <div style="position:absolute;left:56px;right:56px;top:520px;border-top:1px solid #e8e8e8;padding-top:18px;">
    <div class="mono" style="font-size:12px;color:#1a6fb5;letter-spacing:.16em;margin-bottom:12px;">// 本期锚点</div>
    <div style="font-size:17px;color:#333;line-height:2;">
      ▸ {esc(c.get('anchor1',''))}<br>▸ {esc(c.get('anchor2',''))}<br>▸ {esc(c.get('anchor3',''))}
    </div>
  </div>
  <div class="stamp mono" style="right:56px;bottom:100px;font-size:25px;padding:11px 18px;">{num} / 28</div>
  <div class="foot mono" style="left:56px;right:56px;bottom:44px;"><span>事实与观点分离</span><span>出处可见 · 不站队</span></div>
</div>
</body></html>"""


def fig(c):
    stages = c.get("stages", [["01", "节点一", ""], ["02", "节点二", ""], ["03", "节点三", ""]])
    nodes = ""
    for i, s in enumerate(stages[:3]):
        left = 60 + i * 420
        nodes += f"""
  <div style="position:absolute;left:{left}px;top:250px;width:240px;text-align:center;">
    <div class="mono" style="font-size:11px;color:#1a6fb5;letter-spacing:.16em;">STEP {esc(s[0])}</div>
    <div style="font-size:19px;font-weight:700;margin:8px 0;">{esc(s[1])}</div>
    <div style="font-size:13px;color:#777;line-height:1.7;">{s[2]}</div>
  </div>"""
    notes = "<br>".join(esc(n) for n in c.get("notes", ["来源：公开资料"])[:2])
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><style>{CSS}
  #fig {{ position:relative;width:1200px;height:780px;overflow:hidden;background:#fff; }}
  .conn {{ position:absolute;height:1px;background:#1a6fb5; }}
  .dot {{ position:absolute;width:6px;height:6px;background:#1a6fb5;border-radius:50%; }}
</style></head><body><div id="fig">
  <div style="position:absolute;left:48px;top:44px;" class="mono tag" style="font-size:12px;">机制图 {esc(c.get('num','01'))} / 28</div>
  <div class="bar" style="left:48px;top:44px;height:18px;"></div>
  <div style="position:absolute;left:48px;right:48px;top:104px;">
    <div style="font-size:28px;font-weight:700;color:#111;">{esc(c.get('fig_title','机制示意'))}</div>
    <div style="font-size:14px;color:#888;margin-top:8px;">{esc(c.get('fig_sub',''))}</div>
  </div>
  <div class="conn" style="left:150px;top:360px;width:900px;"></div>
  <div class="dot" style="left:148px;top:357px;"></div><div class="dot" style="left:598px;top:357px;"></div><div class="dot" style="left:1048px;top:357px;"></div>
  {nodes}
  <div style="position:absolute;left:48px;right:48px;top:440px;background:#f5f8fb;border-left:3px solid #1a6fb5;padding:18px 22px;">
    <div class="mono" style="font-size:11px;color:#1a6fb5;letter-spacing:.14em;margin-bottom:9px;">{esc(c.get('quote_label','来源立场：公开资料'))}</div>
    <div style="font-size:18px;color:#222;line-height:1.75;">“{esc(c.get('quote','一句可核对的原文。'))}”</div>
  </div>
  <div style="position:absolute;left:48px;bottom:46px;" class="mono" style="font-size:12px;color:#999;line-height:1.8;">{notes}</div>
  <div style="position:absolute;right:48px;bottom:46px;" class="mono" style="font-size:12px;color:#1a6fb5;letter-spacing:.14em;">事实 ≠ 立场 · 出处可见</div>
</div></body></html>"""


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(sys.argv[1]))
    os.makedirs(out, exist_ok=True)
    for name, content in [("封面.html", cover(cfg)), ("插图.html", fig(cfg))]:
        p = os.path.join(out, name)
        open(p, "w", encoding="utf-8").write(content)
        print("OK:", p)


if __name__ == "__main__":
    main()
