# Standard libraries
from typing import NamedTuple, Optional
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import (
    Client,
    ConnectionID,
    IsolatedColumn,
    SchemaID,
    Table,
    TableDraft,
    TableID,
)
from target_redshift_2.db_client.factory import (
    CursorActionFactory,
    TableFactory as DBTableFactory,
)
from target_redshift_2.db_client import prototypes
from target_redshift_2.objects import (
    RedshiftSchema,
    RedshiftField,
)
from target_redshift_2.utils import Transform


class TableFactory(NamedTuple):
    retrieve: Transform[TableID, Optional[Table]]
    create: Transform[TableDraft, Table]
    draft_from_rschema: Transform[RedshiftSchema, TableDraft]
    tid_from_rschema: Transform[RedshiftSchema, TableID]


def draft_from_rschema_builder(
    column_from_rfield: Transform[RedshiftField, IsolatedColumn],
    tid_from_rschema: Transform[RedshiftSchema, TableID]
) -> Transform[RedshiftSchema, TableDraft]:
    """Builder of `draft_from_rschema`"""
    def transform(r_schema: RedshiftSchema) -> TableDraft:
        """Transform `RedshiftSchema` into a `TableDraft`"""
        table_id: TableID = tid_from_rschema(r_schema)
        return TableDraft(
            id=table_id, primary_keys=frozenset(),
            columns=frozenset(
                map(column_from_rfield, r_schema.fields)
            )
        )
    return transform


def tid_from_rschema_builder(connection: ConnectionID):
    """Builder of `tid_from_rschema`"""
    def transform(r_schema: RedshiftSchema) -> TableID:
        """Transform `RedshiftSchema` into a `TableID`"""
        return TableID(
            schema=SchemaID(connection, r_schema.schema_name),
            table_name=r_schema.table_name
        )
    return transform


def factory_1(
    client: Client,
    connection: ConnectionID,
    column_from_rfield: Transform[RedshiftField, IsolatedColumn]
) -> TableFactory:
    """Concrete `TableFactory` implementation #1"""
    db_table_factory = DBTableFactory(
        db_client=client,
        c_action_factory=CursorActionFactory(client.cursor)
    )
    tid_from_rschema = tid_from_rschema_builder(connection)
    table_prototype = prototypes.table_prototype_1(client.execute)

    def table_create(draft: TableDraft):
        table = Table(
            draft.id, draft.primary_keys, draft.columns,
            prototype=table_prototype
        )
        return db_table_factory.create(table)
    return TableFactory(
        retrieve=db_table_factory.retrieve,
        create=table_create,
        draft_from_rschema=draft_from_rschema_builder(
            column_from_rfield, tid_from_rschema
        ),
        tid_from_rschema=tid_from_rschema
    )
