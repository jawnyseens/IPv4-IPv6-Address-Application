import requests
import ipaddress

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_ip_info_ipwho(ip=None):
    url = f"https://ipwho.is/{ip}" if ip else "https://ipwho.is/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get("success", False):
            return None
        return {
            "ip": data.get("ip"),
            "ipv6": data.get("ipv6"),
            "country": data.get("country"),
            "city": data.get("city"),
            "isp": data.get("connection", {}).get("isp"),
            "asn": data.get("connection", {}).get("asn"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }
    except requests.RequestException:
        return None

def get_ip_info_ipapi(ip=None):
    url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return None
        return {
            "ip": data.get("ip"),
            "ipv6": data.get("ipv6", None),
            "country": data.get("country_name"),
            "city": data.get("city"),
            "isp": data.get("org"),
            "asn": data.get("asn"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }
    except requests.RequestException:
        return None

def print_ip_info(source_name, info):
    if not info:
        print(f"{source_name}: Failed to retrieve data.")
        return
    print(f"\n--- {source_name} ---")
    print(f"IP Address: {info['ip']}")
    print(f"IPv6 Address: {info['ipv6'] if info['ipv6'] else 'Not available'}")
    print(f"Location: {info['city']}, {info['country']}")
    print(f"ISP: {info['isp']}")
    print(f"ASN: {info['asn']}")
    print(f"Coordinates: {info['latitude']}, {info['longitude']}")

if __name__ == "__main__":
    # No IP specified — will fetch info about the current public IP
    info_ipwho = get_ip_info_ipwho()
    info_ipapi = get_ip_info_ipapi()

    print_ip_info("ipwho.is", info_ipwho)
    print_ip_info("ipapi.co", info_ipapi)
