'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
'''
import hashlib
import os
from botbeer.tool import serverWeb
import botbeer
import runpy
import time
from botbeer.message import DirectMessage, Message, GroupMessage, C2CMessage
import threading
from botbeer.tool.Config import DATAPATH,bot_config
from botbeer.tool.msgList import MessageHandler
from botbeer.tool.trigger import 消息库


# 同步计算文件的 MD5 值
def get_md5(file_path):
    """计算文件的 MD5 值"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


# 同步加载并执行模块
def load_and_execute_module(path, 回收=True):
    """加载并执行模块"""
    # 先清空加载数据
    if 回收:
        filename = os.path.basename(path)
        print(f"更新：{filename}")
        消息库.clear(path)
    module_globals = runpy.run_path(path)
    return module_globals


# 获取文件夹内所有 .py 文件的路径
def get_py_files_in_folder(folder_path):
    """获取文件夹内所有 .py 文件的路径"""
    py_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


# 同步监控文件夹内所有 .py 文件的变化
def monitor_folder_and_reload(热更新=True):
    folder_path = f"{DATAPATH}/dic"
    interval = 3
    """监控文件夹内所有 .py 文件的变化并自动重新加载"""
    py_files = get_py_files_in_folder(folder_path)
    print(f"加载{len(py_files)}个PY词库文件")

    # 初始化文件的 MD5 状态
    file_states = {file: get_md5(file) for file in py_files}
    for file, _ in file_states.items():
        load_and_execute_module(file, 回收=False)

    if not 热更新:
        return

    while True:
        for file in py_files:
            current_md5 = get_md5(file)
            if current_md5 != file_states[file]:
                load_and_execute_module(file)
                file_states[file] = current_md5

        time.sleep(interval)


class MyClient(botbeer.Client):
    async def on_ready(self):
        print(f"机器人【{self.robot.name}】上线")

    # 频道
    async def on_at_message_create(self, message: Message):
        handler = MessageHandler("频道")
        handler.自己 = self
        handler.发言 = message
        handler.id = message.author.id
        await handler.at_msg(
            message.content[message.content.find(">") + 1 :].lstrip(" ")
        )

    # 频道私聊
    async def on_direct_message_create(self, message: DirectMessage):
        handler = MessageHandler("频道私聊")
        handler.自己 = self
        handler.发言 = message
        handler.id = message.author.id
        await handler.at_msg(message.content)

    # 群聊
    async def on_group_at_message_create(self, message: GroupMessage):
        handler = MessageHandler("群聊")
        handler.自己 = self
        handler.发言 = message
        handler.id = message.author.member_openid
        await handler.at_msg(message.content.lstrip(" "))

    # 私聊
    async def on_c2c_message_create(self, message: C2CMessage):
        handler = MessageHandler("群私聊")
        handler.自己 = self
        handler.发言 = message
        handler.id = message.author.user_openid
        await handler.at_msg(message.content)


def 启动机器人():
    intents = botbeer.Intents(
        public_messages=True, public_guild_messages=True, direct_message=True
    )
    client = MyClient(intents=intents)
    client.run(appid=bot_config["appid"], secret=bot_config["secret"])


def 启动():
    是否启动机器人 = bot_config.get("启动机器人", False)
    词库 = bot_config.get("词库", False)
    服务端 = bot_config.get("服务端", False)
    if 服务端:
        botWeb_thread = threading.Thread(target=serverWeb.start)
        botWeb_thread.start()
    if 词库:
        热更新 = bot_config.get("热更新", False)
        filedic_thread = threading.Thread(target=monitor_folder_and_reload, args=(热更新,))
        filedic_thread.start()

    if 是否启动机器人:
        启动机器人()
