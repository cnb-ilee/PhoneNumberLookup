# AGENT.md: Project Blueprint & Context for AI Code Generation

## Project Overview
This project is a lightweight, zero-cost **Caller ID Pop-up & Zoho Desk Integration Bridge** for Windows 11 PCs. The system captures raw Call Detail Record (CDR) / Station Message Detail Recording (SMDR) logs from an on-premises **NEC SL2100 PBX**, parses the incoming phone number, queries the **Zoho Desk REST API** (portal: `cardandbeyond`), and displays a native Windows 11 desktop toast notification while automatically opening the customer's ticket/contact record in the user's default browser.

---

## 1. System Architecture & Data Flow

```
[NEC SL2100 PBX]
       │
       │ (1) Raw SMDR Stream over TCP Port 8000
       ▼
[Central Listener PC / Python Script]
       │
       │ (2) Parse SMDR raw line & extract caller phone number
       │ (3) Normalize phone number to 10 raw digits (e.g. 2015550199)
       │
       ├───> (4) Fetch matching ticket via Zoho Desk REST API
       │             │
       │             └───> Returns: Contact/Ticket ID & Customer Name
       │
       └───> (5) Trigger Windows 11 Native Desktop Notification (Toast)
                     │
                     └───> Click Notification: Opens Browser to Zoho Ticket URL
```

---

## 2. Technical Requirements & Environment

* **Language:** Python 3.10+
* **Target OS:** Windows 11 (64-bit)
* **PBX Source:** NEC SL2100 Digital PBX (Network SMDR via TCP Port 8000)
* **Target CRM:** Zoho Desk API (`cardandbeyond` organization portal)
* **Key Python Dependencies:**
  * `requests` - REST API calls to Zoho Desk OAuth2 and Search endpoints.
  * `win11toast` or `plyer` - Native Windows 11 desktop notification toasts.
  * `python-dotenv` - Environment variable management for API client credentials.

---

## 3. Core Modules & Technical Specifications

### Module A: Phone Number Normalization (`phone_cleaner.py`)
Because callers, contacts, and tickets input phone numbers in varying formats (`#201-555-0199`, `201 555 0199`, `1 201 555 0199`, `(201) 555-0199`), input strings must be normalized to a standard 10-digit format for search lookups.

#### Logic Rules:
1. Strip all non-numeric characters using Regex `\D`.
2. If the string is 11 digits long and begins with `1` (US country code), remove the leading `1`.
3. Return the clean 10-digit string (e.g., `2015550199`).

#### Code Reference Logic:
```python
import re


def normalize_phone_number(raw_phone: str) -> str:
    """Strips formatting symbols and country codes to return a clean 10-digit number."""
    digits_only = re.sub(r"\D", "", str(raw_phone))
    if len(digits_only) == 11 and digits_only.startswith("1"):
        return digits_only[1:]
    return digits_only
```

---

### Module B: NEC SL2100 SMDR Listener (`smdr_listener.py`)
Connects to the NEC SL2100 PBX IP via TCP socket on port 8000 to listen for real-time ring logs.

#### SMDR TCP Socket Parameters:
* **Protocol:** TCP Client Socket
* **Port:** `8000`
* **Buffer Size:** `1024` bytes
* **Log Sample Output:**
  `09/12/26 14:30:15 IN Trunk 01 2015550199 Ext 101 CallerID: "JOHN DOE"`

---

### Module C: Zoho Desk API Integration (`zoho_client.py`)
Queries Zoho Desk via REST API to ensure format-independent phone lookups across Contacts and Tickets.

#### 1. OAuth2 Setup & Token Management
* **Zoho API Domain:** `https://accounts.zoho.com/oauth/v2/token`
* **Required Scopes:** `ZohoDesk.tickets.READ`, `ZohoDesk.contacts.READ`
* **Grant Type:** `refresh_token`

#### 2. Search Endpoint Specification
* **URL:** `https://desk.zoho.com/api/v1/contacts/search` (or `/api/v1/tickets/search`)
* **Parameter:** `phone={clean_number}`
* **Headers:** 
  * `Authorization: Zoho-oauthtoken {access_token}`
  * `orgId: {YOUR_ZOHO_ORG_ID}`

#### 3. Direct Ticket Web URL Construction
When a match is found, construct the URL for the browser opener:
`https://desk.zoho.com/agent/cardandbeyond/all/tickets/details/{ticket_id}`

If no direct match is found, fall back to the default portal search URL:
`https://desk.zoho.com/agent/cardandbeyond/all/tickets/search?searchDept=all&searchWord={clean_number}`

---

### Module D: Desktop Alert & Browser Launcher (`notifier.py`)
Displays the Windows 11 notification toast with caller details and handles the click event to open the Zoho Desk web interface.

#### Logic Rules:
1. Display Toast with Title: `Incoming Call: {Caller Name / Company}`
2. Message: `Phone: {Formatted Number} | Ticket: #{Ticket Number}`
3. On Click: Execute `webbrowser.open(target_url)`

---

## 4. Environment Variables (`.env.example`)

```ini
# PBX Configuration
PBX_IP=192.168.1.150
PBX_PORT=8000

# Zoho Desk API Credentials
ZOHO_ORG_ID=your_zoho_org_id_here
ZOHO_CLIENT_ID=your_client_id_here
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REFRESH_TOKEN=your_refresh_token_here
ZOHO_PORTAL_NAME=cardandbeyond
```

---

## 5. Development Tasks & Implementation Steps for AntiGravity Agent

1. **Task 1: Set up project structure**
   * Create `smdr_listener.py`, `zoho_client.py`, `phone_cleaner.py`, `notifier.py`, `main.py`, `.env`, and `requirements.txt`.
2. **Task 2: Build `phone_cleaner.py` unit tests**
   * Validate strings like `#201-555-0199`, `201 555 0199`, `1 201 555 0199`, and `(201) 555-0199` clean to `2015550199`.
3. **Task 3: Implement Zoho Desk OAuth2 & API client**
   * Write auto-refresh logic for `access_token` management.
   * Implement ticket and contact search methods.
4. **Task 4: Build Windows 11 Toast notification handler**
   * Connect desktop notification click actions to the `webbrowser` launcher.
5. **Task 5: Implement SMDR socket listener with reconnect loop**
   * Ensure socket auto-reconnects if PBX connection drops.
6. **Task 6: Assemble end-to-end simulation test (`test_sim.py`)**
   * Provide a dry-run script that simulates an incoming call payload to verify desktop toasts and browser pop-ups without needing live PBX hardware.