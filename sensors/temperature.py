
import utime
from adafruit_am2320 import AM2320


class Temperature(object):

    def __init__(self, i2c):
        self.am2315 = AM2320(i2c)
        self.sum = 0
        self.count = 0
        self.last_temperature = 0


    def update(self):
        retries = 0
        while retries < 10:
            try:
                temp = self.am2315.temperature
                if temp:
                    self.last_temperature = temp
                    self.sum += float(temp)
                    self.count += 1
                    return True
            except Exception as e:
                # print("Error reading temperature from AM2315!", retries, e)
                utime.sleep_ms(10)
                retries += 1
        print("Error reading temperature from AM2315!")
        return False


    def get_count(self):
        return self.count


    def get_last_C(self):
        return self.last_temperature


    def get_last_F(self):
        return self.convert_C_to_F(self.get_last_C())


    def get_avg_C(self):
        if self.count > 0:
            return self.sum / self.count
        else:
            return 0


    def get_avg_F(self):
        return self.convert_C_to_F(self.get_avg_C())


    def convert_C_to_F(self, temp_C):
        return ((temp_C*1.8)+32)


    def clear(self):
        self.sum = 0
        self.count = 0
        self.last_temperature = 0
