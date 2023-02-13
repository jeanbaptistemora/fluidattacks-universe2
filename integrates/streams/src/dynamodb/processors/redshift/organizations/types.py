from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    country: str | None
    created_by: str
    created_date: datetime
    name: str


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_by: str
    modified_date: datetime
    pending_deletion_date: datetime | None
    status: str
