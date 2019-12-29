catalog = {
	'mcp4725' : {
		'name'     : 'MCP4725',
		'desc'     : '12-bit DAC',
		'import'   : 'import adafruit_mcp4725',
		'instance' : 'mcp4725 = adafruit_mcp4725.MCP4725(i2c)',
		'test'     : 'mcp4725.normalized_value = 0.0'
		},

	'ssd1306' : {
		'name'     : 'SSD1306',
		'desc'     : '128x32 OLED',
		'import'   : 'import adafruit_ssd1306',
		'instance' : 'ssd1306 = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)',
		'test'     : 'ssd1306.fill(0)'
		},

	'ds3231' : {
		'name'     : 'DS3231',
		'desc'     : 'RTC Wing',
		'import'   : 'import adafruit_ds3231',
		'instance' : 'ds3231 = adafruit_ds3231.DS3231(i2c)',
		'test'     : 'ds3231.datetime'
		},

	'amg8833' : {
		'name'     : 'AMG8833',
		'desc'     : '8x8 Thermal Cam',
		'import'   : 'import adafruit_amg88xx',
		'instance' : 'amg8833 = adafruit_amg88xx.AMG88XX(i2c)',
		'test'     : 'amg.pixels'
		},

	'crickit' : {  # needs to be last I2C device; locks bus
		'name'     : 'Crickit',
		'desc'     : 'Crickit Wing',
		'import'   : 'from adafruit_crickit import crickit',
		'instance' : 'crickit.init_neopixel(1, brightness=0.01)',
		'test'     : 'crickit.onboard_pixel.brightness = 0.01'
		}
}

"""
	device : {
		'name'     : name,
		'desc'     : description,
		'import'   : import string to execute,
		'instance' : instance string to execute,
		'test'     : test string to execute
		}
"""
