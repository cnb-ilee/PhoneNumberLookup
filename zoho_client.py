"""Module C: Zoho Desk API Integration (zoho_client.py)

Handles OAuth2 authentication (refresh_token flow), token caching,
and REST API lookups against Zoho Desk (Contacts & Tickets).
"""

import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)


class ZohoDeskClient:
    """Client for interacting with the Zoho Desk REST API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        org_id: str,
        portal_name: str = "cardandbeyond",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.org_id = org_id
        self.portal_name = portal_name
        self.access_token: Optional[str] = None

    def refresh_access_token(self) -> str:
        """Refresh Zoho Desk OAuth2 access token using refresh_token."""
        # TODO: Implement token refresh in Task 3
        raise NotImplementedError("OAuth2 token refresh will be implemented in Task 3")

    def search_by_phone(self, clean_phone: str) -> Optional[Dict[str, Any]]:
        """Search for customer/ticket in Zoho Desk using normalized 10-digit phone number."""
        # TODO: Implement search in Task 3
        raise NotImplementedError("Zoho Desk search will be implemented in Task 3")

    def get_ticket_url(self, ticket_id: Optional[str], clean_phone: str) -> str:
        """Construct the direct ticket URL or search fallback URL."""
        if ticket_id:
            return f"https://desk.zoho.com/agent/{self.portal_name}/all/tickets/details/{ticket_id}"
        return f"https://desk.zoho.com/agent/{self.portal_name}/all/tickets/search?searchDept=all&searchWord={clean_phone}"

