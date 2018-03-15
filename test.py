#coding=UTF-8

from sqlalchemy import create_engine,exc
import tushare as ts
import time
from datetime import date,timedelta
import MySQLdb as mariadb
import memcache

cursor = mariadb_connection.cursor()


#df_basics = ts.get_stock_basics()
#df_basics = ['002929','600901','300741','000410','000760','002279','002402','600410','002184','002577']
df_basics = ['002577']
#for code in df_basics.index.get_values():
mc = memcache.Client(['127.0.0.1:11211'],debug=0)
#mc.delete('0025772018-02-24')
#mc.delete('0025772018-02-25')
#mc.delete('0025772018-02-26')
#mc.delete('0025772018-02-27')
#mc.delete('0025772018-02-28')

for code in df_basics:
    print code
    tb_name = 'hist' + code
    for i in range(8,0,-1):
        current_date = str(date.today() - timedelta(days=i))
        mc_key = code + current_date
        mc_value = code + ' ' + current_date + ' is done'
        value = mc.get(mc_key)
        if value:
            print value
        else:
            df = ts.get_h_data(code,start=current_date,end=current_date,pause=5) #一次性获取全部日k线数据
            try:
            #追加数据到现有表
                df.to_sql(tb_name,engine,if_exists='append')
            except exc.SQLAlchemyError:
                drop_sql = """DROP TABLE IF EXISTS """ + tb_name
                cursor.execute(drop_sql)
                df.to_sql(tb_name,engine,if_exists='append')
            print 'key not exist!'
#            mc.set(mc_key,mc_value)
    
