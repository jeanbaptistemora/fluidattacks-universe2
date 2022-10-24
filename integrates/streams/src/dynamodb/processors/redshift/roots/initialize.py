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
CODE_LANGUAGES_TABLE: str = f"{SCHEMA_NAME}.roots_code_languages"
ENVIRONMENT_URL_TABLE: str = f"{SCHEMA_NAME}.roots_environment_url"
METADATA_TABLE: str = f"{SCHEMA_NAME}.roots_metadata"


def _initialize_code_languages_table() -> None:
    LOGGER.info("Ensuring %s table exists...", CODE_LANGUAGES_TABLE)
    execute(
        f"""
            CREATE TABLE IF NOT EXISTS {CODE_LANGUAGES_TABLE} (
                id VARCHAR,
                language VARCHAR,
                loc INTEGER,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """,
    )


def _initialize_environment_url_table() -> None:
    LOGGER.info("Ensuring %s table exists...", ENVIRONMENT_URL_TABLE)
    execute(
        f"""
            CREATE TABLE IF NOT EXISTS {ENVIRONMENT_URL_TABLE} (
                id VARCHAR,
                cloud_name VARCHAR,
                created_at TIMESTAMPTZ,
                root_id VARCHAR,
                url_type VARCHAR,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """,
    )


def _initialize_metadata_table() -> None:
    LOGGER.info("Ensuring %s table exists...", METADATA_TABLE)
    execute(
        f"""
            CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
                id VARCHAR,
                created_date TIMESTAMPTZ
                group_name VARCHAR,
                organization_name VARCHAR,
                type VARCHAR,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """,
    )


async def initialize_tables() -> None:
    initialize_schema()
    _initialize_metadata_table()
    _initialize_code_languages_table()
    _initialize_environment_url_table()
