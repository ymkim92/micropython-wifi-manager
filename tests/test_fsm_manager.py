import pytest_asyncio
from logger.null_logger import NullLogger


# @pytest_asyncio.fixture
# async def setup_fsm():
#     from wifi_manager.fsm_manager import create_fsm
#     from wifi_manager.wifi_manager import WifiManager

#     logger = NullLogger()
#     wm = WifiManager(logger)
#     fsm = create_fsm(wm)
#     return fsm, wm
