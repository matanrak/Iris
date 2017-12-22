import os
import json
import socket
import weather
import server
from sys import platform
from selenium import webdriver


class Iris:


    driver = object()
    server_host = 'localhost'
    server_port = 8000

    queryValuesFile = object()


    def __init__(self):

        if platform == "darwin":
            self.driver = webdriver.Chrome(os.path.realpath('assets/chromedriver_mac'))
            self.queryValuesFile = json.load(open('assets/queryValues.json'))
        elif platform == "linux" or platform == "linux2":
            self.driver = webdriver.Chrome(os.path.realpath('assets/chromedriver_linux'))
            self.queryValuesFile = json.load(open('assets/queryValues.json'))
        elif platform == "win32":
            self.driver = webdriver.Chrome(os.path.realpath('assets\chromedriver_win.exe'))
            self.queryValuesFile = json.load(open('assets\queryValues.json'))
        else:
            print 'OS NOT COMPATIBLE, STOPPING SERVER.'
            exit()

        self.driver.get('http://nlp.stanford.edu:8080/corenlp/process')

        print(self.queryValuesFile["weather"]["key"])
        weather.WeatherHandler().getCurrentWeather(self.queryValuesFile["weather"])


        server.Server().listen()

        #text = 'Is the weather nice?'
        #print(text)
        #print(self.is_query(json.loads(self.fetch_from_nlp(text))))
        #tree = json["sentences"][0]["collapsed-dependencies"]



    def fetch_from_nlp(self, text):

        element_select = self.driver.find_element_by_name('outputFormat')
        element_select.send_keys('json')

        element_text = self.driver.find_element_by_name('input')
        element_text.send_keys(text)
        element_text.submit()

        element_out = self.driver.find_element_by_css_selector('pre')
        json_text = element_out.text

        self.driver.close()
        return json_text



    def is_query(self, json):

        if json["sentences"][0]["tokens"][0]["word"].lower() == "the":
            return False

        for obj in json["sentences"][0]["tokens"]:
            if obj["word"].lower() == json["sentences"][0]["collapsed-dependencies"][0]["dependentGloss"].lower():
                if (obj["pos"].lower() == "vbz" and obj["word"].lower() != "does") or (obj["pos"].lower() == "jj") or (obj["pos"].lower() == "vbg"):
                    return False

        for obj in json["sentences"][0]["collapsed-dependencies"]:
            if(obj["dep"].lower() == "expl"):
                return False

        return True




Iris()

