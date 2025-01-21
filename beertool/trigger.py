#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-21 14:26:39
'''
import asyncio
import re
from functools import wraps
from typing import Optional, Dict, List
import inspect
import beertool.sqlite_db as sqlite_db
import beertool.Config as Config
import os


async def 异步循环(i: int, func, *args, **kwargs):
    """
    并发调用 func 函数 i 次，传递额外的参数。

    :param i: 调用次数
    :param func: 要调用的函数
    :param args: 位置参数
    :param kwargs: 关键字参数
    """
    tasks = [func(*args, **kwargs) for _ in range(i)]
    await asyncio.gather(*tasks)


class 功能包:
    def __init__(self, 机器人, 括号):
        from beertool.msgList import MessageHandler

        self.机器人: MessageHandler = 机器人
        self.括号: list = 括号
        self.QQ = 机器人.id

    async def 回调(self, 文本: str = ""):
        """机器人回调"""
        return await self.机器人.回调(文本)

    async def 发送(self, 文本, 图片: str = ""):
        if not isinstance(文本, str):
            文本 = str(文本)
        """机器人发送消息"""
        await self.机器人.发送(文本, 图片)

    def 读(self, 路径, 键, 默认值) -> str:
        """机器人读配置"""
        文件 = sqlite_db.打开文件(os.path.join(Config.DATAPATH, "data"))
        库 = 文件.读库(路径)
        返回 = 库.读(键, 默认值)
        文件.关闭()
        return 返回

    def 写(self, 路径, 键, 值) -> None:
        """机器人写配置"""
        文件 = sqlite_db.打开文件(os.path.join(Config.DATAPATH, "data"))
        库 = 文件.读库(路径)
        库.写(键, 值)
        文件.关闭()

    def 替换(self, 文本: str, 替换: str, 变成: str = "") -> str:
        """替换文本"""
        return 文本.replace(替换, 变成).replace(替换, 变成)

    def 正则(self, 文本: str, 正则: str) -> bool:
        """正则匹配返回true或者false"""
        return bool(re.match(正则, 文本))

    def 正则替换(self, 文本: str, 正则: str, 变成: str = "") -> str:
        """正则替换"""
        return re.sub(正则, 变成, 文本)


class MsgManager:
    def __init__(self):
        self.registered_functions = []  # 存储注册的函数（wrapper）
        self.registered_originals = []  # 存储原始函数的引用
        self.registered_filenames: Dict[str, List[str]] = (
            {}
        )  # 字典存储文件路径和函数名的映射

    def clear(self, filename: Optional[str] = None):
        """
        清空已注册的函数列表。
        如果指定了文件路径，则仅清空与该文件路径相关的函数。

        filename: 可选的文件路径，用于指定清空特定文件的注册函数
        """

        if filename:
            # 检查文件路径是否在字典中
            if filename in self.registered_filenames:
                # 获取该文件中注册的所有函数名
                functions_to_remove = self.registered_filenames[filename]
                # 过滤掉这些函数
                self.registered_functions = [
                    wrapper
                    for wrapper, original in zip(
                        self.registered_functions, self.registered_originals
                    )
                    if inspect.getfile(original) != filename
                    or original.__name__ not in functions_to_remove
                ]
                self.registered_originals = [
                    original
                    for original in self.registered_originals
                    if inspect.getfile(original) != filename
                    or original.__name__ not in functions_to_remove
                ]
                # 从字典中移除该文件的记录
                del self.registered_filenames[filename]
        else:
            # 如果未指定文件路径，清空所有注册的函数和文件记录
            self.registered_functions.clear()
            self.registered_originals.clear()
            self.registered_filenames.clear()

    def msg(self, pattern: str):
        """
        装饰器用于注册消息处理函数

        pattern: 正则
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(方法, input_str: str = "", 回调=False):
                正则 = pattern
                if 正则 == "*":
                    return await func(功能包(机器人=方法, 括号=[input_str]))
                else:
                    if 正则.startswith("[内部]"):
                        正则 = 正则[4:]
                        if not 回调:
                            return None
                    elif 回调:
                        return None
                    m = re.match(f"^{正则}$", input_str)
                    if m:
                        msg: list[str] = [input_str]
                        msg.extend(m.groups())
                        return await func(功能包(机器人=方法, 括号=msg))
                    else:
                        return None

            # 获取函数所属的完整文件路径
            func_filename = inspect.getfile(func)

            # 将被装饰的函数记录到类的列表中
            self.registered_functions.append(wrapper)
            self.registered_originals.append(func)  # 同时记录原始函数的引用
            # 在字典中记录文件路径和函数名
            if func_filename not in self.registered_filenames:
                self.registered_filenames[func_filename] = []
            self.registered_filenames[func_filename].append(func.__name__)
            # print(f"已注册函数: {func.__name__}，文件路径: {func_filename}")
            return wrapper

        return decorator

    async def run(self, 方法, input_str, 回调=False):
        for func in self.registered_functions:
            result = await func(方法, input_str, 回调)
            if result:
                return result
        return None


消息库 = MsgManager()
t = 消息库.msg
