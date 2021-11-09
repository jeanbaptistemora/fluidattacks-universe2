from typing import (
    NamedTuple,
    Optional,
)


class ServicesToeLines(NamedTuple):
    comments: str
    filename: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    tested_date: str
    tested_lines: int
    sorts_risk_level: int

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))


class ServicesToeLinesMetadataToUpdate(NamedTuple):
    comments: Optional[str] = None
    filename: Optional[str] = None
    group_name: Optional[str] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[str] = None
    root_id: Optional[str] = None
    tested_date: Optional[str] = None
    tested_lines: Optional[int] = None
    sorts_risk_level: Optional[int] = None
