"""Strategy Pattern: each class checks one URL characteristic."""


class URLCheckStrategy:
    """Common interface implemented by every URL-check strategy."""

    name = "base"

    def check(self, features: dict):
        raise NotImplementedError("Each strategy must implement check().")


class IPCheckStrategy(URLCheckStrategy):
    name = "IP address host"

    def check(self, features: dict):
        if features.get("host_is_ip"):
            return {
                "score": 60,
                "message": "The host is a raw IPv4 address rather than a domain name.",
            }
        return None


class LengthCheckStrategy(URLCheckStrategy):
    name = "Long URL"

    def check(self, features: dict):
        length = features.get("length", 0)
        if length > 75:
            return {
                "score": 25,
                "message": f"The URL is long ({length} characters; threshold is 75).",
            }
        return None


class KeywordCheckStrategy(URLCheckStrategy):
    name = "Deceptive keywords"
    KEYWORDS = (
        "login-verify",
        "account-update",
        "banking",
        "secure-login",
        "verify-account",
        "password-reset",
        "signin",
    )

    def check(self, features: dict):
        url = features.get("url", "")
        matches = [keyword for keyword in self.KEYWORDS if keyword in url]
        if matches:
            return {
                "score": 45,
                "message": "Potentially deceptive keyword(s): "
                + ", ".join(matches)
                + ".",
            }
        return None
