
from machine import ADC


class WindDirection(object):

    def __init__(self, wind_dir_pin):
        self.direction_counter = [0] * 16
        self.gust_direction_counter = [0] * 16
        self.gust_dir = 0

        # Configure wind direction adc
        adc = ADC()
        self.wind_direction_adc = adc.channel(pin=wind_dir_pin,attn=adc.ATTN_11DB)


    def update(self):
        idx = self.read_wind_direction_adc()
        if idx is not None and (0 <= idx <= 15):
            self.direction_counter[idx] += 1
            self.gust_direction_counter[idx] += 1


    def read_wind_direction_adc(self):
        adc = self.wind_direction_adc.voltage()
        if ( 1100 <= adc <= 1230 ): return 5
        if ( 1231 <= adc <= 1289 ): return 3
        if ( 1290 <= adc <= 1399 ): return 4
        if ( 1400 <= adc <= 1499 ): return 7
        if ( 1500 <= adc <= 1699 ): return 6
        if ( 1700 <= adc <= 1799 ): return 9
        if ( 1800 <= adc <= 2049 ): return 8
        if ( 2050 <= adc <= 2200 ): return 1
        if ( 2201 <= adc <= 2449 ): return 2
        if ( 2450 <= adc <= 2599 ): return 11
        if ( 2600 <= adc <= 2699 ): return 10
        if ( 2700 <= adc <= 2829 ): return 15
        if ( 2830 <= adc <= 2930 ): return 0
        if ( 2931 <= adc <= 2999 ): return 13
        if ( 3000 <= adc <= 3099 ): return 14
        if ( 3100 <= adc <= 3300 ): return 12
        print("Unsupported wind direction! adc:", adc)
        return None


    def read_gust_direction(self):
        max_value = max(self.gust_direction_counter)
        max_index = self.gust_direction_counter.index(max_value)
        self.gust_dir = max_index * 22.5


    def get_wind_direction(self):
        max_value = max(self.direction_counter)
        max_index = self.direction_counter.index(max_value)
        wind_dir = max_index * 22.5
        return wind_dir


    def get_gust_direction(self):
        return self.gust_dir


    def clear(self):
        for i in range(len(self.direction_counter)):
            self.direction_counter[i] = 0
        for i in range(len(self.gust_direction_counter)):
            self.gust_direction_counter[i] = 0


    def clear_gust_direction(self):
        for i in range(len(self.gust_direction_counter)):
            self.gust_direction_counter[i] = 0
