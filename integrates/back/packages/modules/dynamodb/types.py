# Standard
from typing import Any, Dict, NamedTuple, Set, Tuple, Union


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


class GitRootMetadata(NamedTuple):
    branch: str
    type: str
    url: str


class GitRootCloning(NamedTuple):
    modified_date: str
    reason: str
    status: str


class GitRootState(NamedTuple):
    environment_urls: Set[str]
    environment: str
    gitignore: Set[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    nickname: str
    status: str


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    state: GitRootState
    metadata: GitRootMetadata


class IPRootMetadata(NamedTuple):
    type: str


class IPRootState(NamedTuple):
    address: str
    modified_by: str
    modified_date: str
    port: str


class IPRootItem(NamedTuple):
    state: IPRootState
    metadata: IPRootMetadata


class URLRootMetadata(NamedTuple):
    type: str


class URLRootState(NamedTuple):
    host: str
    modified_by: str
    modified_date: str
    path: str
    port: str
    protocol: str


class URLRootItem(NamedTuple):
    state: URLRootState
    metadata: URLRootMetadata


RootItem = Union[GitRootItem, IPRootItem, URLRootItem]
