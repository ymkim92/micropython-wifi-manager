from dataclasses import dataclass
from typing import Dict, Any
from logger.console_logger import ConsoleLogger

# from wifi_manager.wifi_manager import WifiManager


@dataclass
class WifiFsmContext:
    wifi_manager: "WifiManager"
    logger: ConsoleLogger
    state_data: Dict[str, Any] = None

    def __post_init__(self):
        if self.state_data is None:
            self.state_data = {}
