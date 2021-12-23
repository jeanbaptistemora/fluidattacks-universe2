# pylint: skip-file

from code_etl.client import (
    query,
)
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
    return client.cursor.execute_query(query.all_data_count(table)).bind(
        lambda _: client.cursor.fetch_one().map(
            lambda i: unify(assert_int)(assert_key(i, 0))
        )
    )
