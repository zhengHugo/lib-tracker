import core
import requests
from datetime import datetime, date, time, timedelta
from functools import reduce


roomNumber = {
    '61': 'Webster Library LB-251 (Luxembourg)',
    '62': 'Webster Library LB-257 (Croatia)',
    '63': '***NO HDMI CONNECATION*** Webster Library LB-259 (New Zealand)',
    '53': 'Webster Library LB-351 (Netherlands)',
    '54': 'Webster Library LB-353 (Kenya)',
    '55': 'Webster Library LB-359 (Vietnam)',
    '6': 'Webster Library LB-451 (Brazil)',
    '5': 'Webster Library LB-453 (Japan)',
    '4': 'Webster Library LB-459 (Italy)',
    '58': 'Webster Library LB-518 (Ukraine)',
    '57': 'Webster Library LB-520 (South Africa) - Consultation Room',
    '56': 'Webster Library LB-522 (Peru)',
    '59': 'Webster Library LB-547 (Lithuania)',
    '60': 'Webster Library LB-583 (Poland)'
}


def isTimeFormat(input):
    try:
        time.fromisoformat(input)
        return True
    except ValueError:
        return False


def consecutiveSlots(slot1, slot2):
    time1 = slot1.get('startTime')
    delta1 = slot1.get('timeLength')
    time2 = slot2.get('startTime')
    number1 = slot1.get('number')
    number2 = slot2.get('number')
    return time2 - time1 == delta1 and number1 == number2

    # if (time2-time1) == delta1:
    #     return (time1, delta1 + delta2)

# return time slots in the format of (startTime, timedelta)


# merge the half-hour reservable chunks, for display purpose only
def mergeReservables(reservableSlots):
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


def displayMerged(mergedSlots):
    for slot in mergedSlots:
        sdtObj = slot.get('startTime')  # start datetime object
        entry = sdtObj.date().isoformat()
        entry += ' ' + sdtObj.time().isoformat()
        entry += ' for ' + \
            str(slot.get('timeLength').total_seconds() / 60) + 'minutes'
        entry += '\nRoom: ' + roomNumber.get(slot.get('number')) + '\n'
        print(entry)


def validateDate(date_):
    # valid if later or equal to today
    if date_ == 'today':
        date_ = date.today().isoformat()

    now = datetime.now().date()
    try:
        thisVal = date.fromisoformat(date_)
        return now == thisVal or thisVal > now
    except:
        return False


# Preparation
def main():
    session = requests.session()
    phpsessid = core.getSessionid(session)
    core.login(session, phpsessid)

    date_ = input(
        'The date you want to track (format: yyyy-MM-dd or "today" to set date to today)\n')

    while(not validateDate(date_)):
        date_ = input('The date you want to track (format: yyyy-MM-dd)\n')

    stime = input(
        'Start time? (format HH:mm, any invalid format will set this to default value\n')
    etime = input(
        'End time? (format HH:mm, any invalid format will set this to default value)\n')

    if not isTimeFormat(stime):
        stime = "00:00"

    if not isTimeFormat(etime):
        etime = "23:30"

    (reservables, cookie) = core.getReservables(date_, phpsessid)

    displayMerged(mergeReservables(reservables))

    # reserveResult = core.reserve(
    #     60, cookie, '2020-01-14 21:00', '2020-01-14 22:00')


if __name__ == "__main__":
    main()
