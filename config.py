################################################################################
################### UNPARALLEL Weather Station Configuration ###################
################################################################################


################################################################################
# Pinout
################################################################################
# P9:  I2C SDA              (output)
# P10: I2C SCL              (output)
# P11: BAT_STATUS           (input)
# P13: RAIN                 (input)
# P14: WSPD                 (input)
# P15: WDIR                 (input)
# P17: BAT_LVL              (input)
# P19: EN_PWR_SOLAR         (output)
# P20: EN_DIRECT_CHARGE     (output)
# P21: EN_FAST_CHARGE       (output)
# P22: DIS_PWR_SENS         (output)
# P23: LED_ON               (output)

SDA_PIN = 'P9'
SCL_PIN = 'P10'
RAIN_PIN = 'P13'
WIND_SPEED_PIN = 'P14'
WIND_DIR_PIN = 'P15'
BATT_LEVEL_PIN = 'P17'
EN_CHARGE = 'P19'
EN_DIRECT_CHARGE = 'P20'
EN_FAST_CHARGE = 'P21'
DIS_AM2315_PWR = 'P22'


################################################################################
# Time intervals
################################################################################
sensors_read_interval = 5000            # 5 seconds
radiation_read_interval = 2*60*1000     # 2 minutes
send_interval = 15*60*1000              # 15 minutes


################################################################################
# Networks
################################################################################
# send_to = ['sigfox', 'mqtt']    # Send to Sigfox and MQTT
send_to = ['sigfox']            # Only send to Sigfox
# send_to = ['mqtt']              # Only send to MQTT

# MQTT configuration
mqtt_device_id = 'WS-1'
mqtt_topic = 'unparallel-weatherstation/WS-1/'
mqtt_url = 'broker.hivemq.com'
mqtt_port = 1883
mqtt_username = ''
mqtt_password = ''

# Wifi configuration
# Allows configuration of multiple wifi networks
# wifi_list = [("SSID","password"), ("SSID2","password2"), ("SSID3","password3")]
wifi_list = [('your_wifi_SSID','your_wifi_password')]


################################################################################
# Battery Levels
################################################################################
# Enter deepsleep mode if battery is bellow this voltage
batt_deepsleep_V = 3.00

# After reset or exiting deepsleep only start the weather station
# if the battery is higher than this voltage
batt_start_min_V = 3.30

# Enable low power mode if battery is bellow this voltage
batt_low_power_V = 3.90

# Enable direct charge until battery reaches this voltage
batt_direct_charge_max_V = 4.00

# Charge with current limited to 100mA until battery reaches this voltage
batt_charge_max_V = 4.10

# Only enable direct charge to read radiation if battery is bellow this voltage
batt_radiation_direct_charge_max_V = 4.15
