# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
import logging

LOGGER = logging.getLogger(__name__)
METADATA_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_metadata"
STATE_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_state"
TREATMENT_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_treatment"
VERIFICATION_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_verification"
ZERO_RISK_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_zero_risk"


def _initialize_metadata_table() -> None:
    LOGGER.info("Ensuring %s table exists...", METADATA_TABLE)
    execute(
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


def _initialize_state_table() -> None:
    LOGGER.info("Ensuring %s table exists...", STATE_TABLE)
    execute(
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


def _initialize_treatment_table() -> None:
    LOGGER.info("Ensuring %s table exists...", TREATMENT_TABLE)
    execute(
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


def _initialize_verification_table() -> None:
    LOGGER.info("Ensuring %s table exists...", VERIFICATION_TABLE)
    execute(
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


def _initialize_zero_risk_table() -> None:
    LOGGER.info("Ensuring %s table exists...", ZERO_RISK_TABLE)
    execute(
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


def initialize_tables() -> None:
    initialize_schema()
    _initialize_metadata_table()
    _initialize_state_table()
    _initialize_treatment_table()
    _initialize_verification_table()
    _initialize_zero_risk_table()
