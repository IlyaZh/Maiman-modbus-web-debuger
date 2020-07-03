import threading
import logging
from time import sleep

from flask import Flask, jsonify
from flask import json
from flask import request


class ThreadDevicesNetwork(threading.Thread):
    def __init__(self, device_models, port='80'):
        threading.Thread.__init__(self)

        self.__port = port
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
            content = dev_mode.get('content', {
                    'image': None,
                    'description': '',
                    'link': '#'
                })

            dev = {
                'id': id,
                'name': name,
                'content': content
            }
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

        # while not self.kill_received:
        try:
            pass
        except KeyboardInterrupt:
            print("Ctrl-c received! Sending kill to threads...ThreadBzuClimate")
            self.kill_received = True
            sleep(10)
