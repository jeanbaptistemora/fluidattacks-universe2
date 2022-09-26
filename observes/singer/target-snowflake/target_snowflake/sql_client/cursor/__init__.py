# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _assert,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
    Stream,
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
from fa_purity.pure_iter.factory import (
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    until_empty,
)
from fa_purity.utils import (
    raise_exception,
)
from logging import (
    Logger,
)
from target_snowflake.sql_client._inner import (
    RawCursor,
)
from target_snowflake.sql_client.query import (
    Query,
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
            self._log.info(
                "Executing: %s with values %s", query.statement, query.values
            )
            self._cursor.cursor.execute(query.statement, dict(query.values))  # type: ignore[misc]

        return Cmd.from_cmd(_action)

    def fetch_one(self) -> Cmd[Maybe[RowData]]:
        def _action() -> Maybe[RowData]:
            self._log.debug("Fetching one row")
            return Maybe.from_optional(
                _assert.assert_fetch_one(
                    self._cursor.cursor.fetchone()  # type: ignore[misc]
                )
                .alt(raise_exception)
                .unwrap()
            ).map(RowData)

        return Cmd.from_cmd(_action)

    def fetch_all(self) -> Cmd[FrozenList[RowData]]:
        def _action() -> FrozenList[RowData]:
            self._log.debug("Fetching all rows")
            items = _assert.assert_fetch_list(tuple(self._cursor.cursor.fetchall()))  # type: ignore[misc]
            return (
                items.map(lambda l: tuple(map(RowData, l)))
                .alt(raise_exception)
                .unwrap()
            )

        return Cmd.from_cmd(_action)

    def fetch_many(self, chunk: int) -> Cmd[FrozenList[RowData]]:
        def _action() -> FrozenList[RowData]:
            self._log.debug("Fetching %s rows", chunk)
            items = _assert.assert_fetch_list(tuple(self._cursor.cursor.fetchmany(chunk)))  # type: ignore[misc, no-untyped-call]
            return (
                items.map(lambda l: tuple(map(RowData, l)))
                .alt(raise_exception)
                .unwrap()
            )

        return Cmd.from_cmd(_action)

    def data_chunks_stream(self, chunk: int) -> Stream[FrozenList[RowData]]:
        return (
            infinite_range(0, 1)
            .map(
                lambda _: self.fetch_many(chunk).map(
                    lambda i: Maybe.from_optional(i if i else None)
                )
            )
            .transform(lambda i: from_piter(i))
            .transform(lambda i: until_empty(i))
        )
