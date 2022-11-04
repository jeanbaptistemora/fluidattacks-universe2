# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..queries import (
    SQL_INSERT_METADATA,
)
from ..utils import (
    format_sql_query,
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
    extras,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from redshift.operations import (
    execute,
)


async def insert_metadata(
    *,
    item: Item,
) -> None:
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    await execute(
        format_sql_query(SQL_INSERT_METADATA, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_batch_metadata(
    *,
    cursor: cursor_cls,
    items: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = [format_row_metadata(finding) for finding in items]
    sql_query = format_sql_query(
        SQL_INSERT_METADATA, METADATA_TABLE, sql_fields
    )
    extras.execute_batch(cursor, sql_query, sql_values, page_size=1000)
