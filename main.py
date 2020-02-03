import core
import requests
from datetime import datetime, date, time, timedelta
import handler

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


def displayReserables(mergedSlots):
    for slot in mergedSlots:
        sdtObj = slot.get('startTime')  # start datetime object
        entry = sdtObj.date().isoformat()
        entry += ' ' + sdtObj.time().isoformat()
        entry += ' for ' + \
            str(slot.get('timeLength').total_seconds() / 60) + ' minutes'
        entry += '\nRoom: ' + roomNumber.get(slot.get('number')) + '\n'
        print(entry)


def parseDate(date_):
    if date_ == '0':
        date_ = date.today().isoformat()
    if date_ == '1':
        date_ = (date.today() + timedelta(days=1)).isoformat()
    return date_


def validateDate(date_):
    # valid if later or equal to today
    if date_ == '0':
        date_ = date.today().isoformat()
    if date_ == '1':
        date_ = (date.today() + timedelta(days=1)).isoformat()
    now = datetime.now().date()
    try:
        thisVal = date.fromisoformat(date_)
        return now == thisVal or thisVal > now
    except:
        return False


# Preparation
def main():
    h = handler.Handler()

    date_ = input(
        'The date you want to track '
        '(format: yyyy-MM-dd. "0" to set date to today '
        'and "1" to set date to tomorrow)\n'
    )
    date_ = parseDate(date_)

    while(not validateDate(date_)):
        date_ = input('The date you want to track (format: yyyy-MM-dd)\n')
        date_ = parseDate(date_)

    stime = input(
        'Start time? '
        '(format HH:mm, any invalid format will set this to 00:00\n')
    etime = input(
        'End time? '
        '(format HH:mm, any invalid format will set this to 23:30)\n')

    if not isTimeFormat(stime):
        stime = "00:00"

    if not isTimeFormat(etime):
        etime = "23:30"

    reservables = h.getMergedReservables(date_)
    startAfter = time.fromisoformat(stime)
    startBefore = time.fromisoformat(etime)
    inRangeReservables = filter((lambda x: startAfter < x.get(
        'startTime').time() < startBefore), reservables)

    displayReserables(inRangeReservables)


if __name__ == "__main__":
    main()
