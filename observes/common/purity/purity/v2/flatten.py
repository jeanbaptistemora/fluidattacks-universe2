from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.result import (
    Result,
    UnwrapError,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


def flatten_cmds(items: FrozenList[Cmd[_T]]) -> Cmd[FrozenList[_T]]:
    return Cmd.from_cmd(lambda: (tuple(map(unsafe_unwrap, items))))


def flatten_results(
    items: FrozenList[Result[_S, _F]]
) -> Result[FrozenList[_S], _F]:
    try:
        return Result.success(tuple(i.unwrap() for i in items))
    except UnwrapError[_S, _F] as err:
        return Result.failure(err.container.unwrap_fail())
