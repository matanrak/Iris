import os
import json
import socket
import query
import pprint
import server
from sys import platform
from selenium import webdriver


class Iris:

    driver = object()
    server_host = 'localhost'
    server_port = 8000

    json_file = object()

    def __init__(self):

        # This heap of code checks for the os and sets the driver + query file path accordingly
        if platform == "darwin":
            Iris.driver = webdriver.Chrome(os.path.realpath('assets/chromedriver_mac'))
            Iris.json_file = json.load(open('assets/queryValues.json'))
        elif platform == "linux" or platform == "linux2":
            Iris.driver = webdriver.Chrome(os.path.realpath('assets/chromedriver_linux'))
            Iris.json_file = json.load(open('assets/queryValues.json'))
        elif platform == "win32":
            Iris.driver = webdriver.Chrome(os.path.realpath('assets\chromedriver_win.exe'))
            Iris.json_file = json.load(open('assets\queryValues.json'))
        else:
            print 'OS NOT COMPATIBLE, STOPPING SERVER.'
            exit()

        while True:
            Iris.get_answer(raw_input("Ask user for something."))


        Iris.driver.close()
        server.Server().listen()

    @staticmethod
    def get_answer(text):
        Iris.driver.restart()

        data = json.loads(Iris.fetch_from_nlp(text))
        main_entity = Iris.main_entity(data)
        query_file = query_file = Iris.get_query_file(main_entity)

        if query_file is not None:
            if Iris.get_location(data) is not None:
                query.QueryHandler.get_json(query_file, 1, Iris.get_location(data))
            else:
                query.QueryHandler.get_json(query_file, 0, None)
        else:
            "Invalid query"


    @staticmethod
    def fetch_from_nlp(text):
        element_select = Iris.driver.find_element_by_name('outputFormat')
        element_select.send_keys('json')
        element_text = Iris.driver.find_element_by_name('input')
        element_text.send_keys(text)
        element_text.submit()
        element_out = Iris.driver.find_element_by_css_selector('pre')

        return element_out.text

    @staticmethod
    def is_query(data):
        first_word = data["sentences"][0]["tokens"][0]["word"].lower()

        if first_word == "the":
            return False

        if first_word == "how" or first_word == "is":
            return True

        for obj in data["sentences"][0]["tokens"]:
            if obj["word"].lower() == data["sentences"][0]["collapsed-dependencies"][0]["dependentGloss"].lower():
                if (obj["pos"].lower() == "vbz" and obj["word"].lower() != "does") or (obj["pos"].lower() == "jj") or (obj["pos"].lower() == "vbg"):
                    return False

        for obj in data["sentences"][0]["collapsed-dependencies"]:
            if obj["dep"].lower() == "expl":
                return False

        return True

    @staticmethod
    def main_entity(data):
        for entity in data["sentences"][0]["basic-dependencies"]:
            data_local = json.loads(json.dumps(entity))
            if (data_local["dep"] == "nsubj" or data_local["dep"] == "dobj") and not Iris.is_location(data, entity["dependentGloss"]):
                return entity["dependentGloss"]
        return "NOT FOUND"

    @staticmethod
    def get_query_file(name):
        data_file = Iris.json_file
        for q in data_file["questions"]:
            for alias in q["alias"]:
                if alias.upper() == name.upper():
                    return q
        return None

    @staticmethod
    def is_location(data, name):
        for sub_name in name.split():
            for entity in data["sentences"][0]["tokens"]:
                data_local = json.loads(json.dumps(entity))
                if data_local["word"].upper() == sub_name.upper() and data_local["ner"] == "LOCATION":
                    return True
        return False

    @staticmethod
    def get_location(data):
        location_string = None

        for name in data["sentences"][0]["tokens"]:
            data_local = json.loads(json.dumps(name))
            last_location_index = -1
            if data_local["ner"] == "LOCATION":

                if last_location_index == int(data_local["index"]) - 1:
                    location_string += data_local["word"]
                else:
                    location_string = data_local["word"]
                last_location_index = int(data_local["index"])
        return location_string


Iris()