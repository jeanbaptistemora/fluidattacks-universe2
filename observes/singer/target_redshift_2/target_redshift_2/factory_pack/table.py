# Standard libraries
from typing import NamedTuple, Optional
# Third party libraries
# Local libraries
from postgres_client import table
from postgres_client.client import Client
from postgres_client.table import (
    IsolatedColumn,
    Table,
    TableDraft,
    TableID,
)
from singer_io.singer import SingerRecord
from target_redshift_2.factory_pack import columns as columns_factory
from target_redshift_2.objects import (
    RedshiftSchema,
    RedshiftField,
)

from target_redshift_2.utils import Transform


class TableFactory(NamedTuple):
    retrieve: Transform[TableID, Optional[Table]]
    create: Transform[TableDraft, Table]


class TableIDFactory(NamedTuple):
    rschema_to_tid: Transform[RedshiftSchema, TableID]
    srecord_to_tid: Transform[RedshiftSchema, TableID]


class TableDraftFactory(NamedTuple):
    rschema_to_tdraft: Transform[RedshiftSchema, TableDraft]


def _rschema_to_tdraft(
    r_schema: RedshiftSchema,
    rfield_to_column: Transform[RedshiftField, IsolatedColumn],
    rschema_to_tid: Transform[RedshiftSchema, TableID]
) -> TableDraft:
    table_id: TableID = rschema_to_tid(r_schema)
    return TableDraft(
        id=table_id, primary_keys=frozenset(),
        columns=frozenset(
            map(rfield_to_column, r_schema.fields)
        )
    )


def _rschema_to_tid(r_schema: RedshiftSchema) -> TableID:
    return TableID(
        schema=r_schema.schema_name,
        table_name=r_schema.table_name
    )


def _srecord_to_tid(srecord: SingerRecord, schema_name: str) -> TableID:
    return TableID(
        schema=schema_name,
        table_name=srecord.stream
    )


def table_factory(client: Client) -> TableFactory:

    def table_create(draft: TableDraft) -> Table:
        return table.table_builder(client, draft)

    def retrieve_table(table_id: TableID) -> Optional[Table]:
        return table.retrieve(client, table_id)

    return TableFactory(
        retrieve=retrieve_table,
        create=table_create,
    )


def tableid_factory(db_schema: str) -> TableIDFactory:

    def srecord_to_tid(record: SingerRecord) -> Table:
        return _srecord_to_tid(record, db_schema)

    return TableIDFactory(
        rschema_to_tid=_rschema_to_tid,
        srecord_to_tid=srecord_to_tid,
    )


def tabledraft_factory(db_schema: str) -> TableDraftFactory:
    tid_factory = tableid_factory(db_schema)

    def rschema_to_tdraft(schema: RedshiftSchema) -> TableDraft:
        return _rschema_to_tdraft(
            schema, columns_factory.from_rfield, tid_factory.rschema_to_tid
        )

    return TableDraftFactory(
        rschema_to_tdraft=rschema_to_tdraft
    )
