import logging
import socket
import threading

from Device import Device
from default import defaultValuesReader
from modbus.modbusCrc import crc16


class ThreadDevicesNetwork(threading.Thread):

    def __init__(self, device_models, in_ip='127.0.0.1', inPort=502):
        threading.Thread.__init__(self)
        self.port = inPort
        self.ip = in_ip
        self.__change_setup = False
        self.kill_received = False
        self.device_config = device_models
        self.__TIMEOUT__ = 3000
        self.device_list = {}
        self.devices = {}
        self.default = {}
        self.port_changed = False

        self.__MAX_ADDR__ = 32

        for dev_id in device_models:
            dev_mode = device_models.get(dev_id)
            id = dev_mode.get('id', 0)
            name = dev_mode.get('name', "")
            content = dev_mode.get('content', dict(image=None, description='', link='#'))
            dev = dict(id=id, name=name, content=content)
            # self.device_types[dev['id']] = dev
            self.default[id] = defaultValuesReader().readJSON(id)

        # Начальная инициалиация массивов
        for addr in range(1, self.__MAX_ADDR__ + 1):
            self.devices[addr] = Device({}, {})
            '''
            self.devices[addr] = {
                'device': None,
                'data': {},
                'driver': None
            }
        
        for addr in range(1, self.__MAX_ADDR__ + 1):
            self.devices[addr] = {
                'device': self.device_config.get(0, None),
                'data': {}
            }
        '''

    def find_device_by_id(self, id):
        device = self.device_config.get(id, {})
        return device

    def remove(self, addr):
        self.devices[addr] = Device({}, {})
        '''{
            # 'device': self.device_config.get(0, None),
            'device': None,
            'data': {},
            'driver': None
        }'''
        self.device_list[addr] = {
            'timeout': 999
        }

    def devices_map(self):
        devices = {}
        for addr in range(1, self.__MAX_ADDR__ + 1):
            device = self.devices.get(addr)
            if device.id == 0:
                devices[addr] = {
                    "device": None,
                    "data": {}
                }
            else:
                data = {}
                device = self.devices.get(addr)
                list = device.get_commands_list()
                for reg in list:
                    # reg = self.devices[addr].config['commands'][cmd]
                    # code = reg.get('code')
                    # data[reg] = self.devices[addr].__data__[reg]
                    data[reg] = device.get_register(reg, 1).get(reg)
                devices[addr] = {
                    "device": device.get_config(),
                    "data": data  # self.devices[addr].__device__
                }
        return devices

    def add(self, addr, id):
        device_type = self.device_config.get(id)
        device = Device(device_type, self.default.get(id))
        self.devices[addr] = device
        # 'data': {},
        # 'driver': solo_device

        '''
        for cmd in device_type['commands']:
            reg = device_type['commands'][cmd]
            code = int(reg.get('code'), 16)
            # DEBUG DELETE ILIA
            if self.default[id].get(str(hex(code))[2:]) is not None:
                solo_device.__device__[code] = self.default[id].get(str(hex(code))[2:])

            if code == 0x21:
                self.devices[addr]['data'][code] = 1000
            elif code == 0x23:
                self.devices[addr]['data'][code] = 2500
            elif code == 0x25:
                self.devices[addr]['data'][code] = 400
            else:
                #END OF DEBUG
                self.devices[addr]['data'][code] = 0




        self.devices[addr]['data'][int('0001', 16)] = id
    
        self.devices[addr]['data'][int('0001', 16)] = solo_device.id
        self.devices[addr]['data'] = solo_device.__device__.copy()
        '''
        self.device_list[addr] = {
            'timeout': 0
        }

    def set_port(self, port):
        self.port = port
        self.port_changed = True

    def modify(self, addr: int, reg: int, value: int):
        dev = self.devices.get(addr)
        if dev is not None:
            if dev.id != 0:
                if self.devices.get(addr).__data__.get(reg) is not None:
                    self.devices.get(addr).set_register(reg, value)
        '''
        if self.devices.at(addr) is not None:
            if self.devices.at(addr).at('data').at(reg) is not None:
                self.devices[addr]['data'][reg] = value
        '''

    def kill(self):
        self.kill_received = True

    def run(self):
        logging.info("TCP Server is started {:s} : {:d}".format(self.ip, self.port))
        print("TCP Server is started {:s} : {:d}".format(self.ip, self.port))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen(30)
            while True:
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    print("Timeout socket")
                    pass

                with conn:
                    print('Connected by', addr)
                    while True:
                        try:
                            data = conn.recv(1024)
                            print('\n rx (', len(data), ") ", data, '\n')
                            if not data:
                                break
                            answer = self.modbus_handle(data)

                            length = len(answer)
                            # print("Tx len = {:d}".format(length))
                            if length > 0:
                                conn.sendall(answer)
                                print("tx ", answer, '\n')
                        except:
                            pass

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.bind((self.ip, self.port))
        #     print("Listen at port ", self.port)
        #     s.listen(1)
        #     while True:
        #         sock, addr = s.accept()
        #         with sock:
        #             print('Connection address:', addr)
        #
        #             rec_data = sock.recv(255)
        #             if not rec_data:
        #                 break
        #             # if rec_data:
        #             answer = self.modbus_handle(rec_data)
        #             # if len(answer) > 0:
        #             str = ""
        #             for c in answer:
        #                 str += "{:02X}h ".format(c)
        #             print("Tx Data: ", str)
        #             sock.sendall(answer)
        #             # else:
        #             #     break
        #             # sock.close()
        #             if self.port_changed:
        #                 self.port_changed = False
        #                 s.close()
        #                 s.bind((self.ip, self.port))

    def modbus_handle(self, rec):
        msg = ''
        for i in rec:
            msg += "{:02X}h ".format(i)
        # print("received data:", msg)
        answer = bytearray()

        if crc16(rec) != 0:
            return answer
        try:

            addr = int(rec[0])
            cmd = int(rec[1])
            if 0 < addr <= self.__MAX_ADDR__:
                # dev_registers = self.devices.get(addr)
                #if dev_registers.get('device') is not None:
                self.device_list[addr]['timeout'] = 0
                answer.append(addr)
                if cmd == 0x03:
                    dev_data = self.modbus_read(addr, rec)
                    if len(dev_data) == 0:
                        return {}
                    answer.extend(dev_data)
                elif cmd == 0x06:
                    dev_data = self.modbus_write_signle(addr, rec)
                    if len(dev_data) == 0:
                        return {}
                    answer.extend(dev_data)
                elif cmd == 0x10:
                    dev_data = self.modbus_write_mult(addr, rec)
                    if len(dev_data) == 0:
                        return {}
                    answer.extend(dev_data)
                else:
                    # Че за команда? Возвращаем ошибку
                    answer.append(0x80 | cmd)
                    answer.append(0x01)

            # elif addr == 0:
            #     # Широковещательная команда установки параметров
            #     cmd = int(rec[1])
            #     for addr in range(1, self.__MAX_ADDR__ + 1):
            #         dev_data = self.device_data.get(addr)
            #         if dev_data is not None:
            #             self.device_list[addr]['timeout'] = 0
            #             if cmd == 0x06:
            #                 self.modbus_write_signle(addr, rec)
            #             elif cmd == 0x10:
            #                 self.modbus_write_mult(addr, rec)

            else:
                answer.append(0x80 | cmd)
                answer.append(0x0B)

            if len(answer) > 1:
                crc = crc16(answer)
                answer.append((crc & 0xff))
                answer.append((crc & 0xff00) >> 8)

                msg = ''
                for i in answer:
                    msg += "{:02X}h ".format(i)
                # print("sent data:", msg)

            return answer
        except:
            pass
        finally:
            pass

    def modbus_read(self, addr, rec) -> bytearray:
        answer = bytearray()
        cmd = 0x03
        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
        count = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
        is_error = False
        device = self.devices.get(addr)
        devData = {}
        if device is not None and device.id != 0:
            devData = device.get_register(reg, count)
            if len(devData) == 0:
                is_error = True

            if is_error is False:
                answer.append(cmd)
                answer.append(count * 2)

                for reg in devData:
                    value = devData[reg]
                    answer.append((value >> 8) & 0xff)
                    answer.append(value & 0xff)
            else:
                # нет такого регистра. Ошибка!
                answer.append(0x80 | cmd)
                answer.append(0x02)

        return answer

    def modbus_write_signle(self, addr, rec) -> bytearray:
        answer = bytearray()
        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
        value = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))

        print("Write reg=", reg, " value=", value)

        device = self.devices.get(addr)
        if device is not None and device.id != 0:
            if device.set_register(reg, value):
                answer.append(0x06)
                answer.append((reg >> 8) & 0xff)
                answer.append(reg & 0xff)
                answer.append((value >> 8) & 0xff)
                answer.append(value & 0xff)

            else:
                # нет такого регистра. Ошибка!
                answer.append(0x86)
                answer.append(0x02)

        return answer

    def modbus_write_mult(self, addr, rec) -> bytearray:
        answer = bytearray()
        cmd = 0x10
        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
        count = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
        byte_count = int(rec[6])
        is_error = False
        for i in range(int(byte_count / 2)):
            device = self.devices.get(addr)
            if device is not None and device.id != 0:
                if device.get_register(reg, i).get(reg) is None:
                    is_error = True
                    break

        if is_error is False:
            for i in range(int(byte_count / 2)):
                value = int(((rec[7 + 2 * i] << 8) & 0xff00) + (rec[8 + 2 * i] & 0xff))
                self.devices.get(addr).__data__[str(reg + i)] = value
            answer.append(cmd)
            answer.append(rec[2])
            answer.append(rec[3])
            answer.append(rec[4])
            answer.append(rec[5])
        else:
            # нет такого регистра. Ошибка!
            answer.append(0x80 | cmd)
            answer.append(0x02)

        return answer
