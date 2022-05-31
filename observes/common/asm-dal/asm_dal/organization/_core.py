from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class OrganizationId:
    uuid: str
    name: str
