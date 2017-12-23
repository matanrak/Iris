import json
import urllib


class QueryHandler():


    def getJSON(self, values, type):

        print(values["urls"][type]["url"])
        print(values["urlFillings"])

        #url = values["urls"][type] % tuple(values["urlvalFillings"])

        print("url")

        #print (str(valueFileJson['linkCurrentByCityID']))
        #print (str(valueFileJson['linkCurrentByCityID']) %('thing1', 'thing2'))
