from flask import json
from config_loader import ConfigParser
import os


class device:
    def __init__(self, device_model, device_id):
        parser = ConfigParser('config.xml')
        parser.start()
        # self.config = parser.model()
        self.config = device_model
        self.__device__ = {}

        for dev_id in self.config:
            dev_mode = self.config.get(dev_id)
            id_device = dev_mode.get('id')
            if device_id == id_device:
                self.id = dev_mode.get('id', 0)
                self.name = dev_mode.get('name', "")
                self.content = dev_mode.get('content', dict(image=None, description='', link='#'))
                for cmd in dev_mode['commands']:
                    reg = dev_mode['commands'][cmd]
                    code = reg.get('code')
                    self.__device__[int(code, 16)] = 0

    def setRegister(self, command, value):
        if not self.__device__.get(command) == value and any(self.__device__):
            self.__device__[command] = value

    def getRegister(self, command, count):
        commands = {}
        if any(self.__device__):
            for iCount in range(0, count):
                if (command + iCount) in self.__device__:
                    commands[command + iCount] = self.__device__[command + iCount]
                else:
                    return 0
            return commands
    '''
    def readDefault(self):
        if self.id != 0:
            data = defaultValuesReader().readJSON(self.id)
            for code in self.__device__:
                if data.get(str(hex(code))[2:]) is not None:
                    self.__device__[code] = data.get(str(hex(code))[2:])
    '''

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


class driverMap:
    def __init__(self, Commands, Registers):
        self.map = {}


if __name__ == "__main__":
    de = {}
    parser = ConfigParser('config.xml')
    parser.start()

    dev = device(parser.model(), 0x101)
    de[1] = {
        'device': dev.config,
        'data': {},
        'driver': dev
    }

    dev.setRegister(6, 150)
    print(dev.getRegister(6, 3))
    print(dev.name)
    print(dev.id)
    print(dev.__device__)
    print(de.get(1).get("driver").getRegister(6, 1))
    print(de[1]["driver"].getRegister(6, 2))
    for x in dev.__device__:
        print(dev.__device__[x])
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print(os.getcwd() + r"\static\js")
    print(os.path.isfile(os.getcwd() + r"\static\js\myCtrl.js"))
