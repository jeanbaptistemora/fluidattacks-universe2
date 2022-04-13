from code_etl.client import (
    decoder,
    encoder,
    query,
)
from code_etl.client._assert import (
    assert_key,
    assert_type,
)
from code_etl.client.db_client import (
    DbClient,
)
from code_etl.client.encoder import (
    CommitTableRow,
    from_raw,
    from_reg,
    from_stamp,
    RawRow,
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
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.result import (
    ResultE,
)
from fa_purity.stream.core import (
    Stream,
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
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    SqlArgs,
)
import psycopg2
from typing import (
    Optional,
    Type,
    TypeVar,
    Union,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _fetch_action(
    client: DbClient, chunk: int
) -> Maybe[FrozenList[ResultE[CommitTableRow]]]:
    try:
        result = client.fetch_many(chunk).map(
            lambda rows: Maybe.from_optional(
                tuple(from_raw(RawRow(*r)) for r in rows) if rows else None
            )
        )
        return unsafe_unwrap(result)
    except psycopg2.ProgrammingError:
        LOG.warning("Empty fetch response")
        return Maybe.empty()


def _fetch(
    client: DbClient, chunk: int
) -> Cmd[Maybe[FrozenList[ResultE[CommitTableRow]]]]:
    return Cmd.from_cmd(lambda: _fetch_action(client, chunk))


def _fetch_one_result(client: DbClient, d_type: Type[_T]) -> Cmd[ResultE[_T]]:
    return (
        client.fetch_one()
        .map(lambda l: assert_key(l, 0))
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
    _db_client: DbClient
    _table: TableID

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        _query = (
            query.all_data_count(self._table, namespace)
            if namespace
            else query.all_data_count(self._table)
        )
        return self._db_client.execute_query(_query).bind(
            lambda _: self._db_client.fetch_one().map(
                lambda i: assert_key(i, 0).bind(lambda j: assert_type(j, int))
            )
        )

    def insert_rows(self, rows: FrozenList[CommitTableRow]) -> Cmd[None]:
        msg = Cmd.from_cmd(lambda: LOG.debug("inserting %s rows", len(rows)))
        return msg.bind(
            lambda _: self._db_client.execute_batch(
                query.insert_row(self._table),
                tuple(SqlArgs(to_dict(r)) for r in rows),
            )
        )

    def insert_unique_rows(
        self, rows: FrozenList[CommitTableRow]
    ) -> Cmd[None]:
        msg = Cmd.from_cmd(
            lambda: LOG.debug("unique inserting %s rows", len(rows))
        )
        return msg.bind(
            lambda _: self._db_client.execute_batch(
                query.insert_unique_row(self._table),
                tuple(SqlArgs(to_dict(r)) for r in rows),
            )
        )

    def _all_data(
        self, namespace: Maybe[str]
    ) -> Cmd[Stream[ResultE[CommitTableRow]]]:
        pkg_items = 2000
        statement = namespace.map(
            lambda n: query.namespace_data(self._table, n)
        ).or_else_call(lambda: query.all_data(self._table))
        items = infinite_range(0, 1).map(
            lambda _: _fetch(self._db_client, pkg_items)
        )
        return self._db_client.execute_query(statement).map(
            lambda _: from_piter(items)
            .transform(lambda s: until_empty(s))
            .map(lambda l: from_flist(l))
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
                lambda _: self._db_client.execute_query(
                    query.update_row(self._table, new, _fields)
                )
            )
        return Cmd.from_cmd(lambda: LOG.debug("delta update skipped"))


@dataclass(frozen=True)
class Client:
    # exposes utilities from and to DB using not raw objs
    _db_client: DbClient
    _table: TableID
    _raw: RawClient

    def __init__(self, _db_client: RawDbClient, _table: TableID) -> None:
        _client = DbClient(_db_client)
        _raw = RawClient(_client, _table)
        object.__setattr__(self, "_db_client", _client)
        object.__setattr__(self, "_table", _table)
        object.__setattr__(self, "_raw", _raw)

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        return self._raw.all_data_count(namespace)

    def get_context(self, repo: RepoId) -> Cmd[RepoContex]:
        last = self._db_client.execute_query(
            query.last_commit_hash(self._table, repo)
        ).bind(lambda _: _fetch_one_result(self._db_client, str))
        is_new = (
            self._db_client.execute_query(
                query.commit_exists(self._table, repo, COMMIT_HASH_SENTINEL),
            )
            .bind(lambda _: _fetch_not_empty(self._db_client))
            .map(lambda b: not b)
        )
        return last.bind(
            lambda l: is_new.map(
                lambda n: RepoContex(repo, l.value_or(None), n)
            )
        )

    def register_repos(self, reg: FrozenList[RepoRegistration]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: LOG.info("register_repos %s", str(reg))
        )
        encoded = tuple(from_reg(r) for r in reg)
        return log_info.bind(lambda _: self._raw.insert_unique_rows(encoded))

    def insert_stamps(self, stamps: FrozenList[CommitStamp]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: LOG.info("inserting %s stamps", len(stamps))
        )
        encoded = tuple(from_stamp(s) for s in stamps)
        return log_info.bind(lambda _: self._raw.insert_unique_rows(encoded))

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]:
        return self._raw.namespace_data(namespace).map(
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
                lambda _: self._raw.delta_update(
                    encoder.from_stamp(old),
                    encoder.from_stamp(new),
                    ignore_fa_hash,
                )
            )
        return Cmd.from_cmd(lambda: LOG.debug("no changes"))
