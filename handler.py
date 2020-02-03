import requests
import query


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

    def getAllReservables(self, date):
        (result, self.cookie) = query.getReservables(date, self.phpsessid)
        return mergeReservables(result)

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
