
import utime
from machine import Pin


class WindSpeed(object):

    def __init__(self, interrupt_pin, wind_dir):
        now = utime.ticks_ms()
        self.last_int_ms = now
        self.counter_start = now
        self.gust_counter_start = now
        self.count = 0
        self.gust_count = 0
        self.instant_wind_speed = 0
        self.gust_speed = 0
        self.wind_dir = wind_dir

        # Configure wind interrupt pin
        self.int_pin = Pin(interrupt_pin, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.int_pin.callback(Pin.IRQ_RISING, self.callback)
        self.last_pin_value = self.int_pin.value()
        self.interrupt_OK = True


    def callback(self, arg):
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.last_int_ms) > 10:
            self.count += 1
            self.gust_count += 1
            self.instant_wind_speed = 1/(utime.ticks_diff(now, self.last_int_ms)/1000)*2.4
            self.last_int_ms = now
            self.wind_dir.update()
            self.interrupt_OK = True


    def update(self):
        self.check_interrupt_state()
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.gust_counter_start) > 3000:
            time_passed = utime.ticks_diff(now, self.gust_counter_start)/1000
            wind_speed_kph = (self.gust_count/time_passed)*2.4

            if wind_speed_kph > self.gust_speed:
                self.gust_speed = wind_speed_kph
                self.wind_dir.read_gust_direction()

            self.gust_counter_start = now
            self.gust_count = 0
            self.wind_dir.clear_gust_direction()


    def check_interrupt_state(self):
        if self.count == 0:
            pin_value = self.int_pin.value()
            if pin_value and not self.last_pin_value:
                self.interrupt_OK = False
            self.last_pin_value = pin_value


    def is_interrupt_OK(self):
        return self.interrupt_OK


    def get_count(self):
        return self.count


    def get_instant_wind_speed_kph(self):
        return self.instant_wind_speed


    def get_gust_speed_kph(self):
        return self.gust_speed


    def get_wind_speed_avg_kph(self):
        time_passed = utime.ticks_diff(utime.ticks_ms(), self.counter_start)/1000
        wind_speed_kph = (self.count/time_passed)*2.4
        return wind_speed_kph


    def get_instant_wind_speed_mph(self):
        return self.kph_to_mph(self.get_instant_wind_speed_kph())


    def get_gust_speed_mph(self):
        return self.kph_to_mph(self.get_gust_speed_kph())


    def get_wind_speed_avg_mph(self):
        return self.kph_to_mph(self.get_wind_speed_avg_kph())


    def kph_to_mph(self, kph):
        return kph/1.6093445


    def clear(self):
        now = utime.ticks_ms()
        self.counter_start = now
        self.gust_counter_start = now
        self.count = 0
        self.gust_count = 0
        self.gust_speed = 0
