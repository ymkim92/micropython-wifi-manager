"""
FSM-based WiFi Manager (MicroPython)
"""

import logging
import network
import time

log = logging.getLogger("wifi")
log.setLevel(logging.INFO)


# Define Events
class Event:
    pass


class ConnectEvent(Event):
    pass


class ConnectedEvent(Event):
    pass


class ConnectFailedEvent(Event):
    pass


class ConfigReceivedEvent(Event):
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password


# FSM State
class State:
    def __init__(self, name, entry=None, exit=None):
        self.name = name
        self.entry = entry
        self.exit = exit

    def on_entry(self):
        if self.entry:
            self.entry()

    def on_exit(self):
        if self.exit:
            self.exit()


class WifiManagerFSM:
    def __init__(self, wifi_manager):
        self.state = State.INIT
        self.wifi_manager = wifi_manager

    def dispatch(self, event):
        new_state = self.handle_event(self.state, event)
        if new_state != self.state:
            self.state = new_state

    def handle_event(self, state, event):
        if state == State.INIT:
            if event == Event.ConnectEvent:
                if GuardHasSavedConfig(self.wifi_manager):
                    OnExitInit(self.wifi_manager)
                    OnActionConnectToSaved(self.wifi_manager, self.dispatch)
                    OnEntryConnecting(self.wifi_manager)
                    return State.CONNECTING
                else:
                    OnExitInit(self.wifi_manager)
                    OnActionStartAP(self.wifi_manager)
                    OnEntryAPMode(self.wifi_manager)
                    return State.AP_MODE
        # other transitions ...
        return state

    # Guards
    #
    def GuardHasSavedConfig(wifi_manager):
        return wifi_manager.has_saved_config()

    # Actions
    #
    def OnActionConnectToSaved(wifi_manager, fsm_dispatch):
        wifi_manager.connect_to_saved(
            on_success=lambda: fsm_dispatch(Event.ConnectedEvent),
            on_failure=lambda: fsm_dispatch(Event.ConnectFailedEvent),
        )

    def OnActionStartAP(wifi_manager):
        wifi_manager.start_ap_mode()

    def OnActionConnectWithNewConfig(wifi_manager, fsm_dispatch):
        wifi_manager.connect_to_new_config(
            on_success=lambda: fsm_dispatch(Event.ConnectedEvent),
            on_failure=lambda: fsm_dispatch(Event.ConnectFailedEvent),
        )


# FSM Core
class WiFiFSM:
    def __init__(self):
        self.states = {}
        self.transitions = {}
        self.state = None
        self.station = network.WLAN(network.STA_IF)
        self.config = {}

        self._init_states()
        self._set_state("INIT")

    def _init_states(self):
        self._add_state("INIT", self.OnEntryInit, self.OnExitInit)
        self._add_state("CONNECTING", self.OnEntryConnecting, self.OnExitConnecting)
        self._add_state("AP_MODE", self.OnEntryAPMode)
        self._add_state("RECONNECTING", self.OnEntryReconnecting)
        self._add_state("CONNECTED", self.OnEntryConnected)
        self._add_state("FAILED", self.OnEntryFailed)

    def _add_state(self, name, entry=None, exit=None):
        self.states[name] = State(name, entry, exit)

    def _set_state(self, name):
        if self.state:
            self.state.on_exit()
        self.state = self.states[name]
        log.info(f"Transitioned to state: {name}")
        self.state.on_entry()

    def handle_event(self, event):
        name = self.state.name

        if name == "INIT":
            if isinstance(event, ConnectEvent):
                if self.GuardHasSavedConfig():
                    self.OnActionConnectToSaved()
                    self._set_state("CONNECTING")
                else:
                    self.OnActionStartAP()
                    self._set_state("AP_MODE")

        elif name == "CONNECTING":
            if isinstance(event, ConnectedEvent):
                self.OnActionNotifyConnected()
                self._set_state("CONNECTED")
            elif isinstance(event, ConnectFailedEvent):
                self.OnActionStartAP()
                self._set_state("AP_MODE")

        elif name == "AP_MODE":
            if isinstance(event, ConfigReceivedEvent):
                self.OnActionConnectWithNewConfig(event.ssid, event.password)
                self._set_state("RECONNECTING")

        elif name == "RECONNECTING":
            if isinstance(event, ConnectedEvent):
                self.OnActionNotifyConnected()
                self._set_state("CONNECTED")
            elif isinstance(event, ConnectFailedEvent):
                self.OnActionLogError()
                self._set_state("FAILED")

    # Entry/Exit handlers
    def OnEntryInit(self):
        log.info("Entering INIT state")

    def OnExitInit(self):
        log.info("Exiting INIT state")

    def OnEntryConnecting(self):
        log.info("Trying to connect to saved Wi-Fi...")

    def OnExitConnecting(self):
        log.info("Exiting CONNECTING state")

    def OnEntryAPMode(self):
        log.info("Starting AP mode for configuration")
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid="SetupMe")

    def OnEntryReconnecting(self):
        log.info("Reconnecting with new configuration")

    def OnEntryConnected(self):
        log.info("Successfully connected to Wi-Fi")

    def OnEntryFailed(self):
        log.error("Failed to connect after configuration")

    # Guards
    def GuardHasSavedConfig(self):
        return bool(self.config.get("ssid") and self.config.get("password"))

    # Actions
    def OnActionConnectToSaved(self):
        self._connect(self.config["ssid"], self.config["password"])

    def OnActionStartAP(self):
        # Already done in OnEntryAPMode
        pass

    def OnActionConnectWithNewConfig(self, ssid, password):
        self.config = {"ssid": ssid, "password": password}
        self._connect(ssid, password)

    def OnActionNotifyConnected(self):
        log.info("Notify: Connected to Wi-Fi")

    def OnActionLogError(self):
        log.error("Notify: Failed to connect")

    def _connect(self, ssid, password):
        self.station.active(True)
        self.station.connect(ssid, password)

        for _ in range(10):
            if self.station.isconnected():
                self.handle_event(ConnectedEvent())
                return
            time.sleep(1)
        self.handle_event(ConnectFailedEvent())
