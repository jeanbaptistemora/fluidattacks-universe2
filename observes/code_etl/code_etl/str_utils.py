# pylint: skip-file

from dataclasses import (
    dataclass,
)
from returns.functions import (
    raise_exception,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.result import (
    Failure,
    ResultE,
    Success,
)
from typing import (
    Literal,
    TypeVar,
)


def _utf8_lead_byte(byte: int) -> bool:
    """A UTF-8 intermediate byte starts with the bits 10xxxxxx."""
    return (byte & 0b11000000) == 0b10000000


class NotUTF8(Exception):
    pass


class TruncationError(Exception):
    pass


def _lead_bytes_of(byte: int) -> ResultE[int]:
    """UTF-8 lead bytes of char given byte 1"""
    if (byte & 0b10000000) == 0:
        return Success(0)
    if (byte & 0b11100000) == 11000000:
        return Success(1)
    if (byte & 0b11110000) == 11100000:
        return Success(2)
    if (byte & 0b11111000) == 0b11110000:
        return Success(3)
    return Failure(NotUTF8(f"byte: {byte}"))


def _search_last_not_lead_byte(raw: bytes) -> int:
    last = len(raw) - 1
    for i in range(len(raw)):
        if not _utf8_lead_byte(raw[last - i]):
            return last - i
    raise Exception("Unexpected: not lead byte not found")


def utf8_byte_truncate(text: str, max_bytes: int) -> str:
    if max_bytes < 0:
        raise Exception("max_bytes must be >= 0")
    if max_bytes == 0:
        return ""
    utf8 = text.encode("utf8")
    if len(utf8) <= max_bytes:
        return utf8.decode("utf8")
    pre_truncated = utf8[:max_bytes]
    last_not_lead_index = _search_last_not_lead_byte(pre_truncated)
    last_lead_bytes = max_bytes - 1 - last_not_lead_index
    last_not_lead_byte = pre_truncated[last_not_lead_index]
    try:
        if (
            _lead_bytes_of(last_not_lead_byte).alt(raise_exception).unwrap()
            == last_lead_bytes
        ):
            # char bytes fits in the truncation
            return pre_truncated.decode("utf8")
        # discard incomplete char
        return pre_truncated[:last_not_lead_index].decode("utf8")
    except NotUTF8 as err:
        raise TruncationError(
            "utf8_byte_truncate(text, max_bytes)"
            f"\ntext={text}\nmax_bytes={max_bytes}"
            f"\npre_truncated={str(pre_truncated)}"
            f"\nlast_not_lead_byte={last_not_lead_byte}"
        ) from err


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
    draft = _TruncatedStr(limit, utf8_byte_truncate(raw, limit))
    return TruncatedStr(draft)
