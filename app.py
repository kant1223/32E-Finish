#!/usr/bin/env python
# coding: utf-8
from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

access_token = '8zp872p8zjIBjP89c4dtoPewB239ZuOuA62gIShbHcMuBBvssLb8f2fep9rFmVMGh5TBVgoo55L7S0KDYzNgy0+NGvmieYfx7DwunGMlmKefVPjWo0MPrpS3mMDCoAagqJCHIhbKoTRMjbbhx8BTKwdB04t89/1O/w1cDnyilFU='
secret = '575a9bb8ae3a9aa680e0dfb69f5f2750'
app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'

if __name__ == "__main__":
    app.run()
    #run_with_ngrok(app)
    #app.run(host='0.0.0.0', port=5000)

#import os
#if __name__ == "__main__":
 #   port = int(os.environ.get('PORT', 5000))
  #  app.run(host='0.0.0.0', port=port)




