"""Main application entry point (main.py)

Wires together:
1. NEC SL2100 SMDR Listener (TCP Port 8000)
2. Phone number normalization
3. Zoho Desk REST API ticket/contact lookup
4. Windows 11 Toast notification & browser launcher
"""

import os
import sys
import logging
from dotenv import load_dotenv

from phone_cleaner import normalize_phone_number
from zoho_client import ZohoDeskClient
from notifier import show_call_notification
from smdr_listener import start_listener

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("CallerIDBridge")


def handle_incoming_call(
    raw_phone: str,
    caller_id: str | None,
    client: ZohoDeskClient,
) -> None:
    """Process an incoming call event from the SMDR stream."""
    clean_number = normalize_phone_number(raw_phone)
    logger.info(f"Incoming call received: raw={raw_phone}, normalized={clean_number}")
    # Lookup in Zoho Desk and display notification
    pass


def main() -> None:
    """Load configuration and start the caller ID bridge."""
    load_dotenv()

    pbx_ip = os.getenv("PBX_IP", "192.168.1.150")
    pbx_port = int(os.getenv("PBX_PORT", "8000"))

    zoho_org_id = os.getenv("ZOHO_ORG_ID")
    zoho_client_id = os.getenv("ZOHO_CLIENT_ID")
    zoho_client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    zoho_refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
    zoho_portal = os.getenv("ZOHO_PORTAL_NAME", "cardandbeyond")

    logger.info("Initializing Zoho Desk client...")
    client = ZohoDeskClient(
        client_id=zoho_client_id or "",
        client_secret=zoho_client_secret or "",
        refresh_token=zoho_refresh_token or "",
        org_id=zoho_org_id or "",
        portal_name=zoho_portal,
    )

    logger.info(f"Connecting to NEC SL2100 PBX at {pbx_ip}:{pbx_port}...")
    # start_listener will be invoked once implemented
    print("Application initialized. Awaiting implementation of Task 3, 4, 5.")


if __name__ == "__main__":
    main()

