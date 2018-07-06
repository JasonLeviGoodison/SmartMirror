import json
import requests
from darksky import forecast
with open ("apikey_weather.txt", "r") as myfile:
    apiKey=myfile.read().replace('\n','')
with open ("ip_stack_key.txt", "r") as myfile:
    ipStackKey=myfile.read().replace('\n','')
class WeatherIntent:
    @staticmethod
    def getLatLon(city):
        url = 'https://darksky.net/geo?q=' + city
        r = requests.get(url=url, headers={});
        jsonObject = json.loads(r.content)
        lat,lon = jsonObject['latitude'], jsonObject['longitude']
        return lat,lon
    
    @staticmethod
    def getWeather(city = None):
        global apiKey, ipStackKey
        if (city == None):
            send_url = 'http://api.ipstack.com/' + str(get_ip()) + '?access_key=' + ipStackKey
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat, lon = j['latitude'], j['longitude']
        else:
            lat, lon = WeatherIntent.getLatLon(city);
            cityForcast = forecast(apiKey, lat, lon)
        # at this point we have to lat, lon
        url = 'https://api.darksky.net/forecast/' + apiKey + '/' + str(lat) + ',' + str(lon) + '?units=si'
        r = requests.get(url)
        j = json.loads(r.text)
        summary = ''
        if (j['hourly']):
            summary = j['hourly']['summary']
        j = j['currently']
        cityName = WeatherIntent.getCityName(lat, lon);
        return { 'weather': j['summary'],
                 'temp': j['temperature'],
                 'icon': j['icon'],
                 'city': cityName,
                 'summary': summary
        }
    @staticmethod
    def getCityName(lat, lon):
        url = 'https://darksky.net/rgeo?lat=' + str(lat) + '&lon=' + str(lon);
        print(url)
        r = requests.get(url)
        j = json.loads(r.text)
        city = j['name']
        return city

import socket
def get_ip():
    send_url = 'http://api.ipstack.com/check?access_key=' + ipStackKey
    r = requests.get(send_url)
    j = json.loads(r.text)
    return j['ip'];
