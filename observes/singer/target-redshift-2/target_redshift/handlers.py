from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    PureIter,
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
from typing import (
    Dict,
    Tuple,
)

StreamTables = FrozenDict[str, Tuple[TableId, Table]]


def _to_row(table: Table, record: SingerRecord) -> ResultE[RowData]:
    return pure_map(
        lambda c: Maybe.from_optional(record.record.get(c.name))
        .to_result()
        .alt(lambda _: Exception(f"Missing key `{c.name}` on the record"))
        .bind(lambda x: Unfolder(x).to_any_primitive()),
        table.order,
    ).transform(lambda x: all_ok(tuple(x)).map(lambda d: RowData(d)))


@dataclass(frozen=True)
class _TableAndRecords:
    table_id: TableId
    table: Table
    records: PureIter[SingerRecord]


@dataclass(frozen=True)
class SingerHandler:
    schema: SchemaId
    client: TableClient

    def schema_handler(self, schema: SingerSchema) -> Cmd[None]:
        table_id = TableId(self.schema, schema.stream)
        table = extract_table(schema).unwrap()
        return self.client.new(table_id, table)

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
                    tar.records.map(lambda r: _to_row(tar.table, r).unwrap()),
                )
            ).unwrap()
        ).transform(consume)
