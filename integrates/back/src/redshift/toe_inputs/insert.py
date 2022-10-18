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
from redshift.operations import (
    execute,
)


async def insert_metadata(
    *,
    item: Item,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    await execute(
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
