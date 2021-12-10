from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class Patch(Generic[_T]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    inner: _T

    @property
    def unwrap(self) -> _T:
        return self.inner
