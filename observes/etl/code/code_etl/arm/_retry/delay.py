from fa_purity import (
    Cmd,
    Result,
)
from fa_purity.result import (
    ResultFactory,
)
import logging
from time import (
    sleep,
)
from typing import (
    TypeVar,
)

LOG = logging.getLogger(__name__)

_S = TypeVar("_S")
_F = TypeVar("_F")


def sleep_delay(delay: float) -> Cmd[None]:
    return Cmd.from_cmd(lambda: sleep(delay))


def delay_if_fail(
    retry: int,
    prev: Result[_S, _F],
    delay: float,
) -> Cmd[Result[_S, _F]]:
    info = Cmd.from_cmd(lambda: LOG.info("retry #%2s waiting...", retry))
    factory: ResultFactory[_S, _F] = ResultFactory()
    return (
        prev.map(lambda _: Cmd.from_cmd(lambda: prev))
        .alt(
            lambda e: info
            + sleep_delay(delay).map(lambda _: factory.failure(e))
        )
        .to_union()
    )
