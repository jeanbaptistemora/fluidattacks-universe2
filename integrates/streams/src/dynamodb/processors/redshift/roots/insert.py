# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..queries import (
    SQL_INSERT_METADATA,
)
from ..utils import (
    format_query_fields,
)
from .initialize import (
    CODE_LANGUAGES_TABLE,
    ENVIRONMENT_URL_TABLE,
    METADATA_TABLE,
)
from .types import (
    CodeLanguagesTableRow,
    EnvironmentUrlTableRow,
    MetadataTableRow,
)
from .utils import (
    format_row_code_languages,
    format_row_environment_url,
    format_row_metadata,
)
from dynamodb.types import (
    Item,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)


def insert_code_languages(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    _fields, values = format_query_fields(CodeLanguagesTableRow)
    sql_values = format_row_code_languages(item=item)
    cursor.executemany(  # nosec
        SQL_INSERT_METADATA.substitute(
            table_metadata=METADATA_TABLE,
            table_historic=CODE_LANGUAGES_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_environment_url(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    _fields, values = format_query_fields(EnvironmentUrlTableRow)
    sql_values = format_row_environment_url(item)
    cursor.execute(
        SQL_INSERT_METADATA.substitute(
            table=ENVIRONMENT_URL_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_metadata(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    cursor.execute(
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
