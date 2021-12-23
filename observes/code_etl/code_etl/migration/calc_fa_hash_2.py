# pylint: skip-file

from code_etl.client.decoder import (
    assert_datetime,
    assert_str,
    decode_commit_data_2,
    decode_repo_registration,
    RawRow,
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
    raw: RawRow,
) -> Result[CommitStamp, Union[KeyError, TypeError]]:
    data = decode_commit_data_2(raw)
    _id = data.bind(
        lambda cd: assert_str(raw.namespace).bind(
            lambda n: assert_str(raw.repository).bind(
                lambda r: assert_str(raw.hash).map(
                    lambda h: CommitDataId(
                        n,
                        r,
                        CommitId(h, gen_fa_hash(cd)),
                    )
                )
            )
        )
    )
    commit = data.bind(lambda d: _id.map(lambda i: Commit(i, d)))
    return commit.bind(
        lambda c: assert_datetime(raw.seen_at).map(lambda d: CommitStamp(c, d))
    )


def migrate_row(
    row: RawRow,
) -> Result[Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]]:
    reg: Result[
        Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]
    ] = decode_repo_registration(row)
    return reg.lash(lambda _: migrate_commit(row))
