# Standard
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union


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
    new_repo: Optional[str]
    nickname: str
    reason: Optional[str]
    status: str


class GitRootToeInputItem(NamedTuple):
    commit: str
    component: str
    created_date: str
    entry_point: str
    group_name: str
    seen_first_time_by: str
    tested_date: str
    verified: str
    vulns: str


class GitRootToeLinesItem(NamedTuple):
    comments: str
    filename: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    tested_date: str
    tested_lines: int
    sorts_risk_level: float


class GitRootItem(NamedTuple):
    cloning: GitRootCloning
    group_name: str
    id: str
    metadata: GitRootMetadata
    state: GitRootState


class IPRootMetadata(NamedTuple):
    address: str
    type: str
    port: str


class IPRootState(NamedTuple):
    modified_by: str
    modified_date: str
    new_repo: Optional[str]
    reason: Optional[str]
    status: str


class IPRootItem(NamedTuple):
    group_name: str
    id: str
    metadata: IPRootMetadata
    state: IPRootState


class URLRootMetadata(NamedTuple):
    host: str
    path: str
    port: str
    protocol: str
    type: str


class URLRootState(NamedTuple):
    modified_by: str
    modified_date: str
    new_repo: Optional[str]
    reason: Optional[str]
    status: str


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
