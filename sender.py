from tides import UserInfo
import tc
import datetime

NOW = datetime.datetime.now()
TODAY = tc.Date(NOW.day, NOW.month, NOW.year)
DATA = UserInfo.query.all()
for d in DATA:
	tides = tc.Tides(tc.Station(d.state, d.station_number), TODAY)
	SUBJECT = 'Tides for %s' % (str(DATE))
	BODY = str(TIDES.tides)
	with open('email.info','r+') as file:
		INFO = file.readlines()
	EMAIL_INFO = tc.EmailInfo(INFO[0], INFO[1], str('%s@%s' % (d.phone, d.service)))
	ATTACHMENT = tc.Attachment(TIDES.station.site + '.png', TIDES.graph)
	EMAIL = tc.Email([EMAIL_INFO, SUBJECT, BODY, ATTACHMENT])
	print('.')