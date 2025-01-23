"""
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict

class Header(BaseModel):
    eventId: str = Field(..., alias="eventId")
    eventType: str = Field(..., alias="eventType")
    eventTime: int = Field(..., alias="eventTime")

    @field_validator("eventTime")
    def validate_event_time(cls, v):
        if v < 0:
            raise ValueError("eventTime不是整数")
        return v

class Sender(BaseModel):
    senderId: str = Field(..., alias="senderId")
    senderType: str = Field(..., alias="senderType")
    senderUserLevel: str = Field(..., alias="senderUserLevel")
    senderNickname: str = Field(..., alias="senderNickname")

class Chat(BaseModel):
    chatId: str = Field(..., alias="chatId")
    chatType: str = Field(..., alias="chatType")

class Message(BaseModel):
    msgId: str = Field(..., alias="msgId")
    parentId: Optional[str] = Field(None, alias="parentId")
    sendTime: int = Field(..., alias="sendTime")
    chatId: str = Field(..., alias="chatId")
    chatType: str = Field(..., alias="chatType")
    contentType: str = Field(..., alias="contentType")
    content: Dict[str, str] = Field(..., alias="content")

    @field_validator("sendTime")
    def validate_send_time(cls, v):
        if v < 0:
            raise ValueError("sendTime不是整数")
        return v

class Event(BaseModel):
    sender: Sender = Field(..., alias="sender")
    chat: Chat = Field(..., alias="chat")
    message: Message = Field(..., alias="message")

class MainModel(BaseModel):
    version: str = Field(..., alias="version")
    header: Header = Field(..., alias="header")
    event: Event = Field(..., alias="event")