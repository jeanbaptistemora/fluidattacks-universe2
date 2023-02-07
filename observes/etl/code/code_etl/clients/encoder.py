from __future__ import (
    annotations,
)

from ._assert import (
    assert_opt_type,
    assert_type,
)
from ._raw_objs import (
    RawCommitStamp,
)
from code_etl.objs import (
    CommitData,
    CommitDataId,
    CommitStamp,
    RepoRegistration,
)
from code_etl.str_utils import (
    truncate,
)
from code_etl.time_utils import (
    DatetimeTZ,
    DatetimeUTC,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity.frozen import (
    freeze,
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    ResultE,
    ResultFactory,
    UnwrapError,
)
from fa_purity.union import (
    UnionFactory,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    cast,
    Dict,
    Optional,
    TypeVar,
    Union,
)


def from_objs(
    data: Optional[CommitData], commit_id: CommitDataId, seen_at: DatetimeUTC
) -> RawCommitStamp:
    return RawCommitStamp(
        data.author.name if data else None,
        data.author.email if data else None,
        data.authored_at if data else None,
        data.committer.name if data else None,
        data.committer.email if data else None,
        data.committed_at if data else None,
        data.message if data else None,
        data.summary if data else None,
        data.deltas.total_insertions if data else None,
        data.deltas.total_deletions if data else None,
        data.deltas.total_lines if data else None,
        data.deltas.total_files if data else None,
        commit_id.repo.namespace,
        commit_id.repo.repository,
        commit_id.hash.hash,
        commit_id.hash.fa_hash,
        seen_at,
    )


def _optional_datetime_utc(raw: PrimitiveVal) -> ResultE[DatetimeUTC | None]:
    _factory_1: ResultFactory[DatetimeUTC | None, Exception] = ResultFactory()
    _factory_2: UnionFactory[DatetimeUTC, None] = UnionFactory()
    return assert_opt_type(raw, datetime).bind(
        lambda d: DatetimeTZ.assert_tz(d)
        .map(lambda x: DatetimeUTC.to_utc(x))
        .map(_factory_2.inl)
        if d is not None
        else _factory_1.success(d)
    )


def from_raw(raw: FrozenList[PrimitiveVal]) -> ResultE[RawCommitStamp]:
    factory: ResultFactory[RawCommitStamp, Exception] = ResultFactory()
    try:
        author_name = assert_opt_type(raw[0], str).unwrap()
        author_email = assert_opt_type(raw[1], str).unwrap()
        authored_at = _optional_datetime_utc(raw[2]).unwrap()

        committer_name = assert_opt_type(raw[3], str).unwrap()
        committer_email = assert_opt_type(raw[4], str).unwrap()
        committed_at = _optional_datetime_utc(raw[5]).unwrap()

        message = (
            assert_opt_type(raw[6], str)
            .map(lambda s: truncate(s, 4096) if s is not None else s)
            .unwrap()
        )
        summary = (
            assert_opt_type(raw[7], str)
            .map(lambda s: truncate(s, 256) if s is not None else s)
            .unwrap()
        )

        total_insertions = assert_opt_type(raw[8], int).unwrap()
        total_deletions = assert_opt_type(raw[9], int).unwrap()
        total_lines = assert_opt_type(raw[10], int).unwrap()
        total_files = assert_opt_type(raw[11], int).unwrap()

        namespace = assert_type(raw[12], str).unwrap()
        repository = assert_type(raw[13], str).unwrap()
        _hash = assert_type(raw[14], str).unwrap()
        fa_hash = assert_opt_type(raw[15], str).unwrap()

        seen_at = (
            assert_type(raw[16], datetime)
            .bind(DatetimeTZ.assert_tz)
            .map(DatetimeUTC.to_utc)
            .unwrap()
        )
        row = RawCommitStamp(
            author_name,
            author_email,
            authored_at,
            committer_name,
            committer_email,
            committed_at,
            message,
            summary,
            total_insertions,
            total_deletions,
            total_lines,
            total_files,
            namespace,
            repository,
            _hash,
            fa_hash,
            seen_at,
        )
        return factory.success(row)
    except KeyError as err:
        return factory.failure(
            Exception(f"Failed `RawCommitStamp` decode i.e. {err}")
        )
    except UnwrapError as err:
        error = cast(UnwrapError[PrimitiveVal, Exception], err)
        return factory.failure(error.container.unwrap_fail()).alt(
            lambda e: Exception(f"Failed `RawCommitStamp` decode i.e. {e}")
        )


def from_stamp(stamp: CommitStamp) -> RawCommitStamp:
    return from_objs(stamp.commit.data, stamp.commit.commit_id, stamp.seen_at)


def from_reg(reg: RepoRegistration) -> RawCommitStamp:
    return from_objs(None, reg.commit_id, reg.seen_at)


def from_row_obj(item: Union[CommitStamp, RepoRegistration]) -> RawCommitStamp:
    if isinstance(item, RepoRegistration):
        return from_reg(item)
    return from_stamp(item)


_T = TypeVar("_T")


def _from_opt(val: Optional[_T]) -> Maybe[_T]:
    return Maybe.from_optional(val)


def _encode_opt_datetime(date: Optional[DatetimeUTC]) -> Optional[str]:
    return _from_opt(date).map(lambda i: i.time.isoformat()).value_or(None)


def _encode_opt_int(num: Optional[int]) -> Optional[str]:
    return _from_opt(num).map(str).value_or(None)


def to_dict(row: RawCommitStamp) -> Dict[str, Optional[str]]:
    return {
        "author_name": row.author_name,
        "author_email": row.author_email,
        "authored_at": _encode_opt_datetime(row.authored_at),
        "committer_email": row.committer_email,
        "committer_name": row.committer_name,
        "committed_at": _encode_opt_datetime(row.committed_at),
        "message": row.message.msg if row.message else None,
        "summary": row.summary.msg if row.summary else None,
        "total_insertions": _encode_opt_int(row.total_insertions),
        "total_deletions": _encode_opt_int(row.total_deletions),
        "total_lines": _encode_opt_int(row.total_lines),
        "total_files": _encode_opt_int(row.total_files),
        "namespace": row.namespace,
        "repository": row.repository,
        "hash": row.hash,
        "fa_hash": row.fa_hash,
        "seen_at": row.seen_at.time.isoformat(),
    }


def commit_row_to_dict(row: RawCommitStamp) -> FrozenDict[str, PrimitiveVal]:
    raw: Dict[str, PrimitiveVal] = {k: v for k, v in to_dict(row).items()}
    return freeze(raw)
