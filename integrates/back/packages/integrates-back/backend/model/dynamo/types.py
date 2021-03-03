# Standard
from typing import Any, Dict, NamedTuple, Set, Tuple


class VersionedItem(NamedTuple):
    historic: Tuple[Dict[str, Any], ...]
    metadata: Dict[str, Any]


class RootMetadata(NamedTuple):
    branch: str
    type: str
    url: str


class RootHistoric(NamedTuple):
    environment_urls: Set[str]
    environment: str
    gitignore: Set[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    status: str


class RootItem(NamedTuple):
    historic: Tuple[RootHistoric, ...]
    metadata: RootMetadata
