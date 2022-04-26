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


class MaxRetriesReached(Exception):
    pass


def retry_cmd(
    cmd: Cmd[ResultE[_T]], max_retries: int, delay_fx: Callable[[int], float]
) -> Cmd[_T]:
    def _delay_fx(retry_num: int) -> Cmd[ResultE[_T]]:
        err = Exception("delay execution")

        def _action() -> None:
            if retry_num <= max_retries:
                LOG.info("retry #%2s waiting...", retry_num)
                sleep(delay_fx(retry_num))

        return Cmd.from_cmd(_action).map(lambda _: Result.failure(err))

    cmds = (
        from_range(range(0, max_retries + 1))
        .map(lambda i: from_flist((cmd, _delay_fx(i + 1))))
        .transform(lambda i: chain(i))
    )
    return (
        from_piter(cmds)
        .find_first(
            lambda x: x.map(lambda _: True).alt(lambda _: False).to_union()
        )
        .map(
            lambda x: x.to_result()
            .alt(lambda _: MaxRetriesReached(max_retries))
            .alt(raise_exception)
            .unwrap()
            .unwrap()
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
