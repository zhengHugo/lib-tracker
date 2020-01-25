import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def getSessionid(session):
    r = session.get('https://booked.concordia.ca/Web/?')
    phpsessid = r.headers['Set-Cookie'].split(";")[0]
    return phpsessid


def login(session, phpsessid):
    login_url = "https://booked.concordia.ca/Web/index.php"
    payload = {
        'email': "Z_YUGU",
        'password': 'HfkexAB0',
        'login': 'submit'
    }

    result = session.post(
        login_url,
        data=payload,
        headers=dict(referer=login_url, cookie=phpsessid)
    )
    return result

# return all the reservable slots on that day and the cookie for future use


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
        startTime = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        length = timedelta(minutes=30)
        reservables.append(
            {'startTime': startTime, 'timeLength': length, 'number': num})
    _cookie = phpsessid + '; ' + _cookie
    return (reservables, _cookie)


def reserve(roomNumber, cookie, stime, etime):
    getPayload = {
        'rid': roomNumber,
        'sid': 1,
        'rd': stime[:10],
        'sd': stime,
        'ed': etime
    }
    r = requests.get(
        'https://booked.concordia.ca/Web/reservation.php',  headers={'Cookie': cookie}, params=getPayload)

    f = open("submit.html", 'w')
    f.write(r.text)
    f.close()

    soup = BeautifulSoup(r.text, 'html.parser')
    scheduledId = soup.find('input', id='scheduleId').get('value')
    resourceId = soup.find('input', class_='resourceId').get('value')
    csrf_token = soup.find('input', id='csrf_token').get('value')

    postPayload = {
        'userId': 42358,
        'beginDate': stime[:10],
        'beginPeriod': stime[11:],
        'endDate': etime[:10],
        'endPeriod': etime[11:],
        'scheduleId': scheduledId,
        'resourceId': resourceId,
        'reservationTitle': '',
        'reservationDescription': '',
        'reservationId': '',
        'referenceNumber': '',
        'reservationAction': 'create',
        'DELETE_REASON': '',
        'seriesUpdateScope': 'full',
        'CSRF_TOKEN': csrf_token
    }

    postUrl = 'https://booked.concordia.ca/Web/ajax/reservation_save.php'
    result = requests.post(postUrl, data=postPayload,
                           headers={'Cookie': cookie})
    return result


# Procedure:
# 1. get php session id (first cookie)
# 2. login. Looks like that the server marks the session as a login status
# 3. a get request to get a new cookie
# 4. try to figure out how booking status data are loaded.


# session = requests.session()

# # get first cookie: phpsession
# phpsessid = getSessionid(session)

# # login to tell the server that this session has logged in
# login(session, phpsessid)

# # in the tbodydate, room are represented by numbers
# (reservables, _cookie) = getReservables('2020-01-14', phpsessid)

# reserveResult = reserve(60, cookie, '2020-01-14 21:00', '2020-01-14 22:00')

# print(reserveResult.text)
