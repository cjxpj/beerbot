'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
'''
import os
import random
import requests


def 覆盖增值(dist1: dict, dist2: dict) -> dict:
    """
    遍历dist2，将数值与dist1中对应键的数值相加，并覆盖dist1中的值。
    如果dist2中有dist1中不存在的键，这些键值对会被添加到dist1中。

    参数:
    dist1 (dict): 第一个字典，将被更新。
    dist2 (dict): 第二个字典，其值将与dist1中的值相加。

    返回:
    dict: 更新后的dist1。
    """
    for key, value in dist2.items():
        if key in dist1:
            dist1[key] += value
        else:
            dist1[key] = value
    return dist1


def 随机数(最小值, 最大值):
    if 最小值 == 最大值:
        return 最小值
    return random.randint(最小值, 最大值)


def download_file(url, file_path):
    # 检查文件是否存在
    if os.path.exists(file_path):
        return file_path

    # 下载文件
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    else:
        raise Exception(f"无法下载文件，状态码: {response.status_code}")


def generate_progress_bar(max_value=100, current_value=10, num_blocks=5):
    # 计算每个方块代表的进度百分比
    block_percentage = 100 / num_blocks

    # 计算当前进度占总进度的百分比
    current_percentage = (current_value / max_value) * 100

    # 计算应该有多少个黑色方块
    filled_blocks = int(current_percentage // block_percentage)

    # 计算剩余的白色方块数量
    empty_blocks = num_blocks - filled_blocks

    # 创建进度条字符串
    progress_bar = "■" * filled_blocks + "□" * empty_blocks

    return progress_bar
