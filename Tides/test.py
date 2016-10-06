import tc
import datetime
import unittest

class TestTidesMethods(unittest.TestCase):

	def test_station(self):
		now = datetime.datetime.now()
		char_harb = tc.Station('SCarolina', '8665530')
		month_year = tc.Date(str(now.month), str(now.year))
		self.assertEqual(str(char_harb),'SCarolina, 8665530')
		self.assertEqual(str(char_harb.site),'SCarolina')
		self.assertEqual(str(char_harb.station_number),'8665530')

	def test_tides(self):
		now = datetime.datetime.now()
		char_harb = tc.Station('SCarolina', '8665530')
		month_year = tc.Date(str(now.month), str(now.year))
		char_harb_tides = tc.Tides(char_harb, tc.Date('1', '2016')).tides
		self.assertEqual(str(char_harb_tides), '[High, 5:01, AM, 5.3, Low, 11:15, AM, 0.4, High, 5:04, PM, 4.6, Low, 11:13, PM, 0.0]')		
		self.assertEqual(str(char_harb_tides[2]), 'High, 5:04, PM, 4.6')
		self.assertEqual(str(char_harb_tides[1].level), '0.4')

if __name__ == '__main__':
	unittest.main()