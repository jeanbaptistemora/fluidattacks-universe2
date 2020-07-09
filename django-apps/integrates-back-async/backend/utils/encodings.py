def safe_encode(string: str) -> str:
    """Turn a utf-8 string into a string of [a-z0-9] characters."""
    return string.encode('utf-8').hex().lower()


def safe_decode(hexstr: str) -> str:
    """Inverse of: Turn a utf-8 string into a string of [a-z0-9] characters."""
    return bytes.fromhex(hexstr).decode('utf-8')
