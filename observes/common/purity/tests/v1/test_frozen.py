from purity.v1 import (
    FrozenDict,
)
from typing import (
    Dict,
)


def test_dict_mutability() -> None:
    mutable: Dict[str, int] = {"x": 34}
    fdict: FrozenDict[str, int] = FrozenDict(mutable)
    assert fdict == mutable
    mutable["x"] = 1
    assert fdict != mutable


def test_dict_iter() -> None:
    mutable: Dict[str, int] = {"x": 34}
    fdict: FrozenDict[str, int] = FrozenDict(mutable)
    assert mutable.items() == fdict.items()
