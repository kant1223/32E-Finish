#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:20:15 2023

@author: kangyaxiu≥
"""
######
#要刪的東東
from dotenv import load_dotenv
load_dotenv()
########
from flask import Flask, request
import json

import os
import pandas as pd
import pygsheets


# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import string   #拿掉標點符號
import pandas as pd



import time

import fun #載入函數褲

##參數設定
key_word=["貨況：","貨況查詢：","貨况查询","運費","商品價格"]
welcome_message="""你好٩(˃̶͈̀௰˂̶͈́)و
感謝你使用抱米香價格試算及貨況查詢功能
以下將介紹使用方式

1價格試算
請輸入「運費及商品價格」
如：運費50商品價格168

2貨況查詢
請輸入貨況查詢+姓名＋身分證末四碼
如：貨況查詢宋亞軒2468

🌟目遣僅能查到下單最久但還沒發貨的兩筆訂單，之後會開發可以查詢所有訂單！
🌟貨況將於每週日晚上10.更新
🌟4/1前下單的一律無法查詢
🌟若是從自己的app或高會下單的務必確認是否回報單號，否則容易造成貨況誤差

若有其他問題歡迎私訊抱米香官方帳號詢問～"""


menu="""你好～目前輸入的格式可能有誤，麻煩你再確認一下呦

1.價格試算
請輸入「運費及商品價格」
如：運費50商品價格168

2.貨況查詢
請輸入貨況查詢+姓名＋身分證末四碼
如：貨況查詢宋亞軒2468

🌟目遣僅能查到下單最久但還沒發貨的兩筆訂單，之後會開發可以查詢所有訂單若是用自己的高會下單的話務必要記得先回報單號喔～
🌟若是仍然查訊不到可能是因為還沒有更新，更新時間為每週日晚上10點！！
🌟4/1前下單的一律無法查詢
🌟若是從自己的app或高會下單的務必確認是否回報單號，否則容易造成貨況誤差

若有其他問題歡迎私訊抱米香官方帳號詢問～"""






#版本1.0.4

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    print("開始執行")
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    
    
    
    x=open("v.txt","r")
    data = x.read()
    data_into_list = data.split("\n")
    x.close()
    y=fun.readdata(time.time(),data_into_list[1])

    f=open("v.txt","w")
    data_into_list = [str(y[0])+"\n", str(y[1])]
    f.writelines(data_into_list)
    f.close()
    
    
    
    df = pd.read_csv("mm.txt")
    df.index = [df.iloc[:,0]]  #自訂索引值columns = [df.iloc[:,1]]  #自訂欄位名稱

    for i in df.keys():
        df[i]=df[i].apply(str)
    
    
    

    
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        line_bot_api = LineBotApi(os.getenv ("access_token"))              # 確認 token 是否正確
        print("token正確")

        handler = WebhookHandler(os.getenv ("secret"))                     # 確認 secret 是否正確
        print("secret正確")
        try: 
            if json_data['events'][0]['type']=='unfollow':
                x=[json_data['events'][0]['source']['userId'],
                    str(pd.to_datetime(json_data['events'][0]['timestamp']+28800000, unit='ms')),
                    json_data['events'][0]['type']]
                df_j=pd.DataFrame(x)
                df_j=df_j.T
                df_j.columns = ['userId','time',"type"]
                #    df.append(df_j)
                #從google抓使用紀錄
                file=os.getenv ("file")#權杖位置
                gc = pygsheets.authorize(service_file=file)
                survey_url = os.getenv ("survey_url")
                sh = gc.open_by_url(survey_url)
                ws = sh.worksheet_by_title('使用紀錄')   #在哪個工作表作業

                df1 = ws.get_as_df(start='A1', index_colum=1, empty_value='', include_tailing_empty=False,numerize=False) # index 從 1 開始算

                df1=pd.concat([df1,df_j],axis=0)

                ws.set_dataframe(df1, 'A1', copy_index=True, nan='')
        except:
            pass
        json_data = json.loads(body)                         # json 格式化訊息內容

        line_bot_api = LineBotApi(os.getenv ("access_token"))              # 確認 token 是否正確

        handler = WebhookHandler(os.getenv ("secret"))                     # 確認 secret 是否正確

        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        print("取得回傳訊息的 Token")
        userid=json_data['events'][0]["source"]['userId']     #取得回傳訊息的 userId
       # print("取得回傳訊息的 userId",type(userid),userid)
   #     line_bot_api = LineBotApi(os.getenv ("access_token"))
    #    print("再次取得 token")
        profile = line_bot_api.get_profile(userid)            #取得相關資訊(姓名,照片,個簽,id)
        print("取得個人包相關資訊")
        profile = str(profile)

        profile_date = json.loads(profile)                     #包裹轉字典

        pictureUrl = profile_date['pictureUrl']                 #取得使用者照片

        #statusMessage = profile_date['statusMessage']
        name = profile_date['displayName']                    #取得使用者姓名
        #print("profile",profile)
        #print("json_data",json_data)
        #print("使用者姓名:",name,"\n使用者使用者id:",userid,"\n照片：",pictureUrl)
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
#        print("json_data",json_data)
 #       print("profile_date",profile_date)
        #print("資料型態：")                                    #  line 回傳為回傳為格式是格式是str
        #m_type=json_data['events'][0]['message']['type']
        #print("m_type",m_type)
        if json_data['events'][0]['type'] == 'follow':               #如果是新的好友     
            out_msg=TextSendMessage(name+welcome_message) #傳送歡迎訊息
        else:
          
            m_type=json_data['events'][0]['message']['type']
            if m_type == "text":
                msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        #        print("該死的行號226")
                out_msg=TextSendMessage(name+menu)
                
                try:
        #####貨況查詢#####貨況查詢####貨況查詢###貨況查詢######貨況查詢#####
                    
                    msg = msg.translate(str.maketrans('',""," "+'；，。：'+string.punctuation))
                    key_word=["貨況","貨況查詢","貨况查询"]
                    for i in key_word:
                        if i in msg:
                            msg1 = msg.partition(i)
                            y = list(msg1)
                            name_id = y[y.index(i)+1]
                    x=df.loc[[name_id][:]]#抓取消費紀錄
                    if x.shape[0] >=10:              #計算消費次數,大於2顯示前三筆,小於2顯示全部
                        x=x.iloc[:10]
                    else:
                        x=x.iloc[:]
                    y=x.drop(["姓名+身分證末四碼",'身分證末四碼',"圖片名稱","身份證字號"], axis=1)           #刪除不需要的欄位
                    columns_list = y.columns.values.tolist()        #將表頭設成list
                    z=x["圖片名稱"].values.tolist()                #圖片名稱轉list
                    
                    # print("這裡2")
                    #抓取單筆資料放入list
                    shoppy_list=[]
                    a=""
                    c=""
                    for j in range(y.shape[0]):
                        for i in range(len(y.iloc[j,:])):
                            if i == y.shape[1]-1:
                                #c+=columns_list[i]+":"+str(y.iloc[j,i])
                                a=c
                                shoppy_list.append(a)
                                c=""
                            else:
                                c+=columns_list[i]+":"+str(y.iloc[j,i])+"\n"
                    asd=[]
                    # print("這裡3")
                    for i in range(y.shape[0]):
                        c=CarouselColumn(
                            thumbnail_image_url=z[i],
                            title=x.iloc[0][2],
                            text=f'商品名稱:{y["商品名稱"][i]}\n貨物狀況:{y["貨物狀況"][i]}',
                            actions=[
                                PostbackAction(
                                    label='點我觀看該筆消費紀錄',
                                    display_text=shoppy_list[i],
                                    data='action=buy&itemid=1'
                                 ),URIAction(
                        label='點我看商品放大圖',
                        uri=x["圖片名稱"][i]
                                )])
                        asd.append(c)
                    # print("這裡4")
                    out_msg = TemplateSendMessage(
                        alt_text='您於抱米香的消費紀錄',
                        template=CarouselTemplate(image_aspect_ratio='rectangle',image_size='contain',
                                                  columns=asd))
                    
#####
                except:
                    
                    pass
                
                try:
                    out_msg=fun.trial_calculation(msg,name)
                except:
                    pass
                
            else:
                out_msg=TextSendMessage(menu)
                #print(menu)

        print("245/249快跑完了")
        line_bot_api.reply_message(tk,out_msg)# 回傳訊息
        print("已經回傳訊息")
        fun.to_google_sheet(json_data,profile_date)
        print("存檔完成")
        print("_____________________________________________________________")
        print("伺服器接收到的訊息:\n", msg ,"\n使用者姓名：", name)                                       # 印出接收到的內容
        print("伺服器傳送的訊息:\n", out_msg ,"\n使用者姓名：", name)                        #輸出的訊息
        print("_____________________________________________________________")
    except:
        print("錯誤",body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    

















