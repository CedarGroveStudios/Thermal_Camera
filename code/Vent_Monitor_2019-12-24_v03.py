# Vent_Monitor_2019-12-24_v03.py
# Displayio version

import time
from collections import namedtuple
import board
import displayio
from simpleio import map_range
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import adafruit_amg88xx

# establish PyBadger instance
from adafruit_pybadger import PyBadger
panel = PyBadger(pixels_brightness=0.01)

# load the text font
font = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

print("Vent_Monitor_2019-12-24_v03.py")

# look for PyGamer's joystick
if hasattr(board, "JOYSTICK_X"):
    panel.has_joystick = True
else: panel.has_joystick = False

i2c = board.I2C()
amg8833 = adafruit_amg88xx.AMG88XX(i2c)

Coords = namedtuple("Point", "x y")

# Settings
ELEMENT_SIZE = 16
BLACK  = 0x000000
BLUE   = 0x0000FF
GREEN  = 0x00FF00
YELLOW = 0xFFFF00
ORANGE = 0xFF8800
RED    = 0xFF0000
PURPLE = 0xFF00FF
WHITE  = 0xFFFFFF
GRAY   = 0x888888

element_color = [BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE, WHITE]

# Make the display context
disp_group = displayio.Group(max_size=70)
board.DISPLAY.show(disp_group)

# Make a background color fill
color_bitmap = displayio.Bitmap(board.DISPLAY.width,
                                board.DISPLAY.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                               x=0, y=0)
disp_group.append(bg_sprite)

# Converters and Helpers
def c_to_f(temp=0):
    return ((9 / 5) * temp) + 32

def f_to_c(temp=32):
    return (temp - 32) * (5 / 9)

def element_grid(row, col):
    return Coords(ELEMENT_SIZE * row + 30, ELEMENT_SIZE * col + 1)

def update_element(row, col, value=0):
    pos = element_grid(row, col)
    color_index = int(map_range(value, f_to_c(60), f_to_c(100), 0, 6))
    new_element = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                       height=ELEMENT_SIZE, fill=element_color[color_index])
    disp_group[((row * 8) + col) + 5] = new_element
    return

# establish base display group
alarm_display = Label(font, text="alarm", color=WHITE, max_glyphs=5)
alarm_display.x = 0
alarm_display.y = 20
disp_group.append(alarm_display)

max_display = Label(font, text="max", color=RED, max_glyphs=5)
max_display.x = 0
max_display.y = 50
disp_group.append(max_display)

ave_display = Label(font, text="ave", color=YELLOW, max_glyphs=5)
ave_display.x = 0
ave_display.y = 80
disp_group.append(ave_display)

min_display = Label(font, text="min", color=GREEN, max_glyphs=5)
min_display.x = 0
min_display.y = 110
disp_group.append(min_display)

for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(row, col)
        new_element = Rect(x=pos.x, y=pos.y,
                           width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                           fill=element_color[0], outline=BLACK, stroke=2)
        disp_group.append(new_element)
time.sleep(1.0)

v_alarm = 35  # alarm temp in Celsius
while True:  # update display group with camera data
    image = amg8833.pixels
    v_min = 1000
    v_max = -1000
    v_sum = 0

    for row in range(0, 8):
        for col in range(0, 8):
            element_value = image[7 - col][7 - row]
            update_element(row, col, element_value)
            v_sum = v_sum + element_value
            if element_value < v_min : v_min = element_value
            if element_value > v_max : v_max = element_value
    disp_group[1].text = str(int(c_to_f(v_alarm) * 10) / 10)
    disp_group[2].text = str(int(c_to_f(v_max) * 10) / 10)
    disp_group[3].text = str(int(c_to_f(v_sum / 64) * 10) / 10)
    disp_group[4].text = str(int(c_to_f(v_min) * 10) / 10)

    if panel.button.a:  # hold display (shutter = button A)
        while panel.button.a:     time.sleep(0.1)  # wait for button release
        while not panel.button.a: time.sleep(0.1)  # second click: resume
        while panel.button.a:     time.sleep(0.1)  # wait for button release
