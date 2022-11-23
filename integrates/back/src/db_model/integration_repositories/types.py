from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
    Optional,
)


class OrganizationIntegrationRepository(NamedTuple):
    id: str
    organization_id: str
    branch: str
    last_commit_date: str
    commit_count: int
    url: str


class OrganizationIntegrationRepositoryEdge(NamedTuple):
    node: OrganizationIntegrationRepository
    cursor: str


class OrganizationIntegrationRepositoryConnection(NamedTuple):
    edges: tuple[OrganizationIntegrationRepositoryEdge, ...]
    page_info: PageInfo
    total: Optional[int] = None


class OrganizationIntegrationRepositoryRequest(NamedTuple):
    organization_id: str
    after: Optional[str] = None
    first: Optional[int] = None
    paginate: bool = False
