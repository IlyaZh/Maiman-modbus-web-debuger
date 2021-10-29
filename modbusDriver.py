
class device:
    def __init__(self, id, device_model, defaults):
        self.config = device_model
        self.__device__ = {}
        self.id = id
        # self.config.get('id', 0)
        # self.name = self.config.get('name', "")
        # self.content = self.config.get('content', dict(image=None, description='', link='#'))
        if any(self.config):
            for cmd in self.config['commands']:
                reg = self.config['commands'][cmd]
                code = reg.get('code')
                if any(defaults):
                    if defaults.get(str(hex(int(code, 16)))[2:]) is not None:
                        self.__device__[int(code, 16)] = defaults.get(str(hex(int(code, 16)))[2:])# defaults[str(id)].get(str(hex(code))[2:])
                    else:
                        self.__device__[int(code, 16)] = 0
                else:
                    self.__device__[int(code, 16)] = 0

    def setRegister(self, command, value):
        if command == 4:
            if not self.__device__.get(command) == value and any(self.__device__):
                data = self.__device__[command]
                if value == 8:
                    data = data | (1 << 1)
                elif value == 16:
                    data = data & ~(1 << 1)
                if value == 32:
                    data = data | (1 << 2)
                elif value == 64:
                    data = data & ~(1 << 2)
                if value == 512:
                    data = data & ~(1 << 4)
                elif value == 1024:
                    data = data | (1 << 4)
                if value == 4096:
                    data = data & ~(1 << 7)
                elif value == 8192:
                    data = data | (1 << 7)
                if value == 16384:
                    data = data | (1 << 6)
                elif value == 32768:
                    data = data & ~(1 << 6)
                self.__device__[command] = data
        elif not self.__device__.get(command) == value and any(self.__device__):
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
