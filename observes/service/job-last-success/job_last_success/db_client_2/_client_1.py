from ._core import (
    Client,
    JobLastSuccess,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from redshift_client.sql_client import (
    DbConnection,
    Query,
    QueryValues,
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    Dict,
    TypeVar,
)

_T = TypeVar("_T")


def _decode_job_success(raw: RowData) -> ResultE[JobLastSuccess]:
    try:
        job = raw.data[0]
        success_at = raw.data[1]
        if isinstance(job, str) and isinstance(success_at, datetime):
            return Result.success(JobLastSuccess(job, success_at))
    except KeyError as err:
        return Result.failure(Exception(err))
    return Result.failure(
        TypeError(
            f"Expected (str, datetime); got ({type(job)},{type(success_at)})"
        ),
        JobLastSuccess,
    ).alt(Exception)


def _assert_one(items: FrozenList[_T]) -> ResultE[_T]:
    if len(items) == 1:
        return Result.success(items[0])
    return Result.failure(
        Exception(ValueError(f"Expected one item; got {len(items)}"))
    )


@dataclass(frozen=True)
class _Client1:
    _sql: SqlClient
    _schema: str

    def get_job(self, job_name: str) -> Cmd[JobLastSuccess]:
        statement = """
            SELECT job_name, sync_date FROM {schema}.last_sync_jobs
            WHERE job_name=%(job_name)s
        """
        identifiers = {
            "schema": self._schema,
        }
        query = Query.dynamic_query(statement, freeze(identifiers))
        args: Dict[str, PrimitiveVal] = {
            "job_name": job_name,
        }
        return self._sql.execute(
            query, QueryValues(freeze(args))
        ) + self._sql.fetch_all().map(
            lambda x: _assert_one(x).bind(_decode_job_success).unwrap()
        )


def new_client(_sql: SqlClient, _schema: str) -> Client:
    client = _Client1(_sql, _schema)
    return Client.new(client.get_job)
