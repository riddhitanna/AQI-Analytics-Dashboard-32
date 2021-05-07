from flask import Flask, render_template,request,jsonify,redirect,url_for
import requests
import json
import time
import datetime
import urllib
import aqi
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

statesList=["Andhra+Pradesh","Arunachal+Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal+Pradesh","Jharkhand","Karnataka","Kerala",
"Madhya+Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil+Nadu","Telangana","Tripura",
"Uttar+Pradesh","Uttarakhand","West+Bengal","Andaman+and+Nicobar+Islands","Delhi","Jammu+and+Kashmir","Lakshadweep","andhra+pradesh","arunachal+pradesh","assam",
"bihar","chhattisgarh","goa","gujarat","haryana","himachal+pradesh","jharkhand","karnataka","kerala","madhya+pradesh","maharashtra","manipur","meghalaya","mizoram",
"nagaland","odisha","punjab","rajasthan","sikkim","tamil+nadu","telangana","tripura","uttar+pradesh","uttarakhand","west+bengal","andaman+and+nicobar+islands","delhi","jammu+and+kashmir","lakshadweep"]



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
				  "Manipur":{"Imphal","Kakaching","Ukhrul","Moirang","Moreh"},
				  "Meghalaya" : {'Cherrapunji','Shillong','Dawki','Mawlynnong','Laitumkhrah'},
				  "Mizoram" : {'Aizawl','Lunglei','Lengpui','Bairabi','Ngopa'},
				  "Nagaland" : {'Kohima','Ungma','Chumukedima','Mopongchuket','Wokha'},
				  "Odisha" : {'Angul','Baripada','Jeypore','Bhubaneswar','Cuttack'},
				  "Punjab" : {'Amritsar','Bathinda','Ludhiana','Chandigarh','Patiala'},
				  "Rajasthan" : {'Ajmer','Bikaner','Jaipur','Jaisalmer','Jodhpur'},
				  "Sikkim" : {'Gangtok','Lachung','Namchi','Pelling','Ravangla'},
				  "Tamil+Nadu" : {'Chennai','Coimbatore','Rameswaram','Kanyakumari','Ooty'},
				  "Telangana" : {'Hyderabad','Warangal','Nalgonda','Adilabad','Basara'},
				  "Tripura" : {'Agartala','Amarpur','Melaghar','Kailashahar','Belonia'},
				  "Uttar+Pradesh" : {'Agra','Kanpur','Ayodhya','Meerut','Lucknow'},
				  "Uttarakhand" : {'Badrinath','Dehradun','Rishikesh','Haridwar','Kedarnath'},
				  "West+Bengal" : {'Darjeeling','Kolkata','Siliguri','Howrah','Jalpaiguri'},
				  "Andaman+Nicobar+Islands" : {'Port Blair','Diglipur','Prothrapur','Bakultala','Garacharma'},
				  "Delhi" : {'New Delhi','North Delhi','South Delhi','East Delhi','West Delhi'},
				  "Jammu+and+Kashmir" : {'Jammu','Ladakh','Srinagar','Leh','Patnitop'},
				  "Lakshadweep" : {'Kavaratti','Minicoy','Andrott','Bitra','Kalpeni'}
				 })
metro_list = ["Mumbai","Bangalore","Kolkata","Chennai","New Delhi"]




class Foo(object):

	@cache.cached(timeout=300000,key_prefix='access_city')
	def access(self):
		url='https://api.ambeedata.com/latest/by-city'
		qcheck = {"city":'kanpur'}
		use_key=''
		for key in x_api_key:
			headers = {'x-api-key': key,'Content-type' : 'application/json'}
			response = requests.request("GET", url, headers=headers, params=qcheck)
			list_of_data = json.loads(response.text)
			print(key)
			if str(list_of_data['message'])=='success':
				use_key = key
				print(use_key)
				break
		metro_data=[]
		
		for city_name in metro_list:
			querystring = {"city":city_name}
			headers = {'x-api-key': use_key,'Content-type' : 'application/json'}
			response = requests.request("GET", url, headers=headers, params=querystring)
			list_of_data = json.loads(response.text)
			print(list_of_data)
			if str(list_of_data['message'])=='success':

				temp_data = {
							"city_name" : city_name,
							"status" : str(list_of_data['stations'][0]['aqiInfo']['category']),
							"cur_aqi"  :  str(list_of_data['stations'][0]['AQI']), 
							"PM25" : str(list_of_data['stations'][0]['PM25']), 
							"PM10" : str(list_of_data['stations'][0]['PM10']),
							"CO" : str(list_of_data['stations'][0]['CO']),
							"SO2" : str(list_of_data['stations'][0]['SO2'])

						}
				metro_data.append(temp_data)
			else:
				temp_data = {
							"city_name" : str(list_of_data['message']),
							"status" : 'Invalid',
							"cur_aqi"  :  'Invalid', 
							"PM25" : 'Invalid', 
							"PM10" : 'Invalid',
							"CO" : 'Invalid',
							"SO2" : 'Invalid'

						}
				metro_data.append(temp_data)
		return metro_data
				

		
	@cache.cached(timeout=300000,key_prefix='access_state')
	def access1(self):
		aqiData=[]

		for i in range(32):

			lat=0
			lon=0

			# source contain json data from api
			latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+statesList[i]+'&limit=1&appid='+api).read()
			latLonData = json.loads(latLon)

			if(statesList[i] == 'Telangana' or statesList[i] == 'telangana'):
				lat='18.1124'
				lon='79.0193'
			elif(statesList[i] == 'Lakshadweep' or statesList[i] == 'lakshadweep'):
				lat='10.57'
				lon='72.64'
			else:
				lat=str(latLonData[0]['lat'])
				lon=str(latLonData[0]['lon'])

			state = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api).read()

			stateData = json.loads(state)

			stateData = stateData['list'][0]['main']

			aqiData.append(stateData['aqi'])
		return aqiData

	
	

@app.route('/', methods =['POST', 'GET']) 
#@app.route('/maindashboard', methods =['POST', 'GET'])
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
	metro_data = Foo().access()
	aqiData    = Foo().access1()

	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
	return render_template('maindashboard.html', metrodata = metro_data, data = aqiData, len = len(aqiData), error = error, errorlen = len(error))



@app.route('/statedashboard', methods =['POST', 'GET'])
@app.route('/statedashboard/<string:name>/', methods =['POST', 'GET'])
def statedashboard(name=""):
	name=str(name)
	include = 0
	if request.method == 'POST':
		vari = request.form['name']
		#Removing extra whitespaces and converting spaces into + to pass into url.
		#name = "+".join(name.split())
		if len(vari) == 0:
			include = 1
		else:
			#Removing extra whitespaces and converting spaces into + to pass into url.
			vari = "+".join(vari.split())

			if vari not in statesList:
				return redirect(url_for('citydash', name = vari))
			else:
				return redirect(url_for('statedashboard', name = vari))
	url='https://api.ambeedata.com/latest/by-city'
	qcheck = {"city":'rajkot'}
	use_key=''
	for key in x_api_key:
		headers = {'x-api-key': key,'Content-type' : 'application/json'}
		response = requests.request("GET", url, headers=headers, params=qcheck)
		list_of_data = json.loads(response.text)
		if str(list_of_data['message'])=='success':
			use_key = key
			print(use_key)
			break
	city_data=[]
	for city_name in common_list[name]:
		querystring = {"city":city_name}
		headers = {'x-api-key': use_key,'Content-type' : 'application/json'}
		response = requests.request("GET", url, headers=headers, params=querystring)
		list_of_data = json.loads(response.text)
		print(list_of_data)
		if str(list_of_data['message'])=='success':

			temp_data = {
						"city_name" : city_name,
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
						"cur_aqi"  :  'Invalid', 
						"PM25" : 'Invalid', 
						"PM10" : 'Invalid',
						"CO" : 'Invalid',
						"SO2" : 'Invalid'

					}
			city_data.append(temp_data)
			
	lat=0
	lon=0

    # source contain json data from api
	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+name+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	stateData=[]

	if len(latLonData)==0:
		stateData=['Error','Sorry! The Data for '+name+' is not available.']
	elif latLonData[0]['name'].find('State')==-1:
		if name not in statesList:
			return redirect(url_for('citydash', name = name))
	if len(latLonData)>0:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

		state = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api).read()

		stateData = json.loads(state)

		stateData = stateData['list'][0]['components']

		weather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api+'&units=metric').read()

		weatherData = json.loads(weather)

		weatherData = weatherData['main']

		sDate=datetime.date.today()-datetime.timedelta(days=31)
		sDateformatted=sDate.strftime('%d/%m/%Y')
		eDate=datetime.date.today()-datetime.timedelta(days=1)
		eDateformatted=eDate.strftime('%d/%m/%Y')
		sUNIX=int(time.mktime(datetime.datetime.strptime(sDateformatted, "%d/%m/%Y").timetuple()))
		eUNIX=int(time.mktime(datetime.datetime.strptime(eDateformatted, "%d/%m/%Y").timetuple()))

		history = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+str(lat)+'&lon='+str(lon)+'&start='+str(sUNIX)+'&end='+str(eUNIX)+'&appid='+api).read()

		historyData = json.loads(history)

		error=[]

		stateHistoryData=[]

		if 'cod' in historyData:
			error=['404']
		else:
			error=['10000']

		if error[0]=='404':
			stateHistoryData=['Error','Sorry! The requested city data is not available.']
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

			aqiData=[]
			for i in range(len(pm2_5Data)):
				aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])

			stateHistoryData=[aqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']]

	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
	return render_template('statedashboard.html', citydata = city_data, aqiData = stateData, weatherData = weatherData, historyData = stateHistoryData)



@app.route('/citydash', methods =['POST', 'GET'])
@app.route('/citydash/<string:name>/', methods =['POST', 'GET'])
def citydash(name=""):
	name = str(name)
	include = 0
	if request.method == 'POST':
		vari = request.form['name']
		#Removing extra whitespaces and converting spaces into + to pass into url.
		#name = "+".join(name.split())
		if len(vari) == 0:
			include = 1
		else:
			#Removing extra whitespaces and converting spaces into + to pass into url.
			vari = "+".join(vari.split())

			if vari not in statesList:
				return redirect(url_for('citydash', name = vari))
			else:
				return redirect(url_for('statedashboard', name = vari))
	url='https://api.ambeedata.com/latest/by-city'
	qcheck = {"city":'rajkot'}
	use_key=''
	for key in x_api_key:
		headers = {'x-api-key': key,'Content-type' : 'application/json'}
		response = requests.request("GET", url, headers=headers, params=qcheck)
		list_of_data = json.loads(response.text)
		if str(list_of_data['message'])=='success':
			use_key = key
			print(use_key)
			break

	city_data=[]
	
	querystring = {"city":name}
	headers = {'x-api-key': use_key,'Content-type' : 'application/json'}
	response = requests.request("GET", url, headers=headers, params=querystring)
	list_of_data = json.loads(response.text)
	print(list_of_data)
	if str(list_of_data['message'])=='success':
		temp_data = {
					"city_name" : name,
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
						"cur_aqi"  : 'Invalid', 
						"PM25" : 'Invalid', 
						"PM10" : 'Invalid',
						"CO" : 'Invalid',
						"SO2" : 'Invalid'

					}
		city_data.append(temp_data)
	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
	return render_template('citydash.html',citydata=city_data)



@app.route('/cityvscity', methods =['POST', 'GET'])
def cityvscity():
	PollutantsData1=[]
	PollutantsData2=[]
	include = 0
	if request.method == 'GET':
		return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	if request.method == 'POST':
		if len(request.form) == 1:
			vari = request.form['name']
			#Removing extra whitespaces and converting spaces into + to pass into url.
			#name = "+".join(name.split())
			if len(vari) == 0:
				include = 1
			else:
				#Removing extra whitespaces and converting spaces into + to pass into url.
				vari = "+".join(vari.split())

			if vari not in statesList:
				return redirect(url_for('citydash', name = vari))
			else:
				return redirect(url_for('statedashboard', name = vari))
		elif len(request.form) == 2:
			city1 = request.form['city1']
			city2 = request.form['city2']
			if len(city1) == 0 or len(city2) == 0:
				PollutantsData1=['Error','Please enter city names in the respective boxes to compare.']
				PollutantsData2=['Error']
				return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	else:
		city1 = 'ahmedabad'
		city2 = 'surat'

	#Removing extra whitespaces and converting spaces into + to pass into url.
	city1 = "+".join(city1.split())
	city2 = "+".join(city2.split())

	url='https://api.ambeedata.com/latest/by-city'
	qcheck = {"city":'rajkot'}
	use_key=''
	for key in x_api_key:
		headers = {'x-api-key': key,'Content-type' : 'application/json'}
		response = requests.request("GET", url, headers=headers, params=qcheck)
		list_of_data = json.loads(response.text)
		if str(list_of_data['message'])=='success':
			use_key = key
			print(use_key)
			break

	city_data = []
	querystring = {"city":city1}
	headers = {'x-api-key': use_key,'Content-type' : 'application/json'}
	response = requests.request("GET", url, headers=headers, params=querystring)
	list_of_data = json.loads(response.text)
	
	temp_data = { "city_name" : city1,"cur_aqi"  :  str(list_of_data['stations'][0]['AQI'])}
	city_data.append(temp_data)

	querystring = {"city":city2}

	response = requests.request("GET", url, headers=headers, params=querystring)
	list_of_data_1 = json.loads(response.text)
	
	temp_data_1 = { "city_name" : city2, "cur_aqi"  :  str(list_of_data_1['stations'][0]['AQI'])}
	city_data.append(temp_data_1)




	#For city 1
	lat = 0
	lon = 0

	latLon = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city1+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	if len(latLonData)==0:
		PollutantsData1=['Error','Sorry! The Data for '+city1+' is not available.']
	elif latLonData[0]['name'].find('State')!=-1:
		PollutantsData1=['Error','Sorry! This page only shows city related data. Please enter a city name.']
	else:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

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
			PollutantsData1=['Error','Sorry! The requested city data is not available.']
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

			aqiData=[]
			for i in range(len(pm2_5Data)):
				aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])

			PollutantsData1=[aqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']]

	#For city 2
	lat=0
	lon=0

	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city2+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	if len(latLonData)==0:
		PollutantsData2=['Error','Sorry! The data for '+city2+' is not available.']
	elif latLonData[0]['name'].find('State')!=-1:
		PollutantsData2=['Error','Sorry! This page only shows city related data. Please enter a city name.']
	else:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

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
			PollutantsData2=['Error','Sorry! The requested city data is not available.']
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

			aqiData=[]
			for i in range(len(pm2_5Data)):
				aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])

			PollutantsData2=[aqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']]

	error=[]
	if include == 1:
		error = ['Error','Please enter a place in searchbox to search for air pollution details of required place.']
	return render_template('cityvscity.html', citydata = city_data,data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))



@app.route('/statevsstate', methods =['POST', 'GET'])
def statevsstate():
	PollutantsData1=[]
	PollutantsData2=[]
	if request.method == 'GET':
		return render_template('statevsstate.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	if request.method == 'POST':
		state1 = request.form['state1']
		state2 = request.form['state2']
	else:
		state1 = 'Gujarat'
		state2 = 'Maharashtra'

	#Removing extra whitespaces and converting spaces into + to pass into url.
	state1 = "+".join(state1.split())
	state2 = "+".join(state2.split())

	#For state 1
	lat=0
	lon=0

	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+state1+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	if len(latLonData)==0:
		PollutantsData1=['Error','Sorry! The Data for '+state1+' is not available.']
	elif latLonData[0]['name'].find('State')==-1:
		PollutantsData1=['Error','Sorry! This page only shows state related data. Please enter a state name.']
	else:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

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
			PollutantsData1=['Error','Sorry! The requested state data is not available.']
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

			aqiData=[]
			for i in range(len(pm2_5Data)):
				aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])

			PollutantsData1=[aqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']]

	#For state 2
	lat=0
	lon=0

	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+state2+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)

	if len(latLonData)==0:
		PollutantsData2=['Error','Sorry! The data for '+state2+' is not available.']
	elif latLonData[0]['name'].find('State')==-1:
		PollutantsData2=['Error','Sorry! This page only shows state related data. Please enter a state name.']
	else:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

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
			PollutantsData2=['Error','Sorry! The requested state data is not available.']
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

			aqiData=[]
			for i in range(len(pm2_5Data)):
				aqiData.append([pm2_5Data[i][0],aqi.to_aqi([(aqi.POLLUTANT_PM25, pm2_5Data[i][1]),(aqi.POLLUTANT_PM10, pm10Data[i][1])])])

			PollutantsData2=[aqiData,coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,latLonData[0]['name']]

	return render_template('statevsstate.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))



if __name__ == '__main__':
	app.run(debug = True)
