import network
from config import config


def run():
    SERVER_IP = '192.168.0.1'
    SERVER_SUBNET = '255.255.255.0'
    wifi = network.WLAN(network.AP_IF)
    wifi.active(True)
    wifi.ifconfig((SERVER_IP, SERVER_SUBNET, SERVER_IP, SERVER_IP))
    wifi.config(essid=config["ssid"], authmode=network.AUTH_OPEN)
