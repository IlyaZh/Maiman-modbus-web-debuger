
from flask import json


class defaultValuesReader:
    def readJSON(self, id):
        data = {}
        name = str(hex(id))[2:] + ".json"
        path = "defaults/" + name
        try:
            with open(path) as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print("File {} is not found!".format(path))
        return data