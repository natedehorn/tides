import tc
import datetime
import unittest

class TestDate(unittest.TestCase):
	def test_repr(self):
		TEST_DATE = tc.Date(1, 2, 2016)
		self.assertEqual(str(TEST_DATE), '1 2 2016')

	def test_attributes(self):
		TEST_DATE = tc.Date(4, 20, 2015)
		self.assertEqual(TEST_DATE.day, 4)
		self.assertEqual(TEST_DATE.month, 20)
		self.assertEqual(TEST_DATE.year, 2015)

	def test_type(self):
		TODAY = tc.Date(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year)
		self.assertIs(type(TODAY), tc.Date)

class TestStation(unittest.TestCase):
	def test_repr(self):
		TEST_STATION = tc.Station('SCarolina', '8665530')
		self.assertEqual(str(TEST_STATION), 'SCarolina, 8665530')

	def test_attributes(self):
		TEST_STATION = tc.Station('SCarolina', '8665530')
		self.assertEqual(str(TEST_STATION.site),'SCarolina')
		self.assertEqual(str(TEST_STATION.station_number),'8665530')

	def test_type(self):
		TEST_STATION = tc.Station('SCarolina', '8665530')
		self.assertIs(type(TEST_STATION), tc.Station)

class TestTide(unittest.TestCase):
	def test_repr(self):
		TEST_TIDE = tc.Tide('High', '4:20', 'PM', '4.2')
		self.assertEqual(str(TEST_TIDE), 'High, 4:20, PM, 4.2')

	def test_attributes(self):
		TEST_TIDE = tc.Tide('Low', '10:40', 'AM', '-0.2')
		self.assertEqual(TEST_TIDE.phase, 'Low')
		self.assertEqual(TEST_TIDE.time, '10:40')
		self.assertEqual(TEST_TIDE.period, 'AM')
		self.assertEqual(TEST_TIDE.level, '-0.2')

	def test_type(self):
		TEST_TIDE = tc.Tide('High', '12:10', 'AM', 's')
		self.assertIs(type(TEST_TIDE), tc.Tide)

class TestTides(unittest.TestCase):
	def test_attributes(self):
		TEST_STATION = tc.Station('SCarolina', '8665530')
		TODAY = tc.Date(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year)
		TEST_TIDES = tc.Tides(TEST_STATION, TODAY)
		self.assertEqual(str(TEST_TIDES.station), str(tc.Station('SCarolina', '8665530')))
		self.assertEqual(str(TEST_TIDES.date), str(TODAY))
		self.assertTrue(hasattr(TEST_TIDES, 'tides'))
		self.assertTrue(hasattr(TEST_TIDES, 'graph'))

	def test_type(self):
		TEST_STATION = tc.Station('SCarolina', '8665530')
		TODAY = tc.Date(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year)
		TEST_TIDES = tc.Tides(TEST_STATION, TODAY)
		self.assertIs(type(TEST_TIDES), tc.Tides)

class TestEmailInfo(unittest.TestCase):
	def test_repr(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		self.assertEqual(str(TEST_EMAIL_INFO), str('Sender : %s\nPassword: %s\nRecipient: %s' % (TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])))

	def test_attributes(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		self.assertTrue(hasattr(TEST_EMAIL_INFO, 'sender'))
		self.assertTrue(hasattr(TEST_EMAIL_INFO, 'password'))
		self.assertTrue(hasattr(TEST_EMAIL_INFO, 'recipient'))

	def test_type(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		self.assertIs(type(TEST_EMAIL_INFO), tc.EmailInfo)

class TestAttachment(unittest.TestCase):
	def test_repr(self):
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		self.assertEqual(str(TEST_ATTACHMENT), str('Filename: Test.png\nFile: Test.png'))

	def test_attributes(self):
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		self.assertTrue(hasattr(TEST_ATTACHMENT, 'filename'))
		self.assertTrue(hasattr(TEST_ATTACHMENT, 'file'))

	def test_type(self):
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		self.assertIs(type(TEST_ATTACHMENT), tc.Attachment)

class TestEmail(unittest.TestCase):
	def test_basic_repr(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body'])
		self.assertEqual(str(TEST_EMAIL), 'Sender : %s\nPassword: %s\nRecipient: %s\nSubject: %s\nBody: %s' % (TEST_INFO[0], TEST_INFO[1], TEST_INFO[2], 'Test Subject', 'Test Body'))

	def test_basic_attributes(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body'])
		self.assertTrue(hasattr(TEST_EMAIL, 'emailinfo'))
		self.assertEqual(str(TEST_EMAIL.subject), 'Test Subject')
		self.assertEqual(str(TEST_EMAIL.body), 'Test Body')

	def test_basic_type(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body'])
		self.assertIs(type(TEST_EMAIL), tc.Email)
		
	def test_attach_repr(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body', TEST_ATTACHMENT])
		self.assertEqual(str(TEST_EMAIL), str('Sender : %s\nPassword: %s\nRecipient: %s\nSubject: Test Subject\nBody: Test Body\nFilename: Test.png\nFile: Test.png' % (TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])))

	def test_attach_attributes(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body', TEST_ATTACHMENT])
		self.assertTrue(hasattr(TEST_EMAIL, 'emailinfo'))
		self.assertEqual(str(TEST_EMAIL.subject), 'Test Subject')
		self.assertEqual(str(TEST_EMAIL.body), 'Test Body')
		self.assertEqual(str(TEST_EMAIL.attachment.filename), 'Test.png')
		self.assertEqual(str(TEST_EMAIL.attachment.file), 'Test.png')

	def test_attach_type(self):
		with open('test.info','r+') as FILE:
			TEST_INFO = FILE.readlines()
		TEST_EMAIL_INFO = tc.EmailInfo(TEST_INFO[0], TEST_INFO[1], TEST_INFO[2])
		TEST_ATTACHMENT = tc.Attachment('Test.png', 'Test.png')
		TEST_EMAIL = tc.Email([TEST_EMAIL_INFO, 'Test Subject', 'Test Body', TEST_ATTACHMENT])
		self.assertIs(type(TEST_EMAIL), tc.Email)

	def test_send_email(self):
		NOW = datetime.datetime.now()
		DATE = tc.Date(NOW.day + 1, NOW.month, NOW.year)
		TIDES = tc.Tides(tc.Station('SCarolina', '8665099'), DATE)
		SUBJECT = 'Tides for %s' % (str(DATE))
		BODY = str(TIDES.tides)
		with open('test.info','r+') as FILE:
			INFO = FILE.readlines()
		EMAIL_INFO = tc.EmailInfo(INFO[0], INFO[1], INFO[2])
		ATTACHMENT = tc.Attachment(TIDES.station.site + '.png', TIDES.graph)
		EMAIL = tc.Email([EMAIL_INFO, SUBJECT, BODY, ATTACHMENT])
		EMAIL.send()

if __name__ == '__main__':
	unittest.main()