# import pytest_asyncio
# from logger.null_logger import NullLogger


# @pytest_asyncio.fixture
# async def setup_fsm():
#     from wifi_manager.fsm_manager import create_fsm
#     from wifi_manager.wifi_manager import WifiManager

#     logger = NullLogger()
#     wm = WifiManager(logger)
#     fsm = create_fsm(wm)
#     return fsm, wm

# import pytest
from wifi_manager.fsm_manager import WifiFsmManager
from wifi_manager.fsm_message import EventConnectRequest


async def test_fsm_manager_initial_state():
    manager = WifiFsmManager(MockWifiManager(), MockLogger())
    assert manager.get_current_state() == "Init"


async def test_fsm_manager_dispatch_event():
    manager = WifiFsmManager(MockWifiManager(), MockLogger())
    await manager.dispatch_event(EventConnectRequest())
    assert manager.get_current_state() in ["Connecting", "ApMode"]


async def test_fsm_manager_force_ap_mode():
    manager = WifiFsmManager(MockWifiManager(), MockLogger())
    await manager.force_ap_mode()
    assert manager.is_in_ap_mode()
