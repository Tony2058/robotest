#!/bin/bash
logfile=/root/robo_test/auto_import_daily.log
importlog=/root/robo_test/stock_import_daily.log
A=`ps -ef|grep 'stocks_daily_append.p[y]' &>/dev/null;echo $?`
if [ $A -eq 1 ]
then
echo `date` >> $logfile
echo "not ok" >> $logfile
sleep 30
nohup /usr/bin/python /root/robo_test/stocks_daily_append.py &> $importlog &
else
echo "ok" >> $logfile
fi
