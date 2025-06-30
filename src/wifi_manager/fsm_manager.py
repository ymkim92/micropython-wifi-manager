"""FSM Manager for WiFi Manager."""

from async_fsm.fsm_async import AsyncFSM
from logger.console_logger import ConsoleLogger, LogLevel

from wifi_manager.fsm_message import (
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
    def __init__(self, wifi_manager: WifiManager, logger: ConsoleLogger):
        self.wifi_manager = wifi_manager
        self.logger = logger

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
        self.fsm.add_transition(
            init_state,
            EventConnectRequest,
            connecting_state,
            guard=self.guard_has_saved_config,
            action=self.on_action_connect_to_saved,
        )
        self.fsm.add_transition(
            init_state,
            EventConnectRequest,
            connecting_state,
            guard=self.guard_has_saved_config,
            action=self.on_action_start_ap_mode,
        )
        self.fsm.add_transition(init_state, EventConnectRequest, ap_mode_state)

        ctx = {}
        self.fsm.start(ctx)

    # Actions
    #
    def on_action_connect_to_saved(self, ctx, message):
        """Action to connect to saved WiFi networks."""
        # Implement connection logic here
        # For example, call wifi_manager.connect_to_saved_networks()

    def on_action_start_ap_mode(self, ctx, message):
        """Action to start AP mode."""
        # Implement AP mode logic here
        # For example, call wifi_manager.start_ap_mode()
