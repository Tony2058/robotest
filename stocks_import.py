#coding=UTF-8

from sqlalchemy import create_engine
import tushare as ts
import time
import MySQLdb as mariadb

mariadb_connection = mariadb.connect('localhost','xxxxxxx','xxxxxx','xxxxxx')
cursor = mariadb_connection.cursor()

df_basics = ts.get_stock_basics()
for code in df_basics.index.get_values():
    print code
    tb_name = 'hist' + code
    cursor.execute("show tables like '%s'" % (tb_name))
    if cursor.fetchall():
        continue
    else:
        df = ts.get_h_data(code,start='2008-02-10',end='2018-02-14',pause=5) 
        engine = create_engine('mysql://xxxx:xxxxx@127.0.0.1/xxxxx?charset=utf8')
        df.to_sql(tb_name,engine)
        print " "
    #    time.sleep(2)

