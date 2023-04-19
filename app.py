#!/usr/bin/env python
# coding: utf-8
secret="18779859a73653b269c4570ab84547c7"
access_token='3YXDrFR52Zba0fPcUrvopYArbbd+T7PbWoEDL7vAlKstKOG98pr+yQmNxBOI621/VXWn0qAh92vvK+x/hCstQYms3zO9qkzkzXE0865iuzBA92LcQD4bxtqXlyakRYrTJ5fJldpXBTXroH/SNZ5xpAdB04t89/1O/w1cDnyilFU='
#from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

app = Flask(__name__)

@app.route("/kevin", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
   # print(json_data)
    try:
        line_bot_api = LineBotApi(secret)
        print(WebhookHandler(access_token))
        handler = WebhookHandler(access_token)
        signature = request.headers['X-Line-Signature']
       # print("ASDF")
        handler.handle(body, signature)
      #  print("AAA")
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        print(tk)
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        print("shit")
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
        print("this")
    except:
        print('error',"/nbody",body)
    return 'OK'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

