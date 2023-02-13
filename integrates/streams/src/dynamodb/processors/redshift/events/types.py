from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    created_by: str
    created_date: datetime
    event_date: datetime
    group_name: str
    hacker: str
    root_id: str | None
    solution_reason: str | None
    solving_date: datetime | None
    status: str
    type: str
