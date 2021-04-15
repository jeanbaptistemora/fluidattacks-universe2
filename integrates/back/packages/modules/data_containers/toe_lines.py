# Standard
from typing import NamedTuple


class GitRootToeLines(NamedTuple):
    comments: str
    filename: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    tested_date: str
    tested_lines: int

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))
