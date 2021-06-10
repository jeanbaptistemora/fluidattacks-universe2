import logging
from postgres_client.table import (
    TableFactory,
)
from singer_io.singer import (
    SingerSchema,
)
from target_redshift.batcher import (
    Batcher,
)
from target_redshift.data_schema import (
    RedshiftSchema,
)
from typing import (
    Dict,
)

LOG = logging.getLogger(__name__)
SchemasMap = Dict[str, RedshiftSchema]


def schema_handler(
    batcher: Batcher,
    table_factory: TableFactory,
    db_schema: str,
    s_schema: SingerSchema,
    schemas: SchemasMap,
) -> SchemasMap:
    r_schema = RedshiftSchema(db_schema, s_schema)
    modified_map = False
    schemas_map = schemas.copy()
    tname = r_schema.table.table_id.table_name
    if tname not in schemas_map:
        schemas_map[tname] = r_schema
        modified_map = True

    batcher.set_field_names(
        tname, list(map(lambda col: col.name, r_schema.table.columns))
    )
    table_factory.new_table(r_schema.table, True)
    if not modified_map:
        return schemas
    return schemas_map
