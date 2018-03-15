#coding=UTF-8

from sqlalchemy import create_engine
import tushare as ts

df_basics = ts.get_stock_basics()
for code in df_basics.index.get_values():
    print code
    cons =  ts.get_apis()
    df = ts.bar(code,conn=cons,start_date='2008-02-10',end_date='2018-02-14',freq='D') 
    engine = create_engine('mysql://xxxx:xxxxx@127.0.0.1/xxxxxxx?charset=utf8')
    tb_name = 'hist' + code
    df.to_sql(tb_name,engine)
    print " "

