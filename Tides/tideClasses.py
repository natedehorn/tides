class Date:
	def __init__(self, month, year):
		super(Date, self).__init__()
		self.month = month
		self.year = year
			
class Tide:
	"""docstring for Tide"""
	def __init__(self, site, sitenumber, phase, time, period, level):
		super(Tide, self).__init__()
		self.site = site
		self.sitenumber = sitenumber
		self.phase = phase
		self.time = time
		self.period = period
		self.level = level
		

class Notify:
	def __init__(self, _station, _date, start_date):
		super(Notify, self).__init__()
		self.station = _station
		self.date = _date
		self.start_date = start_date

class Email:
	"""docstring for Email"""
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