from datetime import date,timedelta

#today = datetime.date.today()
today = date.today() - timedelta(days=4)
#today = date.today()
print today
weekday = today.weekday()
print weekday
start_delta = timedelta(days=weekday, weeks=19)
print start_delta
start_of_week = today - start_delta
print start_of_week

#delta_days = today - start_of_week

d1 = today
d2 = start_of_week
monday1 = (d1 - timedelta(days=d1.weekday()))
print monday1
monday2 = (d2 - timedelta(days=d2.weekday()))
print monday2

print 'Weeks:', abs((monday2 - monday1).days) / 7
