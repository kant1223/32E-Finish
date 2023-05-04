#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 23:29:43 2023

@author: kangyaxiu
"""

###############################
#要刪的東東
# from dotenv import load_dotenv
# load_dotenv()

###########################

import os
import pygsheets
import pandas as pd
from pandas import DataFrame
import math
from flask import Flask, request
import nums_from_string as nfs
import math
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import string   #拿掉標點符號
#時間
from datetime import datetime



import pygsheets
import time
def readdata(new_time,update＿time):
    
    new_time=float(new_time)
    update＿time=float(update＿time)
    try:
        if new_time-update_time>259200:
            file=os.getenv ("file")#權杖位置
            gc = pygsheets.authorize(service_file=file)
            sh = gc.open_by_url(os.getenv ("survey_url"))
            ws = sh.worksheet_by_title("未發貨")   #在哪個工作表作業
            val = ws.get_as_df(start='A1', index_colum=1, empty_value='', include_tailing_empty=False,numerize=False) # index 從 1 開始算
            val.to_csv("mm.txt")
            update_time=new_time
            print("更新完成")
        else:
            
            #print(time.localtime(update＿time))
            x=time.localtime(update＿time)
            print(f'上次更新時間:{str(x.tm_year).zfill(2)}/{str(x.tm_mon).zfill(2)}/{str(x.tm_mday).zfill(2)}  '
                  f'{str(x.tm_hour).zfill(2)}:{str(x.tm_min).zfill(2)}:{str(x.tm_sec).zfill(2)}')
    
    except:
        #new_time=time.time()
        update＿time=1.0
        file=os.getenv ("file")#權杖位置
        gc = pygsheets.authorize(service_file=file)
        sh = gc.open_by_url(os.getenv ("survey_url"))
        ws = sh.worksheet_by_title("未發貨")   #在哪個工作表作業
        val = ws.get_as_df(start='A1', index_colum=1, empty_value='', include_tailing_empty=False,numerize=False) # index 從 1 開始算
        val.to_csv("mm.txt")        
        print("初始化完成")
    return [new_time,update＿time]














def to_google_sheet(json_data,profile_date):

    msg_time=json_data['events'][0]['timestamp']+28800000
    msg_time=pd.to_datetime(msg_time, unit='ms')
    json_data=json_data
    if json_data['events'][0]['type'] == 'follow':
        x=[json_data['events'][0]['source']['userId'],str(msg_time),json_data['events'][0]['type']]
        df_j=pd.DataFrame(x)
        df_j=df_j.T
        df_j.columns = ['userId','time',"type"]
        
    else:
        m_type=json_data['events'][0]['message']['type']
        if m_type == "text":
            msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
            x=[json_data['events'][0]['source']['userId'],str(msg_time),json_data['events'][0]['message']['type'],
           json_data['events'][0]['message']['text']]
            df_j=pd.DataFrame(x)
            df_j=df_j.T
            df_j.columns = ['userId','time',"type","text"]
        else:
            x=[json_data['events'][0]['source']['userId'],str(msg_time),json_data['events'][0]['message']['type']]
            df_j=pd.DataFrame(x)
            df_j=df_j.T
            df_j.columns = ['userId','time','type']

    profile_date=profile_date
    df_p=pd.DataFrame([profile_date])
    out=pd.merge(df_p, df_j,how='outer',on="userId")
    #讀取google sheet資料
    file=os.getenv ("file")
    survey_url = os.getenv ("survey_url")
    gc = pygsheets.authorize(service_file=file)
    sh = gc.open_by_url(survey_url)
    ws = sh.worksheet_by_title("使用紀錄")   #在哪個工作表作業
    df = ws.get_as_df(start='A1', empty_value='', include_tailing_empty=False,numerize=False) # index 從 1 開始算


    ##############

    df=pd.concat([df, out], ignore_index=True)
    df=df.set_index('displayName')
    
    #DataFrame(df).to_excel(save_addres, sheet_name=read_sheet, index=False, header=True)
#     寫回google sheet
    ws = sh.worksheet_by_title('使用紀錄')   #寫在哪個工作表
#     ws.update_value('A1', 'test')         #寫入位置,內容
    ws.set_dataframe(df, 'A1', copy_index=True, nan='')






 
    
def trial_calculation(msg,name):
    key_word=["運費","商品價格"]
    total=1
    #out_msg= name + "您好：\n請輸入運費及商品價格\n如：運費50商品價格168"
    for i in key_word:
        if i in msg:
            msg1 = msg.partition(i)
            x = list(msg1)
            x.sort()
            number_list = nfs.get_nums(x[x.index(i)-1])
            #print("x1",x,"i",i,number_list)

            if len(number_list)==1:
                number_list.append(nfs.get_nums(x[0]))
             #   print("number_list2",number_list)
                asum = number_list[1][0]+number_list[0]
                total=asum *4.8*1.1
                total=math.ceil(total)
                out_msg= name + "您好：\n您試算的金額如下\n(大陸運費(人民幣)：" + str(number_list[1][0]) + "\n+商品價格(人民幣))：" + str(number_list[0]) + "\n*匯率*4.8\n+手續費一成=" + str(total)
                break
            if number_list == []:
                number_list = nfs.get_nums(x[x.index(i)-2])
                asum = sum(number_list)
                total=asum *4.8*1.1
                total=math.ceil(total)
                out_msg= name + "您好：\n您試算的金額如下\n(大陸運費(人民幣)：" + str(number_list[0]) + "\n+商品價格(人民幣))：" + str(number_list[1]) + "\n*匯率*4.8\n+手續費一成=" + str(total)
                break

            if len(number_list)==2:
               # y = number[x.index(i)-1]
                print("x2",x,"i",i,"number_list",number_list)
                asum = number_list[0]+number_list[1]
                total=asum *4.8 *1.1
                total=math.ceil(total)              
                out_msg= name + "您好：\n您試算的金額如下\n(大陸運費(人民幣)：" + str(number_list[0]) + "\n+商品價格(人民幣))：" + str(number_list[1]) + "\n*匯率*4.8\n+手續費一成=" + str(total)
                break

            else:
                #out_msg= name + "您好：\n請輸入運費及商品價格\n如：運費50商品價格168"
                if i == "運費":
                    number_list.append(nfs.get_nums(x[0]))
              #print("number_list",number_list)
                    asum = number_list[0][0]+number_list[0][1]
                    total=asum *4.8 *1.1
                    total=math.ceil(total)
                    out_msg= name + "您好：\n您試算的金額如下\n(大陸運費(人民幣)："+str(number_list[0][0])+"\n+商品價格(人民幣))：" + str(number_list[0][1]) + "\n*匯率*4.8\n+手續費一成=" + str(total)
                    break
    out_msg=TextSendMessage(out_msg)
    return out_msg
    















