from __future__ import (
    annotations,
)

from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    api_key: str

    @classmethod
    def new(cls, raw: str) -> Credentials:
        return cls(raw)

    def __str__(self) -> str:
        return "masked api_key"
