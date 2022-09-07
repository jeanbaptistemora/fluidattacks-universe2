# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _truncate,
)
from ._grouper import (
    PackagedSinger,
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
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_purity.result.transform import (
    all_ok,
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
from typing import (
    cast,
    Dict,
    Iterable,
    Tuple,
)

LOG = logging.getLogger(__name__)
StreamTables = FrozenDict[str, Tuple[TableId, Table]]


def _in_threads(cmds: PureIter[Cmd[None]], nodes: int) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        pool = ThreadPool(nodes=nodes)  # type: ignore[misc]
        results: Iterable[None] = cast(Iterable[None], pool.imap(lambda c: act.unwrap(c), cmds))  # type: ignore[misc]
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
                MissingKey(f"on non-nullable column `{c.name}`", table)
            )
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
        cmds = chunks.map(
            lambda p: self.client.insert(
                tar.table_id,
                tar.table,
                from_flist(p),
            )
            + Cmd.from_cmd(lambda: LOG.debug("insert done!"))
        )
        return _in_threads(cmds, self.options.pkg_threads)

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
        if isinstance(item, SingerSchema):
            _item = item  # dummy var for fixing mypy error
            return state.freeze().bind(
                lambda t: self.create_table(_item)
                + state.update(self.update_stream_tables(t, _item))
            )
        if isinstance(item, SingerState):
            raise NotImplementedError()
        _item_2 = item
        return state.freeze().bind(lambda t: self.record_handler(t, _item_2))
