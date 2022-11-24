def is_key_sensitive(key: str) -> bool:
    return any(
        key.lower().endswith(suffix)
        for suffix in [
            "key",
            "pass",
            "passwd",
            "user",
            "username",
        ]
    )
