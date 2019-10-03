#!/usr/bin/env python

import smbus
import time
from os import read
import butter.timerfd as tfd
import select

bus = smbus.SMBus(0)

ss = (0x09, 0x08)
mm = (0x0b, 0x0a)
hh = (0x0d, 0x0c)

REG_DIGIT = 0x00

def setdigits(addrs, vals, sep):
    chars = list(divmod(vals, 10))
    if sep:
        chars[0] = chars[0] | 0x40
    if sep > 1:
        chars[1] = chars[1] | 0x40
    for addr, val in zip(addrs, chars):
        bus.write_byte_data(addr, REG_DIGIT, val)

tv = tfd.TimerVal()
tv.occuring.every(seconds=1).offset(seconds=long(time.time() + 2))
timer = tfd.timerfd(clock_type=tfd.CLOCK_REALTIME)
ep = select.epoll()
ep.register(timer, select.EPOLLIN | select.EPOLLET)
tfd.timerfd_settime(timer, tv, tfd.TFD_TIMER_ABSTIME)

while True:
    ep.poll()
    t = time.localtime()
    if 3 <= t.tm_hour < 4:
        digit = (t.tm_min*60+t.tm_sec)%10
        digits = 10*digit+digit
        setdigits(hh, digits, t.tm_sec%2*2)
        setdigits(mm, digits, t.tm_sec%2*2)
        setdigits(ss, digits, t.tm_sec%2*2)
    else:
        setdigits(hh, t.tm_hour, False)
        setdigits(mm, t.tm_min, t.tm_sec%2)
        setdigits(ss, t.tm_sec, t.tm_sec%2)
    read(timer, 8)
