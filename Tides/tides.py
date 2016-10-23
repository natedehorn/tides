import datetime
import tc

NOW = datetime.datetime.now()
CHARLESTON = tc.Station('SCarolina', '8665099')

STATION = CHARLESTON
tides = tc.Tides(STATION, tc.Date(NOW.day, NOW.month, NOW.year))

with open('email.info', 'r+') as f:
	info = f.readlines()
EMAILADD = info[0]
PASSWORD = info[1]
PHONEADD = info[2]
EMAILSUB = str(tides)
EMAILBOD = str(tides.tides)

email = tc.Email(EMAILADD, PASSWORD, PHONEADD, EMAILSUB, EMAILBOD)
email.attach(tides.station.site + '.png', tides.graph)
email.send()