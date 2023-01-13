from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class KeyAccess:
    # [WARNING] This type constructor should be only
    # available to client modules that need the raw key
    # DO NOT export the type (i.e. at export module)
    pass


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class ApiKey:
    _extract: _Patch[Callable[[KeyAccess], str]]

    def extract(self, access: KeyAccess) -> str:
        return self._extract.inner(access)

    @staticmethod
    def protect(raw: str) -> ApiKey:
        return ApiKey(_Patch(lambda _: raw))
