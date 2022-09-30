# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
)

from ._grouper import (
    PackagedSinger,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
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
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
    SingerState,
)
import logging
from pathos.threading import ThreadPool  # type: ignore[import]
from target_snowflake._patch import (
    Patch,
)
from target_snowflake.data_schema import (
    extract_table,
)
from target_snowflake.snowflake_client.schema import (
    SchemaManager,
    TableId,
    TableObj,
)
from target_snowflake.snowflake_client.sql_client import (
    Identifier,
    RowData,
)
from target_snowflake.snowflake_client.table import (
    ColumnId,
    Table,
)
from typing import (
    Callable,
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


def _transform_keys(record: SingerRecord) -> FrozenDict[ColumnId, JsonValue]:
    return FrozenDict(
        {ColumnId(Identifier.from_raw(k)): v for k, v in record.record.items()}
    )


def _to_row(table: Table, record: SingerRecord) -> ResultE[RowData]:
    _record = _transform_keys(record)
    return pure_map(
        lambda c: Maybe.from_optional(_record.get(c))
        .to_result()
        .alt(Exception)
        .lash(
            lambda _: Result.success(JsonValue(None), Exception)
            if table.columns[c].nullable
            else Result.failure(
                KeyError(f"on non-nullable column `{c}`", table)
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
class _Private:
    pass


@dataclass(frozen=True)
class SingerHandlerOptions:
    records_per_query: int
    pkg_threads: int


@dataclass(frozen=True)
class SingerHandler:
    _inner: _Private = field(repr=False, hash=False, compare=False)
    _build_manager: Patch[Callable[[], Cmd[SchemaManager]]]
    options: SingerHandlerOptions

    @staticmethod
    def new(
        manager_builder: Callable[[], Cmd[SchemaManager]],
        options: SingerHandlerOptions,
    ) -> SingerHandler:
        return SingerHandler(_Private(), Patch(manager_builder), options)

    @staticmethod
    def _target_table(schema: SingerSchema) -> TableId:
        return TableId(Identifier.from_raw(schema.stream))

    def _new_manager(self) -> Cmd[SchemaManager]:
        return self._build_manager.inner()

    def create_table(self, schema: SingerSchema) -> Cmd[None]:
        table_id = self._target_table(schema)
        table = extract_table(schema).unwrap()
        return self._new_manager().bind(
            lambda m: m.create(TableObj(table_id, table), False)
        )

    def update_stream_tables(
        self, table_map: StreamTables, schema: SingerSchema
    ) -> StreamTables:
        table_id = self._target_table(schema)
        table = extract_table(schema).unwrap()
        return (
            FrozenDict(dict(table_map) | {schema.stream: (table_id, table)})
            if schema.stream not in table_map
            else table_map
        )

    def _upload_records_chunk(
        self, table: TableObj, chunk: FrozenList[RowData]
    ) -> Cmd[None]:
        # [!] Each chunk must have its own independent cursor for enabling threads execution
        client = self._new_manager().map(
            lambda m: m.table_manager(table.id_obj)
        )
        return client.bind(
            lambda c: c.insert(
                table.table,
                from_flist(chunk),
                self.options.records_per_query,
            )
        )

    def _upload_records(self, tar: _TableAndRecords) -> Cmd[None]:
        chunks = tar.records.map(
            lambda r: _to_row(tar.table, r).unwrap()
        ).chunked(self.options.records_per_query)
        table = TableObj(tar.table_id, tar.table)
        cmds = chunks.map(
            lambda c: self._upload_records_chunk(table, c)
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
