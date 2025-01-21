#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-21 14:26:39
'''
import beertool.mybot as mybot
from beertool.trigger import *

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
    await pj.发送(pj.QQ)

@t("菜单")
async def 菜单(pj: 功能包):
    print("触发")
    await pj.发送(await pj.回调("测试 999"))


if __name__ == "__main__":
    mybot.启动()