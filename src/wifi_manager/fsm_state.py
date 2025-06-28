"""FSM states for WiFi Manager."""

from async_fsm.fsm_async import AsyncState


class Init(AsyncState):
    """State for initialization."""


class Connecting(AsyncState):
    """State for connecting to WiFi."""


class Connected(AsyncState):
    """State for when WiFi is connected."""


class ApMode(AsyncState):
    """State for Access Point mode."""


class Reconnecting(AsyncState):
    """State for reconnecting to WiFi."""


class Failed(AsyncState):
    """State for when connection fails."""
