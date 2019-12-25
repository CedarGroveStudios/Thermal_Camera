# Dryer_Vent_Mon_2019-12-21_v00.py
# Cedar Grove Studios

import time
from cedargrove_pypanel import *

print("Dryer_Vent_Mon_2019-12-21_v00.py")
print(" ")
print("Stemma devices found:")
for i in range(0, len(stemma)):
    print("%s : %s" % (stemma[i][0], stemma[i][2]))
if len(stemma) == 0: print("--none--")
print(" ")
time.sleep(2)

# PyBadge test
panel.pixels.fill((255, 24, 255))  # dim purple neopixels
panel.brightness = 0.9  # set initial display brightness
panel.show_badge(name_string="Vent Monitor", hello_scale=2, my_name_is_scale=1, name_scale=2)
time.sleep(2)
panel.show_terminal()

while True:
    for row in amg8833.pixels:
        # Pad to 1 decimal place
        print(['{0:.1f}'.format(temp) for temp in row])
        print("")
    print("\n")
    time.sleep(1)
