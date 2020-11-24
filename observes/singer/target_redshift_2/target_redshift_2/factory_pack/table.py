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
from target_redshift_2.objects import (
    RedshiftSchema,
    RedshiftField,
)
from target_redshift_2.singer import SingerRecord
from target_redshift_2.utils import Transform


class TableFactory(NamedTuple):
    retrieve: Transform[TableID, Optional[Table]]
    create: Transform[TableDraft, Table]
    draft_from_rschema: Transform[RedshiftSchema, TableDraft]
    tid_from_rschema: Transform[RedshiftSchema, TableID]


def draft_from_rschema_builder(
    column_from_rfield: Transform[RedshiftField, IsolatedColumn],
    tid_from_rschema_function: Transform[RedshiftSchema, TableID]
) -> Transform[RedshiftSchema, TableDraft]:
    """Builder of `draft_from_rschema`"""
    def transform(r_schema: RedshiftSchema) -> TableDraft:
        """Transform `RedshiftSchema` into a `TableDraft`"""
        table_id: TableID = tid_from_rschema_function(r_schema)
        return TableDraft(
            id=table_id, primary_keys=frozenset(),
            columns=frozenset(
                map(column_from_rfield, r_schema.fields)
            )
        )
    return transform


def tid_from_rschema(r_schema: RedshiftSchema) -> TableID:
    """Transform `RedshiftSchema` into a `TableID`"""
    return TableID(
        schema=r_schema.schema_name,
        table_name=r_schema.table_name
    )


def tid_from_srecord_builder(
    schema_name: str
) -> Transform[SingerRecord, TableID]:
    """Builder of `tid_from_srecord`"""
    def transform(srecord: SingerRecord) -> TableID:
        """Transform `SingerRecord` into a `TableID`"""
        return TableID(
            schema=schema_name,
            table_name=srecord.stream
        )
    return transform


def factory_1(
    client: Client,
    column_from_rfield: Transform[RedshiftField, IsolatedColumn]
) -> TableFactory:
    """Concrete `TableFactory` implementation #1"""

    def table_create(draft: TableDraft) -> Table:
        return table.table_builder(client, draft)

    def retrieve_table(table_id: TableID) -> Optional[Table]:
        return table.retrieve(client, table_id)

    return TableFactory(
        retrieve=retrieve_table,
        create=table_create,
        draft_from_rschema=draft_from_rschema_builder(
            column_from_rfield, tid_from_rschema
        ),
        tid_from_rschema=tid_from_rschema
    )
