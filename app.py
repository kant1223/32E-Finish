#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:20:15 2023

@author: kangyaxiu≥
"""
from dotenv import load_dotenv
load_dotenv()
import os
import json
import pygsheets
import time
#權杖位置
file = os.getenv ("file")
gc = pygsheets.authorize(service_file=file)
#gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')
survey_url = 'https://docs.google.com/spreadsheets/d/1t-URenLmeFQYxJQhjhHhilm1nNf_TfXXmrrF00kwFlk/edit#gid=0'#試算表ＩＤ
sh = gc.open_by_url(survey_url)
ws = sh.worksheet_by_title('工作表1')   #在哪個工作表作業
val = ws.get_value('A1')#從哪裡讀取
df = ws.get_as_df(start='A1', index_colum=1, empty_value='', include_tailing_empty=False,numerize=False) # index 從 1 開始算
print(df)
time.sleep(60)
print("等了60秒")


#a=os.getenv ("HOME")
#print(a)



