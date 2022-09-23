# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._inner import (
    RawCursor,
)
from .query import (
    Query,
)
from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json.primitive import (
    Primitive,
)
from logging import (
    Logger,
)


@dataclass(frozen=True)
class RowData:
    data: FrozenList[Primitive]


@dataclass(frozen=True)
class Cursor:
    _log: Logger
    _cursor: RawCursor

    def execute(self, query: Query) -> Cmd[None]:
        def _action() -> None:
            self._log.info("Executing: %s", query.statement)
            self._cursor.cursor.execute(query.statement, dict(query.values))  # type: ignore[misc]

        return Cmd.from_cmd(_action)
