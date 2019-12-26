# Vent_Monitor_2019-12-26_v04.py

import time
from collections import namedtuple
import board
import displayio
from simpleio import map_range
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import adafruit_amg88xx
from adafruit_pybadger import PyBadger

# Establish panel instance
panel = PyBadger(pixels_brightness=0.01)

# Load the text font
font = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

# Look for PyGamer's joystick
if hasattr(board, "JOYSTICK_X"):
    panel.has_joystick = True
else: panel.has_joystick = False

i2c = board.I2C()
amg8833 = adafruit_amg88xx.AMG88XX(i2c)

Coords = namedtuple("Point", "x y")

print("Vent_Monitor_2019-12-26_v04.py")

### Converters and Helpers ###
def c_to_f(temp=0):
    return round(((9 / 5) * temp) + 32, 1)

def f_to_c(temp=32):
    return (temp - 32) * (5 / 9)

def element_grid(row, col):
    return Coords(ELEMENT_SIZE * row + 30, ELEMENT_SIZE * col + 1)

def update_element(row, col, value=0):
    pos = element_grid(row, col)
    color_index = int(map_range(value, MIN_RANGE, MAX_RANGE, 0, 7))
    new_element = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                       height=ELEMENT_SIZE, fill=element_color[color_index])
    disp_group[((row * 8) + col) + 1] = new_element
    return

def update_histogram(value=0):
    histo_index = int(map_range(value, MIN_RANGE, MAX_RANGE, 0, 7))
    element_histo[histo_index] = element_histo[histo_index] + 1
    pos = element_grid(histo_index, 7 - (element_histo[histo_index] // 8))
    new_element = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                       height=ELEMENT_SIZE, fill=element_color[histo_index],
                       outline=BLACK, stroke=1)
    disp_group[((row * 8) + col) + 1] = new_element
    return

### Settings ###
WIDTH  = board.DISPLAY.width
HEIGHT = board.DISPLAY.height

ELEMENT_SIZE = 16
BLACK    = 0x000000
RED      = 0xFF0000
ORANGE   = 0xFF8800
YELLOW   = 0xFFFF00
GREEN    = 0x00FF00
GREEN_DK = 0x002200
CYAN     = 0x00FFFF
BLUE     = 0x0000FF
VIOLET   = 0x9900FF
MAGENTA  = 0xFF0033
PINK     = 0xFF3377
AQUA     = 0x4088FF
WHITE    = 0xFFFFFF
GRAY     = 0x444455

ALARM   = f_to_c(95)  # alarm temp in Celsius
MIN_RANGE = f_to_c(50)
MAX_RANGE = f_to_c(120)

TREE = [
    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
    [BLACK, BLACK, BLACK, BLACK, GREEN, BLACK, BLACK, BLACK, BLACK],
    [BLACK, BLACK, BLACK, GREEN, GREEN, GREEN, BLACK, BLACK],
    [BLACK, BLACK, GREEN, GREEN, GREEN, GREEN, GREEN, BLACK],
    [BLACK, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN],
    [BLACK, BLACK, BLACK, BLACK, GREEN, BLACK, BLACK, BLACK, BLACK],
    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
    [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
    ]

element_color = [GRAY, BLUE, GREEN, YELLOW, ORANGE, RED, VIOLET, WHITE]

# Establish the display context
disp_group = displayio.Group(max_size=70)
board.DISPLAY.show(disp_group)

# Create a background color fill
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                               x=0, y=0)
disp_group.append(bg_sprite)

# Define and build the foundational display group
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(col, row)
        new_element = Rect(x=pos.x, y=pos.y,
                           width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                           fill=TREE[row][col])
        disp_group.append(new_element)

cg_display = Label(font, text="Cedar Grove", color=BLACK, max_glyphs=11)
cg_display.x = (WIDTH // 2) - 15
cg_display.y = 15 + (int(1.5 * HEIGHT) // 4)
disp_group.append(cg_display)

time.sleep(1)

alarm_display = Label(font, text="ALM", color=WHITE, max_glyphs=5)
alarm_display.x = 0
alarm_display.y = 15 + (0 * HEIGHT // 4)
disp_group.append(alarm_display)

max_display = Label(font, text="MAX", color=RED, max_glyphs=5)
max_display.x = 0
max_display.y = 15 + (1 * HEIGHT // 4)
disp_group.append(max_display)

ave_display = Label(font, text="AVE", color=YELLOW, max_glyphs=5)
ave_display.x = 0
ave_display.y = 15 + (2 * HEIGHT // 4)
disp_group.append(ave_display)

min_display = Label(font, text="MIN", color=CYAN, max_glyphs=5)
min_display.x = 0
min_display.y = 15 + (3 * HEIGHT // 4)
disp_group.append(min_display)

time.sleep(1.0)
disp_group[65].text = ""

### Primary Process ###
# Get camera data and update display
display_mode = "image"
while True:
    v_min = 1000   # set ridiculous minimum value
    v_max = -1000  # set ridiculous maximum value
    v_sum = 0      # bucket for building average value
    element_histo = [0, 0, 0, 0, 0, 0 , 0, 0]
    image = amg8833.pixels  # get camera data list

    for row in range(0, 8):  # parse camera data list and update display
        for col in range(0, 8):
            element_value = map_range(image[7 - col][7 - row], 0, 80, 0, 80)
            if display_mode == "image":
                update_element(row, col, element_value)
            elif display_mode == "histogram":
                update_histogram(element_value)
            v_sum = v_sum + element_value  # calculate sum for average
            if element_value < v_min : v_min = element_value  # find min value
            if element_value > v_max : v_max = element_value  # find max value

    # update display text values
    disp_group[66].text = str(c_to_f(ALARM))
    disp_group[67].text = str(c_to_f(v_max))
    disp_group[68].text = str(c_to_f(v_sum / 64))
    disp_group[69].text = str(c_to_f(v_min))

    if panel.button.a:  # hold/release display (shutter = button A)
        while panel.button.a:     time.sleep(0.1)  # wait for button release
        while not panel.button.a:
            disp_group[65].color = BLACK
            disp_group[65].text  = "-hold-"
            time.sleep(0.25)
            disp_group[65].color = WHITE
            time.sleep(0.25)
        while panel.button.a:     time.sleep(0.1)  # wait for button release
        disp_group[65].text  = ""

    if panel.button.select:  # switch display mode (select button)
        while panel.button.select:     time.sleep(0.1)  # wait for button release
        if display_mode == "image":
            display_mode = "histogram"
        else: display_mode = "image"
