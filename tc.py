import plotly
import smtplib
import datetime
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyp
from bs4 import BeautifulSoup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Date:
	def __init__(self, day, month, year):
		self.day = day
		self.month = month
		self.year = year

	def __repr__(self):
		return '%s %s %s' % (self.day, self.month, self.year)

class Station:
	def __init__(self, site, station_number):
		self.site = site
		self.station_number = station_number

	def __repr__(self):
		return self.site + ', ' + self.station_number
		
class Tide:
	def __init__(self, phase, time, period, level):
		self.phase = phase
		self.time = time
		self.period = period
		self.level = level

	def __repr__(self):
		return self.phase + ', ' + self.time + ', ' + self.period + ', ' + self.level

class Tides:
	def __init__(self, station, date):
		self.station = station
		self.date = date
		self.get()
		self.plot()
		self.plotnew()

	def get(self):
		request = str('site=%s&station_number=%s&month=%s&year=%s&start_date=%s&maximum_days=1' 
			% (str(self.station.site), str(self.station.station_number),
			str(self.date.month), str(self.date.year), str(self.date.day)))
		url = 'http://www.saltwatertides.com/cgi-bin/seatlantic.cgi'
		soup = BeautifulSoup(requests.post(url, request).text, 'html.parser')
		lines = ((soup.find('pre').text)[soup.find('pre').text.find(str(self.date.day)):]).splitlines()
		lines.pop()
		self.tides = [Tide(*l) for l in 
			[line.strip()[len(str(self.date.day)):].strip().split()[:4] for line in lines]]
		
	def plot(self):
		with open('plotly.info', 'r+') as file:
			info = file.read().splitlines()
		plotly.tools.set_credentials_file(
			username=info[0],
			api_key=info[1])

		if hasattr(self, 'tides'):
			trace = plotly.graph_objs.Scatter(
				x=[(datetime.datetime.strptime((t.time + t.period),
					'%I:%M%p').strftime("%H:%M")) for t in self.tides],
				y=[t.level for t in self.tides],
				line=dict(shape='spline'))
		layout = plotly.graph_objs.Layout(
			title=self.station.site + ' Tides for ' + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%A, %d %B %Y'),
			xaxis=dict(
				title='Time',
				autotick=False,
				ticks='outside',
				tick0=0,
				dtick=1),
			yaxis=dict(title='Height (ft)'),
			font=dict(family='Open Sans, monospace', size=18, color='#404040'),
			width=600,
			height=420)
		figure = plotly.graph_objs.Figure(
			data=[trace],
			layout=layout)
		self.graph = self.station.site + '.png'
		plotly.plotly.image.save_as(figure, filename=self.graph)

	def plotnew(self):
		if hasattr(self, 'tides'):
			title = self.station.site + ' Tides for ' + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%A, %d %B %Y')
			times = [(datetime.datetime.strptime((t.time + t.period), '%I:%M%p')
				.strftime('%H:%M')) for t in self.tides]
			x = [datetime.datetime.combine(datetime.date.today(), 
				datetime.time(int(t[0:2]), int(t[3:]))) for t in times]
			y = [float(t.level) for t in self.tides]
			pyp.plot_date(x, y, 'b')
			pyp.savefig('test.png')
			pyp.close()
		
class EmailInfo:
	def __init__(self, sender, password, recipient):
		self.sender = sender
		self.password = password
		self.recipient = recipient

	def __repr__(self):
		return 'Sender : %s\nPassword: %s\nRecipient: %s' % (self.sender, self.password, self.recipient)

class Attachment:
	def __init__(self, filename, file):
		self.filename = filename
		self.file = file

	def __repr__(self):
		return 'Filename: %s\nFile: %s' % (self.filename, self.file)
		
class Email:
	def __init__(self, argv):
		assert len(argv) == 3 or len(argv) == 4
		self.emailinfo = argv[0]
		self.subject = argv[1]
		self.body = argv[2]
		if len(argv) == 4:
			self.attachment = argv[3]

	def __repr__(self):
		default = str(self.emailinfo) + '\nSubject: %s\nBody: %s' % (self.subject, self.body)
		if hasattr(self, 'attachment'):
			return default + '\n' + str(self.attachment)
		else:
			return default

	def send(self):
		message = MIMEMultipart()
		message['From'] = self.emailinfo.sender
		message['To'] = self.emailinfo.recipient
		message['Subject'] = self.subject
		message.attach(MIMEText(self.body, 'plain'))
		if hasattr(self, 'attachment'):
			part = MIMEBase('application', 'octet-stream')
			with open(self.attachment.file, 'rb') as F:
				part.set_payload(F.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % self.attachment.filename)
			message.attach(part)
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(self.emailinfo.sender, self.emailinfo.password)
		server.sendmail(message['From'], message['To'], message.as_string())
		server.quit()

