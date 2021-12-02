# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:54:42 2021

@author: ZhangQi
"""


 
 
import yfinance as yf
import datetime as dt
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import streamlit as st
import requests
import os
import sys
import subprocess

# check if the library folder already exists, to avoid building everytime you load the pahe
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("ls -la /app/equity/")
    # build
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    # install
    os.system("make install")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/lib/", "--global-option=-I/home/appuser/include/", "ta-lib"])
finally:
    import talib

import talib as ta
df_cc = pd.read_csv("china_concept.csv",encoding="GB2312")
tickers = list(df_cc.Ticker2)
names = list(df_cc.Name)

years = [2021]
months = list(range(1,13))
days = list(range(1,31))
periods = [10,20,30]


ticker = st.sidebar.selectbox(
    '常关注的一些股票代码：',
     tickers)   

year = st.sidebar.selectbox(
    '选择开始的年份：一般选择2021年',
     years)  

month = st.sidebar.selectbox(
    '选择开始的月份',
     months) 

day = st.sidebar.selectbox(
    '选择开始的日期',
     days) 

period = st.sidebar.selectbox(
    '选择多少天作为基准来计算区间--一般选择20天',
     periods) 

start = dt.datetime(year, month, day)
end = date.today()

stock = yf.Ticker(ticker)
info = stock.info

name = names[tickers.index(ticker)]

#st.title(name)


df= stock.history(ticker, start=start, end=end)
macd,signal,hist =ta.MACD(df.Close, fastperiod=12, slowperiod=26,signalperiod=9)
condition = (macd>=signal) & (macd>0)

fig_1, ax = plt.subplots(2,figsize=(14, 6), facecolor='0.9')
ax[0].plot(df.index,macd,label="DIF_fast")
ax[0].plot(df.index,signal,label="DEA_slow")
ax[0].bar(df.index,hist,label="hist")
ax[0].fill_between(df.index,macd,signal,where=condition>0,color='green', alpha=0.2)
ax[0].plot([df.index[0],df.index[-1]],[0,0],"r")
#ax[0].plot([df.index[0],df.index[-1]],[20,20],"k")
ax[0].legend()

ax[1].plot(df.index,df.Close,"b.-",label="Close")
ax[1].legend()

up,mid,low =ta.BBANDS(df.Close, timeperiod=period, nbdevup=2,nbdevdn=2,matype=0)
fig_2, axe = plt.subplots(figsize=(14, 6), facecolor='0.9')
#axe.plot(df.index,up,label="upperband")
#axe.plot(df.index,mid,label="middleline")
#axe.plot(df.index,low,label="lowerband")
axe.fill_between(df.index,up,low,color='green', alpha=0.2)
axe.plot(df.index,df.Close,"black",label="Close")

st.title(name)
st.pyplot(fig_1)
st.pyplot(fig_2)
