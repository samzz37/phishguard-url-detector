import unittest
from facade import PhishingDetectorFacade


class DetectorTests(unittest.TestCase):
    def setUp(self):
        self.detector = PhishingDetectorFacade()

    def test_empty_input_is_rejected(self):
        result = self.detector.analyze_url("   ")
        self.assertEqual(result["label"], "Invalid input")

    def test_ip_host_is_flagged(self):
        result = self.detector.analyze_url("http://192.168.1.1/account")
        self.assertTrue(result["is_suspicious"])
        self.assertGreaterEqual(result["score"], 60)

    def test_deceptive_keyword_is_flagged(self):
        result = self.detector.analyze_url("https://example.com/login-verify")
        self.assertTrue(result["is_suspicious"])
        self.assertTrue(any("keyword" in item.lower() for item in result["findings"]))

    def test_normal_url_has_no_configured_flags(self):
        result = self.detector.analyze_url("https://example.com")
        self.assertEqual(result["risk"], "Low")

    def test_invalid_scheme_or_host_is_rejected(self):
        result = self.detector.analyze_url("ftp:///missing-host")
        self.assertEqual(result["label"], "Invalid URL")


if __name__ == "__main__":
    unittest.main()
