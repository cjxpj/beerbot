'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
'''
import os
from botbeer.ext.cog_yaml import read

DATAPATH = "GameConfig"

# 确保文件夹存在
os.makedirs(DATAPATH, exist_ok=True)

if os.path.exists(f"{DATAPATH}/config.yaml"):
    bot_config = read(f"{DATAPATH}/config.yaml")
else:
    # 创建新的配置文件
    with open(f"{DATAPATH}/config.yaml", "w+", encoding="utf-8") as f:
        f.write("""
appid: "xxx"
secret: "xxx"
启动机器人: false

服务端: true
# 需要跟随服务端启动,监听地址：/yunhu
云湖: false
云湖token: "xxx"

# 这个用于动态更新的PY词库，如果不需要不要动，吃性能（GameConfig/dic/dic.py）在这个目录下全部PY词库会实时更新
词库: false
热更新: false
""")
    bot_config = read(f"{DATAPATH}/config.yaml")