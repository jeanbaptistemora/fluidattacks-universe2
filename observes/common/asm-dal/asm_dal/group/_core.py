from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class GroupId:
    name: str
