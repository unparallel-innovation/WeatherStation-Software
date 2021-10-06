
from ina219 import INA219


class Radiation(object):

    def __init__(self, i2c):
        self.sum = 0
        self.count = 0
        self.last_radiation = 0

        try:
            SHUNT_OHMS = 0.2
            self.ina = INA219(SHUNT_OHMS, i2c)
            self.ina.configure()
        except:
            self.ina = None
            print("Error connecting to sensor INA219!")


    def update(self, radi=None):
        try:
            if radi is None:
                radi = self.ina.current()*1000/450
            if radi is not None:
                if radi < 0:
                    radi = 0
                self.last_radiation = radi
                self.sum += float(radi)
                self.count += 1
        except Exception as e:
            print("Error reading radiation from INA219!", e)


    def get_voltage(self):
        return self.ina.voltage()


    def get_count(self):
        return self.count


    def get_last_Wpm2(self):
        return self.last_radiation


    def get_avg_Wpm2(self):
        if self.count > 0:
            return self.sum / self.count
        else:
            return 0


    def clear(self):
        self.sum = 0
        self.count = 0
        self.last_radiation = 0
