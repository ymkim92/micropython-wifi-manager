"""FSM actions for WiFi Manager."""

from typing import Any, Dict
from wifi_manager.wifi_manager import WifiManager
from logger.console_logger import ConsoleLogger, LogLevel
from wifi_manager.fsm_utils import get_required


class WifiFsmActions:
    def on_action_connect_to_saved(self, ctx, message):
        """Action to connect to saved WiFi networks."""
        # Implement connection logic here
        # For example, call wifi_manager.connect_to_saved_networks()

    def on_action_start_ap_mode(self, ctx, message):
        """Action to start AP mode."""
        # Implement AP mode logic here
        # For example, call wifi_manager.start_ap_mode()
