# coding=utf-8

from serial_port_settings import SerialPortSettings
from modbus.modbus import Modbus


port = 'COM8'
baud = 921600
timeout_ms = 5


if __name__ == "__main__":
    print("Hello! Let's start! \n\n")

    SerialPortSettings(port, baud, timeout_ms)

    threadDebugger = ThreadDebugServer(SerialPortSettings, 80)

    threadDebugger.daemon = True
    threadDebugger.start()

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
        

