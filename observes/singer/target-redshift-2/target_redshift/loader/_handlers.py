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
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
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
    Dict,
    Tuple,
)

StreamTables = FrozenDict[str, Tuple[TableId, Table]]


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
class SingerHandler:
    schema: SchemaId
    client: TableClient
    truncate_str: bool

    def schema_handler(
        self, table_map: StreamTables, schema: SingerSchema
    ) -> Tuple[StreamTables, Cmd[None]]:
        table_id = TableId(self.schema, schema.stream)
        table = extract_table(schema).unwrap()
        new_table_map = (
            FrozenDict(dict(table_map) | {schema.stream: (table_id, table)})
            if schema.stream not in table_map
            else table_map
        )
        return (new_table_map, self.client.new(table_id, table))

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
            lambda m: m.map(
                lambda tar: self.client.insert(
                    tar.table_id,
                    tar.table,
                    tar.records.map(
                        lambda r: _to_row(tar.table, r)
                        .map(
                            lambda d: _truncate.truncate_row(tar.table, d)
                            if self.truncate_str
                            else d
                        )
                        .unwrap()
                    ),
                )
            ).unwrap()
        ).transform(consume)

    def handle(
        self, state: MutableTableMap, item: PackagedSinger
    ) -> Cmd[None]:
        if isinstance(item, SingerSchema):
            _item = item  # dummy var for fixing mypy error

            def _handler(result: Tuple[StreamTables, Cmd[None]]) -> Cmd[None]:
                return result[1] + state.update(result[0])

            return state.freeze().bind(
                lambda t: _handler(self.schema_handler(t, _item))
            )
        if isinstance(item, SingerState):
            raise NotImplementedError()
        _item_2 = item
        return state.freeze().bind(lambda t: self.record_handler(t, _item_2))
