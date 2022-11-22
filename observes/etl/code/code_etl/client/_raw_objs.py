# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

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
class CommitTableRow:
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
        return tuple(f.name for f in dataclass_fields(CommitTableRow))  # type: ignore[misc]
