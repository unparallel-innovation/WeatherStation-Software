# Unparallel Weather Station Software

The Unparallel Weather Station allows anyone to build their own low-cost weather station, using our custom open-source PCB. The software for the weather station is also open-source and can be used as is, or freely customized to meet your own needs and requirements. A model for printing a 3D case for your weather station is also provided.

The Unparallel Weather Station PCB simplifies the assembly of the weather station using low-cost hardware and a LoPy4 board. The LoPy4 board is equipped with several connectivity options (e.g. Sigfox, LoRa, Wi-Fi and Bluetooth). Currently, the weather station uses Sigfox and/or Wi-Fi to send the data to the cloud, however, the software can be extended to support other connectivity options.

The weather station uses an external sensor (AM2315) for reading temperature and relative humidity, a weather meter kit (SEN-15901) for wind speed, wind direction and precipitation. The weather station is powered from a Li-Ion battery that is charged with a photovoltaic panel which is also used to measure solar radiation. Due to the system’s low-power operation and solar energy harvesting features, it is energy autonomous and can be deployed in remote places.


#### Measured parameters:
*  Temperature (ºC)
*  Relative Humidity (%)
*  Rain (mm/h)
*  Wind Speed (km/h)
*  Wind Gust Speed (km/h)
*  Wind Direction (degrees)
*  Wind Gust Direction (degrees)
*  Solar Radiation (W/m2)
*  Battery Voltage (V)


#### Parts list:
*  [LoPy 4](https://pycom.io/product/lopy4/)
*  [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB)
*  [Unparallel WeatherStation Enclosure](https://github.com/unparallel-innovation/WeatherStation-Enclosure)
*  [Encased I2C Temperature/Humidity Sensor - AM2315](https://www.adafruit.com/product/1293)
*  [Weather Meter Kit - SEN-15901](https://www.sparkfun.com/products/15901)
*  [Li-Ion battery (3.65V - 8000mAh)](https://www.tme.eu/en/details/cl-18650-29e_1s3p/rechargeable-batteries/cellevia-batteries/)
*  [Solar Panel (2.5W - 116x160mm)](https://www.seeedstudio.com/2-5W-Solar-Panel-116X160.html)
*  [Sigfox Antenna Kit (868MHz)](https://pycom.io/product/lora-868mhz-915mhz-sigfox-antenna-kit/)



## Software Configuration

Use the **config.py** file to configure your weather station.  
You can change the reading and sending time intervals, network configuration (Wi-Fi, Sigfox and MQTT) and battery levels for low power operation.



## Related Repositories:
*  [Unparallel WeatherStation PCB](https://github.com/unparallel-innovation/WeatherStation-PCB)
*  [Unparallel WeatherStation Enclosure](https://github.com/unparallel-innovation/WeatherStation-Enclosure)
*  [Unparallel WeatherStation Software](https://github.com/unparallel-innovation/WeatherStation-Software)
*  [Unparallel WeatherStation Connector](https://github.com/unparallel-innovation/WeatherStation-Connector)


___

###### This work was done in the context of SmartAgriHubs Research Project, which has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 818182
