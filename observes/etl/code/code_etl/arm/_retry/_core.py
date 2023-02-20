from fa_purity import (
    Cmd,
    Result,
)
from fa_purity.pure_iter.factory import (
    from_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from typing import (
    Callable,
    TypeVar,
)

_S = TypeVar("_S")
_F = TypeVar("_F")


class MaxRetriesReached(Exception):
    pass


def retry_cmd(
    cmd: Cmd[Result[_S, _F]],
    next_cmd: Callable[[int, Result[_S, _F]], Cmd[Result[_S, _F]]],
    max_retries: int,
) -> Cmd[Result[_S, MaxRetriesReached]]:
    cmds = from_range(range(0, max_retries + 1)).map(
        lambda i: cmd.bind(lambda r: next_cmd(i + 1, r))
    )
    return (
        from_piter(cmds)
        .find_first(
            lambda x: x.map(lambda _: True).alt(lambda _: False).to_union()
        )
        .map(
            lambda x: x.map(lambda r: r.unwrap())
            .to_result()
            .alt(lambda _: MaxRetriesReached(max_retries))
        )
    )
