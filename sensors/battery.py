
from machine import ADC, Pin


class Battery(object):

    def __init__(self, adc_pin, charge_enable_pin, direct_charge_enable_pin, fast_charge_enable_pin):
        self.sum = 0
        self.count = 0
        self.last_voltage = 0
        self.low_power_enable = True

        # Configure battery voltage ADC
        adc = ADC()
        self.battery_V_adc = adc.channel(pin=adc_pin,attn=adc.ATTN_11DB)

        # Configure battery charger control Pins
        self.charge_enable = Pin(charge_enable_pin, Pin.OUT)
        self.direct_charge_enable = Pin(direct_charge_enable_pin, Pin.OUT)
        self.fast_charge_enable = Pin(fast_charge_enable_pin, Pin.OUT)

        self.enable_charge()
        self.disable_direct_charge()
        self.disable_fast_charge()



    def update(self):
        vbatlevel = self.get_instant_V()
        self.last_voltage = vbatlevel
        self.sum += float(vbatlevel)
        self.count += 1


    def get_instant_V(self):
        vbatlevel = ((200+499)/(200))*self.battery_V_adc.voltage()
        return round(((vbatlevel/1000)*0.97),2)


    def get_count(self):
        return self.count


    def get_last_V(self):
        return self.last_voltage


    def get_avg_V(self):
        if self.count > 0:
            return self.sum / self.count


    def clear(self):
        self.sum = 0
        self.count = 0
        self.last_voltage = 0


    def is_low_power_enabled(self):
        return self.low_power_enable

    def enable_low_power(self):
        self.low_power_enable = True

    def disable_low_power(self):
        self.low_power_enable = False


    def is_charge_enabled(self):
        return self.charge_enable.value()

    def enable_charge(self):
        self.charge_enable.value(1)

    def disable_charge(self):
        self.charge_enable.value(0)


    def is_direct_charge_enabled(self):
        return self.direct_charge_enable.value()

    def enable_direct_charge(self):
        self.direct_charge_enable.value(1)

    def disable_direct_charge(self):
        self.direct_charge_enable.value(0)


    def is_fast_charge_enabled(self):
        return self.fast_charge_enable.value()

    def enable_fast_charge(self):
        self.fast_charge_enable.value(1)

    def disable_fast_charge(self):
        self.fast_charge_enable.value(0)
