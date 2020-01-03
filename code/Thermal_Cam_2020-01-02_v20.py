# Thermal_Cam_2020-01-02_v20.py
# (c) 2020 Cedar Grove Studios

print("Thermal_Cam_2020-01-02_v20.py")

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
ORANGE  = 0xFF8811
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

def element_grid(col, row):
    return Coords(ELEMENT_SIZE * col + 30, ELEMENT_SIZE * row + 1)

def update_image_frame():  # Get camera data and display
    minimum = MAX_SENSOR_C  # Set minimum to sensor's maximum C value
    maximum = MIN_SENSOR_C  # Set maximum to sensor's minimum C value

    min_histo.text   = ""  # Clear histogram legend
    max_histo.text   = ""
    range_histo.text = ""

    sum_bucket = 0  # Clear bucket for building average value

    for row in range(0, 8):  # Parse camera data list and update display
        for col in range(0, 8):
            value = map_range(image[7 - row][7 - col],
                            MIN_SENSOR_C, MAX_SENSOR_C, MIN_SENSOR_C, MAX_SENSOR_C)
            color_index = int(map_range(value, MIN_RANGE_C, MAX_RANGE_C, 0, 7))
            image_group[((row * 8) + col) + 1].fill = element_color[color_index]
            sum_bucket = sum_bucket + value  # Calculate sum for average
            minimum = min(value, minimum)
            maximum = max(value, maximum)
    return minimum, maximum, sum_bucket

def update_histo_frame():
    minimum = MAX_SENSOR_C  # Set minimum to sensor's maximum C value
    maximum = MIN_SENSOR_C  # Set maximum to sensor's minimum C value

    min_histo.text   = str(MIN_RANGE_F)  # Display histogram legend
    max_histo.text   = str(MAX_RANGE_F)
    range_histo.text = "-RANGE-"

    sum_bucket = 0  # Clear bucket for building average value

    histo_bucket = [0, 0, 0, 0, 0, 0, 0, 0]  # Clear histogram bucket
    for row in range(7, -1, -1):  # Collect camera data list and calculate spectrum
        for col in range(0, 8):
            value = map_range(image[col][row],
                              MIN_SENSOR_C, MAX_SENSOR_C, MIN_SENSOR_C, MAX_SENSOR_C)
            histo_index = int(map_range(value, MIN_RANGE_C, MAX_RANGE_C, 0, 7))
            histo_bucket[histo_index] = histo_bucket[histo_index] + 1
            sum_bucket = sum_bucket + value  # Calculate sum for average
            minimum = min(value, minimum)
            maximum = max(value, maximum)

    for col in range(0, 8):  # Display histogram
        for row in range(0, 8):
            if histo_bucket[col] / 8 > 7 - row:
                image_group[((row * 8) + col) + 1].fill = element_color[col]
            else:
                image_group[((row * 8) + col) + 1].fill = BLACK

    return minimum, maximum, sum_bucket

def setup_mode():  # Set alarm threshold and minimum/maximum range values
    status_label.color = WHITE
    status_label.text  = "-SET-"

    ave_label.color = BLACK  # Turn off average label and value display
    ave_value.color = BLACK

    max_value.text = str(MAX_RANGE_F)  # Display maximum range value
    min_value.text = str(MIN_RANGE_F)  # Display minimum range value

    time.sleep(0.8)  # Prepare to display parameter type text
    status_label.text  = ""

    param_index = 0  # Clear index of parameter to set

    # Select parameter to set
    while not panel.button.start:
        while (not panel.button.a) and (not panel.button.start):
            left, right, up, down = move_buttons(joystick=panel.has_joystick)
            if up  : param_index = param_index - 1
            if down: param_index = param_index + 1
            if param_index > 2: param_index = 2
            if param_index < 0: param_index = 0
            status_label.text = param_list[param_index][0]
            image_group[param_index + 66].color = BLACK
            status_label.color = BLACK
            time.sleep(0.2)
            image_group[param_index + 66].color = param_list[param_index][1]
            status_label.color = WHITE
            time.sleep(0.2)

        if panel.button.a:  panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass  # wait for button release

        # Adjust parameter value
        param_value = int(image_group[param_index + 70].text)
        while (not panel.button.a) and (not panel.button.start):
            left, right, up, down = move_buttons(joystick=panel.has_joystick)
            if up  :  param_value = param_value + 1
            if down:  param_value = param_value - 1
            if param_value > convert_temp(c=MAX_SENSOR_C):  paramr_value = convert_temp(c=MAX_SENSOR_C)
            if param_value < convert_temp(c=MIN_SENSOR_C):  param_value = convert_temp(c=MIN_SENSOR_C)
            image_group[param_index + 70].text = str(param_value)
            image_group[param_index + 70].color = BLACK
            status_label.color = BLACK
            time.sleep(0.05)
            image_group[param_index + 70].color = param_list[param_index][1]
            status_label.color = WHITE
            time.sleep(0.2)

        if panel.button.a:  panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass  # wait for button release

    # Exit setup process
    if panel.button.start: panel.play_tone(784, 0.030)  # G5
    while panel.button.start:  pass  # wait for button release

    status_label.text = "RESUME"
    time.sleep(0.5)
    status_label.text = ""

    # Display average label and value
    ave_label.color = YELLOW
    ave_value.color = YELLOW
    return int(alarm_value.text), int(max_value.text),int(min_value.text)

def move_buttons(joystick=False):  # Read position buttons and joystick
    if joystick:  # For PyGamer: interpret joystick as buttons
        move_r = move_l = False
        if   panel.joystick[0] > 44000: move_r = True
        elif panel.joystick[0] < 20000: move_l = True
        move_u = move_d = False
        if   panel.joystick[1] < 20000: move_u = True
        elif panel.joystick[1] > 44000: move_d = True
    else:  # For PyBadge
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
image_group = displayio.Group(max_size=77)
board.DISPLAY.show(image_group)

# Create a background color fill
# Background; disp_group[0]
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                                x=0, y=0)
image_group.append(background)

# Define and build the foundational display group
# image_group[1:64]; [x]=(row * 8) + column
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(col, row)
        element = Rect(x=pos.x, y=pos.y,
                       width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                       fill=None, outline=None, stroke=0)
        image_group.append(element)

# Status label; image_group[65]
status_label = Label(font, text="", color=BLACK, max_glyphs=6)
status_label.x = (WIDTH // 2) - 7
status_label.y = int(1.4 * HEIGHT // 4) + 15
image_group.append(status_label)

# Alarm label; image_group[66]
alarm_label = Label(font, text="alm", color=WHITE, max_glyphs=3)
alarm_label.x = 0
alarm_label.y = int(0.5 * HEIGHT // 4) + 10
image_group.append(alarm_label)

# Maximum label; image_group[67]
max_label = Label(font, text="max", color=RED, max_glyphs=3)
max_label.x = 0
max_label.y = int(1.5 * HEIGHT // 4) + 10
image_group.append(max_label)

# Minimum label; image_group[68]
min_label = Label(font, text="min", color=CYAN, max_glyphs=3)
min_label.x = 0
min_label.y = int(3.5 * HEIGHT // 4) + 10
image_group.append(min_label)

# Average label; image_group[69]
ave_label = Label(font, text="ave", color=YELLOW, max_glyphs=3)
ave_label.x = 0
ave_label.y = int(2.5 * HEIGHT // 4) + 10
image_group.append(ave_label)

# Alarm value; image_group[70]
alarm_value = Label(font, text=str(ALARM_F), color=WHITE, max_glyphs=5)
alarm_value.x = 0
alarm_value.y = int(0 * HEIGHT // 4) + 10
image_group.append(alarm_value)

# Maximum value; image_group[71]
max_value = Label(font, text=str(MAX_RANGE_F), color=RED, max_glyphs=5)
max_value.x = 0
max_value.y = int(1 * HEIGHT // 4) + 10
image_group.append(max_value)

# Minimum value; image_group[72]
min_value = Label(font, text=str(MIN_RANGE_F), color=CYAN, max_glyphs=5)
min_value.x = 0
min_value.y = int(3 * HEIGHT // 4) + 10
image_group.append(min_value)

# Average value; image_group[73]
ave_value = Label(font, text="---", color=YELLOW, max_glyphs=5)
ave_value.x = 0
ave_value.y = int(2 * HEIGHT // 4) + 10
image_group.append(ave_value)

# Histogram minimum range value; image_group[74]
min_histo = Label(font, text="", color=CYAN, max_glyphs=3)
min_histo.x = (WIDTH // 4) - 5
min_histo.y = int(3.5 * HEIGHT // 4) + 10
image_group.append(min_histo)

# Histogram maximum range value; image_group[75]
max_histo = Label(font, text="", color=RED, max_glyphs=3)
max_histo.x = int(3 * WIDTH // 4) + 10
max_histo.y = int(3.5 * HEIGHT // 4) + 10
image_group.append(max_histo)

# Histogram range text label; image_group[75]
range_histo = Label(font, text="", color=BLUE, max_glyphs=7)
range_histo.x = int(1.5 * WIDTH // 4) + 5
range_histo.y = int(3.5 * HEIGHT // 4) + 10
image_group.append(range_histo)

###--- Primary Process ---###
display_image = True   # Image display mode; False for histogram
display_hold  = False  # Active display mode; True to hold display
display_focus = False  # Standard display range; True to focus display range
panel.play_tone(880, 0.1)  # A5; ready to start looking

while True:
    if not display_hold:  image = amg8833.pixels  # get camera data list
    if display_image:  # image display mode
        v_min, v_max, v_sum = update_image_frame()
    else:  # histogram display mode
        v_min, v_max, v_sum = update_histo_frame()

    # display alarm, maxumum, minimum, and average values
    alarm_value.text = str(ALARM_F)
    max_value.text = str(convert_temp(c=v_max))
    min_value.text = str(convert_temp(c=v_min))
    ave_value.text = str(convert_temp(c=v_sum // 64))

    # play alarm note if maximum value reaches alarm threshold
    if v_max >= ALARM_C:  panel.play_tone(880, 0.015)  # A5
    if v_max >= ALARM_C:  panel.play_tone(880 + (10 * (v_max - ALARM_C)), 0.015)  # A5

    if display_hold:  # flash hold status text label
        status_label.color = WHITE
        status_label.text  = "-HOLD-"
        time.sleep(0.1)
        status_label.color = BLACK
        time.sleep(0.1)
    else: status_label.text = ""  # clear status text label

    # See if a panel button is pressed
    if panel.button.a:  # toggle display hold (shutter = button A)
        panel.play_tone(1319, 0.030)  # E6
        while panel.button.a:  pass   # wait for button release
        if display_hold == False:  display_hold = True
        else:  display_hold = False

    if panel.button.b:  # toggle image/histogram mode (display mode = button B)
        panel.play_tone(659, 0.030)  # E5
        while panel.button.b:  pass  # wait for button release
        if display_image:  display_image = False
        else: display_image = True

    if panel.button.select:  # toggle focus mode (focus = select button)
        panel.play_tone(698, 0.030)  # F5
        if display_focus:
            display_focus = False  # restore previous range values
            MIN_RANGE_F = temp_min_range_f
            MAX_RANGE_F = temp_max_range_f
            MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)  # update range temp in Celsius
            MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)  # update range temp in Celsius
            status_label.color = WHITE
            status_label.text  = "ORIG"
            time.sleep(0.2)
            status_label.color = BLACK
            time.sleep(0.2)
        else:
            display_focus = True  # set range values to image min/max
            temp_min_range_f = MIN_RANGE_F
            temp_max_range_f = MAX_RANGE_F
            MIN_RANGE_F = convert_temp(c=v_min)
            MAX_RANGE_F = convert_temp(c=v_max)
            MIN_RANGE_C = v_min  # update range temp in Celsius
            MAX_RANGE_C = v_max  # update range temp in Celsius
            status_label.color = WHITE
            status_label.text  = "FOCUS"
            time.sleep(0.2)
            status_label.color = BLACK
            time.sleep(0.2)
        while panel.button.select:  pass  # wait for button release

    if panel.button.start:  # activate setup mode (setup mode = start button)
        panel.play_tone(784, 0.030)  # G5
        while panel.button.start:  pass  # wait for button release
        ALARM_F, MAX_RANGE_F, MIN_RANGE_F = setup_mode()  # get alarm and range values
        ALARM_C = convert_temp(f=ALARM_F)  # update alarm threshold temp in Celsius
        MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)  # update range temp in Celsius
        MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)  # update range temp in Celsius
        
