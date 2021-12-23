# pylint: skip-file

from code_etl.client.encoder import (
    RawRow,
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
from dataclasses import (
    dataclass,
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


def _assert_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise TypeError("Not a datetime obj")


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise TypeError("Not a str obj")


def assert_datetime(raw: Any) -> Result[datetime, TypeError]:
    if isinstance(raw, datetime):
        return Success(raw)
    return Failure(TypeError("Not a datetime obj"))


def assert_str(raw: Any) -> Result[str, TypeError]:
    if isinstance(raw, str):
        return Success(raw)
    return Failure(TypeError("Not a str obj"))


def assert_int(raw: Any) -> Result[int, TypeError]:
    if isinstance(raw, int):
        return Success(raw)
    return Failure(TypeError("Not a int obj"))


def assert_key(raw: FrozenList[Any], key: int) -> Result[Any, KeyError]:
    try:
        return Success(raw[key])
    except KeyError as err:
        return Failure(err)


def decode_commit_data(
    raw: FrozenList[Any],
) -> Result[CommitData, Union[KeyError, TypeError]]:
    try:
        data = CommitData(
            User(_assert_str(raw[0]), _assert_str(raw[1])),
            _assert_datetime(raw[2]),
            User(_assert_str(raw[3]), _assert_str(raw[4])),
            _assert_datetime(raw[5]),
            _assert_str(raw[6]),
            _assert_str(raw[7]),
            Deltas(
                assert_int(raw[8]).alt(raise_exception).unwrap(),
                assert_int(raw[9]).alt(raise_exception).unwrap(),
                assert_int(raw[10]).alt(raise_exception).unwrap(),
                assert_int(raw[11]).alt(raise_exception).unwrap(),
            ),
        )
        return Success(data)
    except KeyError as err:
        return Failure(err)
    except TypeError as err:
        return Failure(err)


def _decode_user(name: Any, email: Any) -> Result[User, TypeError]:
    return assert_str(name).bind(
        lambda n: assert_str(email).map(lambda e: User(n, e))
    )


def decode_deltas(raw: RawRow) -> Result[Deltas, TypeError]:
    return assert_int(raw.total_insertions).bind(
        lambda i: assert_int(raw.total_deletions).bind(
            lambda d: assert_int(raw.total_lines).bind(
                lambda l: assert_int(raw.total_files).map(
                    lambda f: Deltas(i, d, l, f)
                )
            )
        )
    )


def decode_commit_data_2(
    raw: RawRow,
) -> Result[CommitData, Union[KeyError, TypeError]]:
    author = _decode_user(raw.author_name, raw.author_email).bind(
        lambda u: assert_datetime(raw.authored_at).map(lambda d: (u, d))
    )
    commiter = _decode_user(raw.committer_name, raw.committer_email).bind(
        lambda u: assert_datetime(raw.committed_at).map(lambda d: (u, d))
    )
    deltas = decode_deltas(raw)
    return author.bind(
        lambda a: commiter.bind(
            lambda c: deltas.bind(
                lambda dl: assert_str(raw.message).bind(
                    lambda msg: assert_str(raw.summary).map(
                        lambda s: CommitData(
                            a[0], a[1], c[0], c[1], msg, s, dl
                        )
                    )
                )
            )
        )
    )


def decode_commit_data_id(
    raw: RawRow,
) -> Result[CommitDataId, Union[KeyError, TypeError]]:
    try:
        _id = CommitDataId(
            _assert_str(raw.namespace),
            _assert_str(raw.repository),
            CommitId(_assert_str(raw.hash), _assert_str(raw.fa_hash)),
        )
        return Success(_id)
    except KeyError as err:
        return Failure(err)
    except TypeError as err:
        return Failure(err)


def decode_commit_stamp(
    raw: RawRow,
) -> Result[CommitStamp, Union[KeyError, TypeError]]:
    return (
        decode_commit_data_id(raw)
        .bind(lambda i: decode_commit_data_2(raw).map(lambda j: Commit(i, j)))
        .bind(
            lambda c: assert_datetime(raw.seen_at).map(
                lambda d: CommitStamp(c, d)
            )
        )
    )


def decode_repo_registration(
    raw: RawRow,
) -> Result[RepoRegistration, Union[KeyError, TypeError]]:
    try:
        if raw.hash != COMMIT_HASH_SENTINEL:
            return Failure(TypeError("Not a RepoRegistration object"))
        repo = RepoRegistration(
            CommitDataId(
                _assert_str(raw.namespace),
                _assert_str(raw.repository),
                CommitId(_assert_str(raw.hash), "-" * 64),
            ),
            _assert_datetime(raw.seen_at),
        )
        return Success(repo)
    except TypeError as err:
        return Failure(err)


def decode_commit_table_row(
    raw: RawRow,
) -> Result[Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]]:
    reg: Result[
        Union[CommitStamp, RepoRegistration], Union[KeyError, TypeError]
    ] = decode_repo_registration(raw)
    return reg.lash(lambda _: decode_commit_stamp(raw))
