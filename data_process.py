#coding=UTF-8

from sqlalchemy import create_engine,exc
import tushare as ts
import time
from datetime import date,timedelta
import MySQLdb as mariadb
import memcache

mariadb_connection = mariadb.connect('localhost','xxxxxxx','xxxxxx','xxxxxx')
cursor = mariadb_connection.cursor()


#df_basics = ['002929','600901','300741','000410','000760','002279','002402','600410','002184','002577']
df_basics = ['000878']
#test_code = '002929'
test_code = '000878'
date_list = ['2018-02-26','2018-02-27','2018-02-28','2018-03-01','2018-03-02']
#date_list = ['2018-03-05']

#for code in df_basics:
#    print code
#    for current_date in date_list:
#        #print current_date
#        #df = ts.get_h_data(code,start=current_date,end=current_date,pause=5) #一次性获取全部日k线数据
#        df = ts.get_hist_data(code,start=current_date,end=current_date,pause=5) #一次性获取全部日k线数据
#        p_change = df.iloc[0]['p_change']
#        print 'The date is %s , and the p_change is %s' %(current_date,p_change)

def CalStartOfWeek(weeksNum):
    today = date.today() - timedelta(days=4)
    weekday = today.weekday()
    start_delta = timedelta(days=weekday, weeks=weeksNum-1)
    start_of_week = today - start_delta
    return start_of_week

def CalAvgChange(code,days):
    tb_name = 'hist'+code
    mysql_num = days + 1
    cursor.execute("select close from %s order by date desc limit 0,%s" % (tb_name,mysql_num))
    p_change_list = []
    for close in cursor.fetchall():
        p_change_list.append(close[0])
    if len(p_change_list) == days + 1:
        p_change_sum = 0
        for num in range(1,len(p_change_list)):
            p_change = (p_change_list[num-1] - p_change_list[num]) / p_change_list[num] * 100
            p_change_sum += p_change
        p_change_avg = p_change_sum / (len(p_change_list) - 1)
        print 'The amount of increase of ' + code +' during ' + str(days) +'D' + ' is ' + "%.2f" % (p_change_avg)
    else:
        print 'The amount of increase of ' + code +' during ' + str(days) +'D' + ' is ' + 'None'

def CalDailyMA(code,days):
    tb_name = 'hist'+code
    cursor.execute("select close from %s order by date desc limit 0,%s" % (tb_name,days))
    daily_MA_list = []
    for close in cursor.fetchall():
        daily_MA_list.append(close[0])
    if len(daily_MA_list) == days:
        daily_MA_avg = sum(daily_MA_list) / len(daily_MA_list)
        print 'The daily MA of ' + code +' during ' + str(days) +'D' + ' is ' + "%.2f" % (daily_MA_avg)
    else:
        print 'The daily MA of ' + code +' during ' + str(days) +'D' + ' is ' + 'None'

def CalWeeklyMA(code,weeks):
    tb_name = 'hist'+code
    start_of_week = CalStartOfWeek(weeks)
    mysql_date = str(start_of_week) + ' 00:00:00'
    cursor.execute("select close from %s where date >= '%s'" % (tb_name,mysql_date))
    weekly_MA_list = []
    for close in cursor.fetchall():
        weekly_MA_list.append(close[0])
    weekly_MA_avg = sum(weekly_MA_list) / len(weekly_MA_list)
    print 'The weekly MA of ' + code +' during ' + str(weeks) +'W' + ' is ' + "%.2f" % (weekly_MA_avg)
         
         
def CalDailyHigh(code,days):
    tb_name = 'hist'+code
    cursor.execute("select high from %s order by date desc limit 0,%s" % (tb_name,days))
    daily_high_list = []
    for high in cursor.fetchall():
        daily_high_list.append(high[0])
    if len(daily_high_list) == days:
        daily_high = max(daily_high_list)
        print 'The daily high of ' + code +' during ' + str(days) +'D' + ' is ' + "%.2f" % (daily_high)
    else:
        print 'The daily high of ' + code +' during ' + str(days) +'D' + ' is ' + 'None'


def CalDailyLow(code,days):
    tb_name = 'hist'+code
    cursor.execute("select low from %s order by date desc limit 0,%s" % (tb_name,days))
    daily_low_list = []
    for low in cursor.fetchall():
        daily_low_list.append(low[0])
    if len(daily_low_list) == days:
        daily_low = min(daily_low_list)
        print 'The daily low of ' + code +' during ' + str(days) +'D' + ' is ' + "%.2f" % (daily_low)
    else:
        print 'The daily low of ' + code +' during ' + str(days) +'D' + ' is ' + 'None'

def CalWeeklyHigh(code,weeks):
    tb_name = 'hist'+code
    start_of_week = CalStartOfWeek(weeks)
    mysql_date = str(start_of_week) + ' 00:00:00'
    cursor.execute("select high from %s where date >= '%s'" % (tb_name,mysql_date))
    weekly_high_list = []
    for high in cursor.fetchall():
        weekly_high_list.append(high[0])
    weekly_high = max(weekly_high_list)
    print 'The weekly high of ' + code +' during ' + str(weeks) +'W' + ' is ' + "%.2f" % (weekly_high)

def CalWeeklyLow(code,weeks):
    tb_name = 'hist'+code
    start_of_week = CalStartOfWeek(weeks)
    mysql_date = str(start_of_week) + ' 00:00:00'
    cursor.execute("select low from %s where date >= '%s'" % (tb_name,mysql_date))
    weekly_low_list = []
    for low in cursor.fetchall():
        weekly_low_list.append(low[0])
    weekly_low = min(weekly_low_list)
    print 'The weekly low of ' + code +' during ' + str(weeks) +'W' + ' is ' + "%.2f" % (weekly_low)



PriceChangeRatioDays_list = [1,3,5,10,20,30,50,60,100,200]
for period in PriceChangeRatioDays_list:
    CalAvgChange(test_code,period)

DailyMaDays_list = [5,10,20,30,50,60,100,200]
for period in DailyMaDays_list:
    CalDailyMA(test_code,period)

WeeklyMaDays_list = [20,50,100,200]
for period in WeeklyMaDays_list:
    CalWeeklyMA(test_code,period)

DailyHighDays_list = [5,10,20,30,50,60,100,200]
for period in DailyHighDays_list:
    CalDailyHigh(test_code,period)

DailyLowDays_list = [5,10,20,30,50,60,100,200]
for period in DailyLowDays_list:
    CalDailyLow(test_code,period)

WeeklyHighDays_list = [20,50,100,200]
for period in WeeklyHighDays_list:
    CalWeeklyHigh(test_code,period)

WeeklyLowDays_list = [20,50,100,200]
for period in WeeklyLowDays_list:
    CalWeeklyLow(test_code,period)




















