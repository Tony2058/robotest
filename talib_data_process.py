#coding=utf8

import tushare as ts
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import talib

df = ts.get_k_data('603777')
#df = ts.get_k_data('600600',start='2018-03-01', end='2018-03-08')

#df['MA10_rolling'] = df['close'].rolling(10).mean()
#print df
df_open = [float(x) for x in df['open']]
close = [float(x) for x in df['close']]
high = [float(x) for x in df['high']]
low = [float(x) for x in df['low']]
volume = [float(x) for x in df['volume']]
#调用talib计算10日移动平均线的值
#print type(close)
#print type(np.array(close))
df['GAP'] = talib.CDLTASUKIGAP(np.array(df_open), np.array(high), np.array(low), np.array(close))
#df['MA10_talib'] = talib.MA(np.array(close),timeperiod=10) 
#df['MA10_talib'] = talib.MA(close, timeperiod=10) 

# 调用talib计算指数移动平均线的值
#df['EMA12'] = talib.EMA(np.array(close), timeperiod=12)  
#df['EMA26'] = talib.EMA(np.array(close), timeperiod=26)   
# 调用talib计算MACD指标
#df['MACD'],df['MACDsignal'],df['MACDhist'] = talib.MACD(np.array(close),
#                            fastperiod=12, slowperiod=26, signalperiod=9)   
df['DIFF'],df['DEA'],df['MACD'] = talib.MACD(np.array(close),
                            fastperiod=12, slowperiod=26, signalperiod=9)   
#RSI的天数一般是6、12、24
df['MACD'] = df['MACD'] * 2
df['RSI']=talib.RSI(np.array(close), timeperiod=12)    
#df['MOM']=talib.MOM(np.array(close), timeperiod=5)

df['ATR'] = talib.ATR(np.array(high), np.array(low), np.array(close),timeperiod=14)
df['NATR'] = talib.NATR(np.array(high), np.array(low), np.array(close),timeperiod=14)

#df['MFI'] = talib.MFI(np.array(high), np.array(low), np.array(close),np.array(volume),timeperiod=26)
#df['MFR'] = 100 / (100 - df['MFI']) - 1
#print high
#print low
H = talib.MAX(np.array(high), timeperiod=4)
L = talib.MIN(np.array(low), timeperiod=4)
#print H
#print L
#df['SAR'] = talib.SAR(np.array(high),np.array(low), acceleration=0.02, maximum=0.2)
df['SAR'] = talib.SAR(H,L, acceleration=0.02, maximum=0.2)
print df.tail(12)
