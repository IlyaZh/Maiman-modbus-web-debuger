import datetime

class DeviceDataModel:
    def __init__(self, model):
        self.model = model

        self.__registers = {}

        for cmd in self.command_list():
            reg = self.command_list().get(cmd);
            code = int(reg.get('code'), 16)
            self.__registers[code] = 0

    def id(self):
        return self.model['id']

    def name(self):
        return self.model['name']

    def com_stop_delay(self):
        return self.model['com_delays']['stop_command_delay_ms']

    def com_min_stop_delay(self):
        return self.model['com_delays']['stop_command_min_delay_ms']

    def com_max_stop_delay(self):
        return self.model['com_delays']['stop_command_max_delay_ms']

    def image(self):
        return self.model['content']['image']

    def description(self):
        return self.model['content']['description']

    def link(self):
        return self.model['content']['link']

    def command_list(self):
        return self.model['commands']

    def get_data(self, reg):
        return self.__registers.get(reg)

    def set_data(self, reg, value):
        if self.__registers.get(reg) is not None:
            self.__registers[reg] = (value & 0xffff)
            return self.__registers[reg]
        else:
            return None

    def get_reg_divider(self, reg):
        cmd = self.command_list().get(reg)
        if cmd is not None:
            divider = cmd.get('divider')
            if divider is not None:
                return divider

        return 1

    def get_reg_unit(self, reg):
        cmd = self.command_list().get(reg)
        if cmd is not None:
            unit = cmd.get('unit')
            if unit is not None:
                return unit

        return ''