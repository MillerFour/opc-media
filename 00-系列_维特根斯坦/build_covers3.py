# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, "E:/Writing/wx-mp/00-系列_维特根斯坦")
from gen_cover import make

BASE = "E:/Writing/wx-mp/"
CFGS = [
    dict(dir="2026.11.07_维特根斯坦卷三_工程师六年", tag="哲人档案 · 卷三", title="工程师的六年", title2="",
         sub_pre="父亲的期望", sub_post="，与一副螺旋桨", cmd="archive --vol.3", cmdline="engineering --1906-1911",
         lines=[["1906", "柏林学机械工程"], ["1908", "曼彻斯特研究航空"], ["1911", "螺旋桨专利"],
                ["1911", "耶拿见弗雷格"], ["1911", "秋赴剑桥"]],
         foot="PHILOSOPHER ARCHIVE · 卷三 ｜ 2026.11.07", slogan="父亲要的是工程师，<b>他交出了一个哲学家</b>。"),
    dict(dir="2026.11.07_维特根斯坦卷四_罗素与父亲", tag="哲人档案 · 卷四", title="罗素与父亲", title2="",
         sub_pre="1912 天才被确认", sub_post="，1913 父亲去世", cmd="archive --vol.4", cmdline="authority --1911-1914",
         lines=[["1911", "未预约走进罗素房间"], ["1912", "罗素确认其天才"], ["1913", "父亲病逝"],
                ["1913", "散尽遗产"], ["1914", "志愿参军"]],
         foot="PHILOSOPHER ARCHIVE · 卷四 ｜ 2026.11.07", slogan="他终于被判定是天才，<b>然后散掉了家产</b>。"),
    dict(dir="2026.11.07_维特根斯坦卷五_战壕里的书", tag="哲人档案 · 卷五", title="战壕里的书", title2="",
         sub_pre="逻辑", sub_post="与罪，在这里合流", cmd="archive --vol.5", cmdline="trenches --1914-1919",
         lines=[["1914", "志愿上前线"], ["1916", "写下“上帝”之问"], ["1918", "库尔特自尽、品生特空难"],
                ["1918", "意大利被俘"], ["1921", "逻辑哲学论发表"]],
         foot="PHILOSOPHER ARCHIVE · 卷五 ｜ 2026.11.07", slogan="一本讲逻辑的书，<b>结尾在谈上帝</b>。"),
    dict(dir="2026.11.07_维特根斯坦卷六_出逃十年", tag="哲人档案 · 卷六", title="出逃十年", title2="",
         sub_pre="解决完哲学之后", sub_post="，他去山村教书", cmd="archive --vol.6", cmdline="exile --1920-1929",
         lines=[["1920", "山村小学教师"], ["1926", "体罚事件离场"], ["1926", "修道院园丁"],
                ["1928", "造维特根斯坦之家"], ["1929", "重返剑桥"]],
         foot="PHILOSOPHER ARCHIVE · 卷六 ｜ 2026.11.07", slogan="十年里，他<b>没有发表任何哲学</b>。"),
    dict(dir="2026.11.07_维特根斯坦卷七_拆掉自己的房子", tag="哲人档案 · 卷七", title="拆掉自己的房子", title2="",
         sub_pre="他回来", sub_post="，是为了推翻自己", cmd="archive --vol.7", cmdline="revise --1929-1939",
         lines=[["1929", "以旧著获博士学位"], ["1930", "开始开设讲座"], ["1933", "蓝皮书、棕皮书"],
                ["1936", "挪威小屋重写"], ["1939", "接任哲学讲席"]],
         foot="PHILOSOPHER ARCHIVE · 卷七 ｜ 2026.11.07", slogan="多数人守着一座体系，<b>他一生在拆房子</b>。"),
    dict(dir="2026.11.07_维特根斯坦卷八_最后", tag="哲人档案 · 卷八", title="最后", title2="",
         sub_pre="医院、爱尔兰", sub_post="与一句遗言", cmd="archive --vol.8", cmdline="last --1939-1951",
         lines=[["1939", "接任剑桥教授"], ["1941", "医院担架工"], ["1947", "辞去教职"],
                ["1949", "确诊前列腺癌"], ["1951", "剑桥病逝"]],
         foot="PHILOSOPHER ARCHIVE · 卷八 ｜ 2026.11.07", slogan="他说，<b>我度过了极好的一生</b>。"),
]

for c in CFGS:
    d = os.path.join(BASE, c["dir"], "源文件")
    os.makedirs(d, exist_ok=True)
    c["out"] = os.path.join(d, "cover.html")
    make(c)
