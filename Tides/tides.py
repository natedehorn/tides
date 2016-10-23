import datetime
import tc

NOW = datetime.datetime.now()
CHARLESTON = tc.Station('SCarolina', '8665099')

STATION = CHARLESTON
tides = tc.Tides(STATION, tc.Date(NOW.month,NOW.year))

with open('email.info','r+') as f:
	info = f.readlines()
emailadd = info[0]
password = info[1]
phoneadd = info[2]
emailsub = str(tides)
emailbod = str(tides.tides)

email = tc.Email(emailadd, password, phoneadd, emailbod)
email.attach(tides.station.site + '.png', tides.graph)
email.send()