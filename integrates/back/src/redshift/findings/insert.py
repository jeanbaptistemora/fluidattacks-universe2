from .initialize import (
    METADATA_TABLE,
)
from .types import (
    MetadataTableRow,
)
from .utils import (
    format_row_metadata,
)
from db_model.findings.types import (
    Finding,
)
from redshift.operations import (
    execute,
)
from redshift.queries import (
    SQL_INSERT_METADATA,
)
from redshift.utils import (
    format_query_fields,
)


async def insert_metadata(
    *,
    finding: Finding,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(finding)
    await execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
