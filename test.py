from main import mergeReservables
from datetime import datetime, timedelta

reservables = [
    {'startTime': datetime(year=2020, month=1, day=17, hour=22, minute=0),
     'timeLength': timedelta(minutes=30), 'number': 20},
    {'startTime': datetime(year=2020, month=1, day=17, hour=22, minute=30),
     'timeLength': timedelta(minutes=30), 'number': 20},
    {'startTime': datetime(year=2020, month=1, day=18, hour=20, minute=00),
     'timeLength': timedelta(minutes=30), 'number': 20}

]

print(mergeReservables(reservables))
# ls = [1, 2, 3, 4]
# remaining = ls[1:]
# print(remaining)
# print([0] + remaining)
