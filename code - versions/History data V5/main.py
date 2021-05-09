from flask import Flask, render_template,request,jsonify,redirect,url_for
import requests
import json
import time
import datetime 
import urllib
import aqi
import threading

app = Flask(__name__)

api = '72c8a65a1e2fac6803774513f214fb14'

statesList=["Andhra+Pradesh","Arunachal+Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal+Pradesh","Jharkhand","Karnataka","Kerala",
"Madhya+Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil+Nadu","Telangana","Tripura",
"Uttar+Pradesh","Uttarakhand","West+Bengal","Andaman+and+Nicobar+Islands","Delhi","Jammu+and+Kashmir","Lakshadweep","andhra+pradesh","arunachal+pradesh","assam",
"bihar","chhattisgarh","goa","gujarat","haryana","himachal+pradesh","jharkhand","karnataka","kerala","madhya+pradesh","maharashtra","manipur","meghalaya","mizoram",
"nagaland","odisha","punjab","rajasthan","sikkim","tamil+nadu","telangana","tripura","uttar+pradesh","uttarakhand","west+bengal","andaman+and+nicobar+islands","delhi","jammu+and+kashmir","lakshadweep"]

def latLonDataCall(name, latLonData):
	latLon = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+name+'&limit=1&appid='+api).read()
	latLonData.append(json.loads(latLon))



def historyDataCall(lat, lon, latLonData, PollutantsData):
	sDate=datetime.date.today()-datetime.timedelta(days=31)
	sDateformatted=sDate.strftime('%d/%m/%Y')
	eDate=datetime.date.today()-datetime.timedelta(days=1)
	eDateformatted=eDate.strftime('%d/%m/%Y')
	sUNIX=int(time.mktime(datetime.datetime.strptime(sDateformatted, "%d/%m/%Y").timetuple()))
	eUNIX=int(time.mktime(datetime.datetime.strptime(eDateformatted, "%d/%m/%Y").timetuple()))

	history = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+str(lat)+'&lon='+str(lon)+'&start='+str(sUNIX)+'&end='+str(eUNIX)+'&appid='+api).read()

	historyData = json.loads(history)
	
	error=[]

	if 'cod' in historyData:
		error=['404']
	else:
		error=['10000']

	if error[0]=='404':
		PollutantsData=['Error','Sorry! The requested city data is not available.']
	else:
		hData1 = historyData['list']
		prevDate='0'
		count=1
		aqiData=[]
		coData=[]
		noData=[]
		no2Data=[]
		o3Data=[]
		so2Data=[]
		pm2_5Data=[]
		pm10Data=[]
		nh3Data=[]
		for tData in hData1:
			tCO = float(tData['components']['co'])
			tNO = float(tData['components']['no'])
			tNO2 = float(tData['components']['no2'])
			tO3 = float(tData['components']['o3'])
			tSO2 = float(tData['components']['so2'])
			tPM2_5 = float(tData['components']['pm2_5'])
			tPM10 = float(tData['components']['pm10'])
			tNH3 = float(tData['components']['nh3'])
			tDate = datetime.datetime.fromtimestamp(int(tData['dt']))
			tDatef= tDate.strftime ('%d/%m/%Y')
			if prevDate==tDatef:
				coData[len(coData)-1][1]=round((count*(coData[len(pm2_5Data)-1][1])+tCO)/(count+1),2)
				noData[len(noData)-1][1]=round((count*(noData[len(pm2_5Data)-1][1])+tNO)/(count+1),2)
				no2Data[len(no2Data)-1][1]=round((count*(no2Data[len(pm2_5Data)-1][1])+tNO2)/(count+1),2)
				o3Data[len(o3Data)-1][1]=round((count*(o3Data[len(pm2_5Data)-1][1])+tO3)/(count+1),2)
				so2Data[len(so2Data)-1][1]=round((count*(so2Data[len(pm2_5Data)-1][1])+tSO2)/(count+1),2)
				pm2_5Data[len(pm2_5Data)-1][1]=round((count*(pm2_5Data[len(pm2_5Data)-1][1])+tPM2_5)/(count+1),2)
				pm10Data[len(pm10Data)-1][1]=round((count*(pm10Data[len(pm2_5Data)-1][1])+tPM10)/(count+1),2)
				nh3Data[len(nh3Data)-1][1]=round((count*(nh3Data[len(pm2_5Data)-1][1])+tNH3)/(count+1),2)
				count=count+1
			else:
				coData.append([tDatef,tCO])
				noData.append([tDatef,tNO])
				no2Data.append([tDatef,tNO2])
				o3Data.append([tDatef,tO3])
				so2Data.append([tDatef,tSO2])
				pm2_5Data.append([tDatef,tPM2_5])
				pm10Data.append([tDatef,tPM10])
				nh3Data.append([tDatef,tNH3])
				prevDate=tDatef
				count=1

		historyAqiData = aqiDataConverter(pm2_5Data, pm10Data)

		PollutantsData.extend([historyAqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']])



def stateDataCall(lat, lon, stateData):
	state = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api).read()
	stateData.append(json.loads(state))

def weatherDataCall(lat, lon, weatherData):
	weather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api+'&units=metric').read()
	tempData = json.loads(weather)
	weatherData.append(tempData['main'])

def aqiDataConverter(pm2_5Data, pm10Data):
	aqiData=[]
	for i in range(len(pm2_5Data)):
		aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])
	return aqiData

aqiData = ['0']*32

def stateHistoryDataPartCall(start, end):
	start = int(start)
	end = int(end)
	for i in range(start,end,1):

		lat=0
		lon=0

		if(statesList[i] == 'Telangana' or statesList[i] == 'telangana'):
			lat='18.1124'
			lon='79.0193'
		elif(statesList[i] == 'Lakshadweep' or statesList[i] == 'lakshadweep'):
			lat='10.57'
			lon='72.64'
		else:
			latLonData = []
			latLonDataCall(statesList[i], latLonData)
			lat=str(latLonData[0][0]['lat'])
			lon=str(latLonData[0][0]['lon'])

		stateData = []
		stateDataCall(lat, lon, stateData)
		stateData = stateData[0]['list'][0]['main']
		aqiData[i] = stateData['aqi']
		print(aqiData[i])



@app.route('/', methods =['POST', 'GET'])
@app.route('/maindashboard', methods =['POST', 'GET'])
def maindashboard():
	include = 0
	if request.method == "POST":
		name = request.form['name']
		if len(name) == 0:
			include = 1
		else:
			#Removing extra whitespaces and converting spaces into + to pass into url.
			name = "+".join(name.split())
			if name not in statesList:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

	threads = []
	for i in range(32):
		t = threading.Thread(target=stateHistoryDataPartCall, args=(i,i+1))
		t.start()
		threads.append(t)

	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
		include = 0

	for thread in threads:
		thread.join()
	
	return render_template('maindashboard.html', data = aqiData, len = len(aqiData), error = error, errorlen = len(error))



@app.route('/statedashboard', methods =['POST', 'GET'])
@app.route('/statedashboard/<string:name>/', methods =['POST', 'GET'])
def statedashboard(name=""):
	name=str(name)
	if request.method == 'POST':
		name = request.form['name']
		#Removing extra whitespaces and converting spaces into + to pass into url.
		name = "+".join(name.split())
	if name not in statesList:
		return redirect(url_for('citydash', name = name))

	lat=0
	lon=0

	if (name == 'Telangana' or name == 'telangana'):
		latLonData = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
	elif (name == 'Lakshadweep' or name == 'lakshadweep'):
		latLonData = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
	else:
		latLonData = []
		latLonDataCall(name,latLonData)

	if len(latLonData[0])==0:
		stateAqi=0
		stateData=['Error','Sorry! The Data for '+name+' is not available.']
		weatherData=[]
		historyData=[]
	else:
		lat=str(latLonData[0][0]['lat'])
		lon=str(latLonData[0][0]['lon'])

		stateData = []
		t1 = threading.Thread(target=stateDataCall, args=(lat, lon, stateData))
		t1.start()
		weatherData = []
		t2 = threading.Thread(target=weatherDataCall, args=(lat, lon, weatherData))
		t2.start()
		stateHistoryData = []
		t3 = threading.Thread(target=historyDataCall, args=(lat, lon, latLonData[0], stateHistoryData))
		t3.start()

		t1.join()
		stateData = stateData[0]['list'][0]['components']
		stateAqi = aqi.to_aqi([(aqi.POLLUTANT_PM25, stateData['pm2_5']),(aqi.POLLUTANT_PM10, stateData['pm10'])])

		t2.join()
		t3.join()

	return render_template('statedashboard.html', stateAqi = stateAqi, aqiData = stateData, weatherData = weatherData[0], historyData = stateHistoryData)



@app.route('/citydash', methods =['POST', 'GET'])
@app.route('/citydash/<string:name>/', methods =['POST', 'GET'])
def citydash(name=""):

	return render_template('citydash.html')	



@app.route('/cityvscity', methods =['POST', 'GET'])
def cityvscity():
	PollutantsData1=[]
	PollutantsData2=[]
	if request.method == 'GET':
		return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	
	if request.method == 'POST':
		if len(request.form) == 1:
			name = request.form['name']
			#Removing extra whitespaces and converting spaces into + to pass into url.
			name = "+".join(name.split())
			if name not in statesList:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

		if len(request.form) == 2:	
			city1 = request.form['city1']
			city2 = request.form['city2']
			if len(city1) == 0 or len(city2) == 0:
				PollutantsData1=['Error','Please enter city names in the respective boxes to compare.']
				PollutantsData2=['Error']
				return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2)) 

	#Removing extra whitespaces and converting spaces into + to pass into url.
	city1 = "+".join(city1.split())
	city2 = "+".join(city2.split())

	#For city 1
	lat1 = 0
	lon1 = 0

	#For city 2
	lat2 = 0
	lon2 = 0

	latLonData1=[]
	latLonData2=[]
	city1Thread = threading.Thread(target=latLonDataCall, args=(city1, latLonData1))
	city1Thread.start()
	city2Thread = threading.Thread(target=latLonDataCall, args=(city2, latLonData2))
	city2Thread.start()
	city1Thread.join()
	city2Thread.join()
	
	if len(latLonData1[0]) == 0:
		PollutantsData1 = ['Error','Sorry! The Data for '+city1+' is not available.']
		PollutantsData2 = ['Error']
	elif city1 in statesList:
		PollutantsData1 = ['Error','Sorry! This page only shows city related data. Please enter a city name.']
		PollutantsData2 = ['Error']
	elif len(latLonData2[0]) == 0:
		PollutantsData1 = ['Error']
		PollutantsData2 = ['Error','Sorry! The data for '+city2+' is not available.']
	elif city2 in statesList:
		PollutantsData1 = ['Error']
		PollutantsData2 = ['Error','Sorry! This page only shows city related data. Please enter a city name.']
	else:
		lat1 = str(latLonData1[0][0]['lat'])
		lon1 = str(latLonData1[0][0]['lon'])
		lat2 = str(latLonData2[0][0]['lat'])
		lon2 = str(latLonData2[0][0]['lon'])

		PollutantsData1=[]
		PollutantsData2=[]
		city1Thread = threading.Thread(target=historyDataCall, args=(lat1, lon1, latLonData1[0], PollutantsData1))
		city1Thread.start()
		city2Thread = threading.Thread(target=historyDataCall, args=(lat2, lon2, latLonData2[0], PollutantsData2))
		city2Thread.start()
		city1Thread.join()
		city2Thread.join()

	return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))



@app.route('/statevsstate', methods =['POST', 'GET'])
def statevsstate():
	PollutantsData1=[]
	PollutantsData2=[]
	if request.method == 'GET':
		return render_template('statevsstate.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	if request.method == 'POST':
		if len(request.form) == 1:
			name = request.form['name']
			#Removing extra whitespaces and converting spaces into + to pass into url.
			name = "+".join(name.split())
			if name not in statesList:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

		if len(request.form) == 2:	
			state1 = request.form['state1']
			state2 = request.form['state2']
			if len(state1) == 0 or len(state2) == 0:
				PollutantsData1=['Error','Please enter state names in the respective boxes to compare.']
				PollutantsData2=['Error']
				return render_template('statevsstate.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2)) 

	#Removing extra whitespaces and converting spaces into + to pass into url.
	state1 = "+".join(state1.split())
	state2 = "+".join(state2.split())

	stateAqi=[]

	#For state 1
	lat1=0
	lon1=0

	#For state 2
	lat2=0
	lon2=0
  
	if (state1 == 'Telangana' or state1 == 'telangana'):
		latLonData1 = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
	elif (state1 == 'Lakshadweep' or state1 == 'lakshadweep'):
		latLonData1 = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
	else:
		latLonData1 = []
		state1Thread = threading.Thread(target=latLonDataCall, args=(state1, latLonData1))
		state1Thread.start()

	if (state2 == 'Telangana' or state2 == 'telangana'):
		latLonData2 = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
	elif (state2 == 'Lakshadweep' or state2 == 'lakshadweep'):
		latLonData2 = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
	else:
		latLonData2 = []
		state2Thread = threading.Thread(target=latLonDataCall, args=(state2, latLonData2))
		state2Thread.start()

	state1Thread.join()
	state2Thread.join()

	if len(latLonData1[0])==0:
		stateAqi=['Not Found', 'Not Found']
		PollutantsData1=['Error','Sorry! The Data for '+state1+' is not available.']
		PollutantsData2=['Error']
	elif state1 not in statesList:
		stateAqi=['Not Found', 'Not Found']
		PollutantsData1=['Error','Sorry! This page only shows state related data. Please enter a state name.']
		PollutantsData2=['Error']
	elif len(latLonData2[0])==0:
		stateAqi=['Not Found', 'Not Found']
		PollutantsData1=['Error']
		PollutantsData2=['Error','Sorry! The data for '+state2+' is not available.']
	elif state2 not in statesList:
		stateAqi=['Not Found', 'Not Found']
		PollutantsData1=['Error']
		PollutantsData2=['Error','Sorry! This page only shows state related data. Please enter a state name.']
	else:
		lat1=str(latLonData1[0][0]['lat'])
		lon1=str(latLonData1[0][0]['lon'])
		lat2=str(latLonData2[0][0]['lat'])
		lon2=str(latLonData2[0][0]['lon'])

		PollutantsData1=[]
		PollutantsData2=[]
		s1t1 = threading.Thread(target=historyDataCall, args=(lat1, lon1, latLonData1[0], PollutantsData1))
		s1t1.start()
		stateData1 = []
		s1t2 = threading.Thread(target=stateDataCall, args=(lat1, lon1, stateData1))
		s1t2.start()
		s2t1 = threading.Thread(target=historyDataCall, args=(lat2, lon2, latLonData2[0], PollutantsData2))
		s2t1.start()
		stateData2 = []
		s2t2 = threading.Thread(target=stateDataCall, args=(lat2, lon2, stateData2))
		s2t2.start()

		s1t2.join()
		stateData1 = stateData1[0]['list'][0]['components']
		stateAqi.append(aqi.to_aqi([(aqi.POLLUTANT_PM25, stateData1['pm2_5']),(aqi.POLLUTANT_PM10, stateData1['pm10'])]))

		s2t2.join()
		stateData2 = stateData2[0]['list'][0]['components']
		stateAqi.append(aqi.to_aqi([(aqi.POLLUTANT_PM25, stateData2['pm2_5']),(aqi.POLLUTANT_PM10, stateData2['pm10'])]))

		s1t1.join()
		s2t1.join()

	return render_template('statevsstate.html', stateAqi = stateAqi, data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))



if __name__ == '__main__':
	app.run(debug = True)
