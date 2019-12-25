# Dryer_Vent_Mon_2019-12-22_v01.py
# Cedar Grove Studios

import time
from cedargrove_pypanel import *
panel.show_terminal()

print("Dryer_Vent_Mon_2019-12-22_v01.py")
print(" ")
print("Stemma devices found:")
for i in range(0, len(stemma)):
    print("%s : %s" % (stemma[i][0], stemma[i][2]))
if len(stemma) == 0: print("--none--")
print(" ")
time.sleep(1)

# draw 8x8 dot display
disp_size = int(min(board.DISPLAY.width, board.DISPLAY.height) * 0.9)  # 90% of screensize
disp_margin = int(disp_size / 9 / 2)
disp_factor = disp_size // 8
disp_color = [Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.RED, Color.PURPLE, Color.WHITE]

turtle = turtle(board.DISPLAY)
turtle.penup()
disp_start = int(1 / 2 * disp_size) - disp_margin
turtle.goto(-1 * disp_start, disp_start)

while True:
    image = amg8833.pixels
    for y in range(7, -1, -1):
        for x in range(7, -1, -1):
            turtle.goto(disp_start - (x * disp_factor), (y * disp_factor) - disp_start)
            color_index = int((image[y][x] - 15) / 4)
            turtle.pencolor(disp_color[color_index])
            turtle.dot(6)
    time.sleep(0)
