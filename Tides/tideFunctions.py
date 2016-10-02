import datetime
import requests
import tideClasses as tc
from bs4 import BeautifulSoup

def buildReq(notify):
	return 'site=' + notify.station.site + '&station_number=' + notify.station.number + '&month=' + notify.date.month + '&year=' + notify.date.year + '&start_date=' + notify.start_date + '&maximum_days=' + '1'

def getTides(notify):
	soup = BeautifulSoup(requests.post('http://www.saltwatertides.com/cgi-bin/seatlantic.cgi', buildReq(notify)).text, 'html.parser')
	lines = (((soup.find('pre').text)[(soup.find('pre').text.find(str(datetime.datetime.now().day))):]).splitlines())
	lines.pop()
	return [tc.Tide(*l) for l in [line.strip()[len(str(datetime.datetime.now().day)):].strip().split()[:4] for line in lines]]