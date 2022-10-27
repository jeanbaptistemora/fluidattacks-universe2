# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import logging
import logging.config
from redshift.operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
METADATA_TABLE: str = f"{SCHEMA_NAME}.events_metadata"


async def _initialize_metadata_table() -> None:
    LOGGER.info("Ensuring %s table exists...", METADATA_TABLE)
    await execute(
        f"""
            CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
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
        """,
    )


async def initialize_tables() -> None:
    await initialize_schema()
    await _initialize_metadata_table()
