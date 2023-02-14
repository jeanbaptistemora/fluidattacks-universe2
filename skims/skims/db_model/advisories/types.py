from typing import (
    NamedTuple,
)


class Advisory(NamedTuple):
    associated_advisory: str
    package_name: str
    package_manager: str
    vulnerable_version: str
    source: str
    created_at: str | None = None
    modified_at: str | None = None
    severity: str | None = None
