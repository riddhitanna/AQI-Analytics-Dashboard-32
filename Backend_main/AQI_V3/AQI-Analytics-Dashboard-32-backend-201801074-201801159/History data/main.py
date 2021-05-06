from flask import Flask, render_template,request,jsonify
import requests
import json
import time
import datetime 
import urllib

app = Flask(__name__)
 
@app.route('/', methods =['POST', 'GET'])
def weather():
	if request.method == 'POST':
		city = request.form['city']
	else:
		city = 'ahmedabad'
	
	api = '72c8a65a1e2fac6803774513f214fb14'

	lat=0
	lon=0
  
    # source contain json data from api
	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	lat=str(latLonData[0]['lat'])
	lon=str(latLonData[0]['lon'])

	print()
	print('###########################')
	print('Coordinates for '+city+' : lat : '+lat+' lon : '+lon)
	print('###########################')
	print()

	#currentAQI= urllib.request,urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+lon+'&appid='+api).read()

	#currentAQIData= json.loads(currentAQI)

	#aqi=str(currentAQIData[])

	sDate=datetime.date.today()-datetime.timedelta(days=7)
	sDateformatted=sDate.strftime('%d/%m/%Y')
	eDate=datetime.date.today()-datetime.timedelta(days=1)
	eDateformatted=eDate.strftime('%d/%m/%Y')
	sUNIX=int(time.mktime(datetime.datetime.strptime(sDateformatted, "%d/%m/%Y").timetuple()))
	eUNIX=int(time.mktime(datetime.datetime.strptime(eDateformatted, "%d/%m/%Y").timetuple()))

	print()
	print('###########################')
	print('Start time : '+str(sUNIX)+' End time : '+str(eUNIX))
	print('###########################')
	print()

	history = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+str(lat)+'&lon='+str(lon)+'&start='+str(sUNIX)+'&end='+str(eUNIX)+'&appid='+api).read()

	historyData = json.loads(history)

	print()
	print('###########################')
	print(historyData)
	print('###########################')
	print()

	return render_template('index.html', data = historyData)
 
if __name__ == '__main__':
	app.run(debug = True)
