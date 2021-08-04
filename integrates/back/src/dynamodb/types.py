from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

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


class VulnerabilityMetadata(NamedTuple):
    affected_components: str
    attack_vector: str
    cvss: Dict[str, float]
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


class OrgFindingPolicyMetadata(NamedTuple):
    name: str
    tags: Set[str]


class OrgFindingPolicyState(NamedTuple):
    modified_by: str
    modified_date: str
    status: str


class OrgFindingPolicyItem(NamedTuple):
    id: str
    org_name: str
    metadata: OrgFindingPolicyMetadata
    state: OrgFindingPolicyState


class GroupMetadata(NamedTuple):
    name: str
    description: str
    language: str
    agent_token: Optional[str] = None
