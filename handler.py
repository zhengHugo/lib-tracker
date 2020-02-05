import requests
import query
from bs4 import BeautifulSoup


class Handler:
    session = ''
    phpsessid = ''
    cookie = ''

    def __init__(self):
        self.session = requests.session()
        self.phpsessid = self.getSessionid()
        self.login()

    def getSessionid(self):
        r = self.session.get('https://booked.concordia.ca/Web/?')
        return r.headers['Set-Cookie'].split(";")[0]

    def login(self):
        login_url = "https://booked.concordia.ca/Web/index.php"
        payload = {
            'email': "Z_YUGU",
            'password': 'HfkexAB0',
            'login': 'submit'
        }

        result = self.session.post(
            login_url,
            data=payload,
            headers=dict(referer=login_url, cookie=self.phpsessid)
        )
        return result

    def getMergedReservables(self, date):
        (result, self.cookie) = query.getReservables(date, self.phpsessid)
        return mergeReservables(result)

    def reserve(self, roomNumber, stime, etime):
        getPayload = {
            'rid': roomNumber,
            'sid': 1,
            'rd': stime[:10],
            'sd': stime,
            'ed': etime
        }
        r = requests.get(
            'https://booked.concordia.ca/Web/reservation.php',  headers={'Cookie': self.cookie}, params=getPayload)

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
                               headers={'Cookie': self.cookie})
        return result


# class handler ends


def mergeReservables(reservableSlots):
    # merge 30-minutes reservable slots
    if (len(reservableSlots) > 1):
        if (consecutiveSlots(reservableSlots[0], reservableSlots[1])):
            newSlot = {'startTime': reservableSlots[0].get('startTime'), 'timeLength': reservableSlots[0].get(
                'timeLength') + reservableSlots[1].get('timeLength'), 'number': reservableSlots[0].get('number')}
            if (len(reservableSlots) > 2):
                return mergeReservables([newSlot] + reservableSlots[2:])
            else:
                return [newSlot]
        else:
            return [reservableSlots[0]] + mergeReservables(reservableSlots[1:])
    else:
        return reservableSlots


def consecutiveSlots(slot1, slot2):
    # helper function for mergeReservables
    time1 = slot1.get('startTime')
    delta1 = slot1.get('timeLength')
    time2 = slot2.get('startTime')
    number1 = slot1.get('number')
    number2 = slot2.get('number')
    return time2 - time1 == delta1 and number1 == number2
