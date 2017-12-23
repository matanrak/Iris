import json
import urllib


class QueryHandler():

    @staticmethod
    def get_json(values, type):

        url_base = values["urls"][type]["url"]
        url_fillings = QueryHandler.follow_instructions(values, QueryHandler.instruction_translator(values["buildUrl"]))
        url = url_base % tuple(url_fillings)

        print "url: ", url

    @staticmethod
    def follow_instructions(data, instructions):

        fillings = []

        for instruction in instructions:
            if isinstance(instruction, list):
                instruction_data = json.loads(json.dumps(data))
                for path in range(len(instruction)):

                    instruction_path = object()
                    try:
                        int(instruction[path])
                        instruction_path = int(instruction[path])
                    except ValueError:
                        instruction_path = str(instruction[path])

                    if path == len(instruction) - 1:
                        fillings.append(json.dumps(instruction_data[instruction_path]).strip('"'))
                    else:
                        instruction_data = json.loads(json.dumps(instruction_data))[instruction_path]
            else:
                fillings.append(instruction)

        return fillings

    @staticmethod
    def instruction_translator(data):
        instructions = []

        if isinstance(data, list):
            for s in data:
                instructions.append(QueryHandler.instruction_translator(s))

            return instructions

        elif json.dumps(data).__contains__("{"):  # For some reason the is_json is currently acting up, TO DO
            value_json = json.loads(json.dumps(data))

            for json_object in value_json:
                json_subobject = json.loads(json.dumps(value_json[str(json.dumps(json_object)).strip('"')]))

                for count in range(len(json_object)):
                    json_string = str(json_subobject[count]).strip('"').strip(' ')
                    instructions.append(QueryHandler.instruction_translator(json_string))

            return instructions

        elif isinstance(data, int):
            return [data]

        if json.dumps(data).__contains__("json?"):
            return [json.dumps(data).replace("json?", "").strip('"')]

        return json.dumps(data).strip('"')

    @staticmethod
    def is_json(data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True
