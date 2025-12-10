🕵️ IP Address Analyzer (IP Traceability & Multi-API Lookup)
💡 Overview
This Python application goes beyond simple IP lookups. It uses three independent public APIs (ipwho.is, ipapi.co, ipinfo.io) to retrieve, cross-verify, and analyze comprehensive IP address metadata (IPv4/IPv6).
The main goal is to generate a Location Consistency Score and a Privacy Exposure Score, which help detect network anomalies like VPNs, proxies, or inconsistent geolocation reporting.

✨ Features
1. Multi-API Data: Gathers details including Location, ISP, ASN, and Coordinates from 3 sources.

2. Location Consistency Score: Reports the agreement level between APIs on the reported country, flagging high variance (e.g., VPN use).

3. Privacy Exposure Score (0-100): Assesses network traceability based on factors like data consistency, timezone match, and IP type (e.g., IPv6 penalty).

4. IP Validation: Supports and validates both IPv4 and IPv6 formats.

5. Logging: Saves all detailed results and analysis scores to digital_footprint_log.txt.

🛠️ Getting Started
Prerequisites
1. Python 3.6+
2. requests library

Installation:
Bash
pip install requests

🧪 Unit Tests
Run the included tests to verify the core analysis functions (analyze_consistency and privacy_exposure_score):

Bash
python -m unittest ip_analyzer_ver2.py
