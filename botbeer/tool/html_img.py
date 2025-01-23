'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
'''
import os
import uuid
import asyncio
from selenium import webdriver
from PIL import Image
from io import BytesIO

from botbeer.tool.Config import DATAPATH


async def HTML画图(html_content) -> bytes:
    current_dir = os.path.abspath(".")  # 当前文件夹路径
    temp_dir = os.path.join(current_dir, f"{DATAPATH}/api/html_to_img")

    # 确保临时文件夹存在
    os.makedirs(temp_dir, exist_ok=True)

    # 生成唯一的临时文件名
    temp_html_file = os.path.join(temp_dir, f"{uuid.uuid4()}.html")

    # 将HTML内容写入临时文件
    with open(temp_html_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    # 使用selenium打开HTML文件
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")

    driver = webdriver.Edge(options=options)
    driver.get("file://" + temp_html_file)

    # 等待页面加载
    await asyncio.sleep(0.5)

    # 截取整个页面的截图
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    # 删除临时文件
    os.remove(temp_html_file)

    # 使用BytesIO处理图片数据
    image = Image.open(BytesIO(screenshot))
    cropped_image = image.crop((0, 0, image.width, image.height))

    # 将裁剪后的图片保存到BytesIO对象中
    image_data = BytesIO()
    cropped_image.save(image_data, format="PNG")
    image_data.seek(0)

    return image_data.getvalue()
