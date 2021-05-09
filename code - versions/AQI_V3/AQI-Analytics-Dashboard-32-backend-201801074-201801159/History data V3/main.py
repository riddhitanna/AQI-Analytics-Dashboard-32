from flask import Flask, render_template,request,jsonify
import requests
import json
import time
import datetime 
import urllib

app = Flask(__name__)

api = '72c8a65a1e2fac6803774513f214fb14'
 
@app.route('/', methods =['POST', 'GET'])
@app.route('/citydash', methods =['POST', 'GET'])
def citydash():
	return render_template('citydash.html')	

@app.route('/cityvscity', methods =['POST', 'GET'])
def cityvscity():
	PollutantsData1=[]
	PollutantsData2=[]
	if request.method == 'GET':
		return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))
	if request.method == 'POST':
		city1 = request.form['city1']
		city2 = request.form['city2']
	else:
		city1 = 'ahmedabad'
		city2 = 'surat'

	#For city 1
	lat=0
	lon=0
  
	latLon= urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city1+'&limit=1&appid='+api).read()

	latLonData = json.loads(latLon)
	
	if len(latLonData)==0:
		PollutantsData1=['Error','Sorry! The Data for '+city1+' is not available.']
	elif latLonData[0]['name'].find('State')!=-1:
		PollutantsData1=['Error','Sorry! This page only shows city related data. Please enter a city name.']
	else:
		lat=str(latLonData[0]['lat'])
		lon=str(latLonData[0]['lon'])

		sDate=datetime.date.today()-datetime.timedelta(days=8)
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

			PollutantsData1=[coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,city1]

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

		sDate=datetime.date.today()-datetime.timedelta(days=8)
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

			PollutantsData2=[coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,city2]

	return render_template('cityvscity.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))

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

		sDate=datetime.date.today()-datetime.timedelta(days=8)
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

			PollutantsData1=[coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,state1]

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

		sDate=datetime.date.today()-datetime.timedelta(days=8)
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

			PollutantsData2=[coData,noData,no2Data,o3Data,so2Data,pm2_5Data,pm10Data,nh3Data,state2]

	return render_template('statevsstate.html', data1 = PollutantsData1, len1 = len(PollutantsData1), data2 = PollutantsData2, len2 = len(PollutantsData2))

if __name__ == '__main__':
	app.run(debug = True)
