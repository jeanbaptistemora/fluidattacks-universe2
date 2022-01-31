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
METADATA_TABLE: str = f"{SCHEMA_NAME}.findings_metadata"
STATE_TABLE: str = f"{SCHEMA_NAME}.findings_state"
VERIFICATION_TABLE: str = f"{SCHEMA_NAME}.findings_verification"
VERIFICATION_VULN_IDS_TABLE: str = (
    f"{SCHEMA_NAME}.findings_verification_vuln_ids"
)


async def _initialize_metadata_table() -> None:
    LOGGER.info(f"Ensuring {METADATA_TABLE} table exists...", **NOEXTRA)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
                id VARCHAR,
                cvss_version VARCHAR,
                group_name VARCHAR NOT NULL,
                requirements VARCHAR NOT NULL,
                sorts VARCHAR NOT NULL,
                title VARCHAR NOT NULL,

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
                justification VARCHAR NOT NULL,
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


async def _initialize_verification_vuln_ids_table() -> None:
    LOGGER.info(
        f"Ensuring {VERIFICATION_VULN_IDS_TABLE} table exists...", **NOEXTRA
    )
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {VERIFICATION_VULN_IDS_TABLE} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                vulnerability_id VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date,
                    vulnerability_id
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
            _initialize_verification_table(),
            _initialize_verification_vuln_ids_table(),
        )
    )
