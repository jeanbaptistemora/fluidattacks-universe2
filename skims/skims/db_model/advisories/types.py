from typing import (
    NamedTuple,
)


class Advisory(NamedTuple):
    associated_advisory: str
    package_name: str
    package_manager: str
    vulnerable_version: str
    severity: str
    source: str
