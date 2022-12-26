from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import re


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class CleanString:
    _private: _Private
    raw: str

    @staticmethod
    def new(raw: str) -> CleanString:
        """Clean unvalid chars from a string."""
        return CleanString(_Private(), re.sub(r"[^ _a-zA-Z0-9]", "", raw))
