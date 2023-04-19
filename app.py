#!/usr/bin/env python
# coding: utf-8
import os

from flask import Flask
from linebot import LineBotApi, WebhookHandler

app = Flask(__name__)

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

# 利用 handler 處理 LINE 觸發事件
from linebot.models import MessageEvent, TextMessage, TextSendMessage

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"Hello {line_bot_api.get_profile(event.source.user_id).display_name}!")
    )

# 利用 route 處理路由
from flask import request, abort
from linebot.exceptions import InvalidSignatureError

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'