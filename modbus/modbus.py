import serial as serial
from modbus.modbusCrc import crc16
import datetime

if __name__ == "__main__":
    print("This is module. Please import it an use.")


class Modbus:
    def __init__(self, port, baud = 921600, timeout = 10):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.has_new_data = False
        self._CONST_MAX_ADDRESS = 32
        self._DIR_OUT = 0
        self._DIR_IN = 1
        self._DIR_NONE = 2
        self._DIR_MSG = {'self._DIR_OUT': "->", 'self._DIR_IN': "<-", 'self._DIR_NONE': ""}

        self._received_data = {}

        self._serial = serial.Serial(self.port, self.baud, self.timeout, stopbits=1, bytesize=8)

        def writeSingle(self, addr, reg, value):
            if addr <= self._CONST_MAX_ADDRESS:
                with self._serial as s:
                    package = bytearray()
                    package.append(addr)
                    package.append(0x06)
                    package.append((reg >> 8) & 0xff)
                    package.append(reg & 0xff)
                    package.append((value >> 8) & 0xff)
                    package.append(value & 0xff)
                    crc = crc16(package)
                    package.append((crc >> 8) & 0xff)
                    package.append(crc & 0xff)
                    s.write(package)
                    _write_log(self._DIR_OUT, "", package)

                    rx_package = s.read(8)
                    _write_log(self._DIR_IN, "", rx_package)
                    if len(rx_package) >= 8:
                        if crc16(rx_package) == 0:
                            if rx_package[1] == 0x06:
                                r_addr = rx_package[0]
                                r_reg = ((rx_package[2]<<8) & 0xff00) | (rx_package[3] & 0xff)
                                r_value = ((rx_package[4]<<8) & 0xff00) | (rx_package[5] & 0xff)
                                return {'addr': r_addr, 'reg': r_reg, 'values': [r_value]}
                    # Если проверки выше не выполнены, то вываливаемся с нулевыми значениями
                    _write_log("Something went wrong")
                    return {'addr': 0, 'reg': 0, 'values': []}


        def writeMultiple(self, addr, reg, values):
            if addr <= self._CONST_MAX_ADDRESS:
                with self._serial as s:
                    write_reg_count = len(values)
                    package = bytearray()
                    package.append(addr)
                    package.append(0x10)
                    package.append((reg >> 8) & 0xff)
                    package.append(reg & 0xff)
                    package.append((write_reg_count >> 8) & 0xff)
                    package.append(write_reg_count & 0xff)
                    package.append((write_reg_count * 2) & 0xff)
                    for value in values:
                        package.append((value >> 8) & 0xff)
                        package.append(value & 0xff)
                    crc = crc16(package)
                    package.append((crc >> 8) & 0xff)
                    package.append(crc & 0xff)
                    s.write(package)
                    _write_log(self._DIR_OUT, "", package)

                    rx_package = s.read(8)
                    _write_log(self._DIR_IN, "", rx_package)
                    if len(rx_package) >= 8:
                        if crc16(rx_package) == 0:
                            if rx_package[1] == 0x10:
                                r_addr = rx_package[0]
                                r_reg = ((rx_package[2]<<8) & 0xff00) | (rx_package[3] & 0xff)
                                r_value = ((rx_package[4]<<8) & 0xff00) | (rx_package[5] & 0xff)
                                return [r_addr, r_reg, r_value]
                    return {'addr': 0, 'reg': 0, 'values':[]}

        def read_multiple(self, addr, reg, count):
            if addr <= self._CONST_MAX_ADDRESS:
                with self._serial as s:
                    package = bytearray()
                    package.append(addr)
                    package.append(0x03)
                    package.append((reg >> 8) & 0xff)
                    package.append(reg & 0xff)
                    package.append((count >> 8) & 0xff)
                    package.append(count & 0xff)
                    crc = crc16(package)
                    package.append((crc >> 8) & 0xff)
                    package.append(crc & 0xff)
                    s.write(package)
                    _write_log(self._DIR_OUT, "", package)

                    rx_wait_count = 5+2*count
                    rx_package = s.read(rx_wait_count)
                    _write_log(self._DIR_IN, "", rx_package)
                    if len(rx_package) >= rx_wait_count:
                        if crc16(rx_package) == 0:
                            if rx_package[1] == 0x03:
                                r_addr = rx_package[0]
                                r_values = []
                                for i in range(count):
                                    r_values.append(((rx_package[3+2*i]<<8) & 0xff00) | (rx_package[4+2*i] & 0xff))
                                return {'addr': r_addr, 'reg': reg, 'values': [r_values]}
                    # Если проверки выше не выполнены, то вываливаемся с нулевыми значениями
                    _write_log("Something went wrong")
                    return {'addr': 0, 'reg': 0, 'values': []}



        def _write_log(self, dir = self._DIR_NONE, msg, modbus_package):
            for c in modbus_package:
                msg += "0x{:02X} ".format(c)
            print("[", datetime.datetime.now().time(), "][MODBUS] ",self._DIR_MSG[dir], " ", msg)