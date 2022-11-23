from ..utils import (
    format_sql_query_historic,
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    METADATA_TABLE,
    STATE_TABLE,
    TREATMENT_TABLE,
    VERIFICATION_TABLE,
    ZERO_RISK_TABLE,
)
from .types import (
    MetadataTableRow,
    StateTableRow,
    TreatmentTableRow,
    VerificationTableRow,
    ZeroRiskTableRow,
)
from .utils import (
    format_row_metadata,
    format_row_state,
    format_row_treatment,
    format_row_verification,
    format_row_zero_risk,
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
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    cursor.execute(
        format_sql_query_metadata(METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_historic_state(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_state: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(StateTableRow)
    sql_values = [
        format_row_state(vulnerability_id, state) for state in historic_state
    ]
    cursor.executemany(
        format_sql_query_historic(STATE_TABLE, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_historic_treatment(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_treatment: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(TreatmentTableRow)
    sql_values = [
        format_row_treatment(vulnerability_id, treatment)
        for treatment in historic_treatment
    ]
    cursor.executemany(
        format_sql_query_historic(TREATMENT_TABLE, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_historic_verification(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_verification: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(vulnerability_id, verification)
        for verification in historic_verification
    ]
    cursor.executemany(
        format_sql_query_historic(
            VERIFICATION_TABLE, METADATA_TABLE, sql_fields
        ),
        sql_values,
    )


def insert_historic_zero_risk(
    *,
    cursor: cursor_cls,
    vulnerability_id: str,
    historic_zero_risk: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(ZeroRiskTableRow)
    sql_values = [
        format_row_zero_risk(vulnerability_id, zero_risk)
        for zero_risk in historic_zero_risk
    ]
    cursor.executemany(
        format_sql_query_historic(ZERO_RISK_TABLE, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_vulnerability(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    vulnerability_id = item.get("id") or str(item["pk"]).split("#")[1]
    insert_metadata(cursor=cursor, item=item)
    if "state" in item:
        insert_historic_state(
            cursor=cursor,
            vulnerability_id=vulnerability_id,
            historic_state=(item["state"],),
        )
    if "treatment" in item:
        insert_historic_treatment(
            cursor=cursor,
            vulnerability_id=vulnerability_id,
            historic_treatment=(item["treatment"],),
        )
    if "verification" in item:
        insert_historic_verification(
            cursor=cursor,
            vulnerability_id=vulnerability_id,
            historic_verification=(item["verification"],),
        )
    if "zero_risk" in item:
        insert_historic_zero_risk(
            cursor=cursor,
            vulnerability_id=vulnerability_id,
            historic_zero_risk=(item["zero_risk"],),
        )
