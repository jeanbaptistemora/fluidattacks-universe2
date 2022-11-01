# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .operations import (
    SCHEMA_NAME,
)
from dataclasses import (
    fields,
)
from psycopg2 import (
    sql,
)
from typing import (
    Any,
)


def format_sql_query(
    query: str, table_name: str, _fields: list[str]
) -> sql.Composed:
    return sql.SQL(query).format(
        table=sql.Identifier(SCHEMA_NAME, table_name),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def get_query_fields(table_row_class: Any) -> list[str]:
    return list(f.name for f in fields(table_row_class))
