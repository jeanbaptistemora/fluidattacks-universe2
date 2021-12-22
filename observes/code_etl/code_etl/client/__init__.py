# pylint: skip-file

from code_etl.client.decoder import (
    assert_int,
    assert_key,
)
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from returns.io import (
    IO,
)
from returns.pointfree import (
    unify,
)
from returns.result import (
    Result,
)
from typing import (
    Union,
)


def all_data_count(
    client: Client, table: TableID
) -> IO[Result[int, Union[KeyError, TypeError]]]:
    query = Query(
        """
        SELECT COUNT(*) FROM {schema}.{table}
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )
    return client.cursor.execute_query(query).map(
        lambda _: client.cursor.fetch_one().map(
            lambda i: unify(assert_int)(assert_key(i, 0))
        )
    )
