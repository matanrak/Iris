import json
import urllib

class WeatherHandler():


    def getCurrentWeather(self, valueFileJson):

        print(valueFileJson["weather"]["key"])

        response = urllib.urlopen(valueFileJson['linkCurrentByCityID'] %(valueFileJson['defaultID'], valueFileJson['key']))
        data = float(json.loads(response.read())["main"]["temp"])

        print 'Deg: ' + int(round(data / 10))