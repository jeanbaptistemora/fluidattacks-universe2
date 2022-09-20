# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..operations import (
    execute,
)
from ..queries import (
    SQL_INSERT_METADATA,
)
from ..utils import (
    format_query_fields,
)
from .initialize import (
    METADATA_TABLE,
    SEVERITY_CVSS20_TABLE,
    SEVERITY_CVSS31_TABLE,
)
from .types import (
    MetadataTableRow,
    SeverityCvss20TableRow,
    SeverityCvss31TableRow,
)
from .utils import (
    format_row_metadata,
    format_row_severity,
)
from typing import (
    Any,
)


def insert_metadata(
    *,
    item: dict[str, Any],
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_metadata_severity(
    *,
    item: dict[str, Any],
) -> None:
    if item["cvss_version"] == "3.1":
        _fields, values = format_query_fields(SeverityCvss31TableRow)
        severity_table = SEVERITY_CVSS31_TABLE
    else:
        _fields, values = format_query_fields(SeverityCvss20TableRow)
        severity_table = SEVERITY_CVSS20_TABLE
    sql_values = format_row_severity(item)
    execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=severity_table,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
