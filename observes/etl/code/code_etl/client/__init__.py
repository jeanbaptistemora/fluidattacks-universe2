# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
)

from ._raw import (
    RawClient,
)
from ._raw_file_commit import (
    FileRelationFactory,
    RawFileCommitClient,
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
    PureIter,
    ResultE,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
import logging
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.sql_client import (
    SqlClient,
)
from typing import (
    Optional,
    Union,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class _Client:
    sql_client: SqlClient
    table: TableId
    raw: RawClient
    raw_2: RawFileCommitClient


@dataclass(frozen=True)
class Client:
    # exposes utilities from and to DB using not raw objs
    _inner: _Client

    @staticmethod
    def new(_sql_client: SqlClient) -> Client:
        schema = SchemaId("code")
        stamps = TableId(schema, "commits")
        files_relation = TableId(schema, "files")
        return Client(
            _Client(
                _sql_client,
                stamps,
                RawClient(_sql_client, stamps),
                RawFileCommitClient(_sql_client, files_relation),
            )
        )

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        return self._inner.raw.all_data_count(namespace)

    def get_context(self, repo: RepoId) -> Cmd[RepoContex]:
        last = self._inner.sql_client.execute(
            *_query.last_commit_hash(self._inner.table, repo)
        ).bind(
            lambda _: self._inner.sql_client.fetch_one().map(
                lambda m: m.to_result()
                .alt(Exception)
                .bind(
                    lambda r: assert_key(r.data, 0).bind(
                        lambda i: assert_type(i, str)
                    )
                )
            )
        )
        is_new = (
            self._inner.sql_client.execute(
                *_query.commit_exists(
                    self._inner.table, repo, COMMIT_HASH_SENTINEL
                )
            )
            .bind(lambda _: self._inner.sql_client.fetch_one())
            .map(lambda b: not b.map(lambda _: True).value_or(False))
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
        encoded = tuple(encoder.from_reg(r) for r in reg)
        return log_info.bind(
            lambda _: self._inner.raw.insert_unique_rows(encoded)
        )

    def insert_stamps(self, stamps: FrozenList[CommitStamp]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: LOG.info("inserting %s stamps", len(stamps))
        )
        encoded = tuple(encoder.from_stamp(s) for s in stamps)
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
