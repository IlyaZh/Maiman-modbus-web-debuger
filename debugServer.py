import threading
import logging
from time import sleep
import socket
from flask import Flask, jsonify
from flask import json
from flask import request
from modbus.modbusCrc import crc16


class ThreadDevicesNetwork(threading.Thread):
    def __init__(self, device_models, inIp='127.0.0.1', inPort=502):
        threading.Thread.__init__(self)
        self.port = inPort
        self.ip = inIp
        self.__change_setup = False
        self.kill_received = False
        self.device_config = device_models
        self.devices = {}
        self.__TIMEOUT__ = 3000
        self.device_list = {}

        self.port_changed = False

        self.__MAX_ADDR__ = 32

        for dev_id in device_models:
            dev_mode = device_models.get(dev_id)
            id = dev_mode.get('id', 0)
            name = dev_mode.get('name', "")
            content = dev_mode.get('content', dict(image=None, description='', link='#'))
            dev = dict(id=id, name=name, content=content)
            # self.device_types[dev['id']] = dev

        # Начальная инициалиация массивов
        for addr in range(1, self.__MAX_ADDR__ + 1):
            self.devices[addr] = {
                'device': self.device_config.get(0, None),
                'data': {}
            }

    def find_device_by_id(self, id):
        device = self.device_config.get(id, {})
        return device

    def remove(self, addr):
        self.devices[addr] = {
            'device': self.device_config.get(0, None),
            'data': {}
        }
        self.device_list[addr] = {
            'timeout': 999
        }

    def add(self, addr, id):
        device_type = self.device_config.get(id)

        self.devices[addr] = {
            'device': device_type,
            'data': {}
        }
        self.device_list[addr] = {
            'timeout': 0
        }

        for cmd in device_type['commands']:
            reg = device_type['commands'][cmd]
            code = reg.get('code')
            self.devices[addr]['data'][int(code, 16)] = 0

        self.devices[addr]['data'][int('0702', 16)] = id

    def set_port(self, port):
        self.port = port
        self.port_changed = True

    def kill(self):
        self.kill_received = True

    def run(self):
        logging.info("TCP Server is started {:s} : {:d}".format(self.ip, self.port))
        print("TCP Server is started {:s} : {:d}".format(self.ip, self.port))

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.bind((self.ip, self.port))
        #     s.listen(1)
        #     while True:
        #         conn, addr = s.accept()
        #         with conn:
        #             print('Connected by', addr)
        #             while True:
        #                 data = conn.recv(1024)
        #                 print('\n rx', data, '\n')
        #                 if not data: break
        #                 conn.sendall(data)
        #                 answer = self.modbus_handle(data)
        #                 print('tx', data, '\n')
        #                 print("modbus ", answer,  len(answer), '\n')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            print("Listen at port ", self.port)
            s.listen(1)
            while True:
                sock, addr = s.accept()
                with sock:
                    print('Connection address:', addr)

                    rec_data = sock.recv(255)
                    if not rec_data:
                        break
                    # if rec_data:
                    answer = self.modbus_handle(rec_data)
                    if answer is not None:
                        if len(answer) > 0:
                            str = ""
                            for c in answer:
                                str += "{:02X}h ".format(c)
                            print("Tx Data: ", str)
                            sock.sendall(answer)
                        else:
                            break
                    else:
                        break
                    # sock.close()
                    if self.port_changed:
                        self.port_changed = False
                        s.close()
                        s.bind((self.ip, self.port))

    def modbus_handle(self, rec):
        msg = ''
        for i in rec:
            msg += "{:02X}h ".format(i)
        print("received data:", msg)
        answer = bytearray()

        if crc16(rec) != 0:
            return answer
        try:

            addr = int(rec[0])
            cmd = int(rec[1])
            if 0 < addr <= self.__MAX_ADDR__:
                dev_registers = self.devices.get(addr)
                if dev_registers.get('device') is not None:
                    self.device_list[addr]['timeout'] = 0
                    answer.append(addr)
                    if cmd == 0x03:
                        answer.extend(self.modbus_read(addr, rec))
                    elif cmd == 0x06:
                        answer.extend(self.modbus_write_signle(addr, rec))
                    elif cmd == 0x10:
                        answer.extend(self.modbus_write_mult(addr, rec))
                    else:
                        # Че за команда? Возвращаем ошибку
                        answer.append(0x80 | cmd)
                        answer.append(0x01)

            elif addr == 0:
                # Широковещательная команда установки параметров
                cmd = int(rec[1])
                for addr in range(1, self.__MAX_ADDR__ + 1):
                    dev_data = self.device_data.get(addr)
                    if dev_data is not None:
                        self.device_list[addr]['timeout'] = 0
                        if cmd == 0x06:
                            self.modbus_write_signle(addr, rec)
                        elif cmd == 0x10:
                            self.modbus_write_mult(addr, rec)

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
                print("sent data:", msg)

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
        if device is not None:
            devData = device.get('data')
            if devData is not None:
                for i in range(count):
                    dat = devData.get(reg + i)
                    if dat is None:
                        is_error = True
                        break

        if is_error is False:
            answer.append(cmd)
            answer.append(count * 2)
            for i in range(count):
                device = self.devices.get(addr)
                if device is not None:
                    value = device.get("data").get(reg + i)
                    if value is not None:
                        answer.append((value >> 8) & 0xff)
                        answer.append(value & 0xff)
        else:
            # нет такого регистра. Ошибка!
            answer.append(0x80 | cmd)
            answer.append(0x02)

        return answer

    def modbus_write_signle(self, addr, rec) -> bytearray:
        answer = bytearray()
        cmd = 0x06
        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
        value = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
        device = self.devices.get(addr)
        if device is not None:
            reg = device.get(addr).get(reg)
            if reg is not None:
                self.devices.get(addr)[reg] = value

                answer.append(cmd)
                answer.append(rec[2])
                answer.append(rec[3])
                answer.append(rec[4])
                answer.append(rec[5])
            else:
                # нет такого регистра. Ошибка!
                answer.append(0x80 | cmd)
                answer.append(0x02)
        else:
            # нет такого регистра. Ошибка!
            answer.append(0x80 | cmd)
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
            if device is not None:
                if device.get(reg + i) is None:
                    is_error = True
                    break

        if is_error is False:
            for i in range(int(byte_count / 2)):
                value = int(((rec[7 + 2 * i] << 8) & 0xff00) + (rec[8 + 2 * i] & 0xff))
                self.devices.get(addr)[reg + i] = value
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
