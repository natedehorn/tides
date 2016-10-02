import datetime
import time
import requests
import tideClasses as tc
import plotly
import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go
from bs4 import BeautifulSoup

def buildReq(notify):
	return 'site=' + notify.station.site + '&station_number=' + notify.station.number + '&month=' + notify.date.month + '&year=' + notify.date.year + '&start_date=' + notify.start_date + '&maximum_days=' + '1'

def getTides(notify):
	soup = BeautifulSoup(requests.post('http://www.saltwatertides.com/cgi-bin/seatlantic.cgi', buildReq(notify)).text, 'html.parser')
	lines = (((soup.find('pre').text)[(soup.find('pre').text.find(str(datetime.datetime.now().day))):]).splitlines())
	lines.pop()
	return [tc.Tide(*l) for l in [line.strip()[len(str(datetime.datetime.now().day)):].strip().split()[:4] for line in lines]]

def plot(notify):
	name = notify.station.site
	tides = getTides(notify)
	plotly.tools.set_credentials_file(
		username='natedehorn',
		api_key='lc9l1abkiq')
	trace = go.Scatter(
		x=[(datetime.datetime.strptime((tide.time + tide.period), '%I:%M%p').strftime("%H:%M")) for tide in tides],
		y=[tide.level for tide in tides],
		line=dict(shape='spline'))
	layout = go.Layout(
		title=name + ' Tides for ' + datetime.datetime.now().strftime("%A, %d %B %Y"),
		xaxis=dict(
			title='Time',
			autotick=False,
        	ticks='outside',
        	tick0=0,
        	dtick=1),
    	yaxis=dict(title='Height (ft)'),
    	font =dict(family='Open Sans, monospace', size=18, color='#7f7f7f'),
    	width=600,
    	height=420)
	fig = go.Figure(
		data=[trace],
		layout=layout)
	py.image.save_as(fig, filename=name + '.png')