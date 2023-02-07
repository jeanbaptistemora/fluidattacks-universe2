from __future__ import (
    annotations,
)

from . import (
    _query,
    decoder,
    encoder,
)
from ._assert import (
    assert_key,
    assert_type,
)
from ._raw import (
    RawClient,
)
from ._raw_file_commit import (
    FileRelationFactory,
    RawFileCommitClient,
)
from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
)
from code_etl.client import (
    Client,
    CommitStampDiff,
    Tables,
)
from code_etl.objs import (
    CommitStamp,
    RepoContex,
    RepoId,
    RepoRegistration,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
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


def _table_ids(table: Tables) -> TableId:
    schema = SchemaId("code")
    if table is Tables.COMMITS:
        return TableId(schema, "commits")
    if table is Tables.FILES:
        return TableId(schema, "files")


@dataclass(frozen=True)
class _Client:
    sql_client: SqlClient
    table: TableId
    raw: RawClient
    raw_2: RawFileCommitClient


@dataclass(frozen=True)
class RealClient:
    # exposes utilities from and to DB using not raw objs
    _inner: _Client
    log: logging.Logger

    @staticmethod
    def new(_sql_client: SqlClient, log: logging.Logger) -> RealClient:
        stamps = _table_ids(Tables.COMMITS)
        files_relation = _table_ids(Tables.FILES)
        return RealClient(
            _Client(
                _sql_client,
                stamps,
                RawClient(_sql_client, stamps),
                RawFileCommitClient(_sql_client, files_relation),
            ),
            log,
        )

    def client(self) -> Client:
        return Client.new(
            self.init_table,
            self.all_data_count,
            self.get_context,
            self.register_repos,
            self.insert_stamps,
            self.namespace_data,
            self.delta_update,
        )

    def init_table(self, table: Tables) -> Cmd[None]:
        if table is Tables.FILES:
            return self._inner.raw_2.init_table()
        if table is Tables.COMMITS:
            return self._inner.raw.init_table()

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
            lambda: self.log.info(
                "Registering repos: %s", str([r.commit_id.repo for r in reg])
            )
        )
        encoded = tuple(encoder.from_reg(r) for r in reg)
        return log_info.bind(
            lambda _: self._inner.raw.insert_unique_rows(encoded)
        )

    def insert_stamps(self, stamps: FrozenList[CommitStamp]) -> Cmd[None]:
        log_info = Cmd.from_cmd(
            lambda: self.log.info("Inserting %s stamps", len(stamps))
        )
        encoded = tuple(encoder.from_stamp(s) for s in stamps)
        files_relation = (
            from_flist(stamps)
            .bind(lambda s: FileRelationFactory.extract_relations(s))
            .to_list()
        )
        log_info_2 = Cmd.from_cmd(
            lambda: self.log.info(
                "Inserting %s file relations", len(files_relation)
            )
        )
        return (
            log_info
            + self._inner.raw.insert_unique_rows(encoded)
            + log_info_2
            + self._inner.raw_2.insert(files_relation)
        )

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]:
        return self._inner.raw.namespace_data(namespace).map(
            lambda s: s.map(lambda r: r.bind(decoder.decode_commit_table_row))
        )

    def delta_update(self, diff: CommitStampDiff) -> Cmd[None]:
        if diff.is_diff():
            info = Cmd.from_cmd(
                lambda: self.log.info("Delta update %s", diff.commit_id)
            )
            return info + self._inner.raw.delta_update(
                encoder.from_stamp(diff.old),
                encoder.from_stamp(diff.new),
            )
        return Cmd.from_cmd(lambda: None)
