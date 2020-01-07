# Cedar Grove Thermal Camera

### _A portable PyGamer/PyBadge temperature visualization device._
![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05948_comp_wide.jpg)

## Overview

The Thermal Camera is a portable AMG8833-based thermopile array imager device implemented using CircuitPython on an Adafruit PyGamer or PyBadge SAMD51 handheld gaming platform. Features include measurement and imaging of 64 discrete temperatures within the range of 0 to 80 degress Celsius, adjustable color display gradient range, settable alarm threshold with audible alarm, image snapshot, image and histogram display modes, and an automatic temperature range focus option. The PyGamer/PyBadge platform provides the color display, control buttons, a speaker for the audible alarm, and room for a LiPo rechargable battery.

This implementation uses the Adafruit AMG8833 Thermal Camera FeatherWing. The breakout board version of the camera could be used via the Stemma interface in cases where the camera is to be mounted indepently of the PyGamer/PyBadge unit.

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05961a_wide.jpg)


## Project Description

A section of duct for the clothes dryer in our late 1940s-era home seemed to be prone to developing obstructions. It's scheduled to be replaced in a couple of months, but until it is, we'll keep a pretty close eye on it and clean it often. If only there was a way to monitor airflow and temperature along that 2 meter section.

The first duct monitor designs used thermistors and eventually thermocouples connected to an Adafruit Feather M4 Express. Code was to be be written in CircuitPython. Some graphic visualization would be nice as would a wireless IoT approach, but monitoring with a local audible alarm was more important.


## Primary Project Objectives
Required:
1) Continuously monitor and detect abnormal temperatures along a two-meter section of clothes dryer duct with a minimum sampling rate of one series of measurements per ten seconds.
2) Monitor and detect a minimum of three data points (duct entry, middle, and end sections). The minimum temperature monitoring range is from typical room temperature to ten degrees Celsius above the maximum safe operating temperature. The alarm threshold is set by a default start-up configuration file and manually through the device user interface.
3) An alarm condition activates a locally-placed and distintive audible alarm signal that continuously sounds until the high temperature drops to a safe level.
4) The duct temperature measurements will be displayed in easy to read numerals, defaulting to degrees Fahrenheit.
4) The device is powered by a wall-mounted USB power supply that provides primary operating power and charging of the device's internal backup battery. Battery backup duration is one-hour minimum.

Optional:
1) Graphical temperature display that includes a reprentative image, histogram, and trends.
2) Hold measurements for analysis.
3) Interactive minimum and maximum display range settings.
4) Record and retain monitoring history for up to two hours. Display historical data or create file for external analysis.
5) Selectable Celsius or Fahrenheit numerical display.

## Deliverables

## Concepts Learned

## Next Steps

Test video: https://youtu.be/IyMZOlKJu3Q


![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05961a_wide.jpg)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/DSC05942a_wide.jpg)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide1.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide2.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide3.PNG)

![Image of Module](https://github.com/CedarGroveStudios/Thermal_Camera/blob/master/photos%20and%20graphics/screen_cam_matrix/Slide4.PNG)
