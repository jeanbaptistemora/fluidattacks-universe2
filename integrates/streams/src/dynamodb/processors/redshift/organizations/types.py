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
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    country: Optional[str]
    created_by: str
    created_date: datetime
    name: str


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_by: str
    modified_date: datetime
    pending_deletion_date: Optional[datetime]
    status: str
