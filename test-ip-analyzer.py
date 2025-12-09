import unittest
# Assuming your main app code is in 'analyzer.py', import the functions
from ip-analyzer.py import validate_ip, analyze_consistency, privacy_exposure_score

# Mock API results used for testing analysis functions
MOCK_RESULT_1 = {
    "ip": "1.1.1.1", "country": "US", "city": "Cloudflare", "isp": "Cloudflare",
    "type": "IPv4", "timezone": "America/Los_Angeles"
}
MOCK_RESULT_2_SAME = {
    "ip": "1.1.1.1", "country": "US", "city": "Cloudflare", "isp": "Cloudflare",
    "type": "IPv4", "timezone": "America/Los_Angeles"
}
MOCK_RESULT_3_DIFFERENT = {
    "ip": "2.2.2.2", "country": "JP", "city": "Tokyo", "isp": "NTT",
    "type": "IPv6", "timezone": "Asia/Tokyo"
}

class TestAnalyzerFunctions(unittest.TestCase):
    
    # --- Test Cases for validate_ip ---
    def test_valid_ip(self):
        """Test the validation of correct IPv4 and IPv6 addresses."""
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("2001:db8::1"))
        self.assertTrue(validate_ip("1.1.1.1"))

    def test_invalid_ip(self):
        """Test the rejection of invalid formats."""
        self.assertFalse(validate_ip("256.0.0.1")) # Invalid number
        self.assertFalse(validate_ip("invalid_text")) # Non-IP string
        self.assertFalse(validate_ip("192.168.1.1/24")) # Includes CIDR

    # --- Test Cases for analyze_consistency ---
    def test_consistency_high(self):
        """Test case where all APIs return identical location data."""
        results = [MOCK_RESULT_1, MOCK_RESULT_2_SAME, MOCK_RESULT_1]
        summary, score = analyze_consistency(results)
        self.assertAlmostEqual(score, 100.0) # Expect high consistency
        self.assertIn("High confidence", summary)

    def test_consistency_low(self):
        """Test case where APIs return inconsistent location data (e.g., VPN detected)."""
        results = [MOCK_RESULT_1, MOCK_RESULT_3_DIFFERENT, MOCK_RESULT_3_DIFFERENT]
        summary, score = analyze_consistency(results)
        self.assertAlmostEqual(score, (2/3) * 100, places=2) # 66.67% consistency
        self.assertIn("Minor variation detected", summary)
        
    # --- Test Cases for privacy_exposure_score ---
    def test_privacy_score_ipv6(self):
        """Test the score penalty when an IPv6 address is detected."""
        # Mix of two identical IPv4 and one different IPv6 result
        results = [MOCK_RESULT_1, MOCK_RESULT_2_SAME, MOCK_RESULT_3_DIFFERENT] 
        score, notes = privacy_exposure_score(results)
        
        # Expected score: 100 (base) - 0 (country) - 10 (IPv6) - 15 (timezone) = 75
        self.assertEqual(score, 75)
        self.assertIn("IPv6 detected", notes[0])
        self.assertIn("Timezone inconsistency", notes[1])


if __name__ == "__main__":
    unittest.main()
