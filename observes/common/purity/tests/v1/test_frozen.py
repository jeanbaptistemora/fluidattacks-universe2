from purity.v1 import (
    FrozenDict,
)


def test_dict_mutability() -> None:
    mutable: dict[str, int] = {"x": 34}
    fdict: FrozenDict[str, int] = FrozenDict(mutable)
    assert fdict == mutable
    mutable["x"] = 1
    assert fdict != mutable


def test_dict_iter() -> None:
    mutable: dict[str, int] = {"x": 34}
    fdict: FrozenDict[str, int] = FrozenDict(mutable)
    assert mutable.items() == fdict.items()
