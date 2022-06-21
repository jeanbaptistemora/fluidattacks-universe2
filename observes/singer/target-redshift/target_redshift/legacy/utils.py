import re
from typing import (
    Any,
    Iterable,
)

# Type aliases that improve clarity
JSON = Any
PGCONN = Any
PGCURR = Any
JSON_VALIDATOR = Any


def escape(text: str) -> str:
    """Escape characters from an string object.
    Which are known to make a Redshift statement fail.
    """
    str_obj = str(text)
    str_obj = re.sub("\x00", "", str_obj)
    str_obj = str_obj.replace("\\", "\\\\")
    str_obj = str_obj.replace('"', '""')
    str_obj = str_obj.replace("'", "\\'")

    return str_obj


def str_len(str_obj: str, encoding: str = "utf-8") -> int:
    """Returns the length in bytes of a string."""
    return len(str_obj.encode(encoding))


def stringify(iterable: Iterable[Any], do_group: bool = True) -> str:
    """Returns a string representation of an iterable."""

    if do_group:
        return ",".join(f"({x})" for x in iterable)
    return ",".join(f"{x}" for x in iterable)
