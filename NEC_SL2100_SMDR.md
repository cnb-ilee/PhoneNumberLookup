# NEC SL2100 PBX: SMDR Network & TCP Configuration Manual

This document provides step-by-step instructions for obtaining the NEC SL2100 system IP address, enabling Station Message Detail Recording (SMDR) over TCP/IP (Port 8000), testing network connectivity, and understanding the output string structure for consumption by the Python listener bridge.

---

## 1. Network Discovery & IP Identification

Before configuring SMDR or connecting the Python listener bridge, identify the PBX's IP address on your local network.

### Method A: Hardware Desk Phone (Fastest)
1. Go to any primary or administrative digital desk phone (e.g., model `IP7WW-12TXH` or `24TXH`).
2. Press the **Menu** soft key or the **Center Navigation Key**.
3. Dial **`841`** (or `96` on select firmware versions) on the phone's keypad.
4. The LCD display will show the **CPU IP Address** (Default factory IP is typically `192.168.0.10`).
5. *(Optional)* Press the **Right Navigation Key** to display the **VoIPDB IP Address** if VoIP daughterboards are installed.

### Method B: Network Broadcast / Command Prompt
Run a ping sweep or resolve local hostname via Command Prompt:
```cmd
ping sl2100
```
If your local DNS handles NetBIOS/LLMNR hostnames, it will resolve and echo the active LAN IP address.

---

## 2. WebPro / PCPro System Programming

SMDR configuration requires administrative access to the system memory via **WebPro** (web interface) or **PCPro** (Windows administration software).

### Step 1: Login
1. Open a web browser and navigate to:
   ```text
   http://<PBX_IP_ADDRESS>
   ```
2. Enter your technician credentials:
   * **Username:** `tech` (or `installer`)
   * **Password:** `12345678` (or custom installer password)

---

### Step 2: Configure System Program Codes

Navigate to **System Data** mode in WebPro/PCPro and apply the following program settings:

| Program Code | Name / Description | Required Setting | Details |
| :--- | :--- | :--- | :--- |
| **10-20-01** | LAN Control Setup - SMDR Output | `LAN` (or `Ethernet`) | Directs system log routing to the IP network interface rather than RS-232 serial. |
| **35-01-01** | SMDR Basic Options - Output Port | `LAN` | Selects LAN socket streaming as the active SMDR destination. |
| **35-01-04** | SMDR Basic Options - TCP/IP Port | `8000` | Defines the listening TCP port for the socket server (Default: `8000`). |
| **35-01-02** | Output Incoming Calls | `1` (Enabled) | Ensures inbound call logs (with Caller ID) are emitted to the output stream. |
| **35-01-03** | Output Outgoing Calls | `1` (Enabled) | Emits outbound dialed calls to the output stream. |
| **35-02-01** | SMDR Item Print - Date/Time | `1` (Enabled) | Appends date and time stamps to each record. |
| **35-02-03** | SMDR Item Print - Caller ID | `1` (Enabled) | **CRITICAL:** Emits received Caller ID digits and name headers. |
| **35-02-04** | SMDR Item Print - Trunk Number | `1` (Enabled) | Prints CO trunk / line identifier. |

---

### Step 3: Save & Apply Settings
1. Click **Apply** (or **Write to System Memory** in PCPro) to store changes.
2. If prompted, perform a soft reset or session disconnect to restart the SMDR daemon on the PBX.

---

## 3. Network Verification & Socket Testing

The NEC SL2100 acts as a **TCP Server** on Port 8000. Use PowerShell on the Central Listener PC to confirm the port is open and accepting socket connections.

### PowerShell TCP Test Command:
```powershell
Test-NetConnection -ComputerName <PBX_IP_ADDRESS> -Port 8000
```

#### Expected Success Output:
```text
ComputerName           : 192.168.0.10
RemoteAddress          : 192.168.0.10
RemotePort             : 8000
InterfaceAlias         : Ethernet
SourceAddress          : 192.168.0.50
TcpTestSucceeded       : True
```

*Note: If `TcpTestSucceeded` returns `False`, verify Windows Firewall settings on the central machine and ensure no other application (such as old CTI software) is holding port 8000 open.*

---

## 4. SMDR Output Format & Parsing Reference

When an incoming call rings or completes, the PBX broadcasts an ASCII string over the open TCP socket connection. 

### Sample Raw SMDR String:
```text
09/12/26 14:30:15  00:01:23  01  IN   101  2015550199         "JOHN DOE"
```

### Breakdown of Fields:

| Field Index | Sample Data | Description |
| :--- | :--- | :--- |
| **Date** | `09/12/26` | Date formatted as MM/DD/YY |
| **Time** | `14:30:15` | Call arrival / event timestamp |
| **Duration** | `00:01:23` | Call duration (HH:MM:SS) |
| **Trunk** | `01` | PBX Trunk line number |
| **Direction** | `IN` | Call direction (`IN` = Inbound, `OUT` = Outbound) |
| **Extension** | `101` | Receiving extension / station number |
| **Caller ID Number** | `2015550199` | **Target Data:** Raw incoming caller phone digits |
| **Caller Name** | `"JOHN DOE"` | Caller ID Name string (optional / trunk-dependent) |

---

## 5. Summary for Python Listener Development

* **Server/Client Model:** The NEC PBX is the **Server** (Listening on Port 8000). Python script acts as a **Client** (Initiating TCP socket connect to `PBX_IP:8000`).
* **Connection Type:** Continuous TCP socket connection with automatic retry/reconnect logic.
* **Extraction Target:** Parse incoming lines containing directional tag `IN`, extract the Caller ID number token, pass it to `phone_cleaner.py` for standard 10-digit normalization (`2015550199`), and execute the Zoho Desk API search pipeline.