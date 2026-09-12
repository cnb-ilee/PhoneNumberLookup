# Chat History Export & Project Context

## Summary of Previous Context
* **Goal:** Implement an automated Caller ID pop-up system on Windows 11 PCs and integrate incoming calls with a Zoho Desk ticket search (`cardandbeyond` portal).
* **Hardware/PBX Scope:** NEC SL2100 (Digital); requires SMDR via TCP Port 8000. Zero physical hardware modifications.
* **Zoho Desk Limitation:** The web browser search URL (`/search?searchWord=`) performs strictly literal non-fuzzy lookups. It does not support wildcards (`*`) or boolean (`OR`) operators in URL parameters.
* **Solution:** Use the Zoho Desk REST API (`/api/v1/contacts/search?phone=`) which normalizes phone numbers automatically across all fields.

---

## Key Technical Decisions

1. **Phone Normalization:** 
   * Input variations: `#201-555-0199`, `201 555 0199`, `1 201 555 0199`, `(201) 555-0199`.
   * Standard output: 10 raw digits (`2015550199`).

2. **PBX Ingestion:**
   * Central machine connects via TCP socket to port 8000 on the NEC SL2100.
   * Parses SMDR text line, extracts incoming telephone number, passes data to processing modules.

3. **Zoho API Billing Safety:**
   * Zoho Desk API operates on daily allowance limits (thousands of free calls per day), not pay-per-request billing.
   * Zero risk of accidental credit card charges during development or side-project testing.

4. **Integration Workflow:**
   `Incoming Call (TCP:8000) -> Normalize Digits -> Query Zoho REST API -> Win 11 Toast -> Browser Open Ticket Details`