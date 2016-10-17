import datetime
import tc

now = datetime.datetime.now()
charleston = tc.Station('SCarolina', '8665099')

station = charleston
tides = tc.Tides(station, tc.Date(now.month,now.year))

emailadd = 'tidesbot@gmail.com'
password = 'tides4all'
phoneadd = '5742989709@mms.att.net'
emailbod = str(tides.tides)

email = tc.Email(emailadd, password, phoneadd, emailbod)
email.attach(tides.station.site + '.png', tides.graph)
email.send()