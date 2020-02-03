from datetime import time

# reservables = [
#     {'startTime': datetime(year=2020, month=1, day=17, hour=22, minute=0),
#      'timeLength': timedelta(minutes=30), 'number': 20},
#     {'startTime': datetime(year=2020, month=1, day=17, hour=22, minute=30),
#      'timeLength': timedelta(minutes=30), 'number': 20},
#     {'startTime': datetime(year=2020, month=1, day=18, hour=20, minute=00),
#      'timeLength': timedelta(minutes=30), 'number': 20}

# ]
stime = '12:00'
etime = '23:30'

startAfter = time.fromisoformat(stime)
startBefore = time.fromisoformat(etime)
print(type(startAfter))
# ls = [1, 2, 3, 4]
# remaining = ls[1:]
# print(remaining)
# print([0] + remaining)
