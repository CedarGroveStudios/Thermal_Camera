# Cedar Grove Thermal Camera

### _A portable PyGamer/PyBadge temperature visualization device._
![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05948_comp_wide.jpg)

## Overview

The Thermal Camera is a portable AMG8833-based thermopile array imager device implemented using CircuitPython on an Adafruit PyGamer or PyBadge SAMD51 handheld gaming platform. Features include measurement and imaging of 64 discrete temperatures within the range of 0 to 80 degress Celsius, adjustable color display gradient range, settable alarm threshold with audible alarm, image snapshot, image and histogram display modes, and an automatic temperature range focus option. The PyGamer/PyBadge platform provides the color display, control buttons, a speaker for the audible alarm, and room for a LiPo rechargable battery.

This implementation uses the Adafruit AMG8833 Thermal Camera FeatherWing. The breakout board version of the camera could be used via the Stemma interface in cases where the camera is to be mounted indepently of the PyGamer/PyBadge unit.

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05961a_wide.jpg)


## Project Description

A section of duct for the clothes dryer in our late 1940s-era home seemed to be prone to developing obstructions. It's scheduled to be replaced in a couple of months, but until it is, we'll keep a pretty close eye on it and clean it often. This project evolved from the need to watch for abnormal temperature build-up along the problemmatic two-meter section of exhaust duct.

The first duct monitor designs used thermistors (eventually thermocouples) connected to an Adafruit Feather M4 Express for data collection and analysis. Code was to be be written in CircuitPython. Some graphic visualization would be nice as would a wireless IoT approach, but monitoring with a local audible alarm was more important.

As the project design developed, the AMG8833 8x8 thermopile array sensor and its imaging capability became more desireable. Not only did the sensor match the needed temperature range, it provided the capability to measure many points along the duct rather than only three. Also, the sensor could be mounted in a convienient location a distance away from the duct and still perform the needed measurements. There was also no need to string wires and physicallyl mount thermocouples to the ductwork.

It first appeared that CircuitPython may not be fast enough to process the AMG8833 matrix data for real-time graphical imaging, but would only be responsive when conducting simple numerical calculations (like alarm threshold detection) on the matrix data. Since a ten-second measurement interval was fast enough for this project, evolving the design to include a graphical image display was seen as a possibility in spite of those perceived limitations. After some initial prototype tests, it was found that CircuitPython and the DisplayIO library were indeed fast enough and could provide a measurement interval of less than one second per frame of 64 measurements.

The design evolved from the inital prototype tests to a final version that met the original requirements, but also had added features that allowed the unit to be used as a standalone, camera-like device. The code was modified to work with the PyBadge or PyGamer, adjusting for direction buttons or joystick operation. After final testing, a friend referred to the Thermal Camera as being similar to and as useful as a carpentry stud finder.

Test video: https://youtu.be/IyMZOlKJu3Q

The Thermal Camera utilizes four PyGamer/PyBadge-stored files to operate:
*  Thermal_Cam_2020-01-03_v21.py (renamed to code.py), the primary code module, version 2.1, stored in the root directory
*  Thermal_Cam_config.py, a Python-formatted list of default operating parameters in text file format, stored in the root directory
*  Thermal_Cam_splash.bmp, a bitmapped graphics file used for the opening splash screen, stored in the root directory
*  OpenSans-9.bdf, a sans serif font file, stored in a fonts folder

Note: Although the author is experienced with Arduino coding, the choice to use CircuitPython for the software implementation was driven by the desire to continue to learn more about Python coding and particularly the CircuitPython graphical library, DisplayIO.

## Primary Project Objectives
Required:
1) Continuously monitor and detect abnormal temperatures along a two-meter section of clothes dryer duct with a minimum sampling rate of one series of measurements per ten seconds.
2) Monitor and detect a minimum of three data points (duct entry, middle, and end sections). The minimum temperature monitoring range is from typical room temperature to ten degrees Celsius above the maximum safe operating temperature. Typical accuracy of +/-2.5 degrees C is sufficient. The alarm threshold is set by a default start-up configuration file and manually through the device user interface.
3) An alarm condition activates a locally-placed and distintive audible alarm signal that continuously sounds until the high temperature drops to a safe level.
4) The duct temperature measurements will be displayed in easy to read numerals, defaulting to degrees Fahrenheit.
5) The device is powered by a wall-mounted USB power supply that provides primary operating power and charging of the device's internal backup battery. Battery backup duration is one-hour minimum.
6) Utilize CircuitPython for the software implementation.

Optional:
1) Graphical temperature display that includes a reprentative image, histogram, and trends.
2) Image view: 45 to 60-degree field of view over 5-meter minimum imaging range.
2) Hold measurements for analysis.
3) Interactive minimum and maximum display range settings.
4) Record and retain monitoring history for up to two hours. Display historical data or create file for external analysis.
5) Selectable Celsius or Fahrenheit numerical display.

## Deliverables

## Concepts Learned

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide1.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide2.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide3.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide4.PNG)

## Next Steps



![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05942a_wide.jpg)

