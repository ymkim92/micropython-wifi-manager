import time

import network
from logger.console_logger import ConsoleLogger

from wifi_manager.webserver import WebServer

WIFI_CREDENTIALS = "wifi.dat"


class WifiManager:
    def __init__(self, logger: ConsoleLogger, ssid="WifiManager", password="wifimanager"):
        self.logger = logger
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_sta.active(True)
        self.wlan_ap = network.WLAN(network.AP_IF)

        if len(ssid) > 32:
            raise Exception("The SSID cannot be longer than 32 characters.")
        else:
            self.ap_ssid = ssid
        if len(password) < 8:
            raise Exception("The password cannot be less than 8 characters long.")
        else:
            self.ap_password = password

        self.ap_authmode = 3
        self.wlan_sta.disconnect()

    def read_credentials(self) -> dict:
        """return {ssid, password} for WiFi access point into self.profiles"""
        lines = []
        profiles = {}
        try:
            with open(WIFI_CREDENTIALS) as file:
                lines = file.readlines()
        except Exception as error:
            self.logger.error(error)
        for line in lines:
            ssid, password = line.strip().split(";")
            profiles[ssid] = password

        return profiles

    def connect(self, profiles: dict) -> bool:
        if self.wlan_sta.isconnected():
            return True
        for ssid, *_ in self.wlan_sta.scan():
            ssid = ssid.decode("utf-8")
            if ssid in profiles:
                password = profiles[ssid]
                if self.wifi_connect(ssid, password):
                    return True
        # assume it is close to the access point
        self.logger.debug("Could not connect to any WiFi network.")
        return False
        self.web_server()

    def disconnect(self):
        if self.wlan_sta.isconnected():
            self.wlan_sta.disconnect()

    def is_connected(self):
        return self.wlan_sta.isconnected()

    def get_address(self):
        return self.wlan_sta.ifconfig()

    def wifi_connect(self, ssid, password):
        print("Trying to connect to:", ssid)
        self.wlan_sta.connect(ssid, password)
        for _ in range(100):
            if self.wlan_sta.isconnected():
                self.logger.info("\nConnected! Network information:", self.wlan_sta.ifconfig())
                return True
            else:
                time.sleep_ms(100)
        self.logger.error("\nConnection failed!")
        self.wlan_sta.disconnect()
        return False

    def guard_is_connected(self, ctx, msg):
        """Guard to check if the WiFi is connected."""
        return self.wlan_sta.isconnected()

    def web_server(self):
        server = WebServer(self)
        server.run()
