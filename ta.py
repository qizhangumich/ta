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

st.title(name)


df= stock.history(ticker, start=start, end=end)
output = ta.SMA(df.Close)
fig, ax = plt.subplots()
ax.plot(df.index,output)
st.pyplot(fig)