
import uos
import sys
import utime
import pycom
import machine
from machine import I2C, Pin
from network import WLAN

from sensors.temperature import Temperature
from sensors.humidity import Humidity
from sensors.rain import Rain
from sensors.wind_speed import WindSpeed
from sensors.wind_direction import WindDirection
from sensors.radiation import Radiation
from sensors.battery import Battery

import network_utils
import config



def check_battery(battery, radiation):
    battery_V = battery.get_instant_V()

    if battery_V < config.batt_deepsleep_V:
        print("Low battery level:", battery_V)
        print("Entering deep sleep.")
        machine.deepsleep(600000)

    # If there is no sun disable charge and enable low power mode
    if radiation.get_voltage() < (battery_V - 1):
        battery.disable_direct_charge()
        battery.disable_charge()
        battery.enable_low_power()
    else:
        if battery_V > config.batt_direct_charge_max_V:
            battery.disable_direct_charge()

        if battery_V > config.batt_charge_max_V:
            battery.disable_charge()
            battery.disable_low_power()

        if battery_V < config.batt_low_power_V:
            battery.enable_low_power()



# Sometimes the LoPy interrupts stop working
# Reset the device as a workaround
def check_stuck_interrupts(wind_speed):
    if not wind_speed.is_interrupt_OK():
        print("Interrupt error! Restarting WeatherStation...")
        utime.sleep(1)
        machine.reset()



# Sometimes the AM2315 sensor blocks and needs to be powered off to start working again
# Remove the sensor power and reset the device
def reset_AM2315(i2c, am2315_pwr_pin):
    print("AM2315 error! Restarting WeatherStation...")
    i2c.deinit()
    sda_pin = Pin(config.SDA_PIN, mode=Pin.OUT)
    scl_pin = Pin(config.SCL_PIN, mode=Pin.OUT)
    am2315_pwr_pin.value(1)
    sda_pin.value(0)
    scl_pin.value(0)
    utime.sleep(5)
    machine.reset()



def read_sensors(temperature, humidity, battery):
    battery.update()
    if not temperature.update():
        return False
    if not humidity.update():
        return False
    return True



def read_radiation(radiation, battery):
    # Only measure radiation if solar panel voltage is higher than battery voltage
    if radiation.get_voltage() > battery.get_instant_V():
        if not battery.is_charge_enabled() or not battery.is_direct_charge_enabled():
            if battery.get_instant_V() < config.batt_radiation_direct_charge_max_V:
                battery.enable_charge()
                battery.enable_direct_charge()
                utime.sleep(2)

        # Only measure radiation if direct charge is enabled
        if battery.is_charge_enabled() and battery.is_direct_charge_enabled():
            radiation.update()

    else:
        radiation.update(0)

    check_battery(battery, radiation)



def send_values(sigfox, wlan, temperature, humidity, rain, wind_speed, wind_dir, radiation, battery, first_send_after_reset):
    temp_C = temperature.get_avg_C()
    humi_pct = humidity.get_avg()
    rain_mmh = rain.get_mm_per_hour()
    rain_count = rain.get_count_1hour()
    wind_kph = wind_speed.get_wind_speed_avg_kph()
    gust_kph = wind_speed.get_gust_speed_kph()
    wind_deg = wind_dir.get_wind_direction()
    gust_deg = wind_dir.get_gust_direction()
    radi_wpm2 = radiation.get_avg_Wpm2()
    batt_V = battery.get_avg_V()

    print('--------------------------------')
    print("ticks_ms: \t", utime.ticks_ms())
    print("Temperature:\t", temp_C)
    print("Humidity:\t", humi_pct)
    print("Rain:\t\t", rain_mmh)
    print("Rain Count:\t", rain_count)
    print("Wind Speed:\t", wind_kph)
    print("Gust Speed:\t", gust_kph)
    print("Wind Dir:\t", wind_deg)
    print("Gust Dir:\t", gust_deg)
    print("Radiation:\t", radi_wpm2)
    print("Battery Volt: \t", batt_V)

    # Use battery level as a reset indicator
    if first_send_after_reset:
        batt_V = 5.0

    if 'sigfox' in config.send_to:
        network_utils.send_to_sigfox(sigfox, temp_C, humi_pct, rain_count, wind_kph, gust_kph, wind_deg, gust_deg, radi_wpm2, batt_V)

    if 'mqtt' in config.send_to:
        network_utils.send_to_mqtt(wlan, temp_C, humi_pct, rain_mmh, wind_kph, gust_kph, wind_deg, gust_deg, radi_wpm2, batt_V)

    temperature.clear()
    humidity.clear()
    wind_speed.clear()
    wind_dir.clear()
    radiation.clear()
    battery.clear()



def main():
    print("\nInitializing Weather Station...")

    print("System info:")
    for item in str(uos.uname()).replace('(',' ').replace(')','').split(','):
        print(item)

    pycom.pybytes_on_boot(False)
    pycom.smart_config_on_boot(False)
    pycom.lte_modem_en_on_boot(False)
    pycom.wifi_on_boot(False)
    pycom.heartbeat_on_boot(False)
    pycom.heartbeat(False)

    battery = Battery(config.BATT_LEVEL_PIN, config.EN_CHARGE, config.EN_DIRECT_CHARGE, config.EN_FAST_CHARGE)
    battery_V = battery.get_instant_V()

    if battery_V < config.batt_start_min_V:
        print("Low battery level:", battery_V)
        print("Entering deep sleep.")
        machine.deepsleep(600000)

    wdt = machine.WDT(timeout=20000)

    i2c = I2C(0, I2C.MASTER)
    i2c.init(I2C.MASTER, baudrate=100000)
    am2315_pwr_pin = Pin(config.DIS_AM2315_PWR, mode=Pin.OUT)
    am2315_pwr_pin.value(0)
    temperature = Temperature(i2c)
    humidity = Humidity(i2c)
    radiation = Radiation(i2c)

    rain = Rain(config.RAIN_PIN)
    wind_dir = WindDirection(config.WIND_DIR_PIN)
    wind_speed = WindSpeed(config.WIND_SPEED_PIN, wind_dir)
    machine.pin_sleep_wakeup([config.RAIN_PIN, config.WIND_SPEED_PIN], machine.WAKEUP_ANY_HIGH, enable_pull=True)

    sigfox = network_utils.init_sigfox()
    wlan = WLAN(mode=WLAN.STA)

    now = utime.ticks_ms()
    now = now - (now % 1000)
    last_send_values = now
    last_read_sensors = now
    last_read_radiation = now
    first_send_after_reset = True

    print("Weather Station started!")

    while True:
        try:
            sleep_time = 1000 - (utime.ticks_ms() % 1000)

            if battery.is_low_power_enabled():
                machine.sleep(sleep_time, False)
            else:
                utime.sleep_ms(sleep_time)

            wdt.feed()

            check_battery(battery, radiation)

            rain.update()
            wind_speed.update()

            now = utime.ticks_ms()

            if utime.ticks_diff(now, last_read_sensors) >= config.sensors_read_interval:
                last_read_sensors = utime.ticks_add(last_read_sensors, config.sensors_read_interval)
                check_stuck_interrupts(wind_speed)
                if not read_sensors(temperature, humidity, battery):
                    reset_AM2315(i2c, am2315_pwr_pin)

            if utime.ticks_diff(now, last_read_radiation) >= config.radiation_read_interval:
                last_read_radiation = utime.ticks_add(last_read_radiation, config.radiation_read_interval)
                read_radiation(radiation, battery)

            if utime.ticks_diff(now, last_send_values) >= config.send_interval:
                last_send_values = utime.ticks_add(last_send_values, config.send_interval)
                send_values(sigfox, wlan, temperature, humidity, rain, wind_speed, wind_dir, radiation, battery, first_send_after_reset)
                first_send_after_reset = False

        except Exception as e:
            print("Error! -", e)
            sys.print_exception(e)



if __name__ == "__main__":
    main()
