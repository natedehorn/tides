import http
import socket
import plotly
import datetime
import requests
from bs4 import BeautifulSoup

class Date:
	def __init__(self, month, year):
		super(Date, self).__init__()
		self.month = month
		self.year = year

class Station:
	def __init__(self, site, station_number):
		super(Station, self).__init__()
		self.site = site
		self.station_number = station_number
	def __repr__(self):
		return self.site + ', ' + self.station_number
		
class Tide:
		def __init__(self, phase, time, period, level):
			super(Tide, self).__init__()
			self.phase = phase
			self.time = time
			self.period = period
			self.level = level
		def __repr__(self):
			return self.phase + ', ' + self.time + ', ' + self.period + ', ' + self.level

class Tides:
	def __init__(self, station, date):
		super(Tides, self).__init__()
		self.station = station
		self.date = date
		test_con_url = 'www.google.com'
		test_con_resouce = '/intl/en/'
		test_con = http.client.HTTPConnection(test_con_url)
		# ensure network connection
		try:
			test_con.request('GET', test_con_resouce)
			response = test_con.getresponse()
		except Exception as e:
			print('Not connected to internet')
		else:
			self.get()
		test_con.close()

	def get(self):
		request = 'site=' + self.station.site + '&station_number=' + self.station.station_number + '&month=' + self.date.month + '&year=' + self.date.year + '&start_date=' + str(datetime.datetime.now().day) + '&maximum_days=' + '1'
		soup = BeautifulSoup(requests.post('http://www.saltwatertides.com/cgi-bin/seatlantic.cgi', request).text, 'html.parser')
		lines = (((soup.find('pre').text)[(soup.find('pre').text.find(str(datetime.datetime.now().day))):]).splitlines())
		lines.pop()
		self.tides = [Tide(*l) for l in [line.strip()[len(str(datetime.datetime.now().day)):].strip().split()[:4] for line in lines]]
		
	def plot(self):
		plotly.tools.set_credentials_file(
			username = 'tidesbot',
			api_key = 'evpcqc1vir')
		if self.tides != null:
			trace = plotly.graph_objs.Scatter(
				x = [datetime.datetime.srtptime((t.time + t.period, '%I:%M%p').strftime('%H:%M')) for t in self.tides],
				y = [t.level for t in self.tides],
				line = dict(shape = 'spline'))
		else:
			try:
				raise NoTidesError('No Tides Data')
			except NoTidesError:
				raise
		layout = plotly.graph_objs.Layout(
			title = self.site + ' Tides for ' + datetime.datetime.now().strftime('%A, %d %B %Y'),
			xaxis = dict(
				title = 'Time',
				autotick = False,
				ticks = 'outside',
				tick0 = 0,
				dtick = 1),
			yaxis = dict(title = 'Height (ft)'),
			font = dict(family = 'Open Sans, monospace', size = 18,color = '#404040'),
			width = 600,
			height = 420)
		figure = plotly.graph_objs.Figure(
			data = [trace],
			layout = layout)
		plotly.plotly.image.save_as(fig,filename = self.site + '.png')
		self.graph = self.site + '.png'

class Email:
	def __init__(self, sender, password, recipient, body):
		super(Email, self).__init__()
		self.sender = sender
		self.password = password
		self.recipient = recipient
		self.body = body

	def setSubject(self, subject):
		self.subject = subject
		
	def attach(self, filename, attachment):
		self.filename = filename
		self.attachment = attachment

	def send(self):
		message = MIMEMultipart()
		message['From'] = self.sender
		message['To'] = self.recipient
		if self.subject != null:
			message['Subject'] = self.subject
		message.attach(MIMEText(self.body, 'plain'))
		if self.filename != null and self.attachment != null:
			attachment = open(attachment, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((self.attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)
			message.attach(part)
		server = smtplib.SMTP('smtp.google.com', 587)
		server.starttls()
		server.login(self.sender, self.password)
		prepared = message.as_string
		server.sendmail(self.sender, self.recipient, prepared)
		server.quit()