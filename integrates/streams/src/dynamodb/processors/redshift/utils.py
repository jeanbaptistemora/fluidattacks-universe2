# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .operations import (
    SCHEMA_NAME,
)
from .queries import (
    SQL_INSERT_HISTORIC_STR,
    SQL_INSERT_METADATA_STR,
    SQL_INSERT_VERIFICATION_VULNS_IDS,
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


def format_query_fields(table_row_class: Any) -> tuple[str, str]:
    _fields = ",".join(tuple(f.name for f in fields(table_row_class)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(table_row_class)))
    return _fields, values


def format_sql_query_metadata(
    table_name: str, _fields: list[str]
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_METADATA_STR).format(
        table=sql.Identifier(SCHEMA_NAME, table_name),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def format_sql_query_historic(
    table_historic: str, table_metadata: str, _fields: list[str]
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_HISTORIC_STR).format(
        table_historic=sql.Identifier(SCHEMA_NAME, table_historic),
        table_metadata=sql.Identifier(SCHEMA_NAME, table_metadata),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def format_sql_query_verification_vulns_ids(
    table_vulns_ids: str,
    table_metadata: str,
    _fields: list[str],
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_VERIFICATION_VULNS_IDS).format(
        table_vulns_ids=sql.Identifier(SCHEMA_NAME, table_vulns_ids),
        table_metadata=sql.Identifier(SCHEMA_NAME, table_metadata),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def get_query_fields(table_row_class: Any) -> list[str]:
    return list(f.name for f in fields(table_row_class))
