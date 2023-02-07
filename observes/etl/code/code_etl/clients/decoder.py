from ._assert import (
    assert_not_none,
)
from ._raw_objs import (
    RawCommitStamp,
)
from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
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
from fa_purity import (
    Maybe,
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
    Optional,
    Union,
)


def _decode_user(name: Optional[str], email: Optional[str]) -> ResultE[User]:
    return assert_not_none(name).bind(
        lambda n: assert_not_none(email).map(lambda e: User(n, e))
    )


def decode_deltas(raw: RawCommitStamp) -> ResultE[Deltas]:
    return assert_not_none(raw.total_insertions).bind(
        lambda i: assert_not_none(raw.total_deletions).bind(
            lambda d: assert_not_none(raw.total_lines).bind(
                lambda lines: assert_not_none(raw.total_files).map(
                    lambda f: Deltas(i, d, lines, f)
                )
            )
        )
    )


def decode_commit_data_2(
    raw: RawCommitStamp,
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
                            a[0], a[1], c[0], c[1], msg, s, dl, Maybe.empty()
                        )
                    )
                )
            )
        )
    ).alt(lambda e: TypeError(f"Failed `CommitData` decode i.e. {e}"))


def decode_commit_data_id(
    raw: RawCommitStamp,
) -> ResultE[CommitDataId]:
    return (
        assert_not_none(raw.fa_hash)
        .map(
            lambda fa: CommitDataId(
                RepoId(raw.namespace, raw.repository), CommitId(raw.hash, fa)
            )
        )
        .alt(lambda e: TypeError(f"Failed `CommitDataId` decode i.e. {e}"))
    )


def decode_commit_stamp(
    raw: RawCommitStamp,
) -> ResultE[CommitStamp]:
    return (
        decode_commit_data_id(raw)
        .bind(lambda i: decode_commit_data_2(raw).map(lambda j: Commit(i, j)))
        .map(lambda c: CommitStamp(c, raw.seen_at))
    ).alt(lambda e: TypeError(f"Failed `CommitStamp` decode i.e. {e}"))


def decode_repo_registration(
    raw: RawCommitStamp,
) -> ResultE[RepoRegistration]:
    if raw.hash != COMMIT_HASH_SENTINEL:
        return Result.failure(
            TypeError("Failed `RepoRegistration` decode"), RepoRegistration
        ).alt(Exception)
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
    raw: RawCommitStamp,
) -> ResultE[Union[CommitStamp, RepoRegistration]]:
    reg = decode_repo_registration(raw).map(lambda x: inr(x, CommitStamp))
    return reg.lash(lambda _: decode_commit_stamp(raw).map(lambda x: inl(x)))
