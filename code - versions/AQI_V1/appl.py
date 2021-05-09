from flask import Flask, render_template, request

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
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'moscow'

    # your API key will come here
    api = '6959927318fcbc526f939494ae3c70f8a9f3a83e'

    # source contain json data from api
    #source = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+api).read()
    #source = urllib.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+str(lon)+'&lon='+str(lat)+'&appid='+api).read()
    source = urllib.urlopen('https://api.waqi.info/feed/'+city+'/?token='+api).read()
    #https://api.waqi.info/feed/bhopal/?token=6959927318fcbc526f939494ae3c70f8a9f3a83e

    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    for k,v in list_of_data.items():
        print(k,v)
    data = {
        'cur_aqi' : str(list_of_data['data']['city']['name']),
        #'station_name' : str(list_of_data['data']['city']['name']),
        #'Latlon' : str(list_of_data['data']['city']['geo']),
        #"coordinate": str(list_of_data['coord']['lon']) + ' '
                #    + str(list_of_data['coord']['lat']),
        #"temp": str(list_of_data['main']['temp']) + 'k',
        #"pressure": str(list_of_data['main']['pressure']),
        #"humidity": str(list_of_data['main']['humidity']),
    }
    #print(data)
    return render_template('index.html', data = data)



if __name__ == '__main__':
    app.run(debug = True)
