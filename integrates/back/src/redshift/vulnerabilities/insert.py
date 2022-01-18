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
from aioextensions import (
    collect,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from redshift.operations import (
    execute,
    execute_batch,
    execute_many,
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

SQL_INSERT_METADATA = Template(
    """
    INSERT INTO ${table} (${fields}) SELECT ${values}
    WHERE NOT EXISTS (
        SELECT id
        FROM ${table}
        WHERE id = %(id)s
    )
    """
)

SQL_INSERT_HISTORIC = Template(
    """
    INSERT INTO ${table} (${fields}) SELECT ${values}
    WHERE NOT EXISTS (
        SELECT id, modified_date
        FROM ${table}
        WHERE id = %(id)s and modified_date = %(modified_date)s
    )
    """
)


async def _insert_metadata(
    *,
    vulnerability: Vulnerability,
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(vulnerability)
    await execute(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_batch_metadata(
    *,
    vulnerabilities: Tuple[Vulnerability, ...],
) -> None:
    _fields, values = format_query_fields(MetadataTableRow)
    sql_values = [format_row_metadata(vuln) for vuln in vulnerabilities]
    await execute_batch(  # nosec
        SQL_INSERT_METADATA.substitute(
            table=METADATA_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def _insert_historic_state(
    *,
    vulnerability_id: str,
    historic_state: Tuple[VulnerabilityState, ...],
) -> None:
    _fields, values = format_query_fields(StateTableRow)
    sql_values = [
        format_row_state(vulnerability_id, state) for state in historic_state
    ]
    await execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=STATE_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def _insert_historic_treatment(
    *,
    vulnerability_id: str,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
) -> None:
    _fields, values = format_query_fields(TreatmentTableRow)
    sql_values = [
        format_row_treatment(vulnerability_id, treatment)
        for treatment in historic_treatment
    ]
    await execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=TREATMENT_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def _insert_historic_verification(
    *,
    vulnerability_id: str,
    historic_verification: Tuple[VulnerabilityVerification, ...],
) -> None:
    _fields, values = format_query_fields(VerificationTableRow)
    sql_values = [
        format_row_verification(vulnerability_id, verification)
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


async def _insert_historic_zero_risk(
    *,
    vulnerability_id: str,
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
) -> None:
    _fields, values = format_query_fields(ZeroRiskTableRow)
    sql_values = [
        format_row_zero_risk(vulnerability_id, zero_risk)
        for zero_risk in historic_zero_risk
    ]
    await execute_many(  # nosec
        SQL_INSERT_HISTORIC.substitute(
            table=ZERO_RISK_TABLE,
            fields=_fields,
            values=values,
        ),
        sql_values,
    )


async def insert_vulnerability(
    *,
    vulnerability: Vulnerability,
    historic_state: Tuple[VulnerabilityState, ...],
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    historic_verification: Tuple[VulnerabilityVerification, ...],
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
) -> None:
    await _insert_metadata(vulnerability=vulnerability)
    await collect(
        (
            _insert_historic_state(
                vulnerability_id=vulnerability.id,
                historic_state=historic_state,
            ),
            _insert_historic_treatment(
                vulnerability_id=vulnerability.id,
                historic_treatment=historic_treatment,
            ),
            _insert_historic_verification(
                vulnerability_id=vulnerability.id,
                historic_verification=historic_verification,
            ),
            _insert_historic_zero_risk(
                vulnerability_id=vulnerability.id,
                historic_zero_risk=historic_zero_risk,
            ),
        )
    )
