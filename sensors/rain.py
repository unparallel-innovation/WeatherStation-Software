
import utime
from machine import Pin


class Rain(object):

    def __init__(self, interrupt_pin):
        now = utime.ticks_ms()
        self.last_int_ms = now
        self.counter_start = now
        self.accumulator_1hour = [0] * 60
        self.idx = 0

        # Configure rain interrupt pin
        self.int_pin = Pin(interrupt_pin, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.int_pin.callback(Pin.IRQ_RISING, self.callback)


    def callback(self, arg):
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.last_int_ms) > 100:
            self.accumulator_1hour[self.idx] += 1
            self.last_int_ms = now


    def update(self):
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.counter_start) > 60000:
            self.idx = (self.idx + 1) % 60
            self.accumulator_1hour[self.idx] = 0
            self.counter_start = now


    def get_count(self):
        return self.accumulator_1hour[self.idx]


    def get_count_1hour(self):
        count = 0
        for c in self.accumulator_1hour:
            count += c
        return count


    def get_mm_per_hour(self):
        return self.get_count_1hour()*0.2794


    def get_inches_per_hour(self):
        return self.get_count_1hour()*0.011


    def clear(self):
        self.counter_start = utime.ticks_ms()
        self.idx = 0

        for i in range(len(self.accumulator_1hour)):
            self.accumulator_1hour[i] = 0
