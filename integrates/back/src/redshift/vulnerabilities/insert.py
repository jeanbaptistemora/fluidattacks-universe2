from .utils import (
    format_vulnerability_metadata,
)
from aioextensions import (
    collect,
)
from dataclasses import (
    dataclass,
    fields,
)
from datetime import (
    datetime,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
import logging
import logging.config
from redshift.operations import (
    execute,
    execute_batch,
    execute_many,
    initialize_schema,
    SCHEMA_NAME,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    Any,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
METADATA_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_metadata"
STATE_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_state"
TREATMENT_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_treatment"
VERIFICATION_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_verification"
ZERO_RISK_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_zero_risk"


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    finding_id: str
    type: str
    custom_severity: Optional[int]
    skims_method: Optional[str]


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    source: str
    status: str


@dataclass(frozen=True)
class TreatmentTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str
    accepted_until: Optional[datetime]
    acceptance_status: Optional[str]


@dataclass(frozen=True)
class VerificationTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str


@dataclass(frozen=True)
class ZeroRiskTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str


def _format_query_fields(table_row_class: Any) -> Tuple[str, str]:
    _fields = ",".join(tuple(f.name for f in fields(table_row_class)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(table_row_class)))
    return _fields, values


async def _insert_metadata(
    *,
    vulnerability: Vulnerability,
) -> None:
    _fields, values = _format_query_fields(MetadataTableRow)
    sql_values = format_vulnerability_metadata(vulnerability)
    await execute(  # nosec
        f"""
            INSERT INTO {METADATA_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id
                FROM {METADATA_TABLE}
                WHERE id = %(id)s
            )
         """,
        sql_values,
    )


async def insert_batch_metadata(
    *,
    vulnerabilities: Tuple[Vulnerability, ...],
) -> None:
    _fields, values = _format_query_fields(MetadataTableRow)
    sql_values = [
        format_vulnerability_metadata(vuln) for vuln in vulnerabilities
    ]
    await execute_batch(  # nosec
        f"""
            INSERT INTO {METADATA_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id
                FROM {METADATA_TABLE}
                WHERE id = %(id)s
            )
         """,
        sql_values,
    )


async def _insert_historic_state(
    *,
    vulnerability_id: str,
    historic_state: Tuple[VulnerabilityState, ...],
) -> None:
    _fields, values = _format_query_fields(StateTableRow)
    sql_values = [
        dict(
            id=vulnerability_id,
            modified_date=datetime.fromisoformat(state.modified_date),
            source=state.source.value,
            status=state.status.value,
        )
        for state in historic_state
    ]
    await execute_many(  # nosec
        f"""
            INSERT INTO {STATE_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id, modified_date
                FROM {STATE_TABLE}
                WHERE id = %(id)s and modified_date = %(modified_date)s
            )
         """,
        sql_values,
    )


async def _insert_historic_treatment(
    *,
    vulnerability_id: str,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
) -> None:
    _fields, values = _format_query_fields(TreatmentTableRow)
    sql_values = [
        dict(
            id=vulnerability_id,
            modified_date=datetime.fromisoformat(treatment.modified_date),
            status=treatment.status.value,
            accepted_until=datetime.fromisoformat(treatment.accepted_until)
            if treatment.accepted_until
            else None,
            acceptance_status=treatment.acceptance_status.value
            if treatment.acceptance_status
            else None,
        )
        for treatment in historic_treatment
    ]
    await execute_many(  # nosec
        f"""
            INSERT INTO {TREATMENT_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id, modified_date
                FROM {TREATMENT_TABLE}
                WHERE id = %(id)s and modified_date = %(modified_date)s
            )
         """,
        sql_values,
    )


async def _insert_historic_verification(
    *,
    vulnerability_id: str,
    historic_verification: Tuple[VulnerabilityVerification, ...],
) -> None:
    _fields, values = _format_query_fields(VerificationTableRow)
    sql_values = [
        dict(
            id=vulnerability_id,
            modified_date=datetime.fromisoformat(verification.modified_date),
            status=verification.status.value,
        )
        for verification in historic_verification
    ]
    await execute_many(  # nosec
        f"""
            INSERT INTO {VERIFICATION_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id, modified_date
                FROM {VERIFICATION_TABLE}
                WHERE id = %(id)s and modified_date = %(modified_date)s
            )
         """,
        sql_values,
    )


async def _insert_historic_zero_risk(
    *,
    vulnerability_id: str,
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
) -> None:
    _fields, values = _format_query_fields(ZeroRiskTableRow)
    sql_values = [
        dict(
            id=vulnerability_id,
            modified_date=datetime.fromisoformat(zero_risk.modified_date),
            status=zero_risk.status.value,
        )
        for zero_risk in historic_zero_risk
    ]
    await execute_many(  # nosec
        f"""
            INSERT INTO {ZERO_RISK_TABLE} ({_fields}) SELECT {values}
            WHERE NOT EXISTS (
                SELECT id, modified_date
                FROM {ZERO_RISK_TABLE}
                WHERE id = %(id)s and modified_date = %(modified_date)s
            )
         """,
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


async def _initialize_metadata_table() -> None:
    LOGGER.info(f"Ensuring {METADATA_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
                id VARCHAR,
                custom_severity INTEGER,
                finding_id VARCHAR NOT NULL,
                skims_method VARCHAR,
                type VARCHAR NOT NULL,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """,
    )


async def _initialize_state_table() -> None:
    LOGGER.info(f"Ensuring {STATE_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {STATE_TABLE} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                source VARCHAR NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {METADATA_TABLE}(id)
            )
        """,
    )


async def _initialize_treatment_table() -> None:
    LOGGER.info(f"Ensuring {TREATMENT_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {TREATMENT_TABLE} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                accepted_until TIMESTAMPTZ,
                acceptance_status VARCHAR,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {METADATA_TABLE}(id)
            )
        """,
    )


async def _initialize_verification_table() -> None:
    LOGGER.info(f"Ensuring {VERIFICATION_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {VERIFICATION_TABLE} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {METADATA_TABLE}(id)
            )
        """,
    )


async def _initialize_zero_risk_table() -> None:
    LOGGER.info(f"Ensuring {ZERO_RISK_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {ZERO_RISK_TABLE} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {METADATA_TABLE}(id)
            )
        """,
    )


async def initialize_tables() -> None:
    await initialize_schema()
    await _initialize_metadata_table()
    await collect(
        (
            _initialize_state_table(),
            _initialize_treatment_table(),
            _initialize_verification_table(),
            _initialize_zero_risk_table(),
        )
    )
