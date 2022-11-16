# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
)

from code_etl.client import (
    _query,
    decoder,
    encoder,
)
from code_etl.client._assert import (
    assert_key,
    assert_type,
)
from code_etl.client.db_client import (
    DbClient,
)
from code_etl.client.encoder import (
    commit_row_to_dict,
    CommitTableRow,
    from_raw,
    from_reg,
    from_stamp,
    to_dict,
)
from code_etl.objs import (
    CommitStamp,
    RepoContex,
    RepoId,
    RepoRegistration,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
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
from postgres_client.client import (
    Client as RawDbClient,
)
from postgres_client.connection import (
    Credentials as LegacyCredentials,
    DatabaseID,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    SqlArgs,
)
from redshift_client.sql_client import (
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
    Optional,
    Type,
    TypeVar,
    Union,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _fetch(
    client: SqlClient, chunk: int
) -> Cmd[Maybe[FrozenList[ResultE[CommitTableRow]]]]:
    result = client.fetch_many(chunk).map(
        lambda rows: Maybe.from_optional(
            tuple(from_raw(r.data) for r in rows) if rows else None
        )
    )
    return result


def _fetch_one_result(client: DbClient, d_type: Type[_T]) -> Cmd[ResultE[_T]]:
    return (
        client.fetch_one()
        .map(lambda i: assert_key(i, 0))
        .map(lambda v: v.bind(lambda i: assert_type(i, d_type)))
    )


def _fetch_not_empty(client: DbClient) -> Cmd[bool]:
    return client.fetch_one().map(bool)


def _delta_fields(old: CommitTableRow, new: CommitTableRow) -> FrozenList[str]:
    _filter = filter(
        lambda x: x[0],
        ((bool(getattr(new, k) != v), k) for k, v in old.__dict__.items()),
    )
    return tuple(map(lambda x: x[1], _filter))


@dataclass(frozen=True)
class RawClient:
    # exposes utilities from and to DB using raw objs i.e. CommitTableRow
    _sql_client: SqlClient
    _table: TableID

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

    def insert_rows(self, rows: FrozenList[CommitTableRow]) -> Cmd[None]:
        msg = Cmd.from_cmd(lambda: LOG.debug("inserting %s rows", len(rows)))
        return msg.bind(
            lambda _: self._sql_client.batch(
                _query.insert_row(self._table),
                tuple(QueryValues(commit_row_to_dict(r)) for r in rows),
            )
        )

    def insert_unique_rows(
        self, rows: FrozenList[CommitTableRow]
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
    ) -> Cmd[Stream[ResultE[CommitTableRow]]]:
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

    def all_data_raw(self) -> Cmd[Stream[ResultE[CommitTableRow]]]:
        return self._all_data(Maybe.empty())

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[CommitTableRow]]]:
        return self._all_data(Maybe.from_value(namespace))

    def delta_update(
        self,
        old: CommitTableRow,
        new: CommitTableRow,
        ignore_fa_hash: bool = True,
    ) -> Cmd[None]:
        _fields = _delta_fields(old, new)
        if ignore_fa_hash and _fields == ("fa_hash",):
            return Cmd.from_cmd(
                lambda: LOG.warning("delta fa_hash update skipped")
            )
        if len(_fields) > 0:
            changes = tuple(
                f"{f}: {getattr(old, f)} -> {getattr(new, f)}" for f in _fields
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


@dataclass(frozen=True)
class _Client:
    # exposes utilities from and to DB using not raw objs
    db_client: DbClient
    table: TableID
    raw: RawClient


@dataclass(frozen=True)
class Client:
    # exposes utilities from and to DB using not raw objs
    _inner: _Client

    @staticmethod
    def new(
        _db_client: RawDbClient, _sql_client: SqlClient, _table: TableID
    ) -> Client:
        _client = DbClient(_db_client)
        return Client(_Client(_client, _table, RawClient(_sql_client, _table)))

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        return self._inner.raw.all_data_count(namespace)

    def get_context(self, repo: RepoId) -> Cmd[RepoContex]:
        last = self._inner.db_client.execute_query(
            _query.last_commit_hash(self._inner.table, repo)
        ).bind(lambda _: _fetch_one_result(self._inner.db_client, str))
        is_new = (
            self._inner.db_client.execute_query(
                _query.commit_exists(
                    self._inner.table, repo, COMMIT_HASH_SENTINEL
                ),
            )
            .bind(lambda _: _fetch_not_empty(self._inner.db_client))
            .map(lambda b: not b)
        )
        return last.bind(
            lambda i: is_new.map(
                lambda n: RepoContex(repo, i.value_or(None), n)
            )
        )

    def register_repos(self, reg: FrozenList[RepoRegistration]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: LOG.info("register_repos %s", str(reg))
        )
        encoded = tuple(from_reg(r) for r in reg)
        return log_info.bind(
            lambda _: self._inner.raw.insert_unique_rows(encoded)
        )

    def insert_stamps(self, stamps: FrozenList[CommitStamp]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: LOG.info("inserting %s stamps", len(stamps))
        )
        encoded = tuple(from_stamp(s) for s in stamps)
        return log_info.bind(
            lambda _: self._inner.raw.insert_unique_rows(encoded)
        )

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]:
        return self._inner.raw.namespace_data(namespace).map(
            lambda s: s.map(lambda r: r.bind(decoder.decode_commit_table_row))
        )

    def delta_update(
        self, old: CommitStamp, new: CommitStamp, ignore_fa_hash: bool = True
    ) -> Cmd[None]:
        if old != new:
            info = Cmd.from_cmd(
                lambda: LOG.info("delta update %s", old.commit.commit_id)
            )
            return info.bind(
                lambda _: self._inner.raw.delta_update(
                    encoder.from_stamp(old),
                    encoder.from_stamp(new),
                    ignore_fa_hash,
                )
            )
        return Cmd.from_cmd(lambda: LOG.debug("no changes"))


@dataclass(frozen=True)
class LegacyAdapters:
    @staticmethod
    def db_id(db_id: DatabaseID) -> DatabaseId:
        return DatabaseId(db_id.db_name, db_id.host, db_id.port)

    @staticmethod
    def db_creds(creds: LegacyCredentials) -> Credentials:
        return Credentials(creds.user, creds.password)
