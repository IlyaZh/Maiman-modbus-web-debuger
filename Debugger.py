# coding=utf-8

from modbus.modbus import Modbus
from config_loader import ConfigParser
from DeviceDataModel import DeviceDataModel
from debugServer import ThreadDevicesNetwork
from flask import Flask, request, jsonify, json
import logging

timeout_ms = 5

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


# @app.route('/setChannel', methods=['POST'])
# def setChannel():
#     data1 = json.loads(request.args.get('data'))
#
#     if data1['cmd'] == 'set':
#         try:
#             reg = int(data1['param']['reg'])
#             value = int(data1['param']['value'])
#             threadModbus.queue[reg] = value
#         except:
#             pass
#         finally:
#             pass
#
#     # threadModbus.q_comm.append(data1['param'])
#     return ""
@app.route('/')
def index():
    file = open('./static/index.html', encoding='utf-8', mode='r')
    d = file.read();
    file.close()

    return "hi"
    # return d


@app.route('/device_config.json', methods=['GET'])
def device_config():
    device_id = request.args.get('id', type=int)
    if device_id is None:
        return jsonify({})
    elif device_id == 0:
        return jsonify(threadNetwork.device_config)
    else:
        return jsonify(threadNetwork.find_device_id(device_id))

@app.route('/devices_list.json')
def devices_list():
    return jsonify(threadNetwork.device_list)

@app.route('/online.json')
def devices_online():
    return jsonify(threadNetwork.device_online)

@app.route('/add_device', methods=['POST'])
def add_device():
    return 'add_device'


if __name__ == "__main__":
    print("Hello! Let's start! \n\n")

    parser = ConfigParser('config.xml')
    parser.start()
    threadNetwork = ThreadDevicesNetwork(parser.model(), 80)

    threadNetwork.daemon = True
    threadNetwork.start()

    app.run(host='0.0.0.0', port=8080)
