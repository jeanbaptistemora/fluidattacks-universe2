# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    FrozenDict,
)
from target_snowflake.snowflake_client.sql_client import (
    Identifier,
    Query,
)

TEST_TABLE = Identifier.from_raw("test_fetch")
COLM_1 = Identifier.from_raw('"0%00^"$@*()"')
COLM_2 = Identifier.from_raw("column_2")


def create_test_table() -> Query:
    return Query(
        "CREATE OR REPLACE TABLE observes.tests.{table} ({col1} NUMBER, {col2} NUMBER);",
        FrozenDict({"table": TEST_TABLE, "col1": COLM_1, "col2": COLM_2}),
        FrozenDict({}),
    )


def describe_table() -> Query:
    return Query(
        "DESCRIBE TABLE observes.tests.{table} TYPE = COLUMNS;",
        FrozenDict({"table": TEST_TABLE}),
        FrozenDict({}),
    )


def delete_test_table() -> Query:
    return Query(
        "DROP TABLE observes.tests.{table} CASCADE;",
        FrozenDict({"table": TEST_TABLE}),
        FrozenDict({}),
    )
