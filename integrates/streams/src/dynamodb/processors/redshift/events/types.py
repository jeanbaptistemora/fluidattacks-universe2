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
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    created_by: str
    created_date: datetime
    event_date: datetime
    group_name: str
    hacker: str
    root_id: Optional[str]
    solution_reason: Optional[str]
    solving_date: Optional[datetime]
    status: str
    type: str
