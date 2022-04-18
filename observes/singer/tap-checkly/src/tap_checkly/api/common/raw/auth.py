from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class Credentials:
    api_user: str
    api_key: str

    def __str__(self) -> str:
        return "masked api_key"
