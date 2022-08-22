from db_model.forces.enums import (
    VulnerabilityExploitState,
)
from typing import (
    NamedTuple,
    Optional,
)


class ExploitResult(NamedTuple):
    exploitability: str
    kind: str
    state: VulnerabilityExploitState
    where: str
    who: str


class ExecutionVulnerabilities(NamedTuple):
    num_of_accepted_vulnerabilities: int
    num_of_open_vulnerabilities: int
    num_of_closed_vulnerabilities: int
    open: Optional[list[ExploitResult]] = None
    closed: Optional[list[ExploitResult]] = None
    accepted: Optional[list[ExploitResult]] = None


class ForcesExecution(NamedTuple):
    id: str
    group_name: str
    date: str
    commit: str
    repo: str
    branch: str
    kind: str
    exit_code: str
    strictness: str
    origin: str
    severity_threshold: int
    vulnerabilities: ExecutionVulnerabilities
    grace_period: Optional[int] = None
