import sys
from unittest.mock import MagicMock

# Mock the `network` module
sys.modules["network"] = MagicMock()
sys.modules["machine"] = MagicMock()
