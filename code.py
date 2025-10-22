import requests
import ipaddress

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_ip_info(ip=None):
    # If no IP given, API returns info about current public IP
    url = f"https://ipwho.is/{ip}" if ip else "https://ipwho.is/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data.get("success", False):
            print(f"Invalid IP address or data not found for: {ip}")
            return

        # Extract info
        ipv4 = data.get("ip")
        ipv6 = data.get("ipv6")
        country = data.get("country")
        city = data.get("city")
        isp = data.get("connection", {}).get("isp")
        asn = data.get("connection", {}).get("asn")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Display nicely
        print("\n--- IP Information ---")
        print("IP Address:", ipv4)
        print("IPv6 Address:", ipv6 if ipv6 else "Not available")
        print(f"Location: {city}, {country}")
        print("ISP:", isp)
        print("ASN:", asn)
        print(f"Coordinates: {latitude}, {longitude}")

    except requests.RequestException as e:
        print("Error contacting the IP info service:", e)

if __name__ == "__main__":
    ip_input = input("Enter an IP address (leave blank for your current IP): ").strip()

    if ip_input:
        if validate_ip(ip_input):
            get_ip_info(ip_input)
        else:
            print("Invalid IP address format.")
    else:
        get_ip_info()
