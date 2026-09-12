"""Simulation & Dry-run script (test_sim.py)

Simulates incoming call events from the NEC SL2100 PBX to verify:
1. Phone normalization
2. Zoho Desk REST API lookups (or mocked responses)
3. Windows 11 desktop notifications and browser pop-ups
without requiring live PBX hardware.
"""

import os
import sys
import logging
from dotenv import load_dotenv

from phone_cleaner import normalize_phone_number

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("Simulator")


def simulate_incoming_call(raw_log_sample: str) -> None:
    """Parse and simulate handling a single SMDR call line."""
    logger.info(f"Simulating SMDR line: {raw_log_sample}")
    # TODO: Full simulation wiring in Task 6
    pass


if __name__ == "__main__":
    load_dotenv()
    sample = '09/12/26 14:30:15 IN Trunk 01 2015550199 Ext 101 CallerID: "JOHN DOE"'
    simulate_incoming_call(sample)

