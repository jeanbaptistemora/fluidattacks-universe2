# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..queries import (
    SQL_INSERT_HISTORIC,
    SQL_INSERT_METADATA,
)
from ..utils import (
    format_query_fields,
)
from .initialize import (
    METADATA_TABLE,
    STATE_TABLE,
    TREATMENT_TABLE,
)
from .types import (
    MetadataTableRow,
    StateTableRow,
    TreatmentTableRow,
)
from .utils import (
    format_row_metadata,
    format_row_state,
    format_row_treatment,
)
from dynamodb.types import (
    Item,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)


def insert_metadata(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    cursor.execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_historic_state(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_state: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(StateTableRow)
    sql_values = [
        format_row_state(vulnerability_id, state) for state in historic_state
    ]
    cursor.executemany(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table_metadata=METADATA_TABLE,
            table_historic=STATE_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_historic_treatment(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_treatment: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(TreatmentTableRow)
    sql_values = [
        format_row_treatment(vulnerability_id, treatment)
        for treatment in historic_treatment
    ]
    cursor.executemany(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table_metadata=METADATA_TABLE,
            table_historic=TREATMENT_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
