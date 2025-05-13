# network_utils.py
import network
import time
from config import SSID, PASSWORD

def connect_wifi(ssid=SSID, password=PASSWORD):
    """
    This Python function connects to a WiFi network using the provided SSID and password.
    
    :param ssid: Name of the WiFi network you want to connect to
    :param password: password to connect to wifi
    :return:  IP address of the device
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to WiFi - IP info:", wlan.ifconfig())
    return wlan.ifconfig()[0]
