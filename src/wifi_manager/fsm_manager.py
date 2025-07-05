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
from wifi_manager.fsm_actions import WifiFsmActions
from wifi_manager.fsm_guards import WifiFsmGuards
from wifi_manager.fsm_context import WifiFsmContext


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
        fsm_guards = WifiFsmGuards()
        fsm_actions = WifiFsmActions()

        # Add states to FSM
        self.fsm.add_state(init_state)
        self.fsm.add_state(connecting_state)
        self.fsm.add_state(connected_state)
        self.fsm.add_state(ap_mode_state)
        self.fsm.add_state(reconnecting_state)
        self.fsm.add_state(failed_state)

        self.ctx = WifiFsmContext(
            wifi_manager=self.wifi_manager,
            logger=self.logger,
        )
        # Define transitions
        self.fsm.add_transition(
            init_state,
            EventConnectRequest,
            connecting_state,
            guard=fsm_guards.guard_has_saved_config,
            action=fsm_actions.on_action_connect_to_saved,
        )
        # self.fsm.add_transition(
        #     init_state,
        #     EventConnectRequest,
        #     connecting_state,
        #     guard=lambda: fsm_guards.guard_has_saved_config(),
        #     action=fsm_actions.on_action_start_ap_mode,
        # )
        # self.fsm.add_transition(init_state, EventConnectRequest, ap_mode_state)

        self.fsm.start(self.ctx)

    async def dispatch_event(self, event):
        """Dispatch an event to the FSM.

        Args:
            event: The event to dispatch
        """
        await self.fsm.dispatch(self.ctx, event)

    def get_current_state(self) -> str:
        """Get the name of the current state.

        Returns:
            str: Name of current state
        """
        return self.fsm.current_state()
