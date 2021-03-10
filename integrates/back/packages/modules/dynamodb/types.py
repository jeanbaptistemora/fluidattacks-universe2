# Standard
from typing import Any, Dict, NamedTuple, Set, Tuple


Item = Dict[str, Any]


class PrimaryKey(NamedTuple):
    partition_key: str
    sort_key: str


class Entity(NamedTuple):
    primary_key: PrimaryKey


class Facet(NamedTuple):
    attrs: Tuple[str, ...]


class Index(NamedTuple):
    name: str
    primary_key: PrimaryKey


class Table(NamedTuple):
    facets: Dict[str, Facet]
    indexes: Dict[str, Index]
    name: str
    primary_key: PrimaryKey


class RootMetadata(NamedTuple):
    branch: str
    type: str
    url: str


class RootHistoricCloning(NamedTuple):
    modified_date: str
    reason: str
    status: str


class RootHistoricState(NamedTuple):
    environment_urls: Set[str]
    environment: str
    gitignore: Set[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    status: str


class RootItem(NamedTuple):
    historic_cloning: Tuple[RootHistoricCloning, ...]
    historic_state: Tuple[RootHistoricState, ...]
    metadata: RootMetadata
