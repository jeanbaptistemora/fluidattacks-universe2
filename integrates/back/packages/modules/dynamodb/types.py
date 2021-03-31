# Standard
from typing import Any, Dict, List, NamedTuple, Tuple, Union


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
    environment_urls: List[str]
    environment: str
    gitignore: List[str]
    includes_health_check: bool
    modified_by: str
    modified_date: str
    nickname: str
    status: str


class GitRootToeLines(NamedTuple):
    comments: str
    filename: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    tested_date: str
    tested_lines: int


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    metadata: GitRootMetadata
    state: GitRootState


class IPRootMetadata(NamedTuple):
    type: str


class IPRootState(NamedTuple):
    address: str
    modified_by: str
    modified_date: str
    port: str


class IPRootItem(NamedTuple):
    group_name: str
    id: str
    metadata: IPRootMetadata
    state: IPRootState


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
    group_name: str
    id: str
    metadata: URLRootMetadata
    state: URLRootState


RootItem = Union[GitRootItem, IPRootItem, URLRootItem]


class VulnerabilityMetadata(NamedTuple):
    affected_components: str
    attack_vector: str
    cvss: Dict[str, float]
    cwe: str
    description: str
    evidences: Dict[str, str]
    name: str
    recommendation: str
    requirements: str
    source: str
    specific: str
    threat: str
    type: str
    using_sorts: bool
    where: str


class VulnerabilityState(NamedTuple):
    modified_by: str
    modified_date: str
    reason: str
    source: str
    status: str
    tags: List[str]


class VulnerabilityItem(NamedTuple):
    id: str
    metadata: VulnerabilityMetadata
    state: VulnerabilityState
