#coding=UTF-8

from sqlalchemy import create_engine,exc
import tushare as ts
import time
from datetime import date,timedelta
import MySQLdb as mariadb
import memcache

cursor = mariadb_connection.cursor()


df_basics = ts.get_stock_basics()
#df_basics = ['603680']

date_list = ['2018-02-22','2018-02-23','2018-02-26','2018-02-27','2018-02-28','2018-03-01','2018-03-02']
#date_list = ['2018-02-23']

for code in df_basics.index.get_values():
#for code in df_basics:
    print code
    for current_date in date_list:
        tb_name = 'hist' + code
        mysql_date = current_date + ' 00:00:00'
#        print mysql_date
        try:
            del_sql = "DELETE FROM %s WHERE date = '%s'" % (tb_name,mysql_date)
            print del_sql
            cursor.execute(del_sql)
            mariadb_connection.commit()
        except mariadb.OperationalError:
            drop_sql = """DROP TABLE IF EXISTS """ + tb_name
            cursor.execute(drop_sql)
        except mariadb.ProgrammingError:
            break
      

