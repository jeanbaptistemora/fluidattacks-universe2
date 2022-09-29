# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

import os
import pytest
from target_snowflake.snowflake_client.sql_client import (
    Credentials,
    DatabaseId,
    DbConnector,
    Identifier,
)


def test_connection() -> None:
    with pytest.raises(SystemExit) as wrapped_test:
        creds = Credentials(
            os.environ["SNOWFLAKE_USER"],
            os.environ["SNOWFLAKE_PASSWORD"],
            os.environ["SNOWFLAKE_ACCOUNT"],
        )
        conn = DbConnector(creds).connect_db(
            DatabaseId(
                Identifier.from_raw(os.environ["SNOWFLAKE_DB"]), None, None
            ),
        )
        conn.compute()
    assert wrapped_test.value.code == 0
