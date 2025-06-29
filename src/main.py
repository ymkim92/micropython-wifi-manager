import utime

from wifi_manager.fsm_manager import create_fsm
from wifi_manager.wifi_manager import WifiManager


# Example of usage
def main():
    wm = WifiManager()
    fsm = create_fsm(wm)
    wm.connect()

    while True:
        if wm.is_connected():
            print("Connected!")
        else:
            print("Disconnected!")
        utime.sleep(10)


if __name__ == "__main__":
    main()
