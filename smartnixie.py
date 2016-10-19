#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(0)

ss = (0x09, 0x08)
mm = (0x0b, 0x0a)
hh = (0x0d, 0x0c)

REG_DIGIT = 0x00

def setdigits(addrs, vals, sep):
    chars = list(divmod(vals, 10))
    if sep:
        chars[0] = chars[0] | 0x40
    for addr, val in zip(addrs, chars):
        bus.write_byte_data(addr, REG_DIGIT, val)

while True:
    t = time.localtime()
    setdigits(hh, t.tm_hour, False)
    setdigits(mm, t.tm_min, t.tm_sec%2)
    setdigits(ss, t.tm_sec, t.tm_sec%2)
    time.sleep(0.05)
