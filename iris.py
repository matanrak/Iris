import os
import json
import query
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

        Iris.get_answer("What's in the news?")

        while True:
            Iris.get_answer(raw_input("Ask user for something."))


        Iris.driver.close()
        server.Server().listen()

    @staticmethod
    def get_answer(text):

        data = json.loads(Iris.fetch_from_nlp(text))["sentences"][0]
        main_entity = Iris.main_entity(data)
        query_file = Iris.get_query_file(main_entity)
        print("Main: " + main_entity)
        if query_file is not None:
            if Iris.get_location(data) is not None:
                query.QueryHandler.get_json(query_file, 1, Iris.get_location(data))
            else:
                query.QueryHandler.get_json(query_file, 0, None)
        else:
            "Invalid query"

    @staticmethod
    def fetch_from_nlp(text):
        Iris.driver.get("http://nlp.stanford.edu:8080/corenlp/process")
        element_select = Iris.driver.find_element_by_name('outputFormat')
        element_select.send_keys('json')
        element_text = Iris.driver.find_element_by_name('input')
        element_text.send_keys(text)
        element_text.submit()
        element_out = Iris.driver.find_element_by_css_selector('pre')

        return element_out.text

    @staticmethod
    def root_entity(data):
        for entity in data["basic-dependencies"]:
            if entity["dep"] == "ROOT":
                return entity

    @staticmethod
    def get_children(data, index):
        return [entity for entity in data["basic-dependencies"]
                if entity["governor"] == index]

    @staticmethod
    def get_pos(data, index):
        return data["tokens"][int(index) - 1]["pos"]

    @staticmethod
    def get_word(data, index):
        return data["tokens"][int(index) - 1]["word"]

    @staticmethod
    def main_entity(data):
        # Builds an array with the root's non wh-question children's words that have a query file object (Are known)
        root_entity_viable_children = [Iris.get_word(data, entity["dependent"])
                                       for entity in Iris.get_children(data, Iris.root_entity(data)["dependent"])
                                       if Iris.get_pos(data, entity["dependent"]) not in ["WP"]
                                       and Iris.get_query_file(Iris.get_word(data, entity["dependent"])) is not None]

        if root_entity_viable_children:
            return root_entity_viable_children[0]
        return None

    @staticmethod
    def get_query_file(name):
        data_file = Iris.json_file
        for q in data_file["questions"]:
            for alias in q["alias"]:
                if alias.upper() == name.upper():
                    return q

    @staticmethod
    def is_location(data, name):
        for sub_name in name.split():
            for entity in data["tokens"]:
                if entity["word"].upper() == sub_name.upper() and entity["ner"] == "LOCATION":
                    return True
        return False

    @staticmethod
    def get_location(data):
        location_string = None

        for name in data["tokens"]:
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
