
import sys
import utime
import machine
import socket
import ubinascii
import ustruct

from network import Sigfox
from network import WLAN
from mqtt import MQTTClient

import config


def connect_wifi(wlan):
    print("Scanning wifi networks...")
    try:
        nets = wlan.scan()

        for net in nets:
            for wifi in config.wifi_list:
                if net.ssid == wifi[0]:
                    print("Connecting to", net.ssid, "...")
                    wlan.connect(ssid=net.ssid, auth=(net.sec, wifi[1]), timeout=5000)
                    while not wlan.isconnected():
                        machine.idle()
                    print("Wifi connected! IP:", wlan.ifconfig()[0])
                    return
        else:
            print("No known wifi network found!")
    except Exception as e:
        print("Error scanning wifi:", e)
        sys.print_exception(e)



def init_sigfox():
    # Init Sigfox for RCZ1 (Europe)
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
    # Create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
    # Make the socket blocking
    s.setblocking(True)
    # Configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    print("Sigfox ID:", ubinascii.hexlify(sigfox.id()))
    print("Sigfox MAC:", ubinascii.hexlify(sigfox.mac()))
    print("Sigfox PAC:", ubinascii.hexlify(sigfox.pac()))
    return s



def send_to_sigfox(sigfox, temp_C, humi_pct, rain_count, wind_kph, gust_kph, wind_deg, gust_deg, radi_wpm2, batt_V):
    try:
        winddir_gustdir = int(wind_deg/22.5) << 4 | int(gust_deg/22.5)

        msg = ustruct.pack('h', int(temp_C*100))
        msg += ustruct.pack('B', int(humi_pct*2))
        msg += ustruct.pack('B', int(rain_count))
        msg += ustruct.pack('H', int(wind_kph*100))
        msg += ustruct.pack('H', int(gust_kph*100))
        msg += ustruct.pack('B', int(winddir_gustdir))
        msg += ustruct.pack('H', int(radi_wpm2*10))
        msg += ustruct.pack('B', int((batt_V-2.5)*100))

        print("Sigfox msg:", ubinascii.hexlify(msg))
        sigfox.send(msg)

        print("Values sent to Sigfox.")
    except Exception as e:
        print("Failed to send to Sigfox!", e)
        sys.print_exception(e)



def send_to_mqtt(wlan, temp_C, humi_pct, rain_mmh, wind_kph, gust_kph, wind_deg, gust_deg, radi_wpm2, batt_V):
    if not wlan.isconnected():
        wlan = WLAN(mode=WLAN.STA)
        connect_wifi(wlan)

    if wlan.isconnected():
        try:
            clientMQTT = MQTTClient(config.mqtt_device_id, config.mqtt_url, port=config.mqtt_port, user=config.mqtt_username, password=config.mqtt_password, keepalive=5000)
            clientMQTT.connect()
            clientMQTT.publish(config.mqtt_topic+"ticks_ms", str(utime.ticks_ms()))
            clientMQTT.publish(config.mqtt_topic+"temperature", str(temp_C))
            clientMQTT.publish(config.mqtt_topic+"humidity", str(humi_pct))
            clientMQTT.publish(config.mqtt_topic+"rain", str(rain_mmh))
            clientMQTT.publish(config.mqtt_topic+"windSpeed", str(wind_kph))
            clientMQTT.publish(config.mqtt_topic+"gustSpeed", str(gust_kph))
            clientMQTT.publish(config.mqtt_topic+"windDir", str(wind_deg))
            clientMQTT.publish(config.mqtt_topic+"gustDir", str(gust_deg))
            clientMQTT.publish(config.mqtt_topic+"radiation", str(radi_wpm2))
            clientMQTT.publish(config.mqtt_topic+"batteryVolt", str(batt_V))
            utime.sleep_ms(100)  # Wait for MQTT to finish publishing
            print("Values sent to MQTT.")
            clientMQTT.disconnect()
        except Exception as e:
            print("Failed to send to MQTT:", e)
            sys.print_exception(e)

        wlan.disconnect()
