from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField
from flask_sqlalchemy import SQLAlchemy

# App config.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
APP = Flask(__name__)
APP.config.from_object(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qaeotcbasbnjnm:qNv1Ogfn2qOTlUSzfQG1ezNV1a@ec2-54-243-47-83.compute-1.amazonaws.com:5432/dcjfootut9klik'
APP.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
DB = SQLAlchemy(APP)

# Create our database model
class UserInfo(DB.Model):
	name = DB.Column(DB.String(50), primary_key=True)
	state = DB.Column(DB.String(50))
	station_number = DB.Column(DB.String(10))
	phone = DB.Column(DB.String(10))
	service = DB.Column(DB.String(25))

	def __init__(self, name, state, station_number, phone, service):
		self.name = name
		self.state = state
		self.station_number = station_number
		self.phone = phone
		self.service = service

	def __repr__(self):
		return "<tides.UserInfo object %s>" % self.name

class TideForm(Form):
	name = TextField(validators=[validators.required()])
	state = TextField(validators=[validators.required()])
	station_number = TextField(validators=[validators.required()])
	phone = TextField(validators=[validators.required()])
	service = TextField(validators=[validators.required()])
 
@APP.route("/", methods=['GET', 'POST'])
def tideform():
	form = TideForm(request.form)
	print(form.errors)
	if request.method == 'POST':
		if form.validate():
			name = request.form['name']
			state = request.form['state']
			station_number = request.form['station_number']
			phone = request.form['phone']
			service = request.form['service']
			if request.form['submit'] == 'Sign Up':
				if not UserInfo.query.get(name):	
					user = UserInfo(name, state, station_number, phone, service)
					DB.session.add(user)
					flash('Thanks for registration ' + name)
				else:
					flash('Error: User already exists in database.')
			if request.form['submit'] == 'Delete':
				if UserInfo.query.get(name):
					DB.session.delete(UserInfo.query.get(name))
					flash('We\'re sorry to see you go ' + name)
				else:
					flash('Error: User was not found in database.')
			DB.session.commit()
			print(name, state, station_number, phone, service)
		else:
			flash('Error: All fields are required.')
 
	return render_template('index.html', form=form)
 
if __name__ == "__main__":
	APP.run()