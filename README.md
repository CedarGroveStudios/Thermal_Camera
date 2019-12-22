# Cedar Grove Robot Friend FeatherWing

### _A passive FeatherWing adapter for stacking an Adafruit PyBadge or PyGamer onto a Crickit FeatherWing. Includes a prototyping area for custom circuitry and sensors._

![Image of Module](https://github.com/CedarGroveStudios/Robot_Friend_FeatherWing/blob/master/photos%20and%20graphics/Robot_Friend_expl_wide.png)

Perched on the top of a robot chassis, the Cedar Grove Robot Friend FeatherWing passively connects the FeatherWing connections of a PyBadge or PyGamer device with a Crickit FeatherWing. The Crickit provides 3.3V power to the attached PyBadge/PyGamer. All Feather signals are interconnected to accommodate custom alterations to the Crickit module, such as support for IRQ/Busy or sensor modifications.

The Cedar Grove Robot Friend includes a prototype area and a breakout of all Feather pins for further cusomization.

For use ONLY with the Crickit FeatherWing and compatible Feather MCU boards. To date, it has only been tested with the PyGamer and PyBadge. Double-check pin compatibility if you plan to attach or stack other Feather devices.

#### Caution:
The Crickit is capable of providing up to 150mA of 3.3-volt power to the attached PB/PG Feather. In normal operation without any of the NeoPixels lighted or the use of the built-in speaker amplifier, the PB/PG will draw about 60mA from the Crickit's internal 3.3-volt regulator. 

When the PB/PG is powered only by the Crickit via the Feather 3V pin, the PB/PG 3.3v regulator is reverse-biased by the Crickit-supplied +3.3 volts. The AP2112-3.3 regulator has an intrinsic MOSFET diode between its output and input that conducts when reverse-biased, raising the voltage of the input pin to the same as the output pin less the forward voltage drop of the diode. What that means is that 5-volt components like the PB/PG's NeoPixels and Stemma connectors will have approximately +3.2 volts available for operation. The PB/PG NeoPixels seem to work with the lower voltage, but might not be 100% reliable. 

Since the reverse-biased "feature" of the PB/PG's internal regulator is not documented in the datasheet, it's probably a good idea to limit use of the PB/PG NeoPixels when stacked on the Crickit via the Robot Friend FeatherWing. If you need to brightly light the PB/PG NeoPixels or connect a speaker to the on-board amplifier, consider adding a small LiPo battery directly to the PB/PG or just use the Crickit's on-board NeoPixel or drive a string via the Crickit's external NeoPixel connector. If a louder speaker is needed, use the Crickit's speaker output since the Crickit amplifier is not connected to the 3.3-volt power supply.

Intrinsic MOSFET Diode Discussion: https://www.digikey.com/en/articles/techzone/2016/sep/the-significance-of-the-intrinsic-body-diodes-inside-mosfets

OSH Park project: <a href="https://oshpark.com/shared_projects/DxtJkU02"><img src="https://oshpark.com/assets/badge-5b7ec47045b78aef6eb9d83b3bac6b1920de805e9a0c227658eac6e19a045b9c.png" alt="Order from OSH Park"></img></a>

![Image of Module](https://github.com/CedarGroveStudios/Robot_Friend_FeatherWing/blob/master/photos%20and%20graphics/Robot_Friend_glam_wide.png)

![Image of Module](https://github.com/CedarGroveStudios/Robot_Friend_FeatherWing/blob/master/photos%20and%20graphics/Robot_Friend_PCB_combo.png)

