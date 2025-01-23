#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import botbeer.tool.mybot as mybot
from botbeer.tool.trigger import *


@t("*")
async def 任意(pj: 功能包):
    pj.变量["a"] = "内容"


@t("读取变量")
async def 读取变量(pj: 功能包):
    await pj.发送(pj.变量["a"])


@t("重复")
async def 重复(pj: 功能包):
    await pj.发送("a")
    # 拦截
    return True


@t("重复")
async def 重复(pj: 功能包):
    await pj.发送("b")


@t("[内部]测试 ([0-9]+)")
async def 测试(pj: 功能包):
    return "ok" + pj.括号[1]


@t("读写测试")
async def 读写测试(pj: 功能包):
    await pj.发送(pj.读("蔡徐坤文件", "键", "b"))
    pj.写("蔡徐坤文件", "键", "a")
    await pj.发送(pj.读("蔡徐坤文件", "键", "b"))


@t("替换测试")
async def 替换测试(pj: 功能包):
    await pj.发送(pj.替换("5544", "5", "3"))
    await pj.发送(pj.正则替换("a1212b", "[0-9]+", "6"))


@t("正则测试")
async def 正则测试(pj: 功能包):
    await pj.发送(pj.正则("a1212b", "[0-9]+"))
    await pj.发送(pj.正则("1212", "[0-9]+"))


@t("账号")
async def 账号(pj: 功能包):
    await pj.发送(pj.账号)


@t("来源")
async def 来源(pj: 功能包):
    await pj.发送(pj.来源)


@t("HTML画图")
async def HTML画图(pj: 功能包):
    await pj.发送("这是文本", await pj.HTML画图("<h1>图片</h1>"))
    await pj.发送(图片= await pj.HTML画图("<h1>图片</h1>"))
    await pj.发送("完事")


@t("转换")
async def 转换(pj: 功能包):
    a = pj.HTML编码("beer")
    b = pj.HTML解码(a)
    c = pj.URL编码("beer")
    d = pj.URL解码(c)
    e = pj.MD5("beer")
    f = pj.Base64编码("beer")
    g = pj.Base64解码(f)
    await pj.发送(
        f"HTML编码：{a}\nHTML解码：{b}\nURL编码：{c}\nURL解码：{d}\nMD5：{e}\nBase64编码：{f}\nBase64解码：{g}"
    )


@t("菜单")
async def 菜单(pj: 功能包):
    print("触发")
    await pj.发送(await pj.回调("测试 999"))


# 云湖机器人
@t("[内部]MD=(.+)")
async def MD(pj: 功能包):
    print(pj.括号[1])
    await pj.发送("触发markdown卡片")


@t("html")
async def md(pj: 功能包):
    await pj.发送HTML("<h1>这是HTML卡片</h1>")


@t("md")
async def md(pj: 功能包):
    await pj.发送卡片("# 这是卡片")


if __name__ == "__main__":
    mybot.启动()
