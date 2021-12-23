# pylint: skip-file

from code_etl.client._assert import (
    assert_not_none,
    assert_type,
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
    RepoRegistration,
    User,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    FrozenList,
)
from returns.functions import (
    raise_exception,
)
from returns.result import (
    Failure,
    Result,
    Success,
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


def decode_commit_data(
    raw: FrozenList[Any],
) -> Result[CommitData, Union[KeyError, TypeError]]:
    try:
        data = CommitData(
            User(
                assert_type(raw[0], str).alt(raise_exception).unwrap(),
                assert_type(raw[1], str).alt(raise_exception).unwrap(),
            ),
            assert_type(raw[2], datetime).alt(raise_exception).unwrap(),
            User(
                assert_type(raw[3], str).alt(raise_exception).unwrap(),
                assert_type(raw[4], str).alt(raise_exception).unwrap(),
            ),
            assert_type(raw[5], datetime).alt(raise_exception).unwrap(),
            assert_type(raw[6], str).alt(raise_exception).unwrap(),
            assert_type(raw[7], str).alt(raise_exception).unwrap(),
            Deltas(
                assert_type(raw[8], int).alt(raise_exception).unwrap(),
                assert_type(raw[9], int).alt(raise_exception).unwrap(),
                assert_type(raw[10], int).alt(raise_exception).unwrap(),
                assert_type(raw[11], int).alt(raise_exception).unwrap(),
            ),
        )
        return Success(data)
    except KeyError as err:
        return Failure(err)
    except TypeError as err:
        return Failure(err)


def _decode_user(
    name: Optional[str], email: Optional[str]
) -> Result[User, TypeError]:
    return assert_not_none(name).bind(
        lambda n: assert_not_none(email).map(lambda e: User(n, e))
    )


def decode_deltas(raw: CommitTableRow) -> Result[Deltas, TypeError]:
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
) -> Result[CommitData, Union[KeyError, TypeError]]:
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
) -> Result[CommitDataId, Union[KeyError, TypeError]]:
    return assert_not_none(raw.fa_hash).map(
        lambda fa: CommitDataId(
            raw.namespace, raw.repository, CommitId(raw.hash, fa)
        )
    )


def decode_commit_stamp(
    raw: CommitTableRow,
) -> Result[CommitStamp, Union[KeyError, TypeError]]:
    return (
        decode_commit_data_id(raw)
        .bind(lambda i: decode_commit_data_2(raw).map(lambda j: Commit(i, j)))
        .map(lambda c: CommitStamp(c, raw.seen_at))
    )


def decode_repo_registration(
    raw: CommitTableRow,
) -> Result[RepoRegistration, Union[KeyError, TypeError]]:
    if raw.hash != COMMIT_HASH_SENTINEL:
        return Failure(TypeError("Not a RepoRegistration object"))
    return Success(
        RepoRegistration(
            CommitDataId(
                raw.namespace,
                raw.repository,
                CommitId(raw.hash, "-" * 64),
            ),
            raw.seen_at,
        )
    )


def decode_commit_table_row(
    raw: CommitTableRow,
) -> Result[Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]]:
    reg: Result[
        Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]
    ] = decode_repo_registration(raw)
    return reg.lash(lambda _: decode_commit_stamp(raw))
