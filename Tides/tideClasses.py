class Tide:
	def __init__(self, phase, time, period, level):
		super(Tide, self).__init__()
		self.phase = phase
		self.time = time
		self.period = period
		self.level = level
	def show(self):
		print(self.phase, self.time + self.period, self.level)

class Date:
	def __init__(self, month, year):
		super(Date, self).__init__()
		self.month = month
		self.year = year

class Station:
	def __init__(self, site, number):
		super(Station, self).__init__()
		self.site = site
		self.number = number

class Notify:
	def __init__(self, _station, _date, start_date):
		super(Notify, self).__init__()
		self.station = _station
		self.date = _date
		self.start_date = start_date