import xml.etree.ElementTree as ET
from DeviceDataModel import DeviceDataModel


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
            if device.get('name') is not None:
                device_name = device.get('name')
            else:
                device_name = ''

            if device.get('id') is not None:
                device_id = device.get('id')
            else:
                device_id = ''

            device_com_delays = {}

            if device.get('stopCommandDelayMs') is not None:
                device_com_delays['stop_command_delay_ms'] = device.get('stopCommandDelayMs')
            if device.get('minCommandDelayMs') is not None:
                device_com_delays['stop_command_min_delay_ms'] = device.get('minCommandDelayMs')
            if device.get('maxCommandDelayMs') is not None:
                device_com_delays['stop_command_max_delay_ms'] = device.get('maxCommandDelayMs')

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

            device_model['commands'] = device_commands

            self.devices[device_id] = device_model
            # self.devices.append(DeviceDataModel(device_model))