"""
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
"""
import base64
from typing import Union
from botbeer import logging

_log = logging.get_logger()

from botbeer.tool.trigger import 消息库
from botbeer.tool.Config import DATAPATH
import botbeer.tool.yunhu as yunhu


class MessageHandler:
    def __init__(self, 消息类型: str):
        """类型可以是：网页，群私聊，群聊，频道，频道私聊,云湖_群,云湖_私聊"""
        from botbeer.tool.mybot import (
            GroupMessage,
            C2CMessage,
            Message,
            DirectMessage,
        )

        self.发言: Union[
            GroupMessage, C2CMessage, Message, DirectMessage, yunhu.yunhuapi
        ] = None

        self.消息类型 = 消息类型

        # from beertool.mybot import MyClient
        # self.自己: MyClient = None
        self.自己 = None
        self.msg = ""
        self.id = "1"
        self.变量 = {}

    async def 发送(self, msg_template: str = "", img="", 类型: str = "text"):
        """发送消息"""
        if self.消息类型 == "云湖_群":
            if msg_template.startswith("\n"):
                msg_template = msg_template[1:]
            await self.发言.r(msg_template, img, 类型)
            return
        if self.消息类型 == "网页":
            if img != "":
                if isinstance(img, str):
                    img = (
                        "[img="
                        + base64.b64encode(
                            open(DATAPATH + "/" + img, "rb").read()
                        ).decode()
                        + "]"
                    )
                else:
                    img = "[img=" + base64.b64encode(img).decode() + "]"
                self.msg += img
            self.msg += msg_template
            return
        if self.消息类型 == "群私聊":
            if msg_template.startswith("\n"):
                msg_template = msg_template[1:]
        if self.消息类型 == "频道":
            if img != "":
                msg_template = f"<@!{self.id}>" + msg_template
            else:
                if msg_template.startswith("\n"):
                    msg_template = msg_template[1:]
        if self.消息类型 == "频道私聊":
            if msg_template.startswith("\n"):
                msg_template = msg_template[1:]
        if img != "":
            if not isinstance(img, bytes):
                img = DATAPATH + "/" + img
        await self.发言.r(msg_template, img)

    async def 回调(self, 文本: str = ""):
        if (res := await 消息库.run(self, 文本, True)) is not None:
            return res
        return None

    async def 特殊_msg(self, msg):
        _log.info(f"「{self.消息类型}」[{self.id}]：{msg}")
        if (res := await 消息库.run(self, msg, True)) is not None:
            return res
        return None

    async def at_msg(self, msg):
        _log.info(f"「{self.消息类型}」[{self.id}]：{msg}")
        if (stopMsg := await 消息库.run(self, msg)) is not None:
            if stopMsg != True:
                print(stopMsg)
