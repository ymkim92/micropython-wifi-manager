"""FSM Manager for WiFi Manager."""

from async_fsm.fsm_async import AsyncFSM
from logger.console_logger import ConsoleLogger, LogLevel

from wifi_manager.fsm_message import (
    EventConfigReceived,
    EventConnected,
    EventConnectFailed,
    EventConnectRequest,
)
from wifi_manager.fsm_state import (
    ApMode,
    Connected,
    Connecting,
    Failed,
    Init,
    Reconnecting,
)
from wifi_manager.wifi_manager import WifiManager


class WifiFsmManager:
    def __init__(self, wifi_manager: WifiManager):
        # Define states
        init_state = Init("Init")
        connecting_state = Connecting("Connecting")
        connected_state = Connected("Connected")
        ap_mode_state = ApMode("ApMode")
        reconnecting_state = Reconnecting("Reconnecting")
        failed_state = Failed("Failed")

        self.fsm = AsyncFSM(init_state)

        # Add states to FSM
        self.fsm.add_state(init_state)
        self.fsm.add_state(connecting_state)
        self.fsm.add_state(connected_state)
        self.fsm.add_state(ap_mode_state)
        self.fsm.add_state(reconnecting_state)
        self.fsm.add_state(failed_state)

        # Define transitions
        fsm.add_transition(init_state, EventConnectRequest, connecting_state)
        fsm.add_transition(init_state, EventConnectRequest, connecting_state)
        fsm.add_transition(connecting_state, EventConnected, connected_state)
        fsm.add_transition(connecting_state, EventConnectFailed, failed_state)
        fsm.add_transition(connected_state, EventConfigReceived, ap_mode_state)
        fsm.add_transition(ap_mode_state, EventConnectRequest, reconnecting_state)

        ctx = {"logger": ConsoleLogger(LogLevel.INFO)}
        fsm.start(ctx)

        return fsm
