import json
import urllib

class WeatherHandler():


    def getCurrentWeather(self, valueFileJson):

        print (str(valueFileJson['linkCurrentByCityID']))
        print (str(valueFileJson['linkCurrentByCityID']) %('thing1', 'thing2'))

        print ('test')

        url = str(valueFileJson['linkCurrentByCityID']) % (valueFileJson['defaultID'], valueFileJson['key'])

        response = urllib.urlopen(url)
        data = float(json.loads(response.read())["main"]["temp"])

        print 'Deg: ' + int(round(data / 10))