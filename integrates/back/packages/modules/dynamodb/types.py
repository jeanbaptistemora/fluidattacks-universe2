# Standard
from typing import Any, Dict, NamedTuple, Set, Tuple


Item = Dict[str, Any]


class PrimaryKey(NamedTuple):
    partition_key: str
    sort_key: str


class Facet(NamedTuple):
    attrs: Tuple[str, ...]
    pk_alias: str
    sk_alias: str


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


class RootCloning(NamedTuple):
    modified_date: str
    reason: str
    status: str


class RootState(NamedTuple):
    environment_urls: Set[str]
    environment: str
    gitignore: Set[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    status: str


class RootItem(NamedTuple):
    cloning: RootCloning
    state: RootState
    metadata: RootMetadata
