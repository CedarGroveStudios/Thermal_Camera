# Thermal_Cam_2020-01-03_v21.py
# (c) 2020 Cedar Grove Studios

print("Thermal_Cam_2020-01-03_v21.py")

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

# Establish I2C interface for camera wing
i2c = board.I2C()
amg8833 = adafruit_amg88xx.AMG88XX(i2c)

# Display spash graphics
with open("/thermal_cam_splash.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    splash = displayio.Group()
    splash.append(displayio.TileGrid(bitmap,
                  pixel_shader=displayio.ColorConverter()))
    board.DISPLAY.show(splash)
    time.sleep(0.1)  # allow the splash to display

panel.play_tone(440, 0.1)  # A4
panel.play_tone(880, 0.1)  # A5

Coords = namedtuple("Point", "x y")

### Settings ###

# Load F default alarm and min/max range values
from Thermal_Cam_config import *

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
CYAN    = 0x00FFFF
BLUE    = 0x0000FF
VIOLET  = 0x9900FF
WHITE   = 0xFFFFFF
GRAY    = 0x444455

element_color = [GRAY, BLUE, GREEN, YELLOW, ORANGE, RED, VIOLET, WHITE]
param_list = [("ALARM", WHITE), ("RANGE", RED), ("RANGE", CYAN)]

### Converters and Helpers ###
def convert_temp(f=None, c=None):  # convert F to C and C to F
    if f != None and c == None: return round((f - 32) * (5 / 9))  # F to C
    if f == None and c != None: return round(((9 / 5) * c) + 32)  # C to F
    return None

def element_grid(col, row):  # Determine display coordinates for column, row
    return Coords(int(ELEMENT_SIZE * col + 30), int(ELEMENT_SIZE * row + 1))

def flash_status(text="", duration=0.1):  # Flash status message
    status_label.color = WHITE
    status_label.text  = text
    time.sleep(duration)
    status_label.color = BLACK
    time.sleep(duration)
    return

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

    time.sleep(0.8)  # Show SET status text for a while
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
            if param_value > convert_temp(c=MAX_SENSOR_C):  param_value = convert_temp(c=MAX_SENSOR_C)
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
    move_r = move_l = False
    move_u = move_d = False
    if joystick:  # For PyGamer: interpret joystick as buttons
        if   panel.joystick[0] > 44000: move_r = True
        elif panel.joystick[0] < 20000: move_l = True
        if   panel.joystick[1] < 20000: move_u = True
        elif panel.joystick[1] > 44000: move_d = True
    else:  # For PyBadge
        if panel.button.right: move_r = True
        if panel.button.left : move_l = True
        if panel.button.up   : move_u = True
        if panel.button.down : move_d = True
    return move_r, move_l, move_u, move_d

# Set C default alarm and min/max range values
ALARM_C     = convert_temp(f=ALARM_F)  # alarm temp in Celsius
MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)
MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)

# Establish the display context
image_group = displayio.Group(max_size=77)

# Create a background color fill
# Background; disp_group[0]
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                                x=0, y=0)
image_group.append(background)

### Define and build the foundational display group ###
# image_group[1:64]; [x]=(row * 8) + column
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(col, row)
        element = Rect(x=pos.x, y=pos.y,
                       width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                       fill=None, outline=None, stroke=0)
        image_group.append(element)

# Define labels and values using element grid coordinates
status_label = Label(font, text="", color=BLACK, max_glyphs=6)
pos = element_grid(2.5, 4)
status_label.x = pos.x
status_label.y = pos.y
image_group.append(status_label)

alarm_label = Label(font, text="alm", color=WHITE, max_glyphs=3)
pos = element_grid(-1.8, 1.5)
alarm_label.x = pos.x
alarm_label.y = pos.y
image_group.append(alarm_label)

max_label = Label(font, text="max", color=RED, max_glyphs=3)
pos = element_grid(-1.8, 3.5)
max_label.x = pos.x
max_label.y = pos.y
image_group.append(max_label)

min_label = Label(font, text="min", color=CYAN, max_glyphs=3)
pos = element_grid(-1.8, 7.5)
min_label.x = pos.x
min_label.y = pos.y
image_group.append(min_label)

ave_label = Label(font, text="ave", color=YELLOW, max_glyphs=3)
pos = element_grid(-1.8, 5.5)
ave_label.x = pos.x
ave_label.y = pos.y
image_group.append(ave_label)

alarm_value = Label(font, text=str(ALARM_F), color=WHITE, max_glyphs=5)
pos = element_grid(-1.8, 0.5)
alarm_value.x = pos.x
alarm_value.y = pos.y
image_group.append(alarm_value)

max_value = Label(font, text=str(MAX_RANGE_F), color=RED, max_glyphs=5)
pos = element_grid(-1.8, 2.5)
max_value.x = pos.x
max_value.y = pos.y
image_group.append(max_value)

min_value = Label(font, text=str(MIN_RANGE_F), color=CYAN, max_glyphs=5)
pos = element_grid(-1.8, 6.5)
min_value.x = pos.x
min_value.y = pos.y
image_group.append(min_value)

ave_value = Label(font, text="---", color=YELLOW, max_glyphs=5)
pos = element_grid(-1.8, 4.5)
ave_value.x = pos.x
ave_value.y = pos.y
image_group.append(ave_value)

min_histo = Label(font, text="", color=CYAN, max_glyphs=3)
pos = element_grid(0.5, 7.5)
min_histo.x = pos.x
min_histo.y = pos.y
image_group.append(min_histo)

max_histo = Label(font, text="", color=RED, max_glyphs=3)
pos = element_grid(6.5, 7.5)
max_histo.x = pos.x
max_histo.y = pos.y
image_group.append(max_histo)

range_histo = Label(font, text="", color=BLUE, max_glyphs=7)
pos = element_grid(2.5, 7.5)
range_histo.x = pos.x
range_histo.y = pos.y
image_group.append(range_histo)

###--- Primary Process ---###
display_image = True   # Image display mode; False for histogram
display_hold  = False  # Active display mode; True to hold display
display_focus = False  # Standard display range; True to focus display range
board.DISPLAY.show(image_group)
panel.play_tone(880, 0.1)  # A5; ready to start looking

while True:
    if display_hold:  # flash hold status text label
        flash_status("-HOLD-")
    else:
        image = amg8833.pixels  # get camera data list
        status_label.text = ""  # clear status text label

    if display_image:  # image display mode
        v_min, v_max, v_sum = update_image_frame()
    else:  # histogram display mode
        v_min, v_max, v_sum = update_histo_frame()

    # display alarm, maxumum, minimum, and average values
    alarm_value.text = str(ALARM_F)
    max_value.text   = str(convert_temp(c=v_max))
    min_value.text   = str(convert_temp(c=v_min))
    ave_value.text   = str(convert_temp(c=v_sum // 64))

    # play alarm note if maximum value reaches alarm threshold
    if v_max >= ALARM_C:  panel.play_tone(880, 0.015)  # A5
    if v_max >= ALARM_C:  panel.play_tone(880 + (10 * (v_max - ALARM_C)), 0.015)  # A5

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
            flash_status("ORIG", 0.2)
        else:
            display_focus = True  # set range values to image min/max
            temp_min_range_f = MIN_RANGE_F
            temp_max_range_f = MAX_RANGE_F
            MIN_RANGE_F = convert_temp(c=v_min)
            MAX_RANGE_F = convert_temp(c=v_max)
            MIN_RANGE_C = v_min  # update range temp in Celsius
            MAX_RANGE_C = v_max  # update range temp in Celsius
            flash_status("FOCUS", 0.2)
        while panel.button.select:  pass  # wait for button release

    if panel.button.start:  # activate setup mode (setup mode = start button)
        panel.play_tone(784, 0.030)  # G5
        while panel.button.start:  pass  # wait for button release
        ALARM_F, MAX_RANGE_F, MIN_RANGE_F = setup_mode()  # get alarm and range values
        ALARM_C = convert_temp(f=ALARM_F)  # update alarm threshold temp in Celsius
        MIN_RANGE_C = convert_temp(f=MIN_RANGE_F)  # update range temp in Celsius
        MAX_RANGE_C = convert_temp(f=MAX_RANGE_F)  # update range temp in Celsius
