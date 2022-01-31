from aioextensions import (
    collect,
)
import logging
import logging.config
from redshift.operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from settings import (
    LOGGING,
    NOEXTRA,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
METADATA_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_metadata"
STATE_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_state"
TREATMENT_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_treatment"
VERIFICATION_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_verification"
ZERO_RISK_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_zero_risk"


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
                modified_by VARCHAR NOT NULL,
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
