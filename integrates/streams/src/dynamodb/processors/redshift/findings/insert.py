# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..operations import (
    execute,
    execute_many,
)
from ..queries import (
    SQL_INSERT_HISTORIC,
    SQL_INSERT_METADATA,
    SQL_INSERT_VERIFICATION_VULNS_IDS,
)
from ..utils import (
    format_query_fields,
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


def insert_metadata(
    *,
    item: Item,
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
    item: Item,
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


def insert_historic_state(
    *,
    finding_id: str,
    historic_state: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(StateTableRow)
    sql_values = [
        format_row_state(finding_id, state) for state in historic_state
    ]
    execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=STATE_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_historic_verification(
    *,
    finding_id: str,
    historic_verification: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(finding_id, verification)
        for verification in historic_verification
    ]
    execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=VERIFICATION_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


def insert_historic_verification_vuln_ids(
    *,
    finding_id: str,
    historic_verification: tuple[Item, ...],
) -> None:
    _fields, values = format_query_fields(VerificationVulnIdsTableRow)
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
    execute_many(  # nosec
        SQL_INSERT_VERIFICATION_VULNS_IDS.substitute(
            table=VERIFICATION_VULN_IDS_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
