# cedargrove_pypanel.py
# Cedar Grove Studios 2019-12-15 v02
# uses revised adafruit_pybadger and adafruit_crickit
# configuration dictionary is contained in 'pypanel_device.py'

import board
i2c = board.I2C()  # establish i2C instance for Stemma devices

# Enumerate Stemma/I2C-connected devices
stemma = []  # clear the list

try:
    from pypanel_device import catalog
except:
    raise RuntimeError("pypanel_device.py file error")

for device in catalog.keys():
    try:
        exec(catalog[device]['import'])
        exec(catalog[device]['instance'])
        exec(catalog[device]['test'])
        stemma.append((device, catalog[device]['name'], catalog[device]['desc']))
    except:
        pass

# establish PyBadger instance
from adafruit_pybadger import PyBadger
panel = PyBadger(pixels_brightness=0.01)

# look for PyGamer's joystick
if hasattr(board, "JOYSTICK_X"):
    panel.has_joystick = True
else: panel.has_joystick = False

# establish terminalio text display instance
import terminalio
from adafruit_display_text import label
display = board.DISPLAY

# establish displayio instance
import displayio
display = board.DISPLAY

# establish turtle graphics instance
from adafruit_turtle import turtle
