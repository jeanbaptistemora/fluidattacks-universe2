# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _queries,
)
from fa_purity import (
    Cmd,
    Maybe,
)
import logging
import os
import pytest
from target_snowflake.snowflake_client.sql_client import (
    Credentials,
    DatabaseId,
    DbConnector,
    Identifier,
    RowData,
)

LOG = logging.getLogger(__name__)


def test_fetch() -> None:
    with pytest.raises(SystemExit) as wrapped_test:
        creds = Credentials(
            os.environ["SNOWFLAKE_USER"],
            os.environ["SNOWFLAKE_PASSWORD"],
            os.environ["SNOWFLAKE_ACCOUNT"],
        )
        cursor = (
            DbConnector(creds)
            .connect_db(
                DatabaseId(
                    Identifier.from_raw(os.environ["SNOWFLAKE_DB"]), None, None
                ),
            )
            .bind(lambda c: c.cursor(LOG))
        )

        def _test(item: Maybe[RowData]) -> None:
            metadata = item.unwrap().data
            assert Identifier.from_raw(str(metadata[0])) == _queries.COLM_1
            assert str(metadata[1]).upper() == "NUMBER(38,0)".upper()

        cmd: Cmd[None] = cursor.bind(
            lambda c: c.execute(_queries.create_test_table())
            .bind(lambda _: c.execute(_queries.describe_table()))
            .bind(lambda _: c.fetch_one().map(_test))
            .bind(lambda _: c.execute(_queries.delete_test_table()))
        )
        cmd.compute()
    assert wrapped_test.value.code == 0
