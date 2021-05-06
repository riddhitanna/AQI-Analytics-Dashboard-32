from flask import Flask, render_template, request
import requests

# import json to load JSON data to a python dictionary
import json

# urllib.request to make a request to api
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def weather():
    city = 'rajkot'
    if request.method == 'POST':
        city = request.form['city']
    #else:
    #    city = 'rajkot'
    url = "https://api.ambeedata.com/latest/by-city"

    querystring = {"city":city}



    headers = {
	    'x-api-key': 'OP2zHpekf92lMtj0pTuSo5ScTW1j0jLQ3Cq0QAyl',
	    'Content-type' : 'application/json'
	 }

    response = requests.request("GET", url, headers=headers, params=querystring)


    list_of_data = json.loads(response.text)

    postal_code = (list_of_data['stations'][0]['postalCode'])

    url_1 = "https://api.ambeedata.com/latest/by-postal-code"
    querystring_1 = {"postalCode":postal_code,"countryCode":"IN","from":"2021-03-25 12:16:44","to":"2021-04-04 12:16:44"}

    headers_1 = {
	    'x-api-key': 'OP2zHpekf92lMtj0pTuSo5ScTW1j0jLQ3Cq0QAyl',
	    'Content-type': 'application/json'
	}

    response_1 = requests.request("GET", url_1, headers=headers_1, params=querystring_1)


    list_of_data_1 = json.loads(response_1.text)
    #print(response.text)


    # your API key will come here
    #api = '6959927318fcbc526f939494ae3c70f8a9f3a83e'

    # source contain json data from api
    #source = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+api).read()
    #source = urllib.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lon)+'&lon='+str(lat)+'&appid='+api).read()
    #source = urllib.urlopen('https://api.waqi.info/search/?token='+api+'&keyword='+city).read()

    # converting JSON data to a dictionary

    #print(temp)


    # data for variable list_of_data
    data = {
        #'cur_aqi' : str(list_of_data_1['stations'][0]['AQI']),
        #'station_name' : str(list_of_data_1['stations'][1]['AQI']),
        #'Latlon' : str(list_of_data['data'][0]['station']['geo']),
        #"coordinate": str(list_of_data['coord']['lon']) + ' '
                #    + str(list_of_data['coord']['lat']),
        #"temp": str(list_of_data['main']['temp']) + 'k',
        #"pressure": str(list_of_data['main']['pressure']),
        #"humidity": str(list_of_data['main']['humidity']),
    }

    print(list_of_data_1)
    return render_template('index.html', data = list_of_data_1)



if __name__ == '__main__':
    app.run(debug = True)
