import threading
import logging

from flask import Flask, jsonify
from flask import json
from flask import request

logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("ex")

class ThreadDebugServer(threadig.Thread):
    def __init__(self, modbus, web_port='80'):
        threading.Thread.__init__(self)

        self.webPort = web_port
        self.modbusPort = modbus
        self.kill_received = False

        def start(self):
            logging.info("Web server is started!")

        def run(self):
            while not self.kill_received:
                pass