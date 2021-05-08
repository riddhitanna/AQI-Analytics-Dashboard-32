import json
import time
import datetime
import urllib
import threading
import requests
import aqi
from flask import Flask, render_template,request,redirect,url_for
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

api = '72c8a65a1e2fac6803774513f214fb14'

x_api_key = [	
				'y7lqVkwOnq2l09waZuwK48liHGGXtFEu2ewJoOoI',
				'4U85SanTcS7UzUpc6qSNm1grIF21KYfH53J1APie',
				'LYPTDz5sDE52WTH8pOanYaAVCNuk2G3S631o4Lwa',
				'p8hbJLVHBU38Fm3BLUHwm2TXmqUMOvAK7MOK325F',
				'um2IaiAQXu0qUMA9urNy4vtJBSP9CNg5o9Hax7Ue',
				'OP2zHpekf92lMtj0pTuSo5ScTW1j0jLQ3Cq0QAyl',
				'mUziPUNk4G4BEEtA10f4083HFUlaNukg92TBzkhk'
			]

states_list=["Andhra+Pradesh","Arunachal+Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal+Pradesh",
"Jharkhand","Karnataka","Kerala","Madhya+Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab",
"Rajasthan","Sikkim","Tamil+Nadu","Telangana","Tripura","Uttar+Pradesh","Uttarakhand","West+Bengal","Andaman+and+Nicobar+Islands",
"Delhi","Jammu+and+Kashmir","Lakshadweep","andhra+pradesh","arunachal+pradesh","assam","bihar","chhattisgarh","goa","gujarat",
"haryana","himachal+pradesh","jharkhand","karnataka","kerala","madhya+pradesh","maharashtra","manipur","meghalaya","mizoram",
"nagaland","odisha","punjab","rajasthan","sikkim","tamil+nadu","telangana","tripura","uttar+pradesh","uttarakhand","west+bengal",
"andaman+and+nicobar+islands","delhi","jammu+and+kashmir","lakshadweep"]

common_list=dict({
				"Gujarat" : {"Ahmedabad","Rajkot","Surat","Baroda","Dwarka"},
				"Sikkim" :  {"Gangtok","Gezing","Mangan","Lachung","Namchi"},
				"Andhra+Pradesh" : {"Vishakapatnam","Vijayawada","Guntur","Nellore","Kurnool"},
				"Arunachal+Pradesh" :{"Itanagar","Tawang","Naharlagun","Tezu","Roing"},
				"Assam" : {"Dispur","Guwahati","Silchar","Tezpur","Dibrugarh"},
				"Bihar" : {"Patna","Gaya","Bhagalpur","Muzaffarpur","Purnia"},
				"Chhattisgarh" : {"Bhilai","Raipur","Korba","Bilaspur","Raigarh"},
				"Goa":{"Panaji","Margao","Mormugao","Mapusa","Sanguem"},
				"Haryana":{"Gurgaon","Faridabad","Rohtak","Hisar","Panipat"},
				"Himachal+Pradesh":{"Shimla","Dharmashala","Mandi","Solan","Chamba"},
				"Jharkhand":{"Ranchi","Dhanbad","Jamshedpur","Deogarh","Hazaribagh"},
				"Karnataka":{"Bangalore","Mangalore","Mysore","Hubli","Belgaum"},
				"Kerala":{"Kochi","Thiruvanathapuram","Kozhikode","Thrissur","Kolam"},
				"Madhya+Pradesh":{"Indore","Gwalior","Bhopal","Jabalpur","Ujjain"},
				"Maharashtra":{"Mumbai","Nagpur","Pune","Thane","Aurangabad"},
				"Manipur":{"Imphal","Kakaching","Ukhrul","Moirang","Tamenglong"},
				"Meghalaya" : {'Cherrapunji','Shillong','Dawki','Mawlynnong','Laitumkhrah'}, 
				"Mizoram" : {'Aizawl','Lunglei','Lengpui','Bairabi','Ngopa'}, 
				"Nagaland" : {'Kohima','Ungma','Chumukedima','Mopongchuket','Wokha'}, 
				"Odisha" : {'Angul','Baripada','Jeypore','Bhubaneswar','Cuttack'}, 
				"Punjab" : {'Amritsar','Bathinda','Ludhiana','Chandigarh','Patiala'}, 
				"Rajasthan" : {'Ajmer','Bikaner','Jaipur','Jaisalmer','Jodhpur'}, 
				"Tamil+Nadu" : {'Chennai','Coimbatore','Rameswaram','Kanyakumari','Ooty'}, 
				"Telangana" : {'Hyderabad','Warangal','Nalgonda','Adilabad','Basara'}, 
				"Tripura" : {'Agartala','Amarpur','Melaghar','Kailashahar','Belonia'}, 
				"Uttar+Pradesh" : {'Agra','Kanpur','Ayodhya','Meerut','Lucknow'}, 
				"Uttarakhand" : {'Badrinath','Dehradun','Rishikesh','Haridwar','Kedarnath'}, 
				"West+Bengal" : {'Darjeeling','Kolkata','Siliguri','Howrah','Jalpaiguri'}, 
				"Andaman+and+Nicobar+Islands" : {'Port Blair','Diglipur','Prothrapur','Bakultala','Garacharma'}, 
				"Delhi" : {'New Delhi','North Delhi','South Delhi','East Delhi','West Delhi'},
				"Jammu+and+Kashmir" : {'Jammu','Ladakh','Srinagar','Leh','Patnitop'}, 
				"Lakshadweep" : {'Kavaratti','Minicoy','Andrott','Amini','Kalpeni'}
				 })
metro_list = ["Mumbai","Bangalore","Kolkata","Chennai","New Delhi"]



def latLonDataCall(name, latLonData):
	latLon = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+name+'&limit=1&appid='+api).read()
	latLonData.append(json.loads(latLon))



def historyDataCall(lat, lon, latLonData, pollutantsData):
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
		pollutantsData=['Error','Sorry! The requested city data is not available.']
	else:
		hData1 = historyData['list']
		prevDate='0'
		count=1
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

		pollutantsData.extend([historyAqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']])



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

def cityDataCall(city, city_data, use_key):
	print("******************************************")
	url='https://api.ambeedata.com/latest/by-city'
	headers = {'x-api-key': use_key,'Content-type' : 'application/json'}
	querystring = {"city":city}
	response = requests.request("GET", url, headers=headers, params=querystring)
	list_of_data = json.loads(response.text)
	if str(list_of_data['message']) == 'success':
		temp_data = {
					"city_name" : city,
					"status" : str(list_of_data['stations'][0]['aqiInfo']['category']),
					"cur_aqi"  :  str(list_of_data['stations'][0]['AQI']), 
					"PM25" : str(list_of_data['stations'][0]['PM25']), 
					"PM10" : str(list_of_data['stations'][0]['PM10']),
					"CO" : str(list_of_data['stations'][0]['CO']),
					"SO2" : str(list_of_data['stations'][0]['SO2'])

				}
		city_data.append(temp_data)
	else:
		temp_data = {
					"city_name" : str(list_of_data['message']),
					"status" : 'Invalid',
					"cur_aqi" : 'Invalid',
					"PM25" : 'Invalid',
					"PM10" : 'Invalid',
					"CO" : 'Invalid',
					"SO2" : 'Invalid'
				}
		city_data.append(temp_data)



def stateHistoryDataPartCall(name, aqi_data):
	print("#############################################")
	lat=0
	lon=0

	if(name in ('Telangana', 'telangana')):
		lat='18.1124'
		lon='79.0193'
	elif(name in ('Lakshadweep', 'lakshadweep')):
		lat='10.57'
		lon='72.64'
	else:
		latLonData = []
		latLonDataCall(name, latLonData)
		lat=str(latLonData[0][0]['lat'])
		lon=str(latLonData[0][0]['lon'])

	stateData = []
	stateDataCall(lat, lon, stateData)
	stateData = stateData[0]['list'][0]['main']
	aqi_data.append(stateData['aqi'])



def checkCallAvailability():
	url='https://api.ambeedata.com/latest/by-city'
	qcheck = {"city":'kanpur'}
	use_key=''
	for key in x_api_key:
		headers = {'x-api-key': key,'Content-type' : 'application/json'}
		response = requests.request("GET", url, headers=headers, params=qcheck)
		list_of_data = json.loads(response.text)
		if str(list_of_data['message'])=='success':
			use_key = key
			break
	return use_key



class Foo(object):

	@cache.cached(timeout=3600,key_prefix='access_city')
	def access(self):
		use_key = checkCallAvailability()

		metroThreads = []
		metro_data = []
		i=0
		for cityName in metro_list:
			metro_data.append([])
			t = threading.Thread(target=cityDataCall, args=(cityName, metro_data[i], use_key))
			t.start()
			metroThreads.append(t)
			i = i + 1

		for metroThread in metroThreads:
			metroThread.join()

		return metro_data


		
	@cache.cached(timeout=3600,key_prefix='access_state')
	def access1(self):
		aqi_data = []
		threads = []
		for i in range(32):
			aqi_data.append([])
			t = threading.Thread(target=stateHistoryDataPartCall, args=(states_list[i], aqi_data[i]))
			t.start()
			threads.append(t)

		for thread in threads:
			thread.join()

		return aqi_data



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
			if name not in states_list:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

	metro_data = Foo().access()
	aqi_data = Foo().access1()

	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
		include = 0

	return render_template('maindashboard.html', metroData = metro_data, data = aqi_data, len = len(aqi_data), error = error, errorlen = len(error))


@app.route('/mylocation', methods =['POST', 'GET'])
def mylocation():
	url = "https://freegeoip.app/json/"
	headers = {
		'accept': "application/json",
		'content-type': "application/json"
	}

	response = requests.request("GET", url, headers=headers)

	j = json.loads(response.text)
	loc_city = j['city']
	print("*****************")
	print(loc_city)
	print("*****************")

	return redirect(url_for('citydash', name = loc_city))


@app.route('/statedashboard', methods =['POST', 'GET'])
@app.route('/statedashboard/<string:name>/', methods =['POST', 'GET'])
def statedashboard(name=""):
	name=str(name)
	if request.method == 'POST':
		name = request.form['name']
		#Removing extra whitespaces and converting spaces into + to pass into url.
		name = "+".join(name.split())
	if len(name) == 0:
		stateAqi = []
		stateData = []
		weatherData=['Error']
		stateHistoryData=['Error','Please enter a place in searchbox to search for air pollution details of required place.']
		cityData=[]
	else:
		if name not in states_list:
			return redirect(url_for('citydash', name = name))

		lat=0
		lon=0

		if (name in ('Telangana', 'telangana')):
			latLonData = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
		elif (name in ('Lakshadweep', 'lakshadweep')):
			latLonData = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
		else:
			latLonData = []
			latLonDataCall(name,latLonData)

		if len(latLonData[0])==0:
			stateAqi = []
			stateData = []
			weatherData = ['Error']
			stateHistoryData = ['Error','Sorry! The Data for '+name+' is not available.']
			cityData = []
		else:
			use_key = checkCallAvailability()

			cityThreads = []
			cityData=[]
			i=0
			for cityName in common_list[name]:
				cityData.append([])
				t = threading.Thread(target=cityDataCall, args=(cityName, cityData[i], use_key))
				t.start()
				cityThreads.append(t)
				i = i + 1

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

			for cityThread in cityThreads:
				cityThread.join()

			t1.join()
			stateData = stateData[0]['list'][0]['components']
			stateAqi = aqi.to_aqi([(aqi.POLLUTANT_PM25, stateData['pm2_5']),(aqi.POLLUTANT_PM10, stateData['pm10'])])

			t2.join()
			t3.join()

	return render_template('statedashboard.html', cityData = cityData, stateAqi = stateAqi, aqiData = stateData, weatherData = weatherData[0], historyData = stateHistoryData, errorlen = len(stateHistoryData))



@app.route('/citydash', methods =['POST', 'GET'])
@app.route('/citydash/<string:name>/', methods =['POST', 'GET'])
def citydash(name=""):
	name = str(name)
	#Removing extra whitespaces and converting spaces into + to pass into url.
	name = "+".join(name.split())
	if request.method == 'POST':
		name = request.form['name']
		#Removing extra whitespaces and converting spaces into + to pass into url.
		name = "+".join(name.split())
		if len(name) == 0:
			pollutantsData = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
			city_data = []
			weatherData = ['Error']
			return render_template('citydash.html', citydata = city_data, pollutantsData= pollutantsData, len = len(pollutantsData))
		else:
			if name in states_list:
				return redirect(url_for('statedashboard', name = name))

	historyData = []
	lat = 0
	lon = 0

	latLonData=[]
	t = threading.Thread(target=latLonDataCall, args=(name, latLonData))
	t.start()
	t.join()

	if len(latLonData[0]) == 0:
		historyData = ['Error','Sorry! The Data for '+name+' is not available.']
		city_data = ['Error']
		weatherData = ['Error']
	else:
		use_key = checkCallAvailability()

		city_data = []
		t1 = threading.Thread(target=cityDataCall, args=(name, city_data, use_key))
		t1.start()
		t2 = threading.Thread(target=historyDataCall, args=(lat, lon, latLonData[0], historyData))
		t2.start()
		weatherData = []
		t3 = threading.Thread(target=weatherDataCall, args=(lat, lon, weatherData))
		t3.start()

		t1.join()
		t2.join()
		t3.join()

	return render_template('citydash.html', citydata = city_data, weatherData = weatherData[0], historyData= historyData, len = len(historyData))


@app.route('/cityvscity', methods =['POST', 'GET'])
def cityvscity():
	pollutantsData1=[]
	pollutantsData2=[]
	if request.method == 'GET':
		return render_template('cityvscity.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))
	
	if request.method == 'POST':
		if len(request.form) == 1:
			name = request.form['name']
			#Removing extra whitespaces and converting spaces into + to pass into url.
			name = "+".join(name.split())
			if len(name) == 0:
				pollutantsData1=['Error','Please enter a place in searchbox to search for air pollution details of required place.']
				pollutantsData2=['Error']
				return render_template('cityvscity.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))
			elif name not in states_list:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

		if len(request.form) == 2:	
			city1 = request.form['city1']
			city2 = request.form['city2']
			if len(city1) == 0 or len(city2) == 0:
				pollutantsData1=['Error','Please enter city names in the respective boxes to compare.']
				pollutantsData2=['Error']
				return render_template('cityvscity.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2)) 

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
		pollutantsData1 = ['Error','Sorry! The Data for '+city1+' is not available.']
		pollutantsData2 = ['Error']
	elif city1 in states_list:
		pollutantsData1 = ['Error','Sorry! This page only shows city related data. Please enter a city name.']
		pollutantsData2 = ['Error']
	elif len(latLonData2[0]) == 0:
		pollutantsData1 = ['Error']
		pollutantsData2 = ['Error','Sorry! The data for '+city2+' is not available.']
	elif city2 in states_list:
		pollutantsData1 = ['Error']
		pollutantsData2 = ['Error','Sorry! This page only shows city related data. Please enter a city name.']
	else:
		use_key = checkCallAvailability()

		city1_data = []
		tc1 = threading.Thread(target=cityDataCall, args=(city1, city1_data, use_key))
		tc1.start()

		city2_data = []
		tc2 = threading.Thread(target=cityDataCall, args=(city2, city2_data, use_key))
		tc2.start()

		lat1 = str(latLonData1[0][0]['lat'])
		lon1 = str(latLonData1[0][0]['lon'])
		lat2 = str(latLonData2[0][0]['lat'])
		lon2 = str(latLonData2[0][0]['lon'])

		pollutantsData1=[]
		pollutantsData2=[]
		city1Thread = threading.Thread(target=historyDataCall, args=(lat1, lon1, latLonData1[0], pollutantsData1))
		city1Thread.start()
		city2Thread = threading.Thread(target=historyDataCall, args=(lat2, lon2, latLonData2[0], pollutantsData2))
		city2Thread.start()
		city1Thread.join()
		city2Thread.join()

		tc1.join()
		tc2.join()

		city_data = [city1_data, city2_data]

	return render_template('cityvscity.html', citydata = city_data, data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))



@app.route('/statevsstate', methods =['POST', 'GET'])
def statevsstate():
	pollutantsData1=[]
	pollutantsData2=[]
	if request.method == 'GET':
		return render_template('statevsstate.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))
	if request.method == 'POST':
		if len(request.form) == 1:
			name = request.form['name']
			#Removing extra whitespaces and converting spaces into + to pass into url.
			name = "+".join(name.split())
			if len(name) == 0:
				pollutantsData1=['Error','Please enter a place in searchbox to search for air pollution details of required place.']
				pollutantsData2=['Error']
				return render_template('statevsstate.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))
			elif name not in states_list:
				return redirect(url_for('citydash', name = name))
			else:
				return redirect(url_for('statedashboard', name = name))

		if len(request.form) == 2:	
			state1 = request.form['state1']
			state2 = request.form['state2']
			if len(state1) == 0 or len(state2) == 0:
				pollutantsData1=['Error','Please enter state names in the respective boxes to compare.']
				pollutantsData2=['Error']
				return render_template('statevsstate.html', data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2)) 

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
  
	if (state1 in ('Telangana', 'telangana')):
		latLonData1 = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
	elif (state1 in ('Lakshadweep', 'lakshadweep')):
		latLonData1 = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
	else:
		latLonData1 = []
		state1Thread = threading.Thread(target=latLonDataCall, args=(state1, latLonData1))
		state1Thread.start()

	if (state2 in ('Telangana', 'telangana')):
		latLonData2 = [[{'name': 'Telangana', 'lat':'18.1124', 'lon':'79.0193'}]]
	elif (state2 in ('Lakshadweep', 'lakshadweep')):
		latLonData2 = [[{'name': 'Lakshadweep', 'lat':'10.57', 'lon':'72.64'}]]
	else:
		latLonData2 = []
		state2Thread = threading.Thread(target=latLonDataCall, args=(state2, latLonData2))
		state2Thread.start()

	state1Thread.join()
	state2Thread.join()

	if len(latLonData1[0])==0:
		stateAqi=['Not Found', 'Not Found']
		pollutantsData1=['Error','Sorry! The Data for '+state1+' is not available.']
		pollutantsData2=['Error']
	elif state1 not in states_list:
		stateAqi=['Not Found', 'Not Found']
		pollutantsData1=['Error','Sorry! This page only shows state related data. Please enter a state name.']
		pollutantsData2=['Error']
	elif len(latLonData2[0])==0:
		stateAqi=['Not Found', 'Not Found']
		pollutantsData1=['Error']
		pollutantsData2=['Error','Sorry! The data for '+state2+' is not available.']
	elif state2 not in states_list:
		stateAqi=['Not Found', 'Not Found']
		pollutantsData1=['Error']
		pollutantsData2=['Error','Sorry! This page only shows state related data. Please enter a state name.']
	else:
		lat1=str(latLonData1[0][0]['lat'])
		lon1=str(latLonData1[0][0]['lon'])
		lat2=str(latLonData2[0][0]['lat'])
		lon2=str(latLonData2[0][0]['lon'])

		pollutantsData1=[]
		pollutantsData2=[]
		s1t1 = threading.Thread(target=historyDataCall, args=(lat1, lon1, latLonData1[0], pollutantsData1))
		s1t1.start()
		stateData1 = []
		s1t2 = threading.Thread(target=stateDataCall, args=(lat1, lon1, stateData1))
		s1t2.start()
		s2t1 = threading.Thread(target=historyDataCall, args=(lat2, lon2, latLonData2[0], pollutantsData2))
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

	return render_template('statevsstate.html', stateAqi = stateAqi, data1 = pollutantsData1, len1 = len(pollutantsData1), data2 = pollutantsData2, len2 = len(pollutantsData2))



if __name__ == '__main__':
	app.run(debug = True)
