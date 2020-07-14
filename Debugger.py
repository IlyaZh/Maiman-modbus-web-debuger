# coding=utf-8

from config_loader import ConfigParser
from debugServer import ThreadDevicesNetwork
from flask import Flask, request, jsonify, json
import logging

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
        'connected': threadNetwork.device_list,
        'data': threadNetwork.device_data
    }
    return jsonify(db)

@app.route('/types.json')
def device_types():
    types = {
        # 'types': threadNetwork.device_types
        'types': threadNetwork.device_config
    }
    return jsonify(types)

@app.route('/actionAddr', methods=['POST'])
def remove():
    data1 = json.loads(request.args.get('data'))

    if data1['cmd'] == 'del':
        try:
            addr = int(data1['param']['addr'])
            threadNetwork.remove(addr)
        except:
            pass
        finally:
            pass
    elif data1['cmd'] == 'add':
        try:
            addr = int(data1['param']['addr'])
            type = int(data1['param']['type'])
            threadNetwork.add(addr, type)
        except:
            pass
        finally:
            pass

    # threadModbus.q_comm.append(data1['param'])
    return ""

@app.route('/info.json', methods=['GET'])
def device_info():
    device_id = request.args.get('id', type=int)
    if device_id is None:
        return jsonify(None)
    elif device_id == 0:
        return jsonify(threadNetwork.device_config)
    else:
        return jsonify(threadNetwork.find_device_by_id(device_id))

# @app.route('/devices_list.json')
# def devices_list():
#     dev_list = {
#         'count': len(threadNetwork.device_list),
#         'devices': threadNetwork.device_list
#                 }
#
#     return jsonify(dev_list)
#
# @app.route('/online.json')
# def devices_online():
#     return jsonify(threadNetwork.device_timeout)


if __name__ == "__main__":
    print("Hello! Let's start! \n\n")

    parser = ConfigParser('config.xml')
    parser.start()
    threadNetwork = ThreadDevicesNetwork(parser.model(), '127.0.0.1', 502)

    threadNetwork.daemon = True
    threadNetwork.start()

    app.run(host='0.0.0.0', port=8080)
