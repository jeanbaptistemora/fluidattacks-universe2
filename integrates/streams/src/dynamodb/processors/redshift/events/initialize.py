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

METADATA_TABLE: str = f"{SCHEMA_NAME}.events_metadata"


def _initialize_metadata_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table_name} (
                id VARCHAR,
                created_by VARCHAR,
                created_date TIMESTAMPTZ,
                event_date TIMESTAMPTZ,
                group_name VARCHAR,
                hacker VARCHAR,
                root_id VARCHAR,
                solution_reason VARCHAR,
                solving_date TIMESTAMPTZ,
                status VARCHAR,
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
            table_name=sql.Identifier(METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    initialize_schema()
    _initialize_metadata_table()
