from code_etl.client._assert import (
    assert_not_none,
)
from code_etl.client.encoder import (
    CommitTableRow,
)
from code_etl.objs import (
    Commit,
    CommitData,
    CommitDataId,
    CommitId,
    CommitStamp,
    Deltas,
    RepoId,
    RepoRegistration,
    User,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from fa_purity.union import (
    inl,
    inr,
)
from typing import (
    Any,
    Optional,
    Union,
)


class RawDecodeError(Exception):
    def __init__(
        self,
        target: str,
        raw: Any,
    ):
        super().__init__(
            f"TypeError when trying to build `{target}` "
            f"from raw obj `{str(raw)}`"
        )


def _decode_user(name: Optional[str], email: Optional[str]) -> ResultE[User]:
    return assert_not_none(name).bind(
        lambda n: assert_not_none(email).map(lambda e: User(n, e))
    )


def decode_deltas(raw: CommitTableRow) -> ResultE[Deltas]:
    return assert_not_none(raw.total_insertions).bind(
        lambda i: assert_not_none(raw.total_deletions).bind(
            lambda d: assert_not_none(raw.total_lines).bind(
                lambda l: assert_not_none(raw.total_files).map(
                    lambda f: Deltas(i, d, l, f)
                )
            )
        )
    )


def decode_commit_data_2(
    raw: CommitTableRow,
) -> ResultE[CommitData]:
    author = _decode_user(raw.author_name, raw.author_email).bind(
        lambda u: assert_not_none(raw.authored_at).map(lambda d: (u, d))
    )
    commiter = _decode_user(raw.committer_name, raw.committer_email).bind(
        lambda u: assert_not_none(raw.committed_at).map(lambda d: (u, d))
    )
    deltas = decode_deltas(raw)
    return author.bind(
        lambda a: commiter.bind(
            lambda c: deltas.bind(
                lambda dl: assert_not_none(raw.message).bind(
                    lambda msg: assert_not_none(raw.summary).map(
                        lambda s: CommitData(
                            a[0], a[1], c[0], c[1], msg, s, dl
                        )
                    )
                )
            )
        )
    )


def decode_commit_data_id(
    raw: CommitTableRow,
) -> ResultE[CommitDataId]:
    return assert_not_none(raw.fa_hash).map(
        lambda fa: CommitDataId(
            RepoId(raw.namespace, raw.repository), CommitId(raw.hash, fa)
        )
    )


def decode_commit_stamp(
    raw: CommitTableRow,
) -> ResultE[CommitStamp]:
    return (
        decode_commit_data_id(raw)
        .bind(lambda i: decode_commit_data_2(raw).map(lambda j: Commit(i, j)))
        .map(lambda c: CommitStamp(c, raw.seen_at))
    )


def decode_repo_registration(
    raw: CommitTableRow,
) -> ResultE[RepoRegistration]:
    if raw.hash != COMMIT_HASH_SENTINEL:
        return Result.failure(TypeError("Not a RepoRegistration object"))
    return Result.success(
        RepoRegistration(
            CommitDataId(
                RepoId(raw.namespace, raw.repository),
                CommitId(raw.hash, "-" * 64),
            ),
            raw.seen_at,
        )
    )


def decode_commit_table_row(
    raw: CommitTableRow,
) -> ResultE[Union[CommitStamp, RepoRegistration]]:
    reg = decode_repo_registration(raw).map(lambda x: inr(x, CommitStamp))
    return reg.lash(lambda _: decode_commit_stamp(raw).map(inl))
