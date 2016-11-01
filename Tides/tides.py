from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy

# App config.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qaeotcbasbnjnm:qNv1Ogfn2qOTlUSzfQG1ezNV1a@ec2-54-243-47-83.compute-1.amazonaws.com:5432/dcjfootut9klik'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
db = SQLAlchemy(app)

# Create our database model
class UserInfo(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    state = db.Column(db.String(50))
    station_number = db.Column(db.String(10))
    phone = db.Column(db.String(10))
    service = db.Column(db.String(25))

    def __init__(self, name, state, station_number, phone, service):
        self.name = name
        self.state = state
        self.station_number = station_number
        self.phone = phone
        self.service = service

    def __repr__(self):
    	return("<%s, %s, %s, %s, %s>" % (self.name, self.state, self.station_number, self.phone, self.service))

class TideForm(Form):
	name = TextField(validators=[validators.required()])
	state = TextField(validators=[validators.required()])
	station_number = TextField(validators=[validators.required()])
	phone = TextField(validators=[validators.required()])
	service = TextField(validators=[validators.required()])
 
@app.route("/", methods=['GET', 'POST'])
def form():
	form = TideForm(request.form)
	print(form.errors)
	if request.method == 'POST':
		if request.form['submit'] == 'Sign Up':
			if form.validate():
				name=request.form['name']
				state=request.form['state']
				station_number=request.form['station_number']
				phone=request.form['phone']
				service=request.form['service']
				newuser = UserInfo(name, state, station_number, phone, service)
				db.session.add(newuser)
				db.session.commit()
				print(name, state, station_number, phone, service)
				flash('Thanks for registration ' + name)
			else:
				flash('Error: All the form fields are required.')

		if request.form['submit'] == 'Delete':
			pass
		
 
	return render_template('index.html', form=form)
 
if __name__ == "__main__":
	app.run()