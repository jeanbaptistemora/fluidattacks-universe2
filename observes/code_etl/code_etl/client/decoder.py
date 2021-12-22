# pylint: skip-file

from code_etl.objs import (
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


@dataclass(frozen=True)
class RawRow:
    author_name: Any
    author_email: Any
    authored_at: Any
    committer_email: Any
    committer_name: Any
    committed_at: Any
    message: Any
    summary: Any
    total_insertions: Any
    total_deletions: Any
    total_lines: Any
    total_files: Any
    namespace: Any
    repository: Any
    hash: Any
    fa_hash: Any
    seen_at: Any


def _assert_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise TypeError("Not a datetime obj")


def _assert_str(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    raise TypeError("Not a str obj")


def assert_int(raw: Any) -> Result[int, TypeError]:
    if isinstance(raw, int):
        return Success(raw)
    return Failure(TypeError("Not a int obj"))


def assert_key(raw: FrozenList[Any], key: int) -> Result[Any, TypeError]:
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
    return decode_repo_registration(raw).lash(
        lambda _: decode_commit_data_id(raw)
    )
