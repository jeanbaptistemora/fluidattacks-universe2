# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..utils import (
    format_sql_query_historic,
    format_sql_query_metadata,
    format_sql_query_verification_vulns_ids,
    get_query_fields,
)
from .initialize import (
    METADATA_TABLE,
    SEVERITY_CVSS20_TABLE,
    SEVERITY_CVSS31_TABLE,
    STATE_TABLE,
    VERIFICATION_TABLE,
    VERIFICATION_VULN_IDS_TABLE,
)
from .types import (
    MetadataTableRow,
    SeverityCvss20TableRow,
    SeverityCvss31TableRow,
    StateTableRow,
    VerificationTableRow,
    VerificationVulnIdsTableRow,
)
from .utils import (
    format_row_metadata,
    format_row_severity,
    format_row_state,
    format_row_verification,
    format_row_verification_vuln_ids,
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


def insert_metadata_severity(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    if item["cvss_version"] == "3.1":
        sql_fields = get_query_fields(SeverityCvss31TableRow)
        severity_table = SEVERITY_CVSS31_TABLE
    else:
        sql_fields = get_query_fields(SeverityCvss20TableRow)
        severity_table = SEVERITY_CVSS20_TABLE
    sql_values = format_row_severity(item)
    cursor.execute(
        format_sql_query_metadata(severity_table, sql_fields),
        sql_values,
    )


def insert_historic_state(
    *,
    cursor: cursor_cls,
    finding_id: str,
    historic_state: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(StateTableRow)
    sql_values = [
        format_row_state(finding_id, state) for state in historic_state
    ]
    cursor.executemany(
        format_sql_query_historic(STATE_TABLE, METADATA_TABLE, sql_fields),
        sql_values,
    )


def insert_historic_verification(
    *,
    cursor: cursor_cls,
    finding_id: str,
    historic_verification: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(finding_id, verification)
        for verification in historic_verification
    ]
    cursor.executemany(
        format_sql_query_historic(
            VERIFICATION_TABLE, METADATA_TABLE, sql_fields
        ),
        sql_values,
    )


def insert_historic_verification_vuln_ids(
    *,
    cursor: cursor_cls,
    finding_id: str,
    historic_verification: tuple[Item, ...],
) -> None:
    sql_fields = get_query_fields(VerificationVulnIdsTableRow)
    sql_values = [
        format_row_verification_vuln_ids(
            finding_id=finding_id,
            modified_date=verification["modified_date"],
            vulnerability_id=vulnerability_id,
        )
        for verification in historic_verification
        if verification.get("vulnerability_ids")
        for vulnerability_id in verification["vulnerability_ids"]
    ]
    cursor.executemany(
        format_sql_query_verification_vulns_ids(
            VERIFICATION_VULN_IDS_TABLE, METADATA_TABLE, sql_fields
        ),
        sql_values,
    )


def insert_finding(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    insert_metadata(cursor=cursor, item=item)
    insert_metadata_severity(cursor=cursor, item=item)
    finding_id = item["id"]
    state_items = (
        item.get("state"),
        item.get("creation"),
        item.get("submission"),
        item.get("approval"),
    )
    state_items_filtered = tuple(item for item in state_items if item)
    if state_items_filtered:
        insert_historic_state(
            cursor=cursor,
            finding_id=finding_id,
            historic_state=state_items_filtered,
        )
    verification = item.get("verification")
    if verification:
        historic_verification = (verification,)
        insert_historic_verification(
            cursor=cursor,
            finding_id=finding_id,
            historic_verification=historic_verification,
        )
        insert_historic_verification_vuln_ids(
            cursor=cursor,
            finding_id=finding_id,
            historic_verification=historic_verification,
        )
