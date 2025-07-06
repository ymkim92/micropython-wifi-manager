import pytest
from unittest.mock import AsyncMock, MagicMock
from wifi_manager.fsm_manager import WifiFsmManager
from wifi_manager.fsm_message import EventConnectRequest
from wifi_manager.fsm_state import Init, Connecting
from wifi_manager.fsm_actions import WifiFsmActions
from wifi_manager.fsm_guards import WifiFsmGuards
from wifi_manager.wifi_manager import WifiManager
from logger.console_logger import ConsoleLogger


@pytest.mark.asyncio
async def test_fsm_transition_init_to_connecting():
    # Mock dependencies
    mock_wifi_manager = MagicMock(spec=WifiManager)
    mock_logger = MagicMock(spec=ConsoleLogger)
    mock_guards = MagicMock(spec=WifiFsmGuards)
    mock_actions = MagicMock(spec=WifiFsmActions)

    # Mock guard behavior
    mock_guards.guard_has_saved_config.return_value = True

    # Mock action behavior
    mock_actions.on_action_connect_to_saved = AsyncMock()

    # Initialize FSM Manager
    fsm_manager = WifiFsmManager(mock_wifi_manager, mock_logger, mock_guards, mock_actions)

    # Replace guards and actions with mocks
    fsm_manager.fsm_guards = mock_guards
    fsm_manager.fsm_actions = mock_actions

    await fsm_manager.initialize()

    assert fsm_manager.get_current_state_name() == "Init"
    await fsm_manager.dispatch_event(EventConnectRequest())

    assert fsm_manager.get_current_state_name() == "Connecting"
    mock_guards.guard_has_saved_config.assert_called_once()
    mock_actions.on_action_connect_to_saved.assert_awaited_once()
