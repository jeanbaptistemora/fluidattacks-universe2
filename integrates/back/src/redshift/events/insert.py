# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..queries import (
    SQL_INSERT_METADATA,
    SQL_INSERT_METADATA_STR,
)
from ..utils import (
    format_query_fields,
    get_query_fields,
)
from .initialize import (
    METADATA_TABLE,
)
from .types import (
    MetadataTableRow,
)
from .utils import (
    format_row_metadata,
)
from dynamodb.types import (
    Item,
)
from psycopg2 import (
    sql,
)
from redshift.operations import (
    execute,
    execute_batch,
    SCHEMA_NAME,
)


async def insert_metadata(
    *,
    item: Item,
) -> None:
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    await execute(
        sql.SQL(SQL_INSERT_METADATA_STR).format(
            table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
            fields=sql.SQL(", ").join(map(sql.Identifier, sql_fields)),
            values=sql.SQL(", ").join(map(sql.Placeholder, sql_fields)),
        ),
        sql_values,
    )


async def insert_batch_metadata(
    *,
    items: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = [format_row_metadata(finding) for finding in items]
    await execute_batch(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=f"{SCHEMA_NAME}.{METADATA_TABLE}",
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
