from typing import (
    NamedTuple,
    Optional,
)


class ForcesVulnerabilities(NamedTuple):
    num_of_accepted_vulnerabilities: Optional[int]
    num_of_open_vulnerabilities: Optional[int]
    num_of_closed_vulnerabilities: Optional[int]


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
    grace_period: int
    severity_threshold: int
    vulnerabilities: ForcesVulnerabilities
