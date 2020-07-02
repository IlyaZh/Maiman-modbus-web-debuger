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

        self.__MAX_ADDR__ = 10
        self.device_list = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
            '10': 0
        }
        self.device_online = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
            '10': 0
        }

    def find_device_by_id(self, id):
        device = self.device_config.get(str(id))
        if device is not None:
            return device
        else:
            return {}

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
