# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from aioextensions import (
    collect,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingState,
    FindingVerification,
)
from redshift.operations import (
    execute,
    execute_batch,
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


async def _insert_metadata(
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


async def _insert_metadata_severity(
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


async def _insert_historic_state(
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


async def _insert_historic_verification(
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


async def _insert_historic_verification_vuln_ids(
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
        if verification.vulnerability_ids
        for vulnerability_id in verification.vulnerability_ids
    ]
    await execute_many(  # nosec
        SQL_INSERT_VERIFICATION_VULNS_IDS.substitute(
            table=VERIFICATION_VULN_IDS_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_finding(
    *,
    finding: Finding,
    historic_state: Tuple[FindingState, ...],
    historic_verification: Tuple[FindingVerification, ...],
) -> None:
    await _insert_metadata(finding=finding)
    await collect(
        (
            _insert_metadata_severity(
                finding=finding,
            ),
            _insert_historic_state(
                finding_id=finding.id,
                historic_state=historic_state,
            ),
            _insert_historic_verification(
                finding_id=finding.id,
                historic_verification=historic_verification,
            ),
            _insert_historic_verification_vuln_ids(
                finding_id=finding.id,
                historic_verification=historic_verification,
            ),
        )
    )


async def insert_batch_metadata(
    *,
    findings: Tuple[Finding, ...],
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = [format_row_metadata(finding) for finding in findings]
    await execute_batch(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_severity_cvss20(
    *,
    findings: Tuple[Finding, ...],
) -> None:
    _fields, values = format_query_fields(SeverityCvss20TableRow)
    sql_values = [
        format_row_severity(finding)
        for finding in findings
        if isinstance(finding.severity, Finding20Severity)
    ]
    await execute_batch(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=SEVERITY_CVSS20_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_severity_cvss31(
    *,
    findings: Tuple[Finding, ...],
) -> None:
    _fields, values = format_query_fields(SeverityCvss31TableRow)
    sql_values = [
        format_row_severity(finding)
        for finding in findings
        if isinstance(finding.severity, Finding31Severity)
    ]
    await execute_batch(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=SEVERITY_CVSS31_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_state(
    *,
    finding_ids: Tuple[str, ...],
    historics: Tuple[Tuple[FindingState, ...], ...],
) -> None:
    _fields, values = format_query_fields(StateTableRow)
    sql_values = [
        format_row_state(finding_id, historic_entry)
        for finding_id, historic in zip(finding_ids, historics)
        for historic_entry in historic
    ]
    await execute_batch(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=STATE_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_verification(
    *,
    finding_ids: Tuple[str, ...],
    historics: Tuple[Tuple[FindingVerification, ...], ...],
) -> None:
    _fields, values = format_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(finding_id, historic_entry)
        for finding_id, historic in zip(finding_ids, historics)
        for historic_entry in historic
    ]
    await execute_batch(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=VERIFICATION_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_verification_vuln_ids(
    *,
    finding_ids: Tuple[str, ...],
    historics: Tuple[Tuple[FindingVerification, ...], ...],
) -> None:
    _fields, values = format_query_fields(VerificationVulnIdsTableRow)
    sql_values = [
        format_row_verification_vuln_ids(
            finding_id=finding_id,
            modified_date=verification.modified_date,
            vulnerability_id=vulnerability_id,
        )
        for finding_id, historic in zip(finding_ids, historics)
        for verification in historic
        if verification.vulnerability_ids
        for vulnerability_id in verification.vulnerability_ids
    ]
    await execute_batch(  # nosec
        SQL_INSERT_VERIFICATION_VULNS_IDS.substitute(
            table=VERIFICATION_VULN_IDS_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )
