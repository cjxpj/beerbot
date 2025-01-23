"""
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
"""
import base64
import html
import io
import json
import requests

from botbeer.tool.Config import bot_config

云湖token = bot_config.get("云湖token", "")

APIURL = f"https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={云湖token}"
UPAPIURL = f"https://chat-go.jwzhd.com/open-apis/v1/image/upload?token={云湖token}"


class yunhuapi:
    def __init__(self):
        self.send_msg_id = 0
        self.data = {}

    async def r(self, msg_template: str, img="", 发送类型: str = "text"):
        if self.data["event"]["chat"]["chatType"] == "group":
            if 发送类型 == "markdown":
                await self.send_msg(
                    self.data["event"]["chat"]["chatId"],
                    msg_template,
                    "group",
                    "markdown",
                )
            elif 发送类型 == "html":
                await self.send_msg(
                    self.data["event"]["chat"]["chatId"],
                    msg_template,
                    "group",
                    "html",
                )
            else:
                if img != "":
                    await self.send_msgimg(
                        self.data["event"]["chat"]["chatId"],
                        msg_template,
                        img,
                        "group",
                    )
                else:
                    await self.send_msg(
                        self.data["event"]["chat"]["chatId"],
                        msg_template,
                        "group",
                        "text",
                    )

    async def send_msg(
        self,
        id: str,
        msg_template: str,
        send_type: str = "group",
        msgtype: str = "text",
    ) -> str:
        """云湖发送消息"""
        self.send_msg_id += 1
        msg = msg_template.replace("[消息]", str(self.send_msg_id))
        headers = {"Content-Type": "application/json"}
        data = {
            "recvId": id,
            "recvType": send_type,
            "contentType": msgtype,
            "content": {"text": msg},
        }

        # 发送 POST 请求
        response = requests.post(APIURL, headers=headers, data=json.dumps(data))
        # print(response.text)
        return response.text

    async def send_msgimg(
        self,
        id: str,
        msg_template: str,
        img="",
        send_type: str = "group",
    ) -> str:
        """云湖发送消息"""
        self.send_msg_id += 1
        msg = msg_template.replace("[消息]", str(self.send_msg_id))
        headers = {"Content-Type": "application/json"}

        if img != "":
            if msg != "":
                if isinstance(img, str):
                    with open(img, "rb") as f:
                        img = f.read()
                        b64img = base64.b64encode(img).decode("utf-8")
                elif isinstance(img, bytes):
                    b64img = base64.b64encode(img).decode("utf-8")
                b64img = "data:image/png;base64," + b64img
                # html编码
                msg = html.escape(msg)
                data = {
                    "recvId": id,
                    "recvType": send_type,
                    "contentType": "html",
                    "content": {
                        "text": f'<img src="{b64img}" height="228" ><p>{msg}</p>'
                    },
                }
                response = requests.post(APIURL, headers=headers, data=json.dumps(data))
                print(response.text)
                return response.text
            else:
                imgkey = await self.getimg(img)
                data = {
                    "recvId": id,
                    "recvType": send_type,
                    "contentType": "image",
                    "content": {"imageKey": imgkey},
                }
                response = requests.post(APIURL, headers=headers, data=json.dumps(data))
                # print(response.text)
                return response.text
        else:
            data = {
                "recvId": id,
                "recvType": send_type,
                "contentType": "text",
                "content": {"text": msg},
            }
            response = requests.post(APIURL, headers=headers, data=json.dumps(data))
            # print(response.text)
            return response.text

    async def getimg(self, 图) -> str:
        文件 = None

        if isinstance(图, bytes):  # 如果是字节数据
            文件 = {"image": ("image.png", io.BytesIO(图), "image/png")}
        elif isinstance(图, str):  # 如果是文件路径
            try:
                文件 = {"image": open(图, "rb")}
            except FileNotFoundError:
                print("文件不存在，请检查路径")
                return ""
        else:
            print("不支持的类型")
            return ""

        response = requests.request("POST", UPAPIURL, files=文件)
        res: dict = response.json()
        if res.get("code") == 1:
            return res.get("data", {}).get("imageKey", "")
        else:
            print(res.get("msg", ""))
            return ""
