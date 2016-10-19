#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(0)

ss = (0x09, 0x08)
mm = (0x0b, 0x0a)
hh = (0x0d, 0x0c)

REG_DIGIT = 0x00

def blankdigits(addrs):
    for addr in addrs:
        bus.write_byte_data(addr, REG_DIGIT, 0x0b)

blankdigits(hh)
blankdigits(mm)
blankdigits(ss)

