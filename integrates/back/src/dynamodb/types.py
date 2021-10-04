# pylint: disable=inherit-non-class, too-few-public-methods
from typing import (
    Any,
    Dict,
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
    # pylint: disable=unsubscriptable-object
    name: str
    description: str
    language: str
    agent_token: Optional[str] = None
