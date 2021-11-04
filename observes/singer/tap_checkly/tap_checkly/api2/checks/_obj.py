from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    Patch,
)
from returns.io import (
    IO,
)
from tap_checkly.api2.objs.check.result import (
    RolledUpResultObj,
)
from tap_checkly.api2.objs.id_objs import (
    CheckId,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class ChecksApi:
    _ids: Patch[Callable[[int], IO[FrozenList[CheckId]]]]
    _rolled_up_results: Patch[
        Callable[[CheckId, int], IO[FrozenList[RolledUpResultObj]]]
    ]

    def ids(self, page: int) -> IO[FrozenList[CheckId]]:
        return self._ids.unwrap(page)

    def rolled_up_results(
        self, check: CheckId, page: int
    ) -> IO[FrozenList[RolledUpResultObj]]:
        return self._rolled_up_results.unwrap(check, page)
