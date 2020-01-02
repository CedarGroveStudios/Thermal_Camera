# Thermal_Cam_2019-12-31_v10.py

print("Thermal_Cam_2019-12-31_v10.py")

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

# Load default alarm and min/max range values
from Thermal_Cam_config import *

# Establish panel instance
panel = PyBadger(pixels_brightness=0.01)

# Load the text font
font = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

# Look for PyGamer's joystick
if hasattr(board, "JOYSTICK_X"):
    panel.has_joystick = True
else: panel.has_joystick = False

# Establish I2C interface for camera wing
i2c = board.I2C()
amg8833 = adafruit_amg88xx.AMG88XX(i2c)

Coords = namedtuple("Point", "x y")

# display spash graphics

with open("/thermal_cam_splash.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    splash = displayio.Group()
    splash.append(displayio.TileGrid(bitmap,
                  pixel_shader=displayio.ColorConverter()))
    board.DISPLAY.show(splash)
    time.sleep(0.1)  # allow the splash to display

panel.play_tone(440, 0.1)  # A4
panel.play_tone(880, 0.1)  # A5
time.sleep(1)

### Settings ###
WIDTH  = board.DISPLAY.width
HEIGHT = board.DISPLAY.height

MIN_SENSOR_C = 0
MAX_SENSOR_C = 80

ELEMENT_SIZE = 16
BLACK   = 0x000000
RED     = 0xFF0000
ORANGE  = 0xEE8800
YELLOW  = 0xFFFF00
GREEN   = 0x00FF00
D_GRN   = 0x002200
CYAN    = 0x00FFFF
BLUE    = 0x0000FF
VIOLET  = 0x9900FF
MAGENTA = 0xFF0033
PINK    = 0xFF3377
AQUA    = 0x4088FF
WHITE   = 0xFFFFFF
GRAY    = 0x444455

element_color = [GRAY, BLUE, GREEN, YELLOW, ORANGE, RED, VIOLET, WHITE]
param_list = [("ALARM", WHITE), ("RANGE", RED), ("RANGE", CYAN)]

### Converters and Helpers ###
def convert_temp(f=None, c=None):  # convert F to C and C to F
    if f != None and c == None: return round((f - 32) * (5 / 9))
    if f == None and c != None: return round(((9 / 5) * c) + 32)
    return None

def element_grid(row, col):
    return Coords(ELEMENT_SIZE * row + 30, ELEMENT_SIZE * col + 1)

def update_image_frame():
    minimum = MAX_SENSOR_C # set minimum to sensor's maximum C value
    maximum = MIN_SENSOR_C  # set maximum to sensor's minimum C value

    disp_group[74].text = ""
    disp_group[75].text = ""
    disp_group[76].text = ""

    sum_bucket = 0  # bucket for building average value
    for row in range(0, 8):  # parse camera data list and update display
        for col in range(0, 8):
            value = map_range(image[7 - col][7 - row],
                            MIN_SENSOR_C, MAX_SENSOR_C, MIN_SENSOR_C, MAX_SENSOR_C)
            pos = element_grid(row, col)
            color_index = int(map_range(value, MIN_RANGE_C, MAX_RANGE_C, 0, 7))
            disp_group[((row * 8) + col) + 1] = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                                                     height=ELEMENT_SIZE,
                                                     fill=element_color[color_index])
            sum_bucket = sum_bucket + value  # calculate sum for average
            minimum = min(value, minimum)
            maximum = max(value, maximum)
    return minimum, maximum, sum_bucket

def update_histo_frame():
    minimum = MAX_SENSOR_C # set minimum to sensor's maximum C value
    maximum = MIN_SENSOR_C  # set maximum to sensor's minimum C value

    disp_group[74].text = str(MIN_RANGE_F)
    disp_group[75].text = str(MAX_RANGE_F)
    disp_group[76].text = "-RANGE-"

    sum_bucket = 0  # bucket for building average value
    histo_bucket = [0, 0, 0, 0, 0, 0, 0, 0]  # reset histogram bucket
    for row in range(0, 8):  # parse camera data list and update display
        for col in range(7, -1, -1):
            value = map_range(image[7 - col][7 - row],
                              MIN_SENSOR_C, MAX_SENSOR_C, MIN_SENSOR_C, MAX_SENSOR_C)
            histo_index = int(map_range(value, MIN_RANGE_C, MAX_RANGE_C, 0, 7))
            histo_bucket[histo_index] = histo_bucket[histo_index] + 1
            pos = element_grid(histo_index, 7 - (histo_bucket[histo_index] // 8))
            disp_group[((row * 8) + col) + 1] = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                                                     height=ELEMENT_SIZE,
                                                     fill=element_color[histo_index],
                                                     outline=BLACK, stroke=1)
            sum_bucket = sum_bucket + value  # calculate sum for average
            minimum = min(value, minimum)
            maximum = max(value, maximum)

    return minimum, maximum, sum_bucket

def setup_mode():
    disp_group[65].color = WHITE
    disp_group[65].text  = "-SET-"
    disp_group[69].color = BLACK
    disp_group[73].color = BLACK
    disp_group[71].text = str(MAX_RANGE_F)
    disp_group[72].text = str(MIN_RANGE_F)
    time.sleep(0.8)
    disp_group[65].text  = ""

    param_index = 0  # index of parameter to set
    while not panel.button.start:
        while (not panel.button.a) and (not panel.button.start):
            left, right, up, down = move_buttons(joystick=panel.has_joystick)
            if up  : param_index = param_index - 1
            if down: param_index = param_index + 1
            if param_index > 2: param_index = 2
            if param_index < 0: param_index = 0
            disp_group[65].text = param_list[param_index][0]
            disp_group[param_index + 66].color = BLACK
            disp_group[65].color = BLACK
            time.sleep(0.2)
            disp_group[param_index + 66].color = param_list[param_index][1]
            disp_group[65].color = WHITE
            time.sleep(0.2)

        if panel.button.a:  panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass  # wait for button release

        param_value = int(disp_group[param_index + 70].text)
        while (not panel.button.a) and (not panel.button.start):
            left, right, up, down = move_buttons(joystick=panel.has_joystick)
            if up  :  param_value = param_value + 1
            if down:  param_value = param_value - 1
            if param_value > convert_temp(c=MAX_SENSOR_C):  paramr_value = convert_temp(c=MAX_SENSOR_C)
            if param_value < convert_temp(c=MIN_SENSOR_C):  param_value = convert_temp(c=MIN_SENSOR_C)
            disp_group[param_index + 70].text = str(param_value)
            disp_group[param_index + 70].color = BLACK
            disp_group[65].color = BLACK
            time.sleep(0.05)
            disp_group[param_index + 70].color = param_list[param_index][1]
            disp_group[65].color = WHITE
            time.sleep(0.2)

        if panel.button.a:  panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass  # wait for button release

    if panel.button.start: panel.play_tone(784, 0.030)  # G5
    while panel.button.start:  pass  # wait for button release
    disp_group[65].text = "RESUME"
    time.sleep(0.5)
    disp_group[65].text = ""
    disp_group[69].color = YELLOW
    disp_group[73].color = YELLOW
    return int(disp_group[70].text), int(disp_group[71].text),int(disp_group[72].text)

def move_buttons(joystick=False):
    if joystick:  # for PyGamer
        move_r = move_l = False
        if   panel.joystick[0] > 44000: move_r = True
        elif panel.joystick[0] < 20000: move_l = True
        move_u = move_d = False
        if   panel.joystick[1] < 20000: move_u = True
        elif panel.joystick[1] > 44000: move_d = True
    else:  # for PyBadge
        if panel.button.right: move_r = True
        if panel.button.left : move_l = True
        if panel.button.up   : move_u = True
        if panel.button.down : move_d = True
    return move_r, move_l, move_u, move_d

### Set Celsius alarm and range values ###
ALARM_C     = convert_temp(f=ALARM_F)  # alarm temp in Celsius
MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)
MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)

# Establish the display context
disp_group = displayio.Group(max_size=77)
board.DISPLAY.show(disp_group)

# Create a background color fill
# disp_group[0]
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                                x=0, y=0)
disp_group.append(background)

# Define and build the foundational display group
# disp_group[1:64]
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(col, row)
        disp_group.append(Rect(x=pos.x, y=pos.y,
                          width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                          fill=None))

# Status label; disp_group[65]
status_label = Label(font, text="", color=BLACK, max_glyphs=6)
status_label.x = (WIDTH // 2) - 7
status_label.y = int(1.4 * HEIGHT // 4) + 15
disp_group.append(status_label)

# Alarm label; disp_group[66]
alarm_label = Label(font, text="alm", color=WHITE, max_glyphs=3)
alarm_label.x = 0
alarm_label.y = int(0.5 * HEIGHT // 4) + 10
disp_group.append(alarm_label)

# Maximum label; disp_group[67]
max_label = Label(font, text="max", color=RED, max_glyphs=3)
max_label.x = 0
max_label.y = int(1.5 * HEIGHT // 4) + 10
disp_group.append(max_label)

# Minimum label; disp_group[68]
min_label = Label(font, text="min", color=CYAN, max_glyphs=3)
min_label.x = 0
min_label.y = int(3.5 * HEIGHT // 4) + 10
disp_group.append(min_label)

# Average label; disp_group[69]
ave_label = Label(font, text="ave", color=YELLOW, max_glyphs=3)
ave_label.x = 0
ave_label.y = int(2.5 * HEIGHT // 4) + 10
disp_group.append(ave_label)

# Alarm value; disp_group[70]
alarm_display = Label(font, text=str(ALARM_F), color=WHITE, max_glyphs=5)
alarm_display.x = 0
alarm_display.y = int(0 * HEIGHT // 4) + 10
disp_group.append(alarm_display)

# Maximum value; disp_group[71]
max_display = Label(font, text=str(MAX_RANGE_F), color=RED, max_glyphs=5)
max_display.x = 0
max_display.y = int(1 * HEIGHT // 4) + 10
disp_group.append(max_display)

# Minimum value; disp_group[72]
min_display = Label(font, text=str(MIN_RANGE_F), color=CYAN, max_glyphs=5)
min_display.x = 0
min_display.y = int(3 * HEIGHT // 4) + 10
disp_group.append(min_display)

# Average value; disp_group[73]
ave_display = Label(font, text="---", color=YELLOW, max_glyphs=5)
ave_display.x = 0
ave_display.y = int(2 * HEIGHT // 4) + 10
disp_group.append(ave_display)

# Histogram minimum range value; disp_group[74]
min_histo = Label(font, text="", color=CYAN, max_glyphs=3)
min_histo.x = (WIDTH // 4) - 5
min_histo.y = int(3.5 * HEIGHT // 4) + 10
disp_group.append(min_histo)

# Histogram maximum range value; disp_group[75]
max_histo = Label(font, text="", color=RED, max_glyphs=3)
max_histo.x = int(3 * WIDTH // 4) + 10
max_histo.y = int(3.5 * HEIGHT // 4) + 10
disp_group.append(max_histo)

# Histogram range text label; disp_group[75]
range_histo = Label(font, text="", color=BLUE, max_glyphs=7)
range_histo.x = int(1.5 * WIDTH // 4) + 5
range_histo.y = int(3.5 * HEIGHT // 4) + 10
disp_group.append(range_histo)

### Primary Process: Get camera data and update display ###
display_image = True  # image display mode default; False for histogram
display_hold = False  # active display mode default; True to hold display
panel.play_tone(880, 0.1)  # A5

while True:
    if not display_hold:  image = amg8833.pixels  # get camera data list
    if display_image:  # image display mode
        v_min, v_max, v_sum = update_image_frame()
    else:  # histogram display mode
        v_min, v_max, v_sum = update_histo_frame()

    # display alarm, maxumum, minimum, and average values
    disp_group[70].text = str(ALARM_F)
    disp_group[71].text = str(convert_temp(c=v_max))
    disp_group[72].text = str(convert_temp(c=v_min))
    disp_group[73].text = str(convert_temp(c=v_sum // 64))

    # play alarm note if maximum value reaches alarm threshold
    if v_max >= ALARM_C:  panel.play_tone(880, 0.030)  # A5

    if display_hold:  # flash hold status text label
        disp_group[65].color = WHITE
        disp_group[65].text  = "-HOLD-"
        time.sleep(0.1)
        disp_group[65].color = BLACK
        disp_group[65].text  = "-HOLD-"
        time.sleep(0.1)
    else: disp_group[65].text = ""  # clear status text label

    # See if a panel button is pressed
    if panel.button.a:  # toggle display hold (shutter = button A)
        if display_hold == False:  display_hold = True
        else:  display_hold = False
        panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass   # wait for button release

    if panel.button.b:  # toggle image/histogram mode (display mode = button B)
        if display_image:  display_image = False
        else: display_image = True
        panel.play_tone(659, 0.030)  # E5
        while panel.button.b:  pass  # wait for button release

    if panel.button.start:  # activate setup mode (setup mode = start button)
        panel.play_tone(784, 0.030)  # G5
        while panel.button.start:  pass  # wait for button release
        ALARM_F, MAX_RANGE_F, MIN_RANGE_F = setup_mode()  # get new alarm and range values
        ALARM_C = convert_temp(f=ALARM_F)  # update new alarm threshold temp in Celsius
        MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)  # update new range temp in Celsius
        MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)  # update new range temp in Celsius
        
