import serial
import threading
import time
import pynmeagps


class VK172:
    def __init__(self, port, history=60):
        self.port = port
        self.history = history

        self.serial = serial.Serial(port, baudrate=9600, timeout=0.1)
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()
        # positions queue
        self.pos = []
        # last satellite count
        self.sat = 0
        # last time
        self.time = None

    def update(self):
        while True:
            nmr = pynmeagps.NMEAReader(self.serial)
            (raw_data, message) = nmr.read()
            if message is None:
                continue

            if   message.msgID == 'GSV':
                self.sat = message.numMsg
            elif message.msgID == 'GGA':
                if message.quality == 0:
                    continue
                self.time = message.time
                self.pos.append((message.lat, message.lon, message.alt))
            # ignored messages
            elif message.msgID in ['TXT', 'GGA', 'GLL', 'GSA', 'RMC', 'VTG']:
                continue
            # unknown messages
            else:
                raise NotImplementedError(message.msgID)

            while len(self.pos) > self.history:
                self.pos.pop(0)

            time.sleep(0.1)

    def get_position(self, mean=1):
        if len(self.pos) == 0:
            return None

        assert 1 <= mean <= self.history
        mean = min(mean, len(self.pos))

        if mean == 1:
            return self.pos[-1]

        raise NotImplementedError

    def get_time(self):
        return self.time


def print_position(position, dms=False):
    lat, lon, alt = position

    lat = round(lat, 6)
    lon = round(lon, 6)
    alt = round(alt, 1)

    pos = f'{lat:09.6f},{lon:09.6f},{alt:05.1f}'

    if dms:
        print(f'{pos[0:2]}°{pos[3:5]}\'{pos[5:7]}" {pos[10:12]}°{pos[13:15]}\'{pos[15:17]}"')
    else:
        print(f'{pos[0:9]}°', f'{pos[10:19]}°')
