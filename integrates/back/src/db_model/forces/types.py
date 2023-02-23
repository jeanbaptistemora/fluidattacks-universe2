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
    open: list[ExploitResult] | None = None
    closed: list[ExploitResult] | None = None
    accepted: list[ExploitResult] | None = None
    num_of_vulns_in_exploits: int | None = None
    num_of_vulns_in_integrates_exploits: int | None = None
    num_of_vulns_in_accepted_exploits: int | None = None


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
    grace_period: int | None = 0
    severity_threshold: Decimal | None = Decimal("0.0")


class ExecutionEdge(NamedTuple):
    node: Item
    cursor: str


class ExecutionsConnection(NamedTuple):
    edges: tuple[ExecutionEdge, ...]
    page_info: PageInfo
    total: int | None = None


class ForcesExecutionRequest(NamedTuple):
    execution_id: str
    group_name: str


class GroupForcesExecutionsRequest(NamedTuple):
    group_name: str
    limit: int | None = None
