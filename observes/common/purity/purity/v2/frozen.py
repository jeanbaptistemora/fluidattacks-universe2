from collections.abc import (
    Iterator,
    Mapping,
)
from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

FrozenList = tuple[_T, ...]


@dataclass(frozen=True)
class _FrozenDict(Generic[_K, _V]):
    _dict: dict[_K, _V]


class FrozenDict(Mapping[_K, _V], _FrozenDict[_K, _V]):
    def __init__(self, dictionary: dict[_K, _V]):
        super().__init__(dictionary.copy())

    def __getitem__(self, key: _K) -> _V:
        return self._dict[key]

    def __iter__(self) -> Iterator[_K]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self._dict}"
