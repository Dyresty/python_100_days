import datetime as dt

now = dt.datetime.now()
print(now.year)
print(now.day)
print(now.month)
print(now.date())
print(now.time())
print(now)

date_of_birth = dt.datetime(year = 2001, month = 6, day = 30)
print(date_of_birth)

print(now.weekday())