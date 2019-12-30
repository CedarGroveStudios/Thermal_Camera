# Thermal_Cam_2019-12-30_v08.py

print("Thermal_Cam_2019-12-30_v08.py")

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

Coords = namedtuple("Point", "x y")

# display spash graphics

with open("/thermal_cam_splash.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    splash = displayio.Group()
    splash.append(displayio.TileGrid(bitmap,
                  pixel_shader=displayio.ColorConverter()))
    board.DISPLAY.show(splash)
    time.sleep(0.1)  # allow the splash to display

panel.play_tone(880, 0.1)
panel.play_tone(440, 0.1)
time.sleep(1)
panel.play_tone(880, 0.1)

### Settings ###
WIDTH  = board.DISPLAY.width
HEIGHT = board.DISPLAY.height

ELEMENT_SIZE = 16
BLACK   = 0x000000
RED     = 0xFF0000
ORANGE  = 0xFF8800
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

### Converters and Helpers ###
def convert_temp(f=None, c=None):  # convert F to C and C to F
    if f != None and c == None: return round((f - 32) * (5 / 9), 1)
    if f == None and c != None: return int(round(((9 / 5) * c) + 32, 0))
    return None

def element_grid(row, col):
    return Coords(ELEMENT_SIZE * row + 30, ELEMENT_SIZE * col + 1)

def update_image_frame():
    minimum = 80 # set minimum to maximum C value
    maximum = 0  # set maximum to minimum C value
    sum_bucket = 0  # bucket for building average value
    for row in range(0, 8):  # parse camera data list and update display
        for col in range(0, 8):
            value = map_range(image[7 - col][7 - row], 0, 80, 0, 80)
            pos = element_grid(row, col)
            color_index = int(map_range(value, MIN_RANGE, MAX_RANGE, 0, 7))
            disp_group[((row * 8) + col) + 1] = Rect(x=pos.x, y=pos.y, width=ELEMENT_SIZE,
                                                     height=ELEMENT_SIZE,
                                                     fill=element_color[color_index])
            sum_bucket = sum_bucket + value  # calculate sum for average
            minimum = min(value, minimum)
            maximum = max(value, maximum)
    return minimum, maximum, sum_bucket

def update_histo_frame():
    minimum = 80 # set minimum to maximum C value
    maximum = 0  # set maximum to minimum C value
    sum_bucket = 0  # bucket for building average value
    histo_bucket = [0, 0, 0, 0, 0, 0, 0, 0]  # reset histogram bucket
    for row in range(0, 8):  # parse camera data list and update display
        for col in range(7, -1, -1):
            value = map_range(image[7 - col][7 - row], 0, 80, 0, 80)
            histo_index = int(map_range(value, MIN_RANGE, MAX_RANGE, 0, 7))
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

### Set alarm and range values ###
ALARM_F   = 120               # alarm temp in Farenheit
ALARM_C   = convert_temp(f=ALARM_F)  # alarm temp in Celsius
MIN_RANGE = convert_temp(f=50)
MAX_RANGE = convert_temp(f=120)

# Establish the display context
disp_group = displayio.Group(max_size=74)
board.DISPLAY.show(disp_group)

# Create a background color fill
color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                                x=0, y=0)
disp_group.append(background)

# Define and build the foundational display group
for row in range(0, 8):
    for col in range(0, 8):
        pos = element_grid(col, row)
        disp_group.append(Rect(x=pos.x, y=pos.y,
                          width=ELEMENT_SIZE, height=ELEMENT_SIZE,
                          fill=None))

hold_label = Label(font, text="", color=WHITE, max_glyphs=6)
hold_label.x = (WIDTH // 2) - 7
hold_label.y = 15 + int(1.4 * HEIGHT // 4)
disp_group.append(hold_label)

alarm_label = Label(font, text="alm", color=WHITE, max_glyphs=3)
alarm_label.x = 0
alarm_label.y = 10 + int(0.5 * HEIGHT // 4)
disp_group.append(alarm_label)

max_label = Label(font, text="max", color=RED, max_glyphs=3)
max_label.x = 0
max_label.y = 10 + int(1.5 * HEIGHT // 4)
disp_group.append(max_label)

ave_label = Label(font, text="ave", color=YELLOW, max_glyphs=3)
ave_label.x = 0
ave_label.y = 10 + int(2.5 * HEIGHT // 4)
disp_group.append(ave_label)

min_label = Label(font, text="min", color=CYAN, max_glyphs=3)
min_label.x = 0
min_label.y = 10 + int(3.5 * HEIGHT // 4)
disp_group.append(min_label)

alarm_display = Label(font, text=str(ALARM_F), color=WHITE, max_glyphs=5)
alarm_display.x = 0
alarm_display.y = 10 + int(0 * HEIGHT // 4)
disp_group.append(alarm_display)

max_display = Label(font, text="176", color=RED, max_glyphs=5)
max_display.x = 0
max_display.y = 10 + int(1 * HEIGHT // 4)
disp_group.append(max_display)

ave_display = Label(font, text="---", color=YELLOW, max_glyphs=5)
ave_display.x = 0
ave_display.y = 10 + int(2 * HEIGHT // 4)
disp_group.append(ave_display)

min_display = Label(font, text="32", color=CYAN, max_glyphs=5)
min_display.x = 0
min_display.y = 10 + int(3 * HEIGHT // 4)
disp_group.append(min_display)

time.sleep(1.0)
disp_group[65].text = ""

### Primary Process: Get camera data and update display ###
display_image = True  # default to image display mode
display_hold = False       # default to active display mode

while True:  # Display image or histogram
    if not display_hold:  image = amg8833.pixels  # get camera data list
    if display_image:
        v_min, v_max, v_sum = update_image_frame()
    else:
        v_min, v_max, v_sum = update_histo_frame()

    # update display text values
    disp_group[70].text = str(ALARM_F)
    disp_group[71].text = str(convert_temp(c=v_max))
    disp_group[72].text = str(convert_temp(c=v_sum // 64))
    disp_group[73].text = str(convert_temp(c=v_min))

    if v_max >= ALARM_C:  panel.play_tone(880, 0.030)

    if display_hold:  # display hold text label
        disp_group[65].color = WHITE
        disp_group[65].text  = "-hold-"
        time.sleep(0.1)
        disp_group[65].color = BLACK
        disp_group[65].text  = "-hold-"
        time.sleep(0.1)
    else: disp_group[65].text  = ""  # clear hold text label

    # See if a panel button is pressed
    if panel.button.a:  # toggle display hold (shutter = button A)
        if display_hold == False:  display_hold = True
        else:  display_hold = False
        while panel.button.a: pass  # wait for button release
        panel.play_tone(1220, 0.030)

    if panel.button.b:  # toggle image/histogram mode (display mode = button B)
        if display_image:  display_image = False
        else: display_image = True
        while panel.button.b:  pass  # wait for button release
        panel.play_tone(660, 0.030)
