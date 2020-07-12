import threading
import logging
from time import sleep
import socket
from modbus.modbusCrc import crc16

from flask import Flask, jsonify
from flask import json
from flask import request


class ThreadDevicesNetwork(threading.Thread):
    def __init__(self, device_models, ip='127.0.0.1',  port=502):
        threading.Thread.__init__(self)
        self.__port = port
        self.__ip = ip
        self.kill_received = False
        self.device_config = device_models
        self.device_types = {}
        self.device_data = {}
        self.__TIMEOUT__ = 3000

        self.__MAX_ADDR__ = 32
        self.device_list = {}
        self.device_timeout = {}
        self.device_online = {}

        for dev_id in device_models:
            dev_mode = device_models.get(dev_id)
            id = int(dev_mode.get('id', 0), 16)
            name = dev_mode.get('name', "")
            content = dev_mode.get('content', dict(image=None, description='', link='#'))
            dev = dict(id=id, name=name, content=content)
            self.device_types[dev['id']] = dev

        # Начальная инициалиация массивов
        for i in range(self.__MAX_ADDR__):
            self.device_data[i] = {}
            self.device_list[i] = {
                'link': False,
                'timeout': self.__TIMEOUT__,
                'device': self.device_types.get(0, None)
            }

    def find_device_by_id(self, id):
        device = self.device_config.get(str(id), {})
        return device

    def remove(self, addr):
        print("remove", addr)

    def add(self, addr, type):
        print("add", addr, type)

    def kill(self):
        self.kill_received = True

    def run(self):
        logging.info("Web server is started!")
        logging.info("TCP Server is started {:s} : {:d}".format(self.__ip, self.__port))
        print("TCP Server is started {:s} : {:d}".format(self.__ip, self.__port))

        while not self.kill_received:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.__ip, self.__port))
                    s.listen(1)
                    sock, addr = s.accept()
                    print('Connection address:', addr)
                    rec_data = sock.recv(255)
                    if rec_data:
                        answer = self.modbus_handle(rec_data)
                        if answer is not None:
                            sock.send(answer)

            except KeyboardInterrupt:
                print("Ctrl-c received! Sending kill to threads...ThreadBzuClimate")
                self.kill_received = True
                sleep(10)

    def modbus_handle(self, rec):
        msg = ''
        for i in rec:
            msg += "{:02X}h ".format(i)
        print("received data:", msg)

        if crc16(rec) != 0:
            return None
        try:
            addr = int(rec[0])
            if 0 < addr <= self.__MAX_ADDR__:
                answer = bytearray()
                dev_registers = self.device_data.get(addr)
                if dev_registers is not None:
                    answer.append(addr)
                    reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
                    cmd = int(rec[1])
                    if cmd == 0x03:
                        count = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
                        is_error = False
                        for i in range(count):
                            if dev_registers.get(reg+i) is None:
                                is_error = True
                                break

                        if is_error is False:
                            answer.append(cmd)
                            answer.append(count * 2)
                            for i in range(count):
                                value = dev_registers.get(reg + i)
                                if value is not None:
                                    answer.append((value >> 8) & 0xff)
                                    answer.append(value & 0xff)
                        else:
                            # нет такого регистра. Ошибка!
                            answer.append(0x80 | cmd)
                            answer.append(0x02)

                    elif cmd == 0x06:
                        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
                        value = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
                        if dev_registers.get(reg) is not None:
                            dev_registers[reg] = value

                            answer.append(cmd)
                            answer.append(rec[2])
                            answer.append(rec[3])
                            answer.append(rec[4])
                            answer.append(rec[5])
                        else:
                            # нет такого регистра. Ошибка!
                            answer.append(0x80 | cmd)
                            answer.append(0x02)
                    elif cmd == 0x10:
                        reg = int(((rec[2] << 8) & 0xff00) + (rec[3] & 0xff))
                        count = int(((rec[4] << 8) & 0xff00) + (rec[5] & 0xff))
                        byte_count = int(rec[6])
                        is_error = False
                        for i in range(int(byte_count/2)):
                            if dev_registers.get(reg+i) is None:
                                is_error = True
                                break

                        if is_error is False:
                            for i in range(int(byte_count/2)):
                                value = int(((rec[7+2*i] << 8) & 0xff00) + (rec[8+2*i] & 0xff))
                                dev_registers[reg+i] = value
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
                        # Че за команда? Возвращаем ошибку
                        answer.append(0x80 | cmd)
                        answer.append(0x01)




            elif addr == 0:
                # Широковещательная команда установки параметров
                pass
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
