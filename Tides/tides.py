import datetime
import tideClasses as tc
import tideFunctions as tf
import plotly
import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='natedehorn', api_key='lc9l1abkiq')

charl = tc.Notify(tc.Station('SCarolina', '8665530'), tc.Date(str(datetime.datetime.now().month), str(datetime.datetime.now().year)), str(datetime.datetime.now().day))
# = tc.Notify(tc.Station('Georgia', '8677344'), tc.Date(str(datetime.datetime.now().month), str(datetime.datetime.now().year)), str(datetime.datetime.now().day))
tides = tf.getTides(charl)
for tide in tides:
	tide.show()

print("The tides for today are as follows: ")
times = [(tide.time+tide.period) for tide in tides]
levels = [tide.level for tide in tides]
print(times, levels)

trace = go.Scatter(x=times, y=levels, line=dict(shape='spline'))
layout = go.Layout(title='Tides', width=600, height=420)
fig = go.Figure(data=[trace],layout=layout)
py.image.save_as(fig, filename='Tides.png')