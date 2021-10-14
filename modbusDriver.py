from typing import NamedTuple
from config_loader import ConfigParser


class device:
    def __init__(self, device_model):
        parser = ConfigParser('config.xml')
        parser.start()
        config = parser.model()
        self.__device__ = {}

        for dev_id in config:
            dev_mode = config.get(dev_id)
            if device_model == dev_mode.get('id'):
                # self.__device__["id"] = dev_mode.get('id', 0)
                # self.__device__["name"] = dev_mode.get('name', "")
                # self.__device__["content"] = dev_mode.get('content', dict(image=None, description='', link='#'))
                self.id = dev_mode.get('id', 0)
                self.name = dev_mode.get('name', "")
                self.content = dev_mode.get('content', dict(image=None, description='', link='#'))
                for cmd in dev_mode['commands']:
                    reg = dev_mode['commands'][cmd]
                    code = reg.get('code')
                    self.__device__[int(code, 16)] = 0

    def setRegister(self, command, value):
        if not self.__device__.get(command) == value:
            self.__device__[command] = value

    def getRegister(self, command):
        return self.__device__[command]


class driverMap:
    def __init__(self, Commands, Registers):
        self.map = {}


if __name__ == "__main__":
    dev = device(0x611)
    dev.setRegister(0x0006, 150)
    print(dev.getRegister(6))
    print(dev.name)
    print(dev.content)
    print(dev.__device__.items())
