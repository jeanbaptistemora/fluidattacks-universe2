from code_etl.str_utils import (
    TruncatedStr,
)
from code_etl.time_utils import (
    DatetimeUTC,
)
from dataclasses import (
    dataclass,
    fields as dataclass_fields,
)
from fa_purity import (
    FrozenList,
)
from typing import (
    Literal,
    Optional,
)


@dataclass(frozen=True)
class RawCommitStamp:
    # Represents commit table schema
    # pylint: disable=too-many-instance-attributes
    author_name: Optional[str]
    author_email: Optional[str]
    authored_at: Optional[DatetimeUTC]
    committer_name: Optional[str]
    committer_email: Optional[str]
    committed_at: Optional[DatetimeUTC]
    message: Optional[TruncatedStr[Literal[4096]]]
    summary: Optional[TruncatedStr[Literal[256]]]
    total_insertions: Optional[int]
    total_deletions: Optional[int]
    total_lines: Optional[int]
    total_files: Optional[int]
    namespace: str
    repository: str
    hash: str
    fa_hash: Optional[str]
    seen_at: DatetimeUTC

    @staticmethod
    def fields() -> FrozenList[str]:
        return tuple(f.name for f in dataclass_fields(RawCommitStamp))  # type: ignore[misc]


@dataclass(frozen=True)
class RawFileCommitRelation:
    # Represents commit table schema
    namespace: str
    repository: str
    hash: str
    file_path: str

    @staticmethod
    def fields() -> FrozenList[str]:
        return tuple(f.name for f in dataclass_fields(RawFileCommitRelation))  # type: ignore[misc]
