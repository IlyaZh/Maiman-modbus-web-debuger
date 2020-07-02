import xml.etree.ElementTree as ET


class ConfigParser:
    def __init__(self, file_name):
        self._file_name = file_name
        self.devices = {}

    def start(self):
        root = ET.parse('config.xml').getroot()

        for device in root.iter("Device"):
            device_name = device.attrib['name']

            device_content = {}
            content = device.find("Content")
            if content is not None:
                for content_tag in content:
                    


            break

            self.devices[device_name] = device.attrib['id']

parser = ConfigParser("config.xml")
parser.start()

print(parser.devices)