from collections.abc import (
    Callable,
)
from contextlib import (
    suppress,
)
import csv
from operator import (
    methodcaller,
)


def parse_key_value(
    is_header: Callable[[str], bool],
    line: str,
) -> tuple[str, str] | None:
    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not is_header(name):
        return None

    if len(portions) != 2:
        return None

    return name, value


def get_header_value_delimiter(header_value: str) -> str:
    delimiter = ","
    with suppress(csv.Error):
        sniffer = csv.Sniffer()
        data = sniffer.sniff(header_value, delimiters=",;")
        delimiter = data.delimiter

    return delimiter
