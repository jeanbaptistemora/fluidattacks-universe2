from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class CodeLanguagesTableRow:
    # pylint: disable=invalid-name
    id: str
    group_name: str
    language: str
    loc: int


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    created_by: str
    created_date: datetime
    language: str
    name: str
    organization_id: str
    sprint_duration: Optional[int]
    sprint_start_date: Optional[datetime]


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    comments: Optional[str]
    has_machine: bool
    has_squad: bool
    justification: Optional[str]
    managed: str
    modified_by: str
    modified_date: datetime
    pending_deletion_date: Optional[datetime]
    service: Optional[str]
    status: str
    tier: str
    type: str
