# -*- coding: utf-8 -*-
"""sys.py · 公众号创作系统 · P1 状态看板

用法：
    python 00-系统/tools/sys.py status      # 全盘看板
    python 00-系统/tools/sys.py rank        # 选题排序（四维评分）

只读脚本：不改任何文件、不改状态。状态变更留到 P3 的 push/archive。
"""
import sys, io, os, re
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 pyyaml：python -m pip install pyyaml")

ROOT = Path(__file__).resolve().parents[2]
TOPICS = ROOT / "00-系统" / "data" / "topics.yaml"
SERIES_DIR = ROOT / "00-系列_维特根斯坦"

sys.stdout.reconfigure(encoding="utf-8")


def load_yaml(p):
    if not p.exists():
        return None
    with io.open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def article_dirs():
    return sorted([d for d in ROOT.iterdir()
                   if d.is_dir() and re.match(r"^\d{4}\.\d{2}\.\d{2}_", d.name)])


def inspect(d):
    body = (d / "正文.html").exists()
    covers = sorted(p.name for p in d.glob("封面_*.png"))
    figs = sorted(d.glob("插图_*.jpg"))
    manifest = (d / "manifest.yaml").exists()
    return dict(body=body, covers=len(covers), figs=len(figs), manifest=manifest)


def w(s):
    """按东亚字符宽度计算显示宽度"""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(s))


def pad(s, n):
    s = str(s)
    return s + " " * max(0, n - w(s))


def cmd_status():
    topics = load_yaml(TOPICS) or []
    series = load_yaml(SERIES_DIR / "series.yaml") or {}

    print("=" * 78)
    print("文章看板")
    print("=" * 78)
    print(pad("文件夹", 46) + pad("正文", 6) + pad("封面", 6) + pad("插图", 6) + "manifest")
    missing = []
    for d in article_dirs():
        i = inspect(d)
        mark = lambda b: "有" if b else "—"
        print(pad(d.name, 46) + pad(mark(i['body']), 6) + pad(i['covers'], 6) + pad(i['figs'], 6) + mark(i['manifest']))
        if not i["body"]:
            missing.append(f"{d.name}：缺正文")
        if i["covers"] < 1:
            missing.append(f"{d.name}：缺封面")

    print()
    print("=" * 78)
    print("系列台账")
    print("=" * 78)
    if series:
        vols = series.get("volumes") or []
        done = sum(1 for v in vols if v.get("publish_id"))
        print(f"{series.get('name')} · 状态 {series.get('status')} · 已推送 {done}/{len(vols)}")
        for v in vols:
            flag = "✓" if v.get("publish_id") else "…"
            print(f"  {flag} 卷{pad(v.get('vol'), 3)} {pad(str(v.get('title',''))[:22], 26)} {v.get('folder','')}")
    else:
        print("未找到 series.yaml")

    print()
    print("=" * 78)
    print("选题池")
    print("=" * 78)
    if topics:
        by_status = {}
        for t in topics:
            by_status.setdefault(t.get("status", "idea"), []).append(t)
        for st in ["approved", "idea", "drafted", "illustrated", "reviewed", "published", "stale", "dropped"]:
            if st in by_status:
                print(f"{st:<10} {len(by_status[st])} 条")
        ideas = by_status.get("idea", [])
        if ideas:
            print("\n待定选题：")
            for t in ideas:
                print(f"  · {t.get('id')}  {t.get('title')}  ｜ {t.get('angle','(缺 angle)')[:40]}")
    else:
        print("未找到 topics.yaml")

    if missing:
        print()
        print("缺件提醒：")
        for m in missing:
            print("  ! " + m)


def cmd_rank():
    topics = [t for t in (load_yaml(TOPICS) or []) if t.get("status") in ("idea", "approved")]

    def score(t):
        s = 0
        sl = str(t.get("shelf_life") or "")
        s += 5 if sl.endswith("h") and int(re.sub(r"\D", "", sl) or 0) <= 48 else 3 if sl else 1
        s += 3 if t.get("sources") else 1
        s += 3 if len(str(t.get("angle") or "")) > 10 else 0
        s += 3 if t.get("type") == "series" else 2
        return s

    ranked = sorted(((score(t), t) for t in topics), key=lambda x: -x[0])
    print(f"{'分':<4}{'id':<18}{'标题':<30}angle")
    for s, t in ranked:
        print(f"{s:<4}{str(t.get('id'))[:16]:<18}{str(t.get('title'))[:28]:<30}{str(t.get('angle'))[:30]}")
    print("\n规则：<8 分不做；同分先做本周能发的。")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"status": cmd_status, "rank": cmd_rank}.get(cmd, cmd_status)()
