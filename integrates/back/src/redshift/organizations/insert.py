# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..utils import (
    format_sql_query_historic,
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    METADATA_TABLE,
    STATE_TABLE,
)
from .types import (
    MetadataTableRow,
    StateTableRow,
)
from .utils import (
    format_row_metadata,
    format_row_state,
)
from dynamodb.types import (
    Item,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)


def insert_historic_state(
    *,
    cursor: cursor_cls,
    historic_state: tuple[Item, ...],
    organization_id: str,
) -> None:
    sql_fields = get_query_fields(StateTableRow)
    sql_values = [
        format_row_state(state, organization_id) for state in historic_state
    ]
    cursor.executemany(
        format_sql_query_historic(STATE_TABLE, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_metadata(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    cursor.execute(
        format_sql_query_metadata(METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_organization(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    insert_metadata(cursor=cursor, item=item)
    insert_historic_state(
        cursor=cursor,
        historic_state=(item["state"],),
        organization_id=str(item["pk"]).split("#")[1],
    )
