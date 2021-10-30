import logging

from flask import Flask, request, jsonify, json

from config_loader import ConfigParser
from debugServer import ThreadDevicesNetwork

timeout_ms = 5

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


@app.route('/')
def index():
    file = open('./static/index.html', encoding='utf-8', mode='r')
    page = file.read()
    file.close()

    return page


@app.route('/manage.html')
def manage():
    file = open('./static/manage.html', encoding='utf-8', mode='r')
    page = file.read()
    file.close()

    return page


@app.route('/network.html')
def network():
    file = open('./static/network.html', encoding='utf-8', mode='r')
    page = file.read()
    file.close()

    return page


@app.route('/data.json')
def device_data():
    db = {
        # 'network': threadNetwork.devices
        'network': threadNetwork.devices_map()
          }

    return jsonify(db)


@app.route('/types.json')
def device_types():
    types = {
        # 'types': threadNetwork.device_types
        'types': threadNetwork.device_config
    }
    return jsonify(types)


@app.route('/setup.json')
def device_setup():
    setup = {
        'setup': {
            'ip': threadNetwork.ip,
            'port': threadNetwork.port
        }
    }
    return jsonify(setup)


@app.route('/actionAddr', methods=['POST'])
def commandHandler():
    data1 = json.loads(request.args.get('data'))

    if data1['cmd'] == 'del':
        try:
            addr = int(data1['param']['addr'])
            threadNetwork.remove(addr)
        finally:
            pass
    elif data1['cmd'] == 'add':
        try:
            addr = int(data1['param']['addr'])
            type = int(data1['param']['type'])
            threadNetwork.add(addr, type)
        finally:
            pass
    elif data1['cmd'] == 'port':
        try:
            port = int(data1['param']['port'])
            threadNetwork.set_port(port)
        finally:
            pass
    elif data1['cmd'] == 'setValue':
        try:
            addr = int(data1['param']['addr'])
            reg = int(data1['param']['reg'], 16)
            value = int(data1['param']['value'])
            threadNetwork.modify(addr, reg, value)
        finally:
            pass

    # threadModbus.q_comm.append(data1['param'])
    return ""


# @app.route('/info.json', methods=['GET'])
# def device_info():
#     device_id = request.args.get('id', type=int)
#     if device_id is None:
#         return jsonify(None)
#     elif device_id == 0:
#         return jsonify(threadNetwork.device_config)
#     else:
#         return jsonify(threadNetwork.find_device_by_id(device_id))


if __name__ == "__main__":
    print("Hello! Let's start! \n\n")
    port = 502
    host = '127.0.0.1'

    parser = ConfigParser('config.xml')
    parser.start()
    threadNetwork = ThreadDevicesNetwork(parser.model(), host, port)
    print('Webserver started http://{0}:{1}/'.format(host, 80))

    threadNetwork.daemon = True
    threadNetwork.start()

    # DEBUG ONLY
    threadNetwork.add(2, 257)
    threadNetwork.add(1, 257)
    app.run(host='0.0.0.0', port=80)
