import hashlib
import re


_MD5_HEX_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def normalize_login_word(login_word: str) -> str:
    """Return the MD5 login password expected by the backend."""
    value = (login_word or "").strip()
    if not value:
        return ""
    if _MD5_HEX_RE.fullmatch(value):
        return value.lower()
    return hashlib.md5(value.encode("utf-8")).hexdigest()
