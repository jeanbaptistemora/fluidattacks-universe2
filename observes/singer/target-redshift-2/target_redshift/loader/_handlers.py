# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    SingerLoader,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    JsonValue,
    Maybe,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
    SingerState,
)
import logging
from pathos.threading import ThreadPool  # type: ignore[import]
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.sql_client import (
    RowData,
)
from redshift_client.table.client import (
    TableClient,
)
from redshift_client.table.core import (
    Table,
)
from target_redshift.data_schema import (
    extract_table,
)
from target_redshift.errors import (
    MissingKey,
)
from target_redshift.loader import (
    _truncate,
)
from target_redshift.loader._grouper import (
    PackagedSinger,
)
from typing import (
    cast,
    Dict,
    Iterable,
    Tuple,
)

LOG = logging.getLogger(__name__)
StreamTables = FrozenDict[str, Tuple[TableId, Table]]


def _in_threads(commands: PureIter[Cmd[None]], nodes: int) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        pool = ThreadPool(nodes=nodes)  # type: ignore[misc]
        results: Iterable[None] = cast(Iterable[None], pool.imap(lambda c: act.unwrap(c), commands))  # type: ignore[misc]
        for _ in results:
            # compute ThreadPool jobs
            pass

    return new_cmd(_action)


def _to_row(table: Table, record: SingerRecord) -> ResultE[RowData]:
    return pure_map(
        lambda c: Maybe.from_optional(record.record.get(c.name))
        .to_result()
        .alt(Exception)
        .lash(
            lambda _: Result.success(JsonValue(None), Exception)
            if table.columns[c].nullable
            else Result.failure(
                MissingKey(f"on non-nullable column `{c.name}`", table),
                JsonValue,
            ).alt(Exception)
        )
        .bind(lambda x: Unfolder(x).to_any_primitive()),
        table.order,
    ).transform(lambda x: all_ok(tuple(x)).map(lambda d: RowData(d)))


@dataclass(frozen=True)
class _TableAndRecords:
    table_id: TableId
    table: Table
    records: PureIter[SingerRecord]


@dataclass(frozen=True)
class MutableTableMap:
    _table_map: Dict[str, Tuple[TableId, Table]]

    def update(
        self, items: FrozenDict[str, Tuple[TableId, Table]]
    ) -> Cmd[None]:
        return Cmd.from_cmd(lambda: self._table_map.update(items))

    def freeze(self) -> Cmd[StreamTables]:
        return Cmd.from_cmd(lambda: FrozenDict(self._table_map))


@dataclass(frozen=True)
class SingerHandlerOptions:
    truncate_str: bool
    records_per_query: int
    pkg_threads: int


@dataclass(frozen=True)
class SingerHandler:
    schema: SchemaId
    client: TableClient
    options: SingerHandlerOptions

    def create_table(self, schema: SingerSchema) -> Cmd[None]:
        table_id = TableId(self.schema, schema.stream)
        table = extract_table(schema).unwrap()
        return self.client.new(table_id, table)

    def update_stream_tables(
        self, table_map: StreamTables, schema: SingerSchema
    ) -> StreamTables:
        table_id = TableId(self.schema, schema.stream)
        table = extract_table(schema).unwrap()
        return (
            FrozenDict(dict(table_map) | {schema.stream: (table_id, table)})
            if schema.stream not in table_map
            else table_map
        )

    def _upload_records(self, tar: _TableAndRecords) -> Cmd[None]:
        chunks = tar.records.map(
            lambda r: _to_row(tar.table, r)
            .map(
                lambda d: _truncate.truncate_row(tar.table, d)
                if self.options.truncate_str
                else d
            )
            .unwrap()
        ).chunked(self.options.records_per_query)
        commands = chunks.map(
            lambda p: self.client.insert(
                tar.table_id,
                tar.table,
                from_flist(p),
                1000,
            )
            + Cmd.from_cmd(lambda: LOG.debug("insert done!"))
        )
        return _in_threads(commands, self.options.pkg_threads)

    def record_handler(
        self, table_map: StreamTables, records: PureIter[SingerRecord]
    ) -> Cmd[None]:
        tables = frozenset(records.map(lambda r: r.stream))
        grouped = pure_map(
            lambda t: Maybe.from_optional(table_map.get(t)).map(
                lambda u: _TableAndRecords(
                    u[0], u[1], records.filter(lambda r: r.stream == t)
                )
            ),
            tuple(tables),
        )
        return grouped.map(
            lambda m: m.map(self._upload_records).unwrap()
        ).transform(lambda x: _in_threads(x, 100))

    def handle(
        self, state: MutableTableMap, item: PackagedSinger
    ) -> Cmd[None]:
        return item.map(
            lambda records: state.freeze().bind(
                lambda t: self.record_handler(t, records)
            ),
            lambda schema: state.freeze().bind(
                lambda t: self.create_table(schema)
                + state.update(self.update_stream_tables(t, schema))
            ),
            lambda _: raise_exception(NotImplementedError()),
        )

    def loader(self, state: MutableTableMap) -> SingerLoader:
        return SingerLoader.new(lambda p: self.handle(state, p))
