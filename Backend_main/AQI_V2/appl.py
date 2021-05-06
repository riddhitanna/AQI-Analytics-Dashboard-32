from flask import Flask, render_template, request, redirect,url_for
import requests
import json
import urllib
import sys
from importlib import reload
from flask_caching import Cache


app = Flask(__name__)
reload(sys)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})



@app.route('/',methods = ['POST','GET'])
@cache.cached(timeout=60)
def now():
    if request.method == 'POST':
        cur_city = request.form['any']
        return redirect(url_for('singular_city',city_name=cur_city))
    return render_template('navbar.html')

@app.route('/citydash/<string:city_name>',methods = ['POST','GET'])
@cache.cached(timeout=60)
def singular_city(city_name):
        url = "https://api.ambeedata.com/latest/by-city"
        querystring = {"city":city_name}
        headers = {
    	    'x-api-key': 'OP2zHpekf92lMtj0pTuSo5ScTW1j0jLQ3Cq0QAyl',
    	    'Content-type' : 'application/json'
    	 }
        response = requests.request("GET", url, headers=headers, params=querystring)
        list_of_data = json.loads(response.text)
        status = list_of_data['message']

        data = {
                "city_name" : city_name,
                "cur_aqi"  :  str(list_of_data['stations'][0]['AQI']),
                "PM25" :   str(list_of_data['stations'][0]['PM25']),
                "PM10" :    str(list_of_data['stations'][0]['PM10'])
            }
        if request.method == 'POST':
            curr_city = request.form['any']
            return redirect(url_for('singular_city',city_name=curr_city))

        return render_template('citydash.html',data=data)

@app.route('/cvc')
def cvc():
        return render_template('cityvscity.html')

if __name__ == '__main__':
    app.run(debug = True)
