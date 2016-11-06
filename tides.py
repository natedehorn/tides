from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators
from flask_sqlalchemy import SQLAlchemy

# App config.
SQLALCHEMY_TRACK_MODIFICATIONS = False
APP = Flask(__name__)
APP.config.from_object(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uqhlbrxcxuhbyq:_FbOqODzPCsqf583Dwvl8G0zH3@ec2-54-163-240-101.compute-1.amazonaws.com:5432/dacudo927bqbve'
APP.config['SECRET_KEY'] = '_FbOqODzPCsqf583Dwvl8G0zH3'
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
def __main__():
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

@APP.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == "__main__":
    APP.run(debug=True)
