import json
import requests
from darksky import forecast
with open ("apikey_weather.txt", "r") as myfile:
    apiKey=myfile.read().replace('\n','')

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
        global apiKey
        if (city == None):
            send_url = 'http://freegeoip.net/json'
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat, lon = j['latitude'], j['longitude']
            print (lat, lon)
        else:
            lat, lon = WeatherIntent.getLatLon(city);
            cityForcast = forecast(apiKey, lat, lon)
            print(cityForcast)
        

WeatherIntent.getWeather();