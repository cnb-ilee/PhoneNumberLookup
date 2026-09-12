"""Module B: NEC SL2100 SMDR Listener (smdr_listener.py)

Connects to the NEC SL2100 PBX via TCP socket on port 8000 to listen
for real-time Station Message Detail Recording (SMDR) call logs.
"""

import socket
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def parse_smdr_line(line: str) -> Optional[dict]:
    """Parse raw SMDR log line from NEC SL2100 and extract call details.
    
    Sample line format:
    '09/12/26 14:30:15 IN Trunk 01 2015550199 Ext 101 CallerID: "JOHN DOE"'
    """
    # TODO: Implement SMDR regex parser in Task 5
    raise NotImplementedError("SMDR parsing will be implemented in Task 5")


def start_listener(
    host: str,
    port: int,
    on_call_received: Callable[[str, Optional[str]], None],
    buffer_size: int = 1024,
) -> None:
    """Listen for incoming SMDR packets over TCP socket with auto-reconnect."""
    # TODO: Implement socket listener with reconnect loop in Task 5
    raise NotImplementedError("SMDR listener will be implemented in Task 5")

