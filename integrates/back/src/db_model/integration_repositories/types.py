from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
)


class OrganizationIntegrationRepository(NamedTuple):
    id: str
    organization_id: str
    branch: str
    last_commit_date: datetime | None
    commit_count: int
    url: str


class OrganizationIntegrationRepositoryEdge(NamedTuple):
    node: OrganizationIntegrationRepository
    cursor: str


class OrganizationIntegrationRepositoryConnection(NamedTuple):
    edges: tuple[OrganizationIntegrationRepositoryEdge, ...]
    page_info: PageInfo
    total: int | None = None


class OrganizationIntegrationRepositoryRequest(NamedTuple):
    organization_id: str
    after: str | None = None
    first: int | None = None
    paginate: bool = False
