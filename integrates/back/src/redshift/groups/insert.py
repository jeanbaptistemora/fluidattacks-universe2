# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..utils import (
    format_sql_query_historic,
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    CODE_LANGUAGES_TABLE,
    METADATA_TABLE,
    STATE_TABLE,
    UNFULFILLED_STANDARDS_TABLE,
)
from .types import (
    CodeLanguagesTableRow,
    MetadataTableRow,
    StateTableRow,
)
from .utils import (
    format_row_code_languages,
    format_row_metadata,
    format_row_state,
    format_row_unfulfilled_standards,
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
    unreliable_indicators: Item,
) -> None:
    sql_fields = get_query_fields(CodeLanguagesTableRow)
    sql_values = format_row_code_languages(unreliable_indicators)
    if not sql_values:
        return
    cursor.executemany(
        format_sql_query_metadata(CODE_LANGUAGES_TABLE, sql_fields),
        sql_values,
    )


def insert_historic_state(
    *,
    cursor: cursor_cls,
    historic_state: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(StateTableRow)
    sql_values = [format_row_state(state) for state in historic_state]
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


def insert_unfulfilled_standards(
    *,
    cursor: cursor_cls,
    unreliable_indicators: Item,
) -> None:
    sql_fields = get_query_fields(CodeLanguagesTableRow)
    sql_values = format_row_unfulfilled_standards(unreliable_indicators)
    if not sql_values:
        return
    cursor.executemany(
        format_sql_query_metadata(UNFULFILLED_STANDARDS_TABLE, sql_fields),
        sql_values,
    )
