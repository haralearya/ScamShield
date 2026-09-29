import re
from urllib.parse import urlparse

URGENT_WORDS = [
    "urgent", "immediately", "act now", "within 24 hours", "within 2 hours",
    "account will be blocked", "account blocked", "verify now", "last warning",
    "suspended", "expire", "expired", "legal action", "final notice"
]

SENSITIVE_WORDS = [
    "otp", "one time password", "upi pin", "pin", "password", "cvv",
    "card number", "bank account", "net banking", "login details",
    "verification code", "security code"
]

PRIZE_WORDS = [
    "won", "winner", "lottery", "prize", "cash reward", "free gift",
    "congratulations", "claim your reward", "lucky draw"
]

FINANCIAL_WORDS = [
    "refund", "cashback", "payment failed", "payment pending", "kyc",
    "bank", "upi", "wallet", "credit card", "debit card", "tax refund"
]

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly",
    "rb.gy", "shorturl.at", "ow.ly"
}

def _contains_phrase(text, phrases):
    low = text.lower()
    return [p for p in phrases if p in low]

def _score_level(score):
    score = max(0, min(100, int(score)))
    if score < 30:
        return "LOW"
    if score < 60:
        return "MEDIUM"
    return "HIGH"

def analyze_text(text, source_type="Text"):
    text = text.strip()
    low = text.lower()
    score = 0
    reasons = []

    urgent = _contains_phrase(text, URGENT_WORDS)
    sensitive = _contains_phrase(text, SENSITIVE_WORDS)
    prizes = _contains_phrase(text, PRIZE_WORDS)
    financial = _contains_phrase(text, FINANCIAL_WORDS)

    urls = re.findall(r"https?://[^\s]+|www\.[^\s]+", text, flags=re.I)

    if urgent:
        score += min(25, 8 + 5 * len(urgent))
        reasons.append("Urgent or threatening language detected.")

    if sensitive:
        score += min(35, 15 + 4 * len(sensitive))
        reasons.append("The message asks for or mentions sensitive credentials such as OTP, PIN or password.")

    if prizes:
        score += 20
        reasons.append("Prize, lottery or reward language detected.")

    if financial:
        score += 10
        reasons.append("Financial/KYC/payment-related language detected.")

    if urls:
        score += 15
        reasons.append("The message contains a clickable web link.")
        for u in urls[:3]:
            result = analyze_url(u)
            if result["score"] >= 30:
                score += min(25, result["score"] // 3)
                reasons.append("The included URL has suspicious characteristics.")

    if re.search(r"\b\d{6}\b", text) and sensitive:
        score += 8
        reasons.append("A six-digit code appears near credential-related wording.")

    if text.count("!") >= 3:
        score += 5
        reasons.append("Excessive exclamation marks may indicate pressure or urgency.")

    score = min(100, score)
    level = _score_level(score)

    advice = {
        "LOW": "Still verify the sender before clicking links or sharing information.",
        "MEDIUM": "Be cautious. Verify the sender using an official website or known phone number.",
        "HIGH": "Do not click links or share OTP/PIN/password details. Verify independently through an official channel."
    }[level]

    return {
        "type": source_type,
        "score": score,
        "level": level,
        "reasons": list(dict.fromkeys(reasons)),
        "advice": advice
    }

def analyze_url(url, source_type="URL"):
    original = url.strip()
    candidate = original
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", candidate):
        candidate = "http://" + candidate

    score = 0
    reasons = []

    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
        path = parsed.path or ""
        query = parsed.query or ""

        if not host:
            return {
                "type": source_type,
                "score": 80,
                "level": "HIGH",
                "reasons": ["The URL could not be parsed as a normal web address."],
                "advice": "Do not open an invalid or malformed link."
            }

        if parsed.scheme != "https":
            score += 15
            reasons.append("The URL does not use HTTPS.")

        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
            score += 30
            reasons.append("The link uses an IP address instead of a normal domain name.")

        if "@" in candidate:
            score += 25
            reasons.append("The URL contains '@', which can hide the actual destination.")

        if host in SHORTENERS or any(host.endswith("." + x) for x in SHORTENERS):
            score += 20
            reasons.append("The URL uses a link-shortening service.")

        if len(original) > 100:
            score += 10
            reasons.append("The URL is unusually long.")

        if host.count(".") >= 3:
            score += 10
            reasons.append("The domain contains many subdomains.")

        if "-" in host:
            score += 5
            reasons.append("The domain contains hyphens; verify the domain carefully.")

        suspicious_terms = [
            "verify", "login", "secure", "account", "update", "password",
            "wallet", "kyc", "reward", "claim", "free", "bank"
        ]
        found = [w for w in suspicious_terms if w in (host + path + query).lower()]
        if found:
            score += min(15, 5 + 2 * len(found))
            reasons.append("The URL contains terms commonly used in account or reward-related lures.")

        if host.endswith(".zip") or host.endswith(".mov"):
            score += 20
            reasons.append("The domain uses a file-like top-level domain that deserves extra caution.")

    except Exception:
        score = 80
        reasons.append("The URL format could not be safely analyzed.")

    score = min(100, score)
    level = _score_level(score)

    advice = {
        "LOW": "The URL has few obvious structural warning signs. Still confirm the domain before entering information.",
        "MEDIUM": "Treat this URL cautiously. Open the official website manually rather than using the link if possible.",
        "HIGH": "Avoid opening this link or entering credentials. Verify the destination independently."
    }[level]

    return {
        "type": source_type,
        "score": score,
        "level": level,
        "reasons": list(dict.fromkeys(reasons)),
        "advice": advice
    }
