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
#print volume
#df['VR'] = np.array(volume) * 2

def my_vr(close,volume,timeperiod):
    positive_volume_period_sum = 0
    negative_volume_period_sum = 0
    list_range = timeperiod + 1
    close_period_list = close[1:list_range]     
    volume_period_list = volume[1:list_range]     
    if ( close[1] > close[0] ):
        positive_volume_period_sum += volume[1]
    elif ( close[1] < close[0] ):
        negative_volume_period_sum = volume[1]
    elif ( close[1] == close[0] ):
        positive_volume_period_sum += ( volume[1] / 2 )
        negative_volume_period_sum = volume[1] / 2 
    for i in range(2,list_range):
        if ( close[i] > close[i-1] ):
            positive_volume_period_sum += volume[i]
        elif ( close[i] < close[i-1] ):
            negative_volume_period_sum += volume[i]
        elif ( close[i] == close[i-1] ):
            positive_volume_period_sum += ( volume[i] / 2 )
            negative_volume_period_sum += ( volume[i] / 2 )
    positive_volume_period_list = [1 for i in range(0,timeperiod)]
    positive_volume_period_list.append(positive_volume_period_sum)
    negative_volume_period_list = [1 for i in range(0,timeperiod)]
    negative_volume_period_list.append(negative_volume_period_sum)
    for i in range(list_range,len(close)):
        if ( close[i-timeperiod] > close[i-timeperiod-1] ):
           positive_volume_period_sum -= volume[i-timeperiod]
        elif ( close[i-timeperiod] < close[i-timeperiod-1] ):
           negative_volume_period_sum -= volume[i-timeperiod]
        elif ( close[i-timeperiod] == close[i-timeperiod-1] ):
           positive_volume_period_sum -= ( volume[i-timeperiod] / 2 )
           negative_volume_period_sum -= ( volume[i-timeperiod] / 2 )
        if ( close[i] > close[i-1] ):
            positive_volume_period_sum += volume[i]
        elif ( close[i] < close[i-1] ):
            negative_volume_period_sum += volume[i]
        elif ( close[i] == close[i-1] ):
            positive_volume_period_sum += ( volume[i] / 2 )
            negative_volume_period_sum += ( volume[i] / 2 )
        positive_volume_period_list.append(positive_volume_period_sum)
        negative_volume_period_list.append(negative_volume_period_sum)
    return (positive_volume_period_list,negative_volume_period_list)
    
#df['VR'] = my_vr(np.array(close),np.array(volume),timeperiod=14)
(A,B) = my_vr(np.array(close),np.array(volume),timeperiod=26)
#df['PV'] = np.array(A)
#df['NV'] = np.array(B)
df['VR'] = np.array(A) / np.array(B) * 100
print df.tail(10)
