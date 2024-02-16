# PyGPS-VK-172
VK-172 USB GPS/GLONASS u-blox 7 Python Library

### Quick demo
```python
import time
import vk172 as vk

gps = vk.VK172('COMX')

while True:
    time.sleep(1.0)
    vk.print_position(gps.get_position())
```

### TLDR
1. VK-172 are very cheap USB GPS dongle (I bought mine for 3.50€ a piece)
2. This library provides simple function to read position from the dongle
3. This library use [pynmeagps](https://github.com/semuconsulting/pynmeagps) to 
decode NMEA messages.

| VK-172 USB GPS dongle |
|:---------------------:|
| ![image](https://github.com/Cyril-Meyer/PyGPS-VK-172/assets/69190238/8f3720c8-51e8-4b47-ada9-2d7f32fe93b5) |
