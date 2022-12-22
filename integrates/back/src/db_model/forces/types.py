from datetime import (
    datetime,
)
from db_model.forces.enums import (
    VulnerabilityExploitStatus,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
    PageInfo,
)
from typing import (
    NamedTuple,
    Optional,
)


class ExploitResult(NamedTuple):
    exploitability: str
    kind: str
    state: VulnerabilityExploitStatus
    where: str
    who: str


class ExecutionVulnerabilities(NamedTuple):
    num_of_accepted_vulnerabilities: int
    num_of_open_vulnerabilities: int
    num_of_closed_vulnerabilities: int
    open: Optional[list[ExploitResult]] = None
    closed: Optional[list[ExploitResult]] = None
    accepted: Optional[list[ExploitResult]] = None
    num_of_vulns_in_exploits: Optional[int] = None
    num_of_vulns_in_integrates_exploits: Optional[int] = None
    num_of_vulns_in_accepted_exploits: Optional[int] = None


class ForcesExecution(NamedTuple):
    id: str
    group_name: str
    execution_date: datetime
    commit: str
    repo: str
    branch: str
    kind: str
    exit_code: str
    strictness: str
    origin: str
    vulnerabilities: ExecutionVulnerabilities
    grace_period: Optional[int] = 0
    severity_threshold: Optional[Decimal] = Decimal("0.0")


class ExecutionEdge(NamedTuple):
    node: Item
    cursor: str


class ExecutionsConnection(NamedTuple):
    edges: tuple[ExecutionEdge, ...]
    page_info: PageInfo
    total: Optional[int] = None


class ForcesExecutionRequest(NamedTuple):
    execution_id: str
    group_name: str


class GroupForcesExecutionsRequest(NamedTuple):
    group_name: str
    limit: Optional[int] = None
