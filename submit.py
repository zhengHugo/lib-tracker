import requests


cookie = 'PHPSESSID=4i33q8c89e9ria6e2iot9bj382; resource_filter1=%7B%22ScheduleId%22%3A%221%22%2C%22ResourceIds%22%3A%5B%5D%2C%22ResourceTypeId%22%3Anull%2C%22MinCapacity%22%3Anull%2C%22ResourceAttributes%22%3A%5B%5D%2C%22ResourceTypeAttributes%22%3A%5B%5D%7D; schedule_calendar_toggle=false'

payload = {
    'rid': 57,
    'sid': 1,
    'rd': '2020-01-05',
    'sd': '2020-01-05 15:30:00',
    'ed': '2020-01-05 16:30:00'
}
r = requests.get(
    'https://booked.concordia.ca/Web/reservation.php',  headers={'Cookie': cookie}, params=payload)

f = open("submit.html", 'w')
f.write(r.text)
f.close()

# request url: https://booked.concordia.ca/Web/ajax/reservation_save.php
# form data saved on the desktop
# crsf_token is hidden in the html file
# scheduleId and resourceId are all hidden in the html file
