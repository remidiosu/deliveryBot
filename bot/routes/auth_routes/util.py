import re
from typing import Optional

PHONE_RE = re.compile(r"^\+?\d{7,15}$")

def normalize_phone(raw: str) -> Optional[str]:
    if not raw:
        return None
    s = raw.strip()
    plus = s.startswith("+")
    digits = re.sub(r"\D+", "", s)
    if not (7 <= len(digits) <= 15):
        return None
    return f"+{digits}" if plus or not s.startswith("+") else digits
