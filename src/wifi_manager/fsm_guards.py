"""FSM guards for WiFi Manager."""

from typing import Any, Dict
from wifi_manager.wifi_manager import WifiManager
from logger.console_logger import ConsoleLogger, LogLevel
from wifi_manager.fsm_utils import get_required


class WifiFsmGuards:
    """FSM guards for WiFi Manager."""

    def __init__(self, ctx: Dict[str, Any]):
        """Initialize the guards with context.

        Args:
            ctx: FSM context containing wifi_manager and logger
        """
        self.logger: ConsoleLogger = get_required(ctx, "logger")
        self.wifi_manager: WifiManager = get_required(ctx, "wifi_manager")

    def guard_has_saved_config(self, ctx: Dict[str, Any], message: Any) -> bool:
        """Guard to check if there are saved WiFi configurations."""
        profiles = self.wifi_manager.read_credentials()
        return bool(profiles)
