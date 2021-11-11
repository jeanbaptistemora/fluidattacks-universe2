from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class GroupedVulnerabilitiesInfo(NamedTuple):
    commit_hash: Optional[str]
    specific: str
    where: str


class FindingGroupedVulnerabilitiesInfo(NamedTuple):
    grouped_ports_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_inputs_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    where: str


class Treatments(NamedTuple):
    accepted: int
    accepted_undefined: int
    in_progress: int
    new: int
