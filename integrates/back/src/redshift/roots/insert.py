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
    METADATA_TABLE,
)
from .types import (
    CodeLanguagesTableRow,
    MetadataTableRow,
)
from .utils import (
    format_row_code_languages,
    format_row_metadata,
)
from dynamodb.types import (
    Item,
)
from redshift.operations import (
    execute,
    execute_many,
)


async def insert_code_languages(
    *,
    item: Item,
) -> None:
    _fields, values = format_query_fields(CodeLanguagesTableRow)
    sql_values = format_row_code_languages(item=item)
    if not sql_values:
        return
    await execute_many(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=CODE_LANGUAGES_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_metadata(
    *,
    item: Item,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    await execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_root(
    *,
    item: Item,
) -> None:
    await insert_metadata(item=item)
    await insert_code_languages(item=item)
