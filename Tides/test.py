import tc
import datetime
import unittest

class TestTidesMethods(unittest.TestCase):
	def test_station(self):
		char_harb = tc.Station('SCarolina', '8665530')
		self.assertEqual(str(char_harb),'SCarolina, 8665530')
		self.assertEqual(str(char_harb.site),'SCarolina')
		self.assertEqual(str(char_harb.station_number),'8665530')

	def test_tides(self):
		char_harb = tc.Station('SCarolina', '8665530')
		char_harb_tides = tc.Tides(char_harb, tc.Date('1', '2016'))
		self.assertIs(type(char_harb_tides),tc.Tides)

	def testplot(self):
		char_harb = tc.Station('SCarolina', '8665530')
		char_harb_tides = tc.Tides(char_harb, tc.Date('1', '2016'))
		self.assertEqual(str(char_harb_tides.graph), char_harb.site + '.png')

class TestEmailMethods(unittest.TestCase):
	def test_basic_email(self):
		email = tc.Email('tidesbot@gmail.com','tides4all', '5742989709@mms.att.net', 'Test')
		self.assertEqual(str(email),'Sender : tidesbot@gmail.com\nPassword: tides4all\nRecipient: 5742989709@mms.att.net\nBody: Test')

	def test_subject_email(self):
		email = tc.Email('tidesbot@gmail.com','tides4all', '5742989709@mms.att.net', 'Test')
		email.setSubject('Test Subject')
		self.assertEqual(str(email),'Sender : tidesbot@gmail.com\nPassword: tides4all\nRecipient: 5742989709@mms.att.net\nBody: Test\nSubject: Test Subject')

	def test_complete_email(self):
		email = tc.Email('tidesbot@gmail.com','tides4all', '5742989709@mms.att.net', 'Test')
		email.setSubject('Test Subject')
		email.attach('Test.png', 'Test.png')
		self.assertEqual(str(email),'Sender : tidesbot@gmail.com\nPassword: tides4all\nRecipient: 5742989709@mms.att.net\nBody: Test\nSubject: Test Subject\nFilename: Test.png\nAttachment: Test.png')
		
	def test_send_complete_email(self):
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
		
if __name__ == '__main__':
	unittest.main()
	unittest.installHandler()
	unittest.registerResult(result)