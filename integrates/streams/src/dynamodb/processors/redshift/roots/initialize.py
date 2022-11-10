# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ..operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from psycopg2 import (
    sql,
)

CODE_LANGUAGES_TABLE: str = "roots_code_languages"
METADATA_TABLE: str = "roots_metadata"


def _initialize_code_languages_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                language VARCHAR,
                loc INTEGER,
                root_id VARCHAR,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, CODE_LANGUAGES_TABLE),
        ),
    )


def _initialize_metadata_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                created_date TIMESTAMPTZ,
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
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    initialize_schema()
    _initialize_metadata_table()
    _initialize_code_languages_table()
