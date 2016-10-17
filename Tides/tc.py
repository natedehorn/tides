import http
import plotly
import smtplib
import datetime
import requests
from bs4 import BeautifulSoup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Date(object):
	def __init__(self, month, year):
		self.month = month
		self.year = year

class Station(object):
	def __init__(self, site, station_number):
		self.site = site
		self.station_number = station_number
	def __repr__(self):
		return self.site + ', ' + self.station_number
		
class Tide(object):
		def __init__(self, phase, time, period, level):
			self.phase = phase
			self.time = time
			self.period = period
			self.level = level
		def __repr__(self):
			return self.phase + ', ' + self.time + ', ' + self.period + ', ' + self.level

class Tides(object):
	def __init__(self, station, date):
		self.station = station
		self.date = date
		test_con_url = 'www.google.com'
		test_con_resouce = '/intl/en/'
		test_con = http.client.HTTPConnection(test_con_url)
		# ensure network connection
		try:
			test_con.request('GET', test_con_resouce)
		except Exception:
			print('Not connected to internet')
		else:
			self.get()
			self.plot()
		test_con.close()

	def get(self):
		request = str('site=' + self.station.site 
		+ '&station_number=' + str(self.station.station_number) 
		+ '&month=' + str(self.date.month) 
		+ '&year=' + str(self.date.year) 
		+ '&start_date=' + str(datetime.datetime.now().day) 
		+ '&maximum_days=' + '1')
		soup = BeautifulSoup(requests.post('http://www.saltwatertides.com/cgi-bin/seatlantic.cgi', request).text, 'html.parser')
		lines = (((soup.find('pre').text)[(soup.find('pre').text.find(str(datetime.datetime.now().day))):]).splitlines())
		lines.pop()
		self.tides = [Tide(*l) for l in [line.strip()[len(str(datetime.datetime.now().day)):].strip().split()[:4] for line in lines]]
		
	def plot(self):
		plotly.tools.set_credentials_file(
			username = 'tidesbot',
			api_key = 'evpcqc1vir')
		if hasattr(self, 'tides'):
			trace = plotly.graph_objs.Scatter(
				x=[(datetime.datetime.strptime((t.time + t.period), '%I:%M%p').strftime("%H:%M")) for t in self.tides],
				y = [t.level for t in self.tides],
				line = dict(shape = 'spline'))
		else:
			print('No Tides Data')
		layout = plotly.graph_objs.Layout(
			title = self.station.site + ' Tides for ' + datetime.datetime.now().strftime('%A, %d %B %Y'),
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
		plotly.plotly.image.save_as(figure,filename = self.station.site + '.png')
		self.graph = self.station.site + '.png'

class Email(object):
	def __init__(self, sender, password, recipient, body):
		self.sender = sender
		self.password = password
		self.recipient = recipient
		self.body = body

	def __repr__(self):
		default = 'Sender : %s\nPassword: %s\nRecipient: %s\nBody: %s' % (self.sender, self.password, self.recipient, self.body)
		if  hasattr(self, 'subject') and hasattr(self, 'filename') and hasattr(self, 'attachment'):
			return default + '\nSubject: %s\nFilename: %s\nAttachment: %s' % (self.subject, self.filename, self.attachment)
		elif  hasattr(self, 'filename') and hasattr(self, 'attachment'):
			return default + '\nFilename: %s\nAttachment: %s' % (self.filename, self.attachment)
		elif  hasattr(self, 'subject'):
			return default + '\nSubject: %s' % (self.subject)
		else:
			return default

	def setSubject(self, subject):
		self.subject = subject
		
	def attach(self, filename, attachment):
		self.filename = filename
		self.attachment = attachment

	def send(self):
		message = MIMEMultipart()
		message['From'] = self.sender
		message['To'] = self.recipient
		if hasattr(self, 'subject'):
			message['Subject'] = self.subject
		message.attach(MIMEText(self.body, 'plain'))
		if hasattr(self, 'filename') and hasattr(self, 'attachment'):
			attachment = open(self.attachment, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)
			message.attach(part)
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(self.sender, self.password)
		server.sendmail(message['From'], message['To'], message.as_string())
		server.quit()