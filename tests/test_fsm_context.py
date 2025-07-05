from wifi_manager.fsm_context import WifiFsmContext
from unittest.mock import MagicMock


def test_fsm_context_creation():
    wifi_manager = MagicMock()
    logger = MagicMock()
    ctx = WifiFsmContext(wifi_manager=wifi_manager, logger=logger)

    assert ctx.wifi_manager == wifi_manager
    assert ctx.logger == logger
    assert ctx.state_data == {}
