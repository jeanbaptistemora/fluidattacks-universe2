from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from typing import (
    Generic,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass
class Cache(Generic[_T]):
    item: Optional[_T]

    def get_or_set(self, item: Cmd[_T]) -> _T:
        if not self.item:
            # unsafe_unwrap is safe since the result will be cached
            self.item = unsafe_unwrap(item)
        return self.item
