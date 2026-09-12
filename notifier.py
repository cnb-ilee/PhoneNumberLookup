"""Module D: Desktop Alert & Browser Launcher (notifier.py)

Displays Windows 11 native desktop toast notifications for incoming calls
and triggers the user's default browser to the Zoho Desk ticket or contact URL on click.
"""

import logging
import webbrowser
from typing import Optional

logger = logging.getLogger(__name__)


def show_call_notification(
    caller_name: str,
    phone_number: str,
    ticket_number: Optional[str],
    target_url: str,
) -> None:
    """Display native Windows 11 toast notification with on-click browser launch."""
    # TODO: Implement Windows 11 toast with callback in Task 4
    raise NotImplementedError("Windows 11 toast handler will be implemented in Task 4")


def open_browser_url(url: str) -> None:
    """Open target URL in default browser."""
    logger.info(f"Opening browser URL: {url}")
    webbrowser.open(url)

