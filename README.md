
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


# Unparallel Weather Station Software

<p align="center">
  <img src="https://user-images.githubusercontent.com/20951805/137321564-7b948da6-5f59-482f-b4c2-27412b858842.png" alt="Service Connector logo" max-height="250px"/>
</p>

The Unparallel Weather Station allows anyone to build their own low-cost weather station, using our custom open-source PCB. The software for the weather station is also open-source and can be used as is, or freely customized to meet your own needs and requirements. A model for printing a 3D case for your weather station is also provided.

The Unparallel Weather Station PCB simplifies the assembly of the weather station using low-cost hardware and a LoPy4 board. The LoPy4 board is equipped with several connectivity options (e.g. Sigfox, LoRa, Wi-Fi and Bluetooth). Currently, the weather station uses Sigfox and/or Wi-Fi to send the data to the cloud, however, the software can be extended to support other connectivity options.

The weather station uses an external sensor (AM2315) for reading temperature and relative humidity, a weather meter kit (SEN-15901) for wind speed, wind direction and precipitation. The weather station is powered from a Li-Ion battery that is charged with a photovoltaic panel which is also used to measure the approximate solar radiation. Due to the system’s low-power operation and solar energy harvesting features, it is energy autonomous and can be deployed in remote places.

For more information about the Unparallel Weather Station check the [Related Repositories](#related-repositories) and [Iot-Catalogue](https://www.iot-catalogue.com/search/component/60704f126dc1142086fa54f6).


#### Measured parameters:
*  Temperature (ºC)
*  Relative Humidity (%)
*  Rainfall (mm/h)
*  Wind Speed (km/h)
*  Wind Gust Speed (km/h)
*  Wind Direction (degrees)
*  Wind Gust Direction (degrees)
*  Solar Radiation (W/m2)
*  Battery Voltage (V)

##### Note: The measured solar radiation is an approximation and can vary depending on the solar panel.


#### Components:
*  [LoPy 4](https://pycom.io/product/lopy4/)
*  [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB)
*  [Unparallel WeatherStation Enclosure](https://github.com/unparallel-innovation/WeatherStation-Enclosure)
*  [Encased I2C Temperature/Humidity Sensor - AM2315](https://www.adafruit.com/product/1293)
*  [Weather Meter Kit - SEN-15901](https://www.sparkfun.com/products/15901)
*  [Li-Ion battery (3.65V - 8000mAh)](https://www.tme.eu/en/details/cl-18650-29e_1s3p/rechargeable-batteries/cellevia-batteries/)
*  [Solar Panel (2.5W - 116x160mm)](https://www.seeedstudio.com/2-5W-Solar-Panel-116X160.html)
*  [Sigfox Antenna Kit (868MHz)](https://pycom.io/product/lora-868mhz-915mhz-sigfox-antenna-kit/)
*  [Expansion Board 3.0](https://pycom.io/product/expansion-board-3-0/)



## Quick Start
To upload software to your device follow the Pymakr Plugin install guide for [Atom](https://docs.pycom.io/gettingstarted/software/atom/) or [VS Code](https://docs.pycom.io/gettingstarted/software/vscode/).

Download or clone this repo and open it with Atom or VS Code.

Insert your LoPy4 into the expansion board and connect the USB cable.

After having successfully connected your LoPy4 board to Atom or VS Code, click the upload button to program you LoPy4 with this weather station software.

When the upload finishes the LoPy4 should reset and run the weather station software. Disconnect the USB cable, remove the LoPy4 from the expansion board and insert it into the [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB).

For more information check the complete instructions on [pycom getting started](https://docs.pycom.io/gettingstarted/).



## Software Configuration
The weather station can be used with Sigfox with the default settings, without any modification to the configuration. If you wish to use Wi-FI and MQTT you have to edit [config.py](config.py) to configure your network and MQTT broker. In the configuration file there are options to change the reading and sending time intervals, network configuration (Wi-Fi, Sigfox and MQTT) and battery levels for low power operation.

After changing the configuration the software needs to be re-upload to the weather station to update the configuration.



### Time intervals
#### Sensors read interval
The external sensor AM2315, used for reading temperature and relative humidity, and an internal ADC, used for reading battery level, are read periodically and provide an averaged value for the whole "send_interval" period. The sensors reading period is configured with the following variable.
```
sensors_read_interval = 5000            # 5 seconds
```

#### Radiation read interval
Reading the radiation requires the weather station to pull all the energy available from the solar panel to get a reading of the available solar radiation. The [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB) has a direct charging circuit that allows the battery to pull all the current the solar panel can provide. This circuit must be enabled before reading solar radiation. In conditions where the battery is fully charged, this circuit can overcharge the battery if the radiation is read too frequently. Thus the solar radiation is read with a longer time interval to ensure the weather station does not overcharge while reading solar radiation.
```
radiation_read_interval = 2*60*1000     # 2 minutes
```

#### Send interval
Sigfox only allows for 140 messages per day for each device. This corresponds to sending one message every 10 minutes and 18 seconds.
Due to this limitation, the software is configured to send every 15 minutes, but it can be adjusted with "send_interval". If MQTT is used instead of Sigfox the send_interval can be much smaller.
```
send_interval = 15*60*1000              # 15 minutes
```



### Networks
Configure if data should be sent to Sigfox and/or MQTT.

To use MQTT the weather station needs to be in reach of a known and preconfigured Wi-Fi network.

Send to Sigfox and MQTT:
```
send_to = ['sigfox', 'mqtt']
```
Only send to Sigfox:
```
send_to = ['sigfox']
```
Only send to MQTT:
```
send_to = ['mqtt']
```

#### MQTT configuration
Replace the default values with your MQTT Broker configuration.  
Please note that the MQTT topic must be terminated with a slash '/' symbol.
```
mqtt_device_id = 'Your-WeatherStation-name'
mqtt_topic = 'your-mqtt-topic/'
mqtt_url = 'broker.example.com'
mqtt_port = 1883
mqtt_username = 'broker-user'
mqtt_password = 'broker-password'
```
Example using the [public HiveMQ MQTT broker](https://www.hivemq.com/public-mqtt-broker/):
```
mqtt_device_id = 'WS-1'
mqtt_topic = 'unparallel-weatherstation/WS-1/'
mqtt_url = 'broker.hivemq.com'
mqtt_port = 1883
mqtt_username = ''
mqtt_password = ''
```

#### Wifi configuration
A Wi-Fi network needs to be defined to allow using MQTT.  
This can be ignored if MQTT is not being used.
```
wifi_list = [('your_wifi_SSID','your_wifi_password')]
```
It also allows the definition of multiple wifi networks. The order of the networks does not matter. The weather station will scan for networks and connect to the first known network that it finds.
```
wifi_list = [("SSID","password"), ("SSID2","password2"), ("SSID3","password3")]
```



### Battery Levels
#### Weather Station Low power operation
The weather station software uses [pycom sleep modes](https://docs.pycom.io/tutorials/basic/sleep/) for low power operation.

Pycom **deep sleep** is used when the battery is discharged to reduce power consumption to a minimum and allow the battery to charge using the solar panel. In this mode the weather station will not read the sensors or send any data to avoid over-discharging the battery.

Enter deep sleep mode if battery is bellow this voltage.
```
batt_deepsleep_V = 3.00
```
After reset or exiting deep sleep the weather station will only start if the battery is higher than this voltage. If the battery is bellow this voltage the weather station will stay in deep sleep until the battery is charged above this threshold.
```
batt_start_min_V = 3.30
```
Low power mode uses pycom **light sleep** to reduce power consumption while still maintaining full operation. Enable low power mode if battery is bellow this voltage.
```
batt_low_power_V = 3.90
```

#### Charge controller
The [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB) has a direct charging circuit that allows charging the battery without limiting the current and maximize the energy harvested from the solar panel. This circuit also enables the weather station to use the solar panel to measure solar radiation.

Enable direct charge until battery reaches this voltage.
```
batt_direct_charge_max_V = 4.00
```
Charge with current limited to 100mA until battery reaches this voltage.
```
batt_charge_max_V = 4.10
```
Only enable direct charge to read radiation if battery is bellow this voltage. This is to protect the battery from over-charging and show not be increased.

**Increasing this value may lead to permanent damage to the battery and pose a fire risk!**
```
batt_radiation_direct_charge_max_V = 4.15
```

<br>

After changing the configuration in [config.py](config.py) the sotware needs to be re-upload to the weather station to update the configuration.



## Related Repositories:
*  [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB)
*  [Unparallel WeatherStation Enclosure](https://github.com/unparallel-innovation/WeatherStation-Enclosure)
*  [Unparallel WeatherStation Documentation](https://github.com/unparallel-innovation/WeatherStation-Documentation)
*  [Unparallel WeatherStation Connector](https://github.com/unparallel-innovation/WeatherStation-Connector)


## Getting Support
If you'd like to report a bug or a missing feature, please use [GitHub issue tracker](https://github.com/unparallel-innovation/WeatherStation-Software/issues).


## License
This software is free and is distributed under [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0).

___

###### This work was done in the context of SmartAgriHubs Research Project, which has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 818182
