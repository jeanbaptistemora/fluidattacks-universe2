from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.cmd.core import (
    unsafe_unwrap,
)
from pathos.pp import ParallelPool  # type: ignore[import]
from typing import (
    cast,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


def parallel_cmds(
    cmds: FrozenList[Cmd[_T]], nodes: Optional[int]
) -> Cmd[FrozenList[_T]]:
    def _action() -> FrozenList[_T]:
        pool = ParallelPool(nodes=nodes) if nodes else ParallelPool()  # type: ignore[misc]
        results = cast(
            FrozenList[_T],
            tuple(pool.map(unsafe_unwrap, cmds)),  # type: ignore[misc]
        )
        # unsafe_unwrap is used instead of CmdUnwrapper because `act` method cannot be processed by the pool
        return results

    return Cmd.from_cmd(_action)
