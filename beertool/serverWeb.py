#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-21 14:26:39
'''
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import uvicorn
import beertool.html_img as html_img


from beertool.msgList import MessageHandler

from beertool.Config import DATAPATH

app = FastAPI()

# app.mount("/static", StaticFiles(directory=f"{DATAPATH}/static"), name="static")


def start():
    """启动服务"""
    端口 = 5000
    print(f"测试服务地址：http://127.0.0.1:{端口}/test_chat")
    uvicorn.run(app, host="0.0.0.0", port=端口)


# 设置模板路径
template_path = f"{DATAPATH}/templates"
# 加载模板
template_loader = FileSystemLoader(template_path)
# 创建模板环境
template_env = Environment(loader=template_loader)


@app.get("/test_chat")
async def chat():
    return HTMLResponse(
        content="""
<!DOCTYPE html>
<html lang="zh-cn">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试区域</title>
    <style>
        body {
            background-color: #121212; /* 深灰色背景 */
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            color: #e0e0e0; /* 浅灰色字体 */
        }

        #header {
            background-color: #212121; /* 深灰色背景 */
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
        }

        #chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin: 20px;
            background-color: #1e1e1e; /* 深灰色背景 */
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }

        #messages {
            flex: 1;
            overflow-y: scroll;
            border: 1px solid #333; /* 深灰色边框 */
            padding: 10px;
            background-color: #2a2a2a; /* 深灰色背景 */
        }

        .message {
            display: flex;
            margin-bottom: 10px;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message.bot {
            justify-content: flex-start;
        }

        .bubble {
            max-width: 60%;
            padding: 10px;
            border-radius: 10px;
            position: relative;
        }

        .user-bubble {
            background-color: #0084ff; /* 蓝色气泡 */
            color: white;
            border-bottom-right-radius: 0;
        }

        .bot-bubble {
            background-color: #333; /* 深灰色气泡 */
            color: #e0e0e0; /* 浅灰色字体 */
            border-bottom-left-radius: 0;
        }

        #input-container {
            display: flex;
            margin-top: 20px;
        }

        #input-container input {
            flex: 1;
            padding: 10px;
            border: 1px solid #333; /* 深灰色边框 */
            border-radius: 4px;
            background-color: #2a2a2a; /* 深灰色背景 */
            color: #e0e0e0; /* 浅灰色字体 */
        }

        #input-container button {
            padding: 10px 20px;
            border: none;
            background-color: #007bff; /* 蓝色按钮 */
            color: white;
            border-radius: 4px;
            margin-left: 10px;
            cursor: pointer;
        }

        #messages {
            flex: 1;
            overflow-y: scroll;
            border: 1px solid #333; /* 深灰色边框 */
            padding: 10px;
            background-color: #2a2a2a; /* 深灰色背景 */
            -ms-overflow-style: none;
            /* IE and Edge */
            scrollbar-width: none;
            /* Firefox */
        }

        /* 隐藏Chrome, Safari, Opera的滚动条 */
        #messages::-webkit-scrollbar {
            display: none;
        }
    </style>
</head>

<body>
    <div id="header">
        <span>测试</span>
    </div>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-container">
            <input type="text" id="message-input" placeholder="输入消息...">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        function escapeHtml(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        let formIdCounter = 0; // 用于生成唯一的表单ID

        function sendMessage() {
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;
            if (!message) return;

            const messagesContainer = document.getElementById('messages');
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.innerHTML = `<div class="bubble user-bubble">${escapeHtml(message)}</div>`;
            messagesContainer.appendChild(userMessage);

            if (message == '清屏') {
                messageInput.value = '';
                messagesContainer.innerHTML = '';
                return;
            }

            fetch('/robot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    msg: message
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.reply == "") {
                        return;
                    }
                    const botMessage = document.createElement('div');
                    botMessage.className = 'message bot';
                    botMessage.innerHTML = `<div class="bubble bot-bubble">${escapeHtml(data.reply.trim()).replace(/\[POST跳转=(.+?)=(.+?),(.+?)\]/, (match, p1, p2, p3) => {
                        const label = p1;
                        const url = p2;
                        const base64EncodedData = p3;

                        // 创建一个隐藏的表单
                        const formId = `form_${++formIdCounter}`; // 生成唯一的表单ID
                        const form = document.createElement('form');
                        form.method = 'post';
                        form.action = url;
                        form.id = formId; // 分配唯一ID
                        form.style.display = 'none';
                        document.body.appendChild(form); // 将表单添加到DOM中

                        // 创建一个隐藏的输入字段来存储Base64编码的数据
                        const input = document.createElement('input');
                        input.type = 'hidden';
                        input.name = 'data';
                        input.value = decodedData;
                        form.appendChild(input);

                        // 返回一个可见的按钮来触发表单提交
                        return `<button type="button" class="post-link" data-form-id="${formId}">${label}</button>`;
                    }).replace(/\[img=(.*?)\]/g, (match, p1) => {
                        // 假设 p1 是 base64 编码的图片数据
                        return `<img src="data:image/png;base64,${p1}" alt="Image" style="max-width: 100%; height: auto;">`;
                    }).replace(/\n/g, '<br>')}</div>`;
                    messagesContainer.appendChild(botMessage);

                    // 为新创建的按钮添加点击事件监听器
                    const postButtons = botMessage.querySelectorAll('.post-link');
                    postButtons.forEach(button => {
                        button.addEventListener('click', function (event) {
                            event.preventDefault();
                            const formId = this.getAttribute('data-form-id');
                            const form = document.getElementById(formId);
                            if (form) {
                                console.log("Submitting form:", form); // 调试信息
                                form.submit(); // 提交表单
                            } else {
                                console.error("Form not found with ID:", formId); // 调试信息
                            }
                        });
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    const botMessage = document.createElement('div');
                    botMessage.className = 'message bot';
                    botMessage.innerHTML = `<div class="bubble bot-bubble">对不起，我无法回答您的问题。</div>`;
                    messagesContainer.appendChild(botMessage);
                });

            messageInput.value = '';
        }

        document.getElementById('message-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>

</html>
"""
    )


@app.post("/robot")
async def robot(request: Request):
    data: dict = await request.json()
    if not data:
        raise HTTPException(status_code=400, detail="error")

    msg = data.get("msg")
    id = "test"

    m = MessageHandler()
    m.id = id
    m.消息类型 = "网页"
    await m.at_msg(msg)
    reply = m.msg

    return {"reply": reply}

@app.get("/api/htmlimg")
async def html_to_img(html: str = None):
    if not html:
        raise HTTPException(status_code=400, detail="html null")

    image_data = await html_img.html_to_image(html)

    return Response(content=image_data, media_type="image/png")


@app.get("/test")
async def test():
    return {"message": "test"}
