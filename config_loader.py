import xml.etree.ElementTree as ET


class ConfigParser:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.devices = {}

    def model(self):
        return self.devices

    def start(self):
        root = ET.parse('config.xml').getroot()

        for device in root.iter("Device"):
            device_model = {}
            device_name = device.get('name', '')

            device_id = int(device.get('id', 0), 16)

            device_com_delays = {}

            device_com_delays['stop_command_delay_ms'] = device.get('stopCommandDelayMs', 50)
            device_com_delays['stop_command_min_delay_ms'] = device.get('minCommandDelayMs', 50)
            device_com_delays['stop_command_max_delay_ms'] = device.get('maxCommandDelayMs', 50)

            device_model['name'] = device_name
            device_model['id'] = device_id
            device_model['com_delays'] = device_com_delays

            device_content = {}
            content = device.find("Content")
            if content is not None:
                for content_child in content:
                    tag_name = str(content_child.tag).lower()
                    device_content[tag_name] = content_child.text

            device_model['content'] = device_content

            device_commands = {}
            commands = device.find("Commands")
            if commands is not None:
                for cmd in commands:
                    code = int(cmd.get('code'), 16)
                    device_commands[code] = cmd.attrib
                    if device_commands[code].get('unit','-') == '(deg)':
                        device_commands[code]['unit'] = '°C'

            device_model['commands'] = device_commands

            device_params = {}
            params = device.find("Param")
            if params is not None:
                for param in params:
                    min = param.get('min')
                    max = param.get('max')
                    value = param.get('value')
                    real = param.get('real')
            device_model['params'] = device_params

            self.devices[device_id] = device_model
            # self.devices.append(DeviceDataModel(device_model))