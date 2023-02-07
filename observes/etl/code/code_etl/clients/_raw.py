from __future__ import (
    annotations,
)

from . import (
    _query,
    encoder,
)
from ._assert import (
    assert_key,
    assert_type,
)
from ._raw_objs import (
    RawCommitStamp,
)
from .encoder import (
    commit_row_to_dict,
    from_raw,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    ResultE,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
)
import logging
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
    SqlClient,
)
from typing import (
    Dict,
    Optional,
)

LOG = logging.getLogger(__name__)


def _fetch(
    client: SqlClient, chunk: int
) -> Cmd[Maybe[FrozenList[ResultE[RawCommitStamp]]]]:
    result = client.fetch_many(chunk).map(
        lambda rows: Maybe.from_optional(
            tuple(from_raw(r.data) for r in rows) if rows else None
        )
    )
    return result


def _delta_fields(old: RawCommitStamp, new: RawCommitStamp) -> FrozenList[str]:
    _filter = filter(
        lambda x: x[0],  # type: ignore[misc]
        ((bool(getattr(new, k) != v), k) for k, v in old.__dict__.items()),  # type: ignore[misc]
    )
    return tuple(map(lambda x: x[1], _filter))  # type: ignore[misc]


@dataclass(frozen=True)
class RawClient:
    # exposes utilities from and to DB using raw objs i.e. RawCommitStamp
    _sql_client: SqlClient
    _table: TableId

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        query_items = (
            _query.all_data_count(self._table, namespace)
            if namespace
            else _query.all_data_count(self._table)
        )
        return self._sql_client.execute(*query_items).bind(
            lambda _: self._sql_client.fetch_one()
            .map(lambda m: m.unwrap())
            .map(
                lambda i: assert_key(i.data, 0).bind(
                    lambda j: assert_type(j, int)
                )
            )
        )

    def insert_rows(self, rows: FrozenList[RawCommitStamp]) -> Cmd[None]:
        msg = Cmd.from_cmd(lambda: LOG.debug("inserting %s rows", len(rows)))
        return msg.bind(
            lambda _: self._sql_client.batch(
                _query.insert_row(self._table),
                tuple(QueryValues(commit_row_to_dict(r)) for r in rows),
            )
        )

    def insert_unique_rows(
        self, rows: FrozenList[RawCommitStamp]
    ) -> Cmd[None]:
        msg = Cmd.from_cmd(
            lambda: LOG.debug("unique inserting %s rows", len(rows))
        )
        args = tuple(QueryValues(commit_row_to_dict(r)) for r in rows)
        return msg.bind(
            lambda _: self._sql_client.batch(
                _query.insert_unique_row(self._table),
                args,
            )
        )

    def _all_data(
        self, namespace: Maybe[str]
    ) -> Cmd[Stream[ResultE[RawCommitStamp]]]:
        pkg_items = 2000
        query_pair = namespace.map(
            lambda n: _query.namespace_data(self._table, n)
        ).or_else_call(lambda: _query.all_data(self._table))
        items = infinite_range(0, 1).map(
            lambda _: _fetch(self._sql_client, pkg_items)
        )
        return self._sql_client.execute(*query_pair).map(
            lambda _: from_piter(items)
            .transform(lambda s: until_empty(s))
            .map(lambda i: from_flist(i))
            .transform(lambda s: chain(s))
        )

    def all_data_raw(self) -> Cmd[Stream[ResultE[RawCommitStamp]]]:
        return self._all_data(Maybe.empty())

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[RawCommitStamp]]]:
        return self._all_data(Maybe.from_value(namespace))

    def delta_update(
        self,
        old: RawCommitStamp,
        new: RawCommitStamp,
    ) -> Cmd[None]:
        _fields = _delta_fields(old, new)
        if len(_fields) > 0:
            changes = tuple(
                f"{f}: {getattr(old, f)} -> {getattr(new, f)}" for f in _fields  # type: ignore[misc]
            )
            log_info = Cmd.from_cmd(
                lambda: LOG.info(
                    "delta update %s fields:\n%s",
                    len(_fields),
                    "\n".join(changes),
                )
            )
            return log_info.bind(
                lambda _: self._sql_client.execute(
                    _query.update_row(self._table, _fields),
                    QueryValues(encoder.commit_row_to_dict(new)),
                )
            )
        return Cmd.from_cmd(lambda: LOG.debug("delta update skipped"))

    def init_table(self) -> Cmd[None]:
        statement = """
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                author_email VARCHAR(256),
                author_name VARCHAR(256),
                authored_at TIMESTAMPTZ,
                committer_email VARCHAR(256),
                committer_name VARCHAR(256),
                committed_at TIMESTAMPTZ,
                hash CHAR(40) NOT NULL,
                fa_hash CHAR(64),
                message VARCHAR(4096),
                summary VARCHAR(256),
                total_insertions INTEGER,
                total_deletions INTEGER,
                total_lines INTEGER,
                total_files INTEGER,

                namespace VARCHAR(64) NOT NULL,
                repository VARCHAR(4096) NOT NULL,
                seen_at TIMESTAMPTZ,

                PRIMARY KEY (
                    namespace,
                    repository,
                    hash
                )
            ) SORTKEY (namespace, repository)
            """
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        return self._sql_client.execute(
            Query.dynamic_query(statement, freeze(identifiers)), None
        )
