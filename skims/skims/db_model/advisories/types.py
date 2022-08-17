from typing import (
    NamedTuple,
    Optional,
)


class Advisory(NamedTuple):
    associated_advisory: str
    package_name: str
    package_manager: str
    vulnerable_version: str
    source: str
    severity: Optional[str] = None
