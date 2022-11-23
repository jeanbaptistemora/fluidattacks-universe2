from fa_purity import (
    Cmd,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def log_cmd(log_action: Callable[[], None], item: _T) -> Cmd[_T]:
    def _action() -> _T:
        log_action()
        return item

    return Cmd.from_cmd(_action)
