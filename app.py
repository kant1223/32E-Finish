#!/usr/bin/env python
# coding: utf-8
#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT


#from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(os.getenv('access_token'))
    #    line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(os.getenv('secret'))                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'

import os
if __name__ == "__main__":
 #   app.run()
    port=5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)