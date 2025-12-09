The IP Address Analyzer is a Python application designed to trace and analyze the network metadata of a public IPv4 or IPv6 address. Unlike basic IP lookup tools, this application utilizes three distinct public APIs to cross-verify the collected data (geolocation, ISP, ASN, etc.) and generate an Analysis Summary and a Privacy Exposure Score.This powerful comparison feature helps determine the consistency of the reported location, which can alert the user to potential signs of a VPN, proxy use, or mobile network routing.✨ FeaturesMulti-API Data Collection: Gathers comprehensive network data from three public APIs: ipwho.is, ipapi.co, and ipinfo.io.IP Validation: Validates both IPv4 and IPv6 address formats.Comprehensive Data Retrieval: Retrieves key details, including:Public IP Address and Type (IPv4/IPv6)Geolocation (City, Region, Country, Timezone)Network Identity (ISP - Internet Service Provider, ASN - Autonomous System Number)Geographic Coordinates (Latitude and Longitude)Traceability Analysis: Compares API results to determine a Location Consistency Score.Privacy Exposure Scoring: Calculates a score (out of 100) based on factors like IP type (IPv6), data inconsistency, and missing details, providing a basic assessment of network traceability.Persistent Logging: All results, including the summary and scores, are saved to a file named digital_footprint_log.txt.🛠️ Getting StartedPrerequisitesPython 3.6 or laterThe requests library for making API calls.InstallationClone the repository (assuming the project is hosted/packaged) or save the provided code as a Python file (e.g., digital_footprint_analyzer.py).Install dependencies using pip:Bashpip install requests
UsageRun the script from your terminal. When prompted, you can enter a specific IP address to analyze, or simply press Enter to analyze your current public IP address.Bashpython digital_footprint_analyzer.py
Example Session:🔍 Running Digital Footprint Analyzer...

Enter an IP address to analyze (or press Enter for your public IP): 1.1.1.1 
Analyzing IP: 1.1.1.1

Fetching data from external APIs...

--- IPWHO.IS ---
IP: 1.1.1.1 (IPv4)
Location: Cloudflare, California, United States
ISP: Cloudflare, Inc.
...

=== Analysis Summary ===
Most APIs report your location as United States. ✅ High confidence in this location.
Location Consistency Score: 100.0%
Privacy Exposure Score: 100/100
...

🗂️ Results saved to digital_footprint_log.txt ✅
📝 Code OverviewThe application is structured into clear, maintainable sections:SectionDescriptionKey FunctionsUtility FunctionsHandles input validation and safe API fetching.validate_ip(), fetch_json()Data CollectionCalls the three external IP APIs and standardizes their diverse JSON responses into a unified Python dictionary.get_ipwho(), get_ipapi(), get_ipinfo()Analysis FunctionsCore logic for comparative analysis.analyze_consistency(), privacy_exposure_score()Output and LoggingFormats the final results for display and persistence.print_ip_info(), log_results()🧪 Running Unit TestsThe included unittest code ensures the core analysis logic is working correctly, particularly the calculations for consistency and privacy scoring.To run the tests, save the provided test code separately (or include it at the end of your main file) and run:Bashpython -m unittest ip_analyzer_ver2.py 
