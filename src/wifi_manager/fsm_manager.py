from async_fsm.fsm_async import AsyncFSM

from logger.console_logger import ConsoleLogger, LogLevel

from wifi_manager.fsm_state import (
    Init,
    Connecting,
    Connected,
    ApMode,
    Reconnecting,
    Failed,
)
from wifi_manager.fsm_message import (
    EventConnectRequest,
    EventConnected,
    EventConnectFailed,
    EventConfigReceived,
)


def create_fsm():
    """Create the FSM for WiFi Manager."""

    # Define states
    init_state = Init("Init")
    connecting_state = Connecting("Connecting")
    connected_state = Connected("Connected")
    ap_mode_state = ApMode("ApMode")
    reconnecting_state = Reconnecting("Reconnecting")
    failed_state = Failed("Failed")

    fsm = AsyncFSM(init_state)
    # Add states to FSM
    fsm.add_state(init_state)
    fsm.add_state(connecting_state)
    fsm.add_state(connected_state)
    fsm.add_state(ap_mode_state)
    fsm.add_state(reconnecting_state)
    fsm.add_state(failed_state)

    # Define transitions
    fsm.add_transition(init_state, EventConnectRequest, connecting_state)
    fsm.add_transition(connecting_state, EventConnected, connected_state)
    fsm.add_transition(connecting_state, EventConnectFailed, failed_state)
    fsm.add_transition(connected_state, EventConfigReceived, ap_mode_state)
    fsm.add_transition(ap_mode_state, EventConnectRequest, reconnecting_state)

    ctx = {"logger": ConsoleLogger(LogLevel.INFO)}
    fsm.start(ctx)

    return fsm
