import re


def normalize_phone_number(raw_phone: str) -> str:
    """Strips formatting symbols and country codes to return a clean 10-digit number."""
    digits_only = re.sub(r"\D", "", str(raw_phone))
    if len(digits_only) == 11 and digits_only.startswith("1"):
        return digits_only[1:]
    return digits_only

