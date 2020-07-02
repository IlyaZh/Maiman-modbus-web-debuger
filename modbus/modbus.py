import serial as serial
from modbus.modbusCrc import crc16
import datetime

if __name__ == "__main__":
    print("This is module. Please import it an use.")


class Modbus:
    def __init__(self, ip, port):
        self.__port = port
        self.__ip = ip
        self._CONST_MAX_ADDRESS = 32
        self._DIR_OUT = 0
        self._DIR_IN = 1
        self._DIR_NONE = 2
        self._DIR_MSG = {'self._DIR_OUT': "->", 'self._DIR_IN': "<-", 'self._DIR_NONE': ""}

        def _write_log(self, msg, modbus_package, dir = self._DIR_NONE):
            for c in modbus_package:
                msg += "0x{:02X} ".format(c)
            print("[", datetime.datetime.now().time(), "][MODBUS] ",self._DIR_MSG[dir], " ", msg)