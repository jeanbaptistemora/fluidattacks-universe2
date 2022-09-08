# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Cmd,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from requests.exceptions import (
    HTTPError,
)
from time import (
    sleep,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


class MaxRetriesReached(Exception):
    pass


def retry_cmd(
    cmd: Cmd[Result[_S, _F]],
    max_retries: int,
    delay_fx: Callable[[int], float],
) -> Cmd[Result[_S, MaxRetriesReached]]:
    def _delay_fx(err: _F, retry_num: int) -> Cmd[Result[_S, _F]]:
        def _action() -> None:
            if retry_num <= max_retries:
                LOG.info("retry #%2s waiting...", retry_num)
                sleep(delay_fx(retry_num))

        return Cmd.from_cmd(_action).map(lambda _: Result.failure(err))

    def _cmd_with_delay(
        index: int, result: Result[_S, _F]
    ) -> Cmd[Result[_S, _F]]:
        return (
            result.map(lambda _: Cmd.from_cmd(lambda: result))
            .alt(lambda e: _delay_fx(e, index + 1))
            .to_union()
        )

    cmds = from_range(range(0, max_retries + 1)).map(
        lambda i: cmd.bind(lambda r: _cmd_with_delay(i, r))
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


def api_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    def _action(act: CmdUnwrapper) -> ResultE[_T]:
        try:
            return Result.success(act.unwrap(cmd))
        except HTTPError as err:  # type: ignore[misc]
            err_code: int = err.response.status_code  # type: ignore[misc]
            # 429: Too Many Requests
            if err_code in (429,):
                return Result.failure(err)
            raise err

    return new_cmd(_action)
