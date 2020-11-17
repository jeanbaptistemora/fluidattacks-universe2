# Standard libraries
from typing import NamedTuple, Optional
# Third party libraries
# Local libraries
from target_redshift_2.db_client.objects import (
    IsolatedColumn,
    SchemaID,
    Table,
    TableDraft,
    TableID,
)
from target_redshift_2.objects import (
    RedshiftSchema,
    RedshiftField,
)
from target_redshift_2.utils import Transform


class TableFactory(NamedTuple):
    retrieve: Transform[TableID, Optional[Table]]
    create: Transform[TableDraft, Table]
    from_rschema: Transform[RedshiftSchema, TableDraft]


def from_rschema_builder(
    from_rfield: Transform[RedshiftField, IsolatedColumn],
) -> Transform[RedshiftSchema, TableDraft]:
    """Transform `RedshiftSchema` into a `TableDraft`"""
    def transform(r_schema: RedshiftSchema) -> TableDraft:
        table_id = TableID(
            schema=SchemaID(None, r_schema.schema_name),
            table_name=r_schema.table_name
        )
        return TableDraft(
            id=table_id, primary_keys=frozenset(),
            columns=frozenset(
                map(from_rfield, r_schema.fields)
            )
        )
    return transform
