from .db_client_2 import (
    new_compound_job_client,
    new_job_client,
)
import click
from fa_purity import (
    Cmd,
    FrozenDict,
    JsonObj,
    Maybe,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from job_last_success import (
    db_client,
)
from job_last_success.conf import (
    COMPOUND_JOBS,
    COMPOUND_JOBS_TABLES,
    SINGLE_JOBS,
)
import json
import logging
from redshift_client.sql_client import (
    DbConnection,
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    connect,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def wrap_connection(
    new_connection: Cmd[DbConnection],
    action: Callable[[DbConnection], Cmd[_T]],
) -> Cmd[_T]:
    """Ensures that connection is closed regardless of action errors"""

    def _inner(connection: DbConnection) -> Cmd[_T]:
        def _action(unwrapper: CmdUnwrapper) -> _T:
            try:
                return unwrapper.act(action(connection))
            finally:
                unwrapper.act(connection.close())

        return Cmd.new_cmd(_action)

    return new_connection.bind(_inner)


def update_single_job(connection: DbConnection, job: str) -> Cmd[None]:
    return (
        new_client(connection, LOG)
        .map(new_job_client)
        .bind(lambda c: c.upsert(job))
    )


def update_compound_job(
    connection: DbConnection, job: str, child: str
) -> Cmd[None]:
    return new_client(connection, LOG).bind(
        lambda sql: new_compound_job_client(
            sql, COMPOUND_JOBS_TABLES[job]
        ).upsert(child)
    )
