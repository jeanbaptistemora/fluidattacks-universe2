# pylint: skip-file

from code_etl.client.decoder import (
    decode_commit_data_2,
    decode_repo_registration,
)
from code_etl.client.encoder import (
    CommitTableRow,
)
from code_etl.factories import (
    gen_fa_hash,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitId,
    CommitStamp,
    RepoRegistration,
)
import logging
from returns.result import (
    Result,
)
from typing import (
    Union,
)

LOG = logging.getLogger(__name__)


def migrate_commit(
    raw: CommitTableRow,
) -> Result[CommitStamp, Union[KeyError, TypeError]]:
    data = decode_commit_data_2(raw)
    _id = data.map(
        lambda cd: CommitDataId(
            raw.namespace,
            raw.repository,
            CommitId(raw.hash, gen_fa_hash(cd)),
        )
    )
    commit = data.bind(lambda d: _id.map(lambda i: Commit(i, d)))
    return commit.map(lambda c: CommitStamp(c, raw.seen_at))


def migrate_row(
    row: CommitTableRow,
) -> Result[Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]]:
    reg: Result[
        Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]
    ] = decode_repo_registration(row)
    return reg.lash(lambda _: migrate_commit(row))
