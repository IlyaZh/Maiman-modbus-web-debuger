
from config_loader import ConfigParser


class device:
    def __init__(self, device_model):
        parser = ConfigParser('config.xml')
        parser.start()
        self.config = parser.model()
        self.__device__ = {}

        for dev_id in self.config:
            dev_mode = self.config.get(dev_id)
            id_device = dev_mode.get('id')
            if device_model == id_device:
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


class driverMap:
    def __init__(self, Commands, Registers):
        self.map = {}


if __name__ == "__main__":
    de = {}
    dev = device(0x611)
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
    print(de.get(1).get("driver").getRegister(6,1))
    print(de[1]["driver"].getRegister(6,2))