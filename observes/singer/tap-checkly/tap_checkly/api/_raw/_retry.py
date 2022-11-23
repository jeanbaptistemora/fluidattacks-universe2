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
import logging
from time import (
    sleep,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
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
        lambda i: cmd.bind(lambda r: next_cmd(i, r))
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


def delay(
    index: int,
    result: Result[_S, _F],
    max_retries: int,
    delay_fx: Callable[[int], float],
) -> Cmd[Result[_S, _F]]:
    def _delay_fx(err: _F, retry_num: int) -> Cmd[Result[_S, _F]]:
        def _action() -> None:
            if retry_num <= max_retries:
                LOG.info("retry #%2s waiting...", retry_num)
                sleep(delay_fx(retry_num))

        return Cmd.from_cmd(_action).map(lambda _: Result.failure(err))

    return (
        result.map(lambda _: Cmd.from_cmd(lambda: result))
        .alt(lambda e: _delay_fx(e, index + 1))
        .to_union()
    )
