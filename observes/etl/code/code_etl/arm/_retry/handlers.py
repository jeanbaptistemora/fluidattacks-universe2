from code_etl.arm._error import (
    ApiError,
)
from fa_purity import (
    Cmd,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.json.value.factory import (
    from_any,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result import (
    ResultFactory,
)
from gql.transport.exceptions import (
    TransportQueryError,
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


def api_error_handler(cmd: Cmd[_T]) -> Cmd[Result[_T, ApiError]]:
    factory: ResultFactory[_T, ApiError] = ResultFactory()

    def _action(unwrapper: CmdUnwrapper) -> Result[_T, ApiError]:
        try:
            return factory.success(unwrapper.act(cmd))
        except TransportQueryError as err:  # type: ignore[misc]
            errors = from_any(err).bind(lambda x: Unfolder(x).to_list())
            return factory.failure(ApiError(errors.unwrap()))

    return Cmd.new_cmd(_action)


def too_many_requests_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    return http_status_handler(lambda c: c == 429, cmd)


def server_error_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    return http_status_handler(lambda c: c in range(500, 600), cmd)
