# Dryer_Vent_Mon_2019-12-23_v02.py
# Displayio version

import time
from collections import namedtuple
import board
import displayio
from simpleio import map_range
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import adafruit_amg88xx

i2c = board.I2C()
amg8833 = adafruit_amg88xx.AMG88XX(i2c)

Coords = namedtuple("Point", "x y")

print("Dryer_Vent_Mon_2019-12-23_v02.py")

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
disp_group = displayio.Group(max_size=65)
board.DISPLAY.show(disp_group)

# Make a background color fill
color_bitmap = displayio.Bitmap(board.DISPLAY.width,
                                board.DISPLAY.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                               x=0, y=0)
disp_group.append(bg_sprite)

# Some element functions
def element_grid(row, col):
    return Coords(ELEMENT_SIZE * row + 17, ELEMENT_SIZE * col + 1)

def update_element(row, col, value=0):
    pos = element_grid(row, col)
    color_index = int(map_range(value, 15.56, 37.78, 0, 6))
    new_element = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                       height=ELEMENT_SIZE, fill=element_color[color_index])
    disp_group[((row * 8) + col) + 1] = new_element
    return

# establish base display group
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(row, col)
        new_element = Rect(x=pos.x, y=pos.y,
                           width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                           fill=element_color[0], outline=BLACK, stroke=2)
        disp_group.append(new_element)
time.sleep(1.0)

while True:  # update display group with camera data
    image = amg8833.pixels
    #vmin = 1000
    #vmax = -1000
    #vsum = 0
    for row in range(0, 8):
        for col in range(0, 8):
            element_value = image[7 - col][7 - row]
            update_element(row, col, element_value)
            #vsum = vsum + element_value
            #if element_value < vmin : vmin = element_value
            #if element_value > vmax : vmax = element_value
    #print("min: %2.2f max: %2.2f ave: %2.2f" % (vmin, vmax, vsum / 64))
