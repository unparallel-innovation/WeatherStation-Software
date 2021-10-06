
import utime
from adafruit_am2320 import AM2320


class Humidity(object):

    def __init__(self, i2c):
        self.am2315 = AM2320(i2c)
        self.sum = 0
        self.count = 0
        self.last_humidity = 0


    def update(self):
        retries = 0
        while retries < 10:
            try:
                humi = self.am2315.relative_humidity
                if humi:
                    self.last_humidity = humi
                    self.sum += float(humi)
                    self.count += 1
                    return True
            except Exception as e:
                # print("Error reading humidity from AM2315!", retries, e)
                utime.sleep_ms(10)
                retries += 1
        print("Error reading humidity from AM2315!")
        return False


    def get_count(self):
        return self.count


    def get_last(self):
        return self.last_humidity


    def get_avg(self):
        if self.count > 0:
            return self.sum / self.count
        else:
            return 0


    def clear(self):
        self.sum = 0
        self.count = 0
        self.last_humidity = 0
