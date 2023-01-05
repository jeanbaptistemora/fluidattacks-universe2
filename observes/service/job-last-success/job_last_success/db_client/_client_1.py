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
    FrozenDict,
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from redshift_client.sql_client import (
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


def _assert_bool(raw: RowData) -> ResultE[bool]:
    if len(raw.data) == 1 and isinstance(raw.data[0], bool):
        return Result.success(raw.data[0])
    return Result.failure(
        Exception(ValueError(f"Expected one bool item; got {raw.data}"))
    )


@dataclass(frozen=True)
class _Client1:
    _sql: SqlClient
    _schema: str
    _table: str
    _name_column: str

    @property
    def _common_identifiers(self) -> FrozenDict[str, str]:
        identifiers = {
            "schema": self._schema,
            "table": self._table,
            "name_column": self._name_column,
        }
        return freeze(identifiers)

    def get_job(self, job_name: str) -> Cmd[JobLastSuccess]:
        statement = """
            SELECT {name_column}, sync_date FROM {schema}.{table}
            WHERE {name_column}=%(job_name)s
        """
        query = Query.dynamic_query(statement, self._common_identifiers)
        args: Dict[str, PrimitiveVal] = {
            "job_name": job_name,
        }
        return self._sql.execute(
            query, QueryValues(freeze(args))
        ) + self._sql.fetch_all().map(
            lambda x: _assert_one(x).bind(_decode_job_success).unwrap()
        )

    def job_exist(self, job_name: str) -> Cmd[bool]:
        statement = """
            SELECT EXISTS (
                SELECT 1 FROM {schema}.{table}
                WHERE {name_column}=%(job_name)s
            )
        """
        query = Query.dynamic_query(statement, self._common_identifiers)
        args: Dict[str, PrimitiveVal] = {
            "job_name": job_name,
        }
        return self._sql.execute(
            query, QueryValues(freeze(args))
        ) + self._sql.fetch_one().map(
            lambda m: _assert_bool(m.unwrap()).unwrap()
        )

    def _new_timestamp_job(self, job_name: str) -> Cmd[None]:
        statement = """
            INSERT INTO {schema}.{table}
            ({name_column}, sync_date) VALUES
            (%(job_name)s, getdate())
        """
        query = Query.dynamic_query(statement, self._common_identifiers)
        args: Dict[str, PrimitiveVal] = {
            "job_name": job_name,
        }
        return self._sql.execute(query, QueryValues(freeze(args)))

    def _update_job(self, job_name: str) -> Cmd[None]:
        statement = """
            UPDATE {schema}.{table}
            set sync_date=getdate() WHERE {name_column}=%(job_name)s
        """
        query = Query.dynamic_query(statement, self._common_identifiers)
        args: Dict[str, PrimitiveVal] = {
            "job_name": job_name,
        }
        return self._sql.execute(query, QueryValues(freeze(args)))

    def upsert(self, job_name: str) -> Cmd[None]:
        return (
            self.job_exist(job_name)
            .map(lambda b: self._update_job if b else self._new_timestamp_job)
            .bind(lambda f: f(job_name))
        )


SCHEMA = "repos-s3-sync"


def new_job_client(_sql: SqlClient) -> Client:
    client = _Client1(_sql, SCHEMA, "last_sync_jobs", "job_name")
    return Client.new(client.get_job, client.upsert)


def new_compound_job_client(_sql: SqlClient, table: str) -> Client:
    client = _Client1(_sql, SCHEMA, table, "group_name")
    return Client.new(client.get_job, client.upsert)
