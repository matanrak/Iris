import json
import random
import urllib
import re
from random import randint

class QueryHandler():

    @staticmethod
    def get_json(values, type, location):

        answers = []
        answer = "UNKNOWN"
        n = 0

        url_base = values["urls"][type]["url"]
        url_fillings = QueryHandler.follow_instructions(values, QueryHandler.instruction_translator(values["buildUrl"]))
        url = url_base % tuple(url_fillings)

        response = json.loads(urllib.urlopen(url).read())

        for path in values["answerPath"]:  # This gets the answer from the response using the json answerPath
            translated_instructions = QueryHandler.instruction_translator(path)
            answer_in_path = QueryHandler.follow_instructions_fromlist(response, translated_instructions)
            answers.append(answer_in_path)

        if len(answers) == 1 and re.match("^\d+?\.\d+?$", answers[0]) is not None: # In case there is 1 value it's a float, used in weather
                n = int(round(float(answers[0])))
                answers[0] = n

        for action in values["actionsOnOutput"]:  # This preforms the actions that are specified in actionsOnOutput

            if json.dumps(action).__contains__("math?"):  # Checks if the action is a math function and updates n
                index = -1
                if n in answers:
                    index = answers.index(n)

                n = eval(str(json.dumps(action)).replace("math?", "").replace('"', ""))

                if index is not -1:
                    answers[index] = n

            elif json.dumps(action).__contains__("command?"):  # Checks if the action is a kind of command
                command = str(json.dumps(action)).replace("command?", "").replace('"', "")

                if command == "buildAnswer":
                    answer_base = random.choice(list(values["answers"][type]["sentences"]))
                    answer = answer_base % tuple(answers)

                elif command == "sendBack":
                    print ("sent back")
                    # TODO Will send the info back to the requester

        print (answer)

    @staticmethod
    def follow_instructions_fromlist(data, instruction):  # follow_instructions_fromlist follows translated instructions
        instruction_data = json.loads(json.dumps(data))   # and returns a translated value

        for path in range(len(instruction)):
            instruction_path = object()

            try:
                int(instruction[path])
                instruction_path = int(instruction[path])
            except ValueError:
                instruction_path = str(instruction[path])

            if path == len(instruction) - 1:
                return json.dumps(instruction_data[instruction_path]).strip('"')
            else:
                instruction_data = json.loads(json.dumps(instruction_data))[instruction_path]

        return "Could'nt follow json instructions"

    @staticmethod
    def follow_instructions(data, instructions):  # follow_instructions is an extension of fromlist, it returns an array
        fillings = []                             # of translated instructions, this is used when building the url

        for instruction in instructions:
            if isinstance(instruction, list):
                fillings.append(QueryHandler.follow_instructions_fromlist(data, instruction))
            else:
                fillings.append(instruction)

        return fillings

    @staticmethod
    def instruction_translator(data):
        instructions = []

        if isinstance(data, list):  # Checks if the object is a list, and if so builds a list of instructions from it
            for s in data:
                instructions.append(QueryHandler.instruction_translator(s))

            return instructions

        elif json.dumps(data).__contains__("{"):  # Checks if the object is more json, and parses it accordingly
            value_json = json.loads(json.dumps(data))

            for json_object in value_json:
                json_sub_object = json.loads(json.dumps(value_json[str(json.dumps(json_object)).strip('"')]))

                for count in range(len(json_object)):
                    json_string = str(json_sub_object[count]).strip('"').strip(' ')
                    instructions.append(QueryHandler.instruction_translator(json_string))

            return instructions

        elif isinstance(data, int):  # Checks if the object is an int, mostly for use in arrays
            return [data]

        if json.dumps(data).__contains__("json?"): # Checks if the object is a json instruction
            return [json.dumps(data).replace("json?", "").strip('"')]

        if json.dumps(data).__contains__("random?"):  # Checks if the object is random number, and if so generates one
            num = randint(0, int(json.dumps(data).replace("random?", "").strip('"')))
            print "NUMM: ",num
            return num

        return json.dumps(data).strip('"')
