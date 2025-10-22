# IPv4-IPv6-Address-Application

## Overview

This Python application retrieves and displays detailed public IP address information for a specified IPv4 or IPv6 address. If no IP is specified, it defaults to the current public IP address. The app uses two public APIs — [ipwho.is](https://ipwho.is/) and [ipapi.co](https://ipapi.co/) — to gather comprehensive IP data, including geolocation, ISP, ASN, and coordinates.

---

## Features

- Validates IPv4 and IPv6 address formats.
- Retrieves IP information including:
  - Public IPv4 and IPv6 addresses
  - Location (City, Country)
  - ISP (Internet Service Provider)
  - ASN (Autonomous System Number)
  - Geographic coordinates (Latitude and Longitude)
- Supports querying information for any valid IP address.
- Uses two APIs to cross-verify and enrich IP information.

---

## Getting Started

### Prerequisites

- Python 3.6 or later
- `requests` library

Install dependencies using pip:

```bash
pip install requests
