from .operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from aioextensions import (
    collect,
)
from dataclasses import (
    dataclass,
    fields,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import logging
import logging.config
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


def _format_query_fields(table_row_class: Any) -> Tuple[str, str]:
    _fields = ",".join(tuple(f.name for f in fields(table_row_class)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(table_row_class)))
    return _fields, values


async def insert_metadata(
    *,
    vulnerability: Vulnerability,
) -> None:
    _fields, values = _format_query_fields(MetadataTableRow)
    sql_values = dict(
        id=vulnerability.id,
        custom_severity=vulnerability.custom_severity,
        finding_id=vulnerability.finding_id,
        skims_method=vulnerability.skims_method,
        type=vulnerability.type.value,
    )
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
