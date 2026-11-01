"""Coordinates URL cleanup, feature extraction, and the configured checks."""

from urllib.parse import urlparse
from strategies import IPCheckStrategy, LengthCheckStrategy, KeywordCheckStrategy


class URLNormalizer:
    """Prepare URL text for consistent heuristic checks."""

    def clean(self, raw_url: str) -> str:
        value = (raw_url or "").strip()
        if not value:
            return ""

        # Add a scheme when the user enters a domain without one.
        if "://" not in value:
            value = "https://" + value

        # Keep the path and query intact; lowercase the host-oriented input
        # for predictable matching in this educational detector.
        return value.rstrip("/").lower()


class FeatureExtractor:
    """Collect the URL details used by the strategies."""

    def extract(self, clean_url: str) -> dict:
        parsed = urlparse(clean_url)
        host = parsed.hostname or ""
        return {
            "url": clean_url,
            "length": len(clean_url),
            "host": host,
            "host_is_ip": self._looks_like_ipv4(host),
            "path": parsed.path or "",
        }

    @staticmethod
    def _looks_like_ipv4(host: str) -> bool:
        parts = host.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False


class PhishingDetectorFacade:
    """One entry point for the Flask controller."""

    def __init__(self):
        self.normalizer = URLNormalizer()
        self.extractor = FeatureExtractor()
        self.strategies = [
            IPCheckStrategy(),
            LengthCheckStrategy(),
            KeywordCheckStrategy(),
        ]

    def analyze_url(self, raw_url: str) -> dict:
        clean_url = self.normalizer.clean(raw_url)
        if not clean_url:
            return {
                "label": "Invalid input",
                "risk": "Unknown",
                "score": 0,
                "is_suspicious": True,
                "findings": ["Enter a URL to analyze."],
                "normalized_url": "",
            }

        parsed = urlparse(clean_url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return {
                "label": "Invalid URL",
                "risk": "Unknown",
                "score": 0,
                "is_suspicious": True,
                "findings": ["Enter a valid HTTP or HTTPS URL with a host name."],
                "normalized_url": clean_url,
            }

        features = self.extractor.extract(clean_url)
        findings = []
        score = 0

        for strategy in self.strategies:
            finding = strategy.check(features)
            if finding:
                findings.append(finding["message"])
                score += finding["score"]

        score = min(score, 100)
        suspicious = score >= 35

        if suspicious:
            label = "Potentially suspicious"
            risk = "High" if score >= 60 else "Medium"
        else:
            label = "No obvious heuristic flags"
            risk = "Low"

        if not findings:
            findings = ["No configured heuristic rules were triggered."]

        return {
            "label": label,
            "risk": risk,
            "score": score,
            "is_suspicious": suspicious,
            "findings": findings,
            "normalized_url": clean_url,
            "url_length": features["length"],
            "host": features["host"],
        }
