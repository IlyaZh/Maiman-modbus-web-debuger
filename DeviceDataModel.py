import datetime

class DeviceDataModel:
    def __init__(self, address, registers):
        self.addr = address
        self.regs = []
        self.regs = registers
        self.link = False

        self._lastLinkTimer = round(datetime.datetime.now().microsecond/1000, 0)
        self._sequences = []
        self._seqItt = 0

        last_cmd = -9999
        sequence_cmd_count = 0
        sequence_cmd = 0
        i = 0
        for cmd in self.regs:
            if cmd-1 == last_cmd:
                sequence_cmd_count += 1
            else:
                if i == 0:
                    sequence_cmd = cmd
                self._sequences.append([sequence_cmd, sequence_cmd_count])
                sequence_cmd = last_cmd = cmd

        for item in self._sequences:
            print("{:s}\n".format(item))



    def next_command(self):
        ret = self._sequences[self._seqItt]
        if self._seqItt < len(self._sequences):
            self._seqItt += 1
        else:
            self._seqItt = 0
        return ret
