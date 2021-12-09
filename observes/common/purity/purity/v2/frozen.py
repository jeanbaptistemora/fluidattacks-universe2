from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    Dict,
    Iterator,
    Mapping,
    Tuple,
    TypeVar,
)

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

FrozenList = Tuple[_T, ...]


@dataclass(frozen=True)
class _FrozenDict(SupportsKind2["_FrozenDict[_K, _V]", _K, _V]):
    _dict: Dict[_K, _V]


class FrozenDict(Mapping[_K, _V], _FrozenDict[_K, _V]):
    def __init__(self, dictionary: Dict[_K, _V]):
        super().__init__(dictionary.copy())

    def __getitem__(self, key: _K) -> _V:
        return self._dict[key]

    def __iter__(self) -> Iterator[_K]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self._dict}"
