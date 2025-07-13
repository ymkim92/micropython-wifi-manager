"""FSM guards for WiFi Manager."""

from typing import Any

from wifi_manager.fsm_context import WifiFsmContext


class WifiFsmGuards:
    """FSM guards for WiFi Manager."""

    def guard_has_saved_config(self, ctx: WifiFsmContext, message: Any) -> bool:
        """Guard to check if there are saved WiFi configurations."""
        profiles = ctx.wifi_manager.read_credentials()
        return bool(profiles)

    def guard_has_no_saved_config(self, ctx: WifiFsmContext, message: Any) -> bool:
        """Guard to check if there are no saved WiFi configurations."""
        profiles = ctx.wifi_manager.read_credentials()
        return bool(profiles)
