import requests
from ncclient import manager
from ncclient.transport.errors import SSHError
from ncclient.operations.errors import OperationError
import xml.dom.minidom as dom
import socket  # Used to check for valid IP format

# --- Configuration Variables ---
# NOTE: The default HOST IP is now defined here.
DEFAULT_HOST = "192.168.1.10"
PORT = 830             # Standard NETCONF port
USER = "devnet"
PASS = "cisco123"
WEBEX_TOKEN = "YOUR_WEBEX_BOT_TOKEN_HERE"
WEBEX_ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00v..."

# --- YANG / XML Payload (Unchanged) ---
NETCONF_CONFIG = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1/0/1</name>
        <description>CUSTOMER_X_SERVICE_UPGRADE_10G</description>
      </GigabitEthernet>
      <GigabitEthernet>
        <name>1/0/2</name>
        <description>CIRCUIT_ID_L1-AUTOMATION-12345</description>
      </GigabitEthernet>
    </interface>
    <hostname>R1-NIM-UPDATED</hostname>
  </native>
</config>
"""

# -------------------------------
# --- NEW IP INPUT FUNCTION ---
# -------------------------------


def get_host_ip(default_ip):
    """Prompts the user for the router IP and validates the input."""
    while True:
        prompt = f"Please enter the **Target Router IP** (default: {default_ip}): "
        ip_input = input(prompt).strip()

        if not ip_input:
            # If input is empty, use the default IP
            print(f"Using default IP: {default_ip}")
            return default_ip

        try:
            # Validate the input format as an IP address
            socket.inet_aton(ip_input)
            return ip_input
        except socket.error:
            print("❌ Invalid IP address format. Please try again.")

# --- Utility Functions (Unchanged) ---


def send_webex_notification(message):
    # ... (function body unchanged)
    url = "https://api.webex.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {WEBEX_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "roomId": WEBEX_ROOM_ID,
        "markdown": message
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("\n✅ WebEx Notification Sent Successfully.")
    except requests.RequestException as e:
        print(f"❌ WebEx API Error: Failed to send notification. Details: {e}")


def get_config_filtered(m, filter_xml):
    # ... (function body unchanged)
    try:
        result = m.get(filter=filter_xml).data_xml
        pretty_xml = dom.parseString(result).toprettyxml(indent='  ')
        return pretty_xml
    except Exception as e:
        print(f"Error retrieving filtered config: {e}")
        return "N/A"

# -------------------------------
# --- Main Automation Logic ---
# -------------------------------


def automate_config_change(host_ip):
    """
    Automates the 5-step process, taking the host_ip as an argument.
    """
    NATIVE_FILTER = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1/0/1</name>
          </GigabitEthernet>
          <GigabitEthernet>
            <name>1/0/2</name>
          </GigabitEthernet>
        </interface>
        <hostname/>
      </native>
    </filter>
    """

    notification_message = ""

    try:
        # 1. Connect and Verify Initial Config
        print(f"🔗 Attempting to connect to {host_ip}:{PORT}...")
        with manager.connect(host=host_ip, port=PORT, username=USER, password=PASS,
                             hostkey_verify=False, device_params={'name': 'iosxe'}) as m:
            print("✅ Connection successful. Device capabilities exchanged.")

            print("\n1. Verifying current running-config (Snapshot)...")
            initial_config_xml = get_config_filtered(m, NATIVE_FILTER)
            print("--- Initial Config Snapshot ---\n" + initial_config_xml)

            # 2. Apply Configuration (Make three changes)
            print("\n2. Applying configuration changes via <edit-config>...")
            edit_result = m.edit_config(
                target='running', config=NETCONF_CONFIG)
            print(f"✅ Configuration applied. Result: {edit_result.ok}")

            # 3. Verify specific changes & 4. Verify new running-config
            print("\n3 & 4. Verifying final running-config...")
            final_config_xml = get_config_filtered(m, NATIVE_FILTER)
            print("--- Final Config Snapshot ---\n" + final_config_xml)

            # --- Check for Success/Failure in output ---
            if "R1-NIM-UPDATED" in final_config_xml:
                status = "SUCCESS"
                notification_message = f"**NETCONF AUTOMATION ALERT**\n\n**Device:** `{host_ip}` (Hostname: `R1-NIM-UPDATED`)\n**Status:** {status} ✅. Configuration successfully updated by L1 automation.\n**Changes:** Descriptions set on Gi1/0/1 and Gi1/0/2, and hostname changed."
            else:
                status = "FAILURE"
                notification_message = f"**NETCONF AUTOMATION ALERT**\n\n**Device:** `{host_ip}`\n**Status:** {status} ❌. Configuration failed to verify. Manual intervention required."

    except SSHError as e:
        status = "FAILURE"
        error_msg = f"NETCONF SSH Connection Error: {e}"
        print(f"❌ {error_msg}")
        notification_message = f"**NETCONF AUTOMATION ALERT**\n\n**Device:** `{host_ip}`\n**Status:** {status} ❌. **Connection Error** (Check IP, Port 830, and Firewall).\n**Details:** `{error_msg}`"

    except OperationError as e:
        status = "FAILURE"
        error_msg = f"NETCONF Operation Error: {e}"
        print(f"❌ {error_msg}")
        notification_message = f"**NETCONF AUTOMATION ALERT**\n\n**Device:** `{host_ip}`\n**Status:** {status} ❌. **Protocol Error** (Check XML payload/Credentials).\n**Details:** `{error_msg}`"

    except Exception as e:
        status = "FAILURE"
        error_msg = f"An unexpected error occurred: {e}"
        print(f"❌ {error_msg}")
        notification_message = f"**NETCONF AUTOMATION ALERT**\n\n**Device:** `{host_ip}`\n**Status:** {status} ❌. **Application Error**.\n**Details:** `{error_msg}`"

    # 5. Send WebEx Notification
    if notification_message:
        send_webex_notification(notification_message)

# -------------------------------
# --- EXECUTION BLOCK ---
# -------------------------------


if __name__ == "__main__":
    # Get the target IP from user input, using the default if empty.
    TARGET_HOST = get_host_ip(DEFAULT_HOST)
    # Pass the determined IP to the main function
    automate_config_change(TARGET_HOST)
