import requests
import ipaddress
from datetime import datetime

# ===============================
# Utility Functions
# ===============================

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def fetch_json(url):
    """Fetch JSON safely with a custom header and fallback handling."""
    try:
        response = requests.get(url, headers={"User-Agent": "DigitalFootprintAnalyzer/3.0"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

# ===============================
# Data Collection from APIs
# ===============================

def get_ipwho(ip=None):
    data = fetch_json(f"https://ipwho.is/{ip}" if ip else "https://ipwho.is/")
    if not data or not data.get("success", False):
        return None
    return {
        "source": "ipwho.is",
        "ip": data.get("ip"),
        "country": data.get("country"),
        "region": data.get("region"),
        "city": data.get("city"),
        "isp": data.get("connection", {}).get("isp"),
        "asn": data.get("connection", {}).get("asn"),
        "type": data.get("type"),
        "timezone": data.get("timezone", {}).get("id"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
    }

def get_ipapi(ip=None):
    data = fetch_json(f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/")
    if not data or "error" in data:
        return None
    return {
        "source": "ipapi.co",
        "ip": data.get("ip"),
        "country": data.get("country_name"),
        "region": data.get("region"),
        "city": data.get("city"),
        "isp": data.get("org"),
        "asn": data.get("asn"),
        "type": data.get("version"),
        "timezone": data.get("timezone"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
    }

def get_ipinfo(ip=None):
    data = fetch_json(f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json")
    if not data:
        return None
    loc = data.get("loc", ",").split(",")
    return {
        "source": "ipinfo.io",
        "ip": data.get("ip"),
        "country": data.get("country"),
        "region": data.get("region"),
        "city": data.get("city"),
        "isp": data.get("org"),
        "asn": data.get("asn"),
        "type": "IPv6" if ":" in str(data.get("ip")) else "IPv4",
        "timezone": data.get("timezone"),
        "latitude": loc[0] if len(loc) > 0 else None,
        "longitude": loc[1] if len(loc) > 1 else None,
    }

# ===============================
# Analysis Functions
# ===============================

def analyze_consistency(results):
    """Compare country and city consistency between APIs"""
    countries = [r["country"] for r in results if r]
    cities = [r["city"] for r in results if r]
    isps = [r["isp"] for r in results if r]

    if not countries:
        return "No data available", 0

    common_country = max(set(countries), key=countries.count)
    consistency = (countries.count(common_country) / len(countries)) * 100

    message = f"Most APIs report your location as {common_country}."
    if consistency < 50:
        message += " 🌐 Possible VPN or proxy detected — your data varies significantly."
    elif consistency < 80:
        message += " ⚠️ Minor variation detected — you may be on mobile data or using dynamic routing."
    else:
        message += " ✅ High confidence in this location."

    # Detect ISP anomalies
    if len(set(isps)) > 1:
        message += f" Multiple ISPs detected ({', '.join(set(isps))}), which might indicate network rerouting."

    return message, round(consistency, 2)

def privacy_exposure_score(results):
    """Estimate a basic privacy exposure score based on metadata consistency and traceability."""
    score = 100
    notes = []

    if not results:
        return 0, ["No data available."]

    # Lower score for mismatched countries
    countries = [r["country"] for r in results if r]
    if len(set(countries)) > 1:
        score -= 20
        notes.append("Inconsistent geolocation across APIs — potential anonymization detected.")

    # Lower score if using IPv6 (less common, but can leak device-level info)
    if any(r["type"] == "IPv6" for r in results):
        score -= 10
        notes.append("IPv6 detected — can expose more precise network details.")

    # Lower score if ISP info missing
    if any(not r["isp"] for r in results):
        score -= 10
        notes.append("Missing ISP data — reduced transparency in network identity.")

    # Lower score if timezone mismatch
    timezones = [r["timezone"] for r in results if r and r["timezone"]]
    if len(set(timezones)) > 1:
        score -= 15
        notes.append("Timezone inconsistency — possible VPN or region masking.")

    # Cap score
    score = max(score, 0)
    return score, notes

# ===============================
# Output and Logging
# ===============================

def print_ip_info(info):
    print(f"\n--- {info['source'].upper()} ---")
    print(f"IP: {info['ip']} ({info['type']})")
    print(f"Location: {info['city']}, {info['region']}, {info['country']}")
    print(f"ISP: {info['isp']}")
    print(f"ASN: {info['asn']}")
    print(f"Timezone: {info['timezone']}")
    print(f"Coordinates: {info['latitude']}, {info['longitude']}")

def log_results(results, summary, consistency_score, privacy_score, privacy_notes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("digital_footprint_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n=== Digital Footprint Report ({timestamp}) ===\n")
        for info in results:
            if info:
                f.write(f"\n[{info['source'].upper()}]\n")
                f.write(f"IP: {info['ip']} ({info['type']})\n")
                f.write(f"Location: {info['city']}, {info['region']}, {info['country']}\n")
                f.write(f"ISP: {info['isp']}\n")
                f.write(f"ASN: {info['asn']}\n")
                f.write(f"Timezone: {info['timezone']}\n")
                f.write(f"Coordinates: {info['latitude']}, {info['longitude']}\n")
            else:
                f.write("\n[FAILED TO RETRIEVE DATA]\n")
        f.write(f"\nLocation Consistency: {consistency_score}%\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"\nPrivacy Exposure Score: {privacy_score}/100\n")
        if privacy_notes:
            f.write("Notes:\n- " + "\n- ".join(privacy_notes) + "\n")
        f.write("=" * 60 + "\n")

# ===============================
# Main Program
# ===============================

if __name__ == "__main__":
    print("🔍 Running Digital Footprint Analyzer...\n")

    ipwho = get_ipwho()
    ipapi = get_ipapi()
    ipinfo = get_ipinfo()

    results = [ipwho, ipapi, ipinfo]

    for r in results:
        if r:
            print_ip_info(r)
        else:
            print("\n--- One API failed to return data ---")

    summary, consistency_score = analyze_consistency([r for r in results if r])
    privacy_score, privacy_notes = privacy_exposure_score([r for r in results if r])

    print("\n=== Analysis Summary ===")
    print(summary)
    print(f"Location Consistency Score: {consistency_score}%")
    print(f"Privacy Exposure Score: {privacy_score}/100")
    if privacy_notes:
        print("Notes:")
        for note in privacy_notes:
            print(" -", note)

    log_results([r for r in results if r], summary, consistency_score, privacy_score, privacy_notes)
    print("\n🗂️ Results saved to digital_footprint_log.txt ✅")