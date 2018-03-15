#!/bin/bash
logfile=/root/robo_test/auto_import.log
importlog=/root/robo_test/stock_import.log
A=`ps -ef|grep 'stocks_import.p[y]' &>/dev/null;echo $?`
if [ $A -eq 1 ]
then
echo `date` >> $logfile
echo "not ok" >> $logfile
sleep 60
nohup /usr/bin/python /root/robo_test/stocks_import.py &>> $importlog &
else
echo "ok" >> $logfile
fi
