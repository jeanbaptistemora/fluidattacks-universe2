from http_headers.types import (
    AcceptHeader,
)
from operator import (
    methodcaller,
)


def _is_accept(name: str) -> bool:
    return name.lower() == "accept"


def parse(line: str) -> AcceptHeader | None:
    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_accept(name):
        return None

    return AcceptHeader(
        name=name,
        value=value,
    )
