
class Device:
    __config__ = None
    __data__ = {}
    id = 0

    def __init__(self, device_model, defaults):
        self.__config__ = device_model
        self.__data__ = {}
        self.id = self.__config__.get('id', 0)
        # self.config.get('id', 0)
        # self.name = self.config.get('name', "")
        # self.content = self.config.get('content', dict(image=None, description='', link='#'))

        self.__data__[1] = self.__config__.get('id', 0)
        if any(self.__config__):
            for cmd in self.__config__['commands']:
                reg = self.__config__['commands'][cmd]
                code = reg.get('code')
                if any(defaults):
                    if defaults.get(str(hex(int(code, 16)))[2:]) is not None:
                        self.__data__[int(code, 16)] = defaults.get(
                            str(hex(int(code, 16)))[2:])  # defaults[str(id)].get(str(hex(code))[2:])
                    else:
                        self.__data__[int(code, 16)] = 0
                else:
                    self.__data__[int(code, 16)] = 0

    def get_config(self):
        return self.__config__

    def get_commands_list(self):
        list = []
        for item in self.__data__:
            list.append(item)
        return list;

    def set_register(self, command, value):
        if not self.__data__.get(command) == value and any(self.__data__):
            if command == 4:
                data = self.__data__[command]
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
                self.__data__[command] = data
                return True
            elif command == 1:
                pass
            elif not self.__data__.get(command) == value and any(self.__data__):
                self.__data__[command] = value
                return True
        return False

    def get_register(self, reg, count):
        commands = {}
        if any(self.__data__):
            for iCount in range(0, count):
                if (reg + iCount) in self.__data__:
                    commands[reg + iCount] = self.__data__[reg + iCount]
        return commands

    '''
    def readDefault(self):
        if self.id != 0:
            data = defaultValuesReader().readJSON(self.id)
            for code in self.__device__:
                if data.get(str(hex(code))[2:]) is not None:
                    self.__device__[code] = data.get(str(hex(code))[2:])
    '''
