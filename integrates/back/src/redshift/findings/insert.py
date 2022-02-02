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
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingState,
    FindingVerification,
)
from redshift.operations import (
    execute,
    execute_many,
)
from redshift.queries import (
    SQL_INSERT_HISTORIC,
    SQL_INSERT_METADATA,
)
from redshift.utils import (
    format_query_fields,
)
from string import (
    Template,
)
from typing import (
    Tuple,
)

SQL_INSERT_VERIFICATION_VULNS_IDS = Template(
    """
    INSERT INTO ${table} (${fields}) SELECT ${values}
    WHERE NOT EXISTS (
        SELECT id, modified_date, vulnerability_id
        FROM ${table}
        WHERE id = %(id)s
            and modified_date = %(modified_date)s
            and vulnerability_id = %(vulnerability_id)s
    )
    """
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


async def insert_metadata_severity(
    *,
    finding: Finding,
) -> None:
    if isinstance(finding.severity, Finding31Severity):
        _fields, values = format_query_fields(SeverityCvss31TableRow)
        severity_table = SEVERITY_CVSS31_TABLE
    else:
        _fields, values = format_query_fields(SeverityCvss20TableRow)
        severity_table = SEVERITY_CVSS20_TABLE
    sql_values = format_row_severity(finding)
    await execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=severity_table,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_historic_state(
    *,
    finding_id: str,
    historic_state: Tuple[FindingState, ...],
) -> None:
    _fields, values = format_query_fields(StateTableRow)
    sql_values = [
        format_row_state(finding_id, state) for state in historic_state
    ]
    await execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=STATE_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_historic_verification(
    *,
    finding_id: str,
    historic_verification: Tuple[FindingVerification, ...],
) -> None:
    _fields, values = format_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(finding_id, verification)
        for verification in historic_verification
    ]
    await execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=VERIFICATION_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_historic_verification_vuln_ids(
    *,
    finding_id: str,
    historic_verification: Tuple[FindingVerification, ...],
) -> None:
    _fields, values = format_query_fields(VerificationVulnIdsTableRow)
    sql_values = [
        format_row_verification_vuln_ids(
            finding_id=finding_id,
            modified_date=verification.modified_date,
            vulnerability_id=vulnerability_id,
        )
        for verification in historic_verification
        for vulnerability_id in verification.vulnerability_ids
        if verification.vulnerability_ids
    ]
    await execute_many(  # nosec
        SQL_INSERT_VERIFICATION_VULNS_IDS.substitute(
            table=VERIFICATION_VULN_IDS_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
