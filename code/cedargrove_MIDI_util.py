# The MIT License (MIT)

# Copyright (c) 2019 Cedar Grove Studios

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`cedargrove_MIDI_util`
================================================================================
cedargrove_MIDI_util.py 2019-03-31 v00 09:20PM
A CircuitPython method collection for processing MIDI notes.

* Author(s): Cedar Grove Studios

Implementation Notes
--------------------
**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/MIDI_Util.git"

from math import log  # required for freq_note helper

# list of valid note names used by note_lexo, note_name, and name_note helpers
note_base = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_lexo(input):
    """ Bidirectionally translates a MIDI sequential note value to a note name
          or a note name to a MIDI sequential note value. Note values are
          of integer type in the range of 0 to 127 (inclusive). Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). If the input value is outside of the note
          value or name range, the value of None is returned.
    """
    if type(input) == str:  # if input is type string, assume it's a name
        return name_note(input)  # get note value from name_note helper
    elif type(input) == int:  # if input is integer, assume it's a note value
        return note_name(input)  # get note name from note_name helper
    else: return None  # invalid input parameter type

def note_name(note):
    """ Translates a MIDI sequential note value to a note name. Note values are
          of integer type in the range of 0 to 127 (inclusive). Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). If the input value is outside of that range,
          the value of None is returned.
    """
    if 0 <= note <= 127:  # check for valid note value range
        return note_base[note % 12] + str((note // 12)-1)  # assemble name
    else: return None  # note value outside valid range

def name_note(name):
    """ Translates a note name to a MIDI sequential note value. Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). Note values are of integer type in the range
          of 0 to 127 (inclusive). If the input value is outside of that range,
          the value of None is returned.
    """
    name = name.upper()  # convert lower to uppercase
    if (name[:1] or name[:2]) in note_base:  # check for valid note name
        if '#' in name:  # find name and extract octave
            note = note_base.index(name[:2])
            octave = int(name[2:])
        else:  # find name and extract octave
            note = note_base.index(name[0])
            octave = int(name[1:])
        return note + (12 * (octave + 1))  # calculate note value
    else: return None  # string not in note_base

def note_freq(note):
    """ Translates a MIDI sequential note value to its corresponding frequency
          in Hertz (Hz). Note values are of integer type in the range of 0 to
          127 (inclusive). Frequency values are floating point. If the input
          note value is less than 0 or greater than 127, the input is
          considered to be invalid and the value of None is returned.
          Ref: MIDI Tuning Standard formula.
    """
    if 0 <= note <= 127:
        return pow(2, (note - 69) / 12) * 440
    else: return None  # note value outside valid range

def freq_note(freq):
    """ Translates a frequency in Hertz (Hz) to the closest MIDI sequential
          note value. Frequency values are floating point. Note values are of
          integer type in the range of 0 to 127 (inclusive). If the input
          frequency is less than the corresponding frequency for note 0 or
          greater than note 127, the input is considered to be invalid and
          the value of None is returned. Ref: MIDI Tuning Standard formula.
    """
    if (pow(2, (0 - 69) / 12) * 440) <= freq <= (pow(2, (127 - 69) / 12) * 440):
        return int(69 + (12* log(freq / 440, 2)))
    else: return None  # frequency outside valid range

# Controller definitions -- no list offset
#   0-63 continuous, 64-121 switch, 122-127 channel mode
controllers = [
    ('Bank_Select'),
    ('Modulation'),
    ('Breath_Ctrl'),
    ('Ctrl_3'),
    ('Foot_Ctrl'),
    ('Portamento_Time'),
    ('Data_Entry_MSB'),
    ('Chan_Vol'),
    ('Balance'),
    ('Ctrl_9',),
    ('Pan_Ctrl'),
    ('Exp_Pedal'),
    ('FX_Ctrl_1'),
    ('FX_Ctrl_2'),
    ('Ctrl_14'),
    ('Ctrl_15'),
    ('Gen_Pur_1'),
    ('Gen_Pur_2'),
    ('Gen_Pur_3'),
    ('Gen_Pur_4'),
    ('Ctrl_20'),
    ('Ctrl_21'),
    ('Ctrl_22'),
    ('Ctrl_23'),
    ('Ctrl_24'),
    ('Ctrl_25'),
    ('Ctrl_26'),
    ('Ctrl_27'),
    ('Ctrl_28'),
    ('Ctrl_29'),
    ('Ctrl_30'),
    ('Ctrl_31'),
    ('Bank_Sel_LSB'),
    ('Modulation_LSB'),
    ('Breath_Ctrl_LSB'),
    ('Ctrl_3_LSB'),
    ('Foot_Ctrl_LSB'),
    ('Portamento_Time_LSB'),
    ('Data_Entry_LSB'),
    ('Chan_Vol_LSB'),
    ('Balance_LSB'),
    ('Ctrl_9_LSB'),
    ('Pan_Ctrl_LSB'),
    ('Exp_Pedal_LSB'),
    ('FX_Ctrl_1_LSB'),
    ('FX_Ctrl_2_LSB'),
    ('Ctrl_14_LSB'),
    ('Ctrl_15_LSB'),
    ('Gen_Pur_1_LSB'),
    ('Gen_Pur_2_LSB'),
    ('Gen_Pur_3_LSB'),
    ('Gen_Pur_4_LSB'),
    ('Ctrl_20_LSB'),
    ('Ctrl_21_LSB'),
    ('Ctrl_22_LSB'),
    ('Ctrl_23_LSB'),
    ('Ctrl_24_LSB'),
    ('Ctrl_25_LSB'),
    ('Ctrl_26_LSB'),
    ('Ctrl_27_LSB'),
    ('Ctrl_28_LSB'),
    ('Ctrl_29_LSB'),
    ('Ctrl_30_LSB'),
    ('Ctrl_31_LSB'),
    ('Sus_Damp_Pedal_sw'),
    ('Portamento_sw'),
    ('Sostenuto_sw'),
    ('Soft_Pedal_sw'),
    ('Legato_Foot_sw'),
    ('Hold_2_sw'),
    ('Sound_Ctrl_1_Variation'),
    ('Sound_Ctrl_2_Tibre'),
    ('Sound_Ctrl_3_Release'),
    ('Sound_Ctrl_4_Attack'),
    ('Sound_Ctrl_5_Bright'),
    ('Sound_Ctrl_6_Decay'),
    ('Sound_Ctrl_7_Vib_Rate'),
    ('Sound_Ctrl_8_Vib_Depth'),
    ('Sound_Ctrl_9_Vib_Delay'),
    ('Sound_Ctrl_10'),
    ('Gen_Pur_5'),
    ('Gen_Pur_6'),
    ('Gen_Pur_7'),
    ('Gen_Pur_8'),
    ('Portamento_Ctrl'),
    ('Ctrl_85'),
    ('Ctrl_86'),
    ('Ctrl_87'),
    ('HR_Vel_Prefix'),
    ('Ctrl_89'),
    ('Ctrl_90'),
    ('FX_1_Depth_Reverb'),
    ('FX_2_Depth'),
    ('FX_3_Depth'),
    ('FX_4_Depth'),
    ('FX_5_Depth'),
    ('Data_Inc', 'Value'),
    ('Data_Dec', 'Value'),
    ('NRPN_LSB', 'Value'),
    ('NRPN_MSB', 'Value'),
    ('RPN_LSB', 'Value'),
    ('RPN_MSB', 'Value'),
    ('Ctrl_102'),
    ('Ctrl_103'),
    ('Ctrl_104'),
    ('Ctrl_105'),
    ('Ctrl_106'),
    ('Ctrl_107'),
    ('Ctrl_108'),
    ('Ctrl_109'),
    ('Ctrl_110'),
    ('Ctrl_111'),
    ('Ctrl_112'),
    ('Ctrl_113'),
    ('Ctrl_114'),
    ('Ctrl_115'),
    ('Ctrl_116'),
    ('Ctrl_117'),
    ('Ctrl_118'),
    ('Ctrl_119'),
    ('All_Sound_Off'),
    ('Reset_All_Ctrls'),
    ('Local_Ctrl_sw'),
    ('All_Notes_Off'),
    ('Omni_Mode_Off'),
    ('Omni_Mode_On'),
    ('Mono_Mode_On'),
    ('Poly_Mode_On'),
    ]

def cc_decoder(cc_code):
    """ Decodes a Control Change controller code into the controller description
# ref: https://www.midi.org/specifications/item/table-3-control-change-messages-data-bytes-2
    """
    return controllers[cc_code]
