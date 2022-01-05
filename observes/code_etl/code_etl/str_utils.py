from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    Literal,
    TypeVar,
)

_L = TypeVar("_L", Literal[64], Literal[256], Literal[4096])


@dataclass(frozen=True)
class _TruncatedStr(SupportsKind1["_TruncatedStr[_L]", _L]):
    _length: _L
    msg: str


@dataclass(frozen=True)
class TruncatedStr(_TruncatedStr[_L]):
    def __init__(self, obj: _TruncatedStr[_L]) -> None:
        super().__init__(obj._length, obj.msg)  # type: ignore


def truncate(raw: str, limit: _L) -> TruncatedStr[_L]:
    draft = _TruncatedStr(limit, raw.encode()[:limit].decode())
    return TruncatedStr(draft)
