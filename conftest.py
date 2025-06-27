import sys
import os

lib_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dependencies/async-fsm/src")
)
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
