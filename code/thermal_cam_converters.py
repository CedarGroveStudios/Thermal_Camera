# Thermal_Cam_converters.py
# (c) 2020 Cedar Grove Studios

def celsius_to_fahrenheit(deg_c=None):  # convert C to F
    return round(((9 / 5) * deg_c) + 32)

def fahrenheit_to_celsius(deg_f=None):  # convert F to C
    return round((deg_f - 32) * (5 / 9))
