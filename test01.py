#coding=UTF-8

from sqlalchemy import create_engine,exc
import tushare as ts
import time
from datetime import date,timedelta
import MySQLdb as mariadb
import memcache

cursor = mariadb_connection.cursor()


#df_basics = ['002929','600901','300741','000410','000760','002279','002402','600410','002184','002577']
df_basics = ['000001']
#date_list = ['2018-02-22','2018-02-23','2018-02-26','2018-02-27','2018-02-28','2018-03-01','2018-03-02']
date_list = ['2018-03-04']

for code in df_basics:
    print code
    for current_date in date_list:
        print current_date
        df = ts.get_h_data(code,start=current_date,end=current_date,pause=5) #一次性获取全部日k线数据
        print df.index.get_values()
        if df.index.get_values():
            print 'It is open today'
        else:
            print 'It is close today'


current_date = str(date.today() - timedelta(days=1))
print current_date
