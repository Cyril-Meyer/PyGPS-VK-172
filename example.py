import argparse
import serial.tools.list_ports
import time

import vk172 as vk

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, help='selected VK-172 port')
parser.add_argument('--list-port', action='store_true', help='list serial port')
args = parser.parse_args()

if args.list_port:
    for port in serial.tools.list_ports.comports():
        print(port.device)

if args.port is None:
    print('ERROR: NO SERIAL PORT SPECIFIED')
    exit(0)
else:
    port = args.port

gps = vk.VK172(port)

while True:
    time.sleep(1.0)
    pos = gps.get_position()

    if pos is not None:
        vk.print_position(pos)
