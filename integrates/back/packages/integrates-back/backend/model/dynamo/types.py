# Standard
from typing import Any, Dict, NamedTuple, Set, Tuple


Item = Dict[str, Any]


class VersionedItem(NamedTuple):
    historic: Tuple[Dict[str, Any], ...]
    metadata: Dict[str, Any]


class PrimaryKey(NamedTuple):
    partition_key: str
    sort_key: str


class Entity(NamedTuple):
    primary_key: PrimaryKey


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
