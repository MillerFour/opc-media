# -*- coding: utf-8 -*-
import io, json, sys
sys.path.insert(0, "E:/Writing/wx-mp/00-系列_维特根斯坦")
from gen_cover import make

BASE = "E:/Writing/wx-mp/"
CFGS = [
    dict(out=BASE + "2026.11.07_维特根斯坦卷一1_林荫巷16号/源文件/cover.html",
         tag="哲人档案 · 卷一 ①", title="林荫巷 16 号", title2="",
         sub_pre="父亲的钢铁", sub_post="，与母亲的七架钢琴",
         cmd="archive --vol.1-1", cmdline="family --vienna --1890s",
         lines=[["1874", "长女赫尔敏出生"], ["1889", "幼子路德维希出生"],
                ["1902", "长子汉斯失踪"], ["1912", "父母在音乐厅合奏"], ["1913", "父亲卡尔去世"]],
         foot="PHILOSOPHER ARCHIVE · 卷一 ① ｜ 2026.11.07",
         slogan="这栋房子，<b>既是音乐厅，也是法庭</b>。"),
    dict(out=BASE + "2026.11.07_维特根斯坦卷一2_八个孩子/源文件/cover.html",
         tag="哲人档案 · 卷一 ②", title="八个孩子", title2="",
         sub_pre="天赋是礼物", sub_post="，也是判决",
         cmd="archive --vol.1-2", cmdline="siblings --eight",
         lines=[["1877", "长子汉斯，音乐神童"], ["1902", "汉斯出逃后失踪"],
                ["1904", "鲁迪在柏林自尽"], ["1918", "库尔特在前线自尽"],
                ["1961", "保罗用左手弹到七十四岁"]],
         foot="PHILOSOPHER ARCHIVE · 卷一 ② ｜ 2026.11.07",
         slogan="五个儿子，<b>三个死在自己手里</b>，一个靠左手活了下来。"),
    dict(out=BASE + "2026.11.07_维特根斯坦卷二1_两次丧兄/源文件/cover.html",
         tag="哲人档案 · 卷二 ①", title="家里少了两个人", title2="",
         sub_pre="1902 与 1904", sub_post="，两个哥哥先后消失",
         cmd="archive --vol.2-1", cmdline="silence --1902-1904",
         lines=[["1902", "汉斯从船上消失"], ["1903", "路德维希赴林兹上学"],
                ["1904", "鲁迪在柏林自尽"], ["1904", "父亲禁止再提他的名字"], ["1913", "父亲去世"]],
         foot="PHILOSOPHER ARCHIVE · 卷二 ① ｜ 2026.11.07",
         slogan="所有人都知道发生了什么，<b>所有人都不能说</b>。"),
    dict(out=BASE + "2026.11.07_维特根斯坦卷二2_林兹三本书/源文件/cover.html",
         tag="哲人档案 · 卷二 ②", title="林兹三年", title2="",
         sub_pre="三本书", sub_post="，和一个自杀的教授",
         cmd="archive --vol.2-2", cmdline="books --linz --1903-1906",
         lines=[["1903", "进入林兹实科中学"], ["1903", "魏宁格自杀，遗著出版"],
                ["1904", "姐姐递来叔本华"], ["1906", "玻尔兹曼自杀"], ["1906", "改道柏林学工程"]],
         foot="PHILOSOPHER ARCHIVE · 卷二 ② ｜ 2026.11.07",
         slogan="哲学的任务，是让<b>某些焦虑消失</b>。"),
]

for c in CFGS:
    make(c)
