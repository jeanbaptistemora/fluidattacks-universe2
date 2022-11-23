from ..utils import (
    format_sql_query_historic,
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    CODE_LANGUAGES_TABLE,
    METADATA_TABLE,
    STATE_TABLE,
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
    group_name: str,
    historic_state: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(StateTableRow)
    sql_values = [
        format_row_state(group_name, state) for state in historic_state
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


def insert_group(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    insert_metadata(cursor=cursor, item=item)
    insert_historic_state(
        cursor=cursor,
        group_name=str(item["pk"]).split("#")[1],
        historic_state=(item["state"],),
    )
