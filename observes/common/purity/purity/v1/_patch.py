from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")


@dataclass(frozen=True)
class Patch(Generic[_DataTVar]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    inner: _DataTVar

    @property
    def unwrap(self) -> _DataTVar:
        return self.inner
