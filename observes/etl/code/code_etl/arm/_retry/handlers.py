from fa_purity import (
    Cmd,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.result import (
    ResultFactory,
)
from gql.transport.exceptions import (
    TransportServerError,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def http_status_handler(
    is_handled: Callable[[int], bool], cmd: Cmd[_T]
) -> Cmd[ResultE[_T]]:
    factory: ResultFactory[_T, Exception] = ResultFactory()

    def _action(unwrapper: CmdUnwrapper) -> ResultE[_T]:
        try:
            return factory.success(unwrapper.act(cmd))
        except TransportServerError as err:
            if err.code is not None and is_handled(err.code):
                return factory.failure(err)
            raise err

    return Cmd.new_cmd(_action)


def too_many_requests_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    return http_status_handler(lambda c: c == 429, cmd)


def server_error_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    return http_status_handler(lambda c: c in range(500, 600), cmd)
