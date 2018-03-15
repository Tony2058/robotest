#coding=UTF-8

from sqlalchemy import create_engine,exc
import tushare as ts
import time
from datetime import date,timedelta
import MySQLdb as mariadb
import memcache

mariadb_connection = mariadb.connect('localhost','xxxxxxx','xxxxxx','xxxxxx')
cursor = mariadb_connection.cursor()
mc = memcache.Client(['127.0.0.1:11211'],debug=0)
engine = create_engine('mysql://xxxx:xxxxx@127.0.0.1/xxxxx?charset=utf8')

def GetDailyData(date):
    df_basics = ts.get_stock_basics()
    for code in df_basics.index.get_values():
        print code
        tb_name = 'hist' + code
        mc_key = code + date
        mc_value = code + ' ' + date + ' is done'
        value = mc.get(mc_key)
        if value:
            print value
        else:
            print 'key not exist!'
            df = ts.get_h_data(code,start=date,end=date,pause=5) #一次性获取全部日k线数据
            try:
            #追加数据到现有表
                df.to_sql(tb_name,engine,if_exists='append')
            except exc.SQLAlchemyError:
                drop_sql = """DROP TABLE IF EXISTS """ + tb_name
                cursor.execute(drop_sql)
                df.to_sql(tb_name,engine,if_exists='append')
            mc.set(mc_key,mc_value)
            time.sleep(2)
        print " "


#Check the A shares open or close
#date_list = ['2018-02-22','2018-02-23','2018-02-26','2018-02-27','2018-02-28','2018-03-01','2018-03-02']
#date_list = ['2018-03-07']
#current_date = date_list[0]
yesterday_date = str(date.today() - timedelta(days=1))
df = ts.get_h_data('000001',start=yesterday_date,end=yesterday_date,pause=5) #一次性获取全部日k线数据
print df.index.get_values()
if df.index.get_values():
    print 'It is open today'
    GetDailyData(yesterday_date)
else:
    print 'It is close today'

