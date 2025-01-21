#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-21 14:26:39
'''
import base64
from typing import Union
from botbeer import logging

_log = logging.get_logger()

from beertool.trigger import 消息库

from beertool.Config import DATAPATH


class MessageHandler:
    def __init__(self, msgType: str = "网页"):
        """类型可以是：网页，群私聊，群聊，频道，频道私聊"""
        from beertool.mybot import (
            GroupMessage,
            C2CMessage,
            Message,
            DirectMessage,
        )

        self.消息类型: Union[GroupMessage, C2CMessage, Message, DirectMessage] = msgType
        # self.消息类型 = msgType
        self.发言者 = None

        # from beertool.mybot import MyClient
        # self.自己: MyClient = None
        self.自己 = None
        self.msg = ""
        self.id = "1"

    async def 发送(self, msg_template: str = "", img: str = ""):
        """发送消息"""
        if self.消息类型 == "网页":
            if img != "":
                img = (
                    "[img="
                    + base64.b64encode(open(DATAPATH + "/" + img, "rb").read()).decode()
                    + "]"
                )
                self.msg += img
            self.msg += msg_template
            return
        if self.消息类型 == "群私聊":
            msg_template = msg_template.lstrip("\n")
        if self.消息类型 == "频道":
            if img != "":
                msg_template = f"<@!{self.id}>" + msg_template
            else:
                msg_template = msg_template.lstrip("\n")
        if self.消息类型 == "频道私聊":
            msg_template = msg_template.lstrip("\n")
        if img != "":
            img = DATAPATH + "/" + img
        await self.发言者.r(msg_template, img)

    async def 回调(self, 文本: str = ""):
        if (res := await 消息库.run(self, 文本, True)) is not None:
            return res
        return None

    async def at_msg(self, msg):
        _log.info(f"「{self.消息类型}」[{self.id}]：{msg}")
        # id = db_QQ_bind_user.读(self.id, playerConfig.注册数量)

        if (stopMsg := await 消息库.run(self, msg)) is not None:
            if stopMsg != True:
                print(stopMsg)
