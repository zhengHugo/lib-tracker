import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def getReservables(date, phpsessid):
    # date in the query parameter
    payload = {'sid': 1, 'sd': date}

    r = requests.get(
        'https://booked.concordia.ca/Web/schedule.php', headers={'Cookie': phpsessid}, params=payload)

    # store the response for debug
    f = open("page.html", 'w')
    f.write(r.text)
    f.close()

    f = open("debug.log", 'w')
    f.write('getReservable() Response Headers: \n')
    f.write(str(r.headers))
    f.close()

    # get the new cookie and modify for some reason
    _cookie = r.headers['Set-Cookie']
    _cookie = _cookie.split(';')[0]
    _cookie += '; schedule_calendar_toggle=false'

    # get the tbody data for the html parser
    soup = BeautifulSoup(r.text, 'html.parser')
    reservableSlots = soup.find_all('td', class_='reservable clickres slot')
    reservables = []
    for x in reservableSlots:
        ref = x['ref']
        year = ref[:4]
        month = ref[4:6]
        day = ref[6:8]
        hour = ref[8:10]
        minute = ref[10:12]
        num = ref[14:]
        startTime = datetime(year=int(year), month=int(
            month), day=int(day), hour=int(hour), minute=int(minute))
        length = timedelta(minutes=30)
        reservables.append(
            {'startTime': startTime, 'timeLength': length, 'number': num})
    _cookie = phpsessid + '; ' + _cookie
    return (reservables, _cookie)
