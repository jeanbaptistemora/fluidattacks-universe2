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
METADATA_TABLE: str = f"{SCHEMA_NAME}.toe_inputs_metadata"


def _initialize_metadata_table() -> None:
    LOGGER.info("Ensuring %s table exists...", METADATA_TABLE)
    execute(
        f"""
            CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
                id VARCHAR,
                attacked_at TIMESTAMPTZ,
                attacked_by VARCHAR,
                be_present BOOLEAN,
                be_present_until TIMESTAMPTZ,
                first_attack_at TIMESTAMPTZ,
                group_name VARCHAR,
                has_vulnerabilities BOOLEAN,
                root_id VARCHAR,
                seen_at TIMESTAMPTZ,
                seen_first_time_by VARCHAR,

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
