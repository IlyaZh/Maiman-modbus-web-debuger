from debugServer import ThreadDevicesNetwork
from config_loader import ConfigParser
from modbusDriver import device

if __name__ == "__main__":
    port = 502
    host = '127.0.0.1'
    parser = ConfigParser('tests/config.xml')
    parser.start()
    threadNetwork = ThreadDevicesNetwork(parser.model(), host, port)
    print(threadNetwork.devices.get(1).id)

    dev = device(257, threadNetwork.device_config.get(257), threadNetwork.default.get(257))
    # print(dev.__device__.items())