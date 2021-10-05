# pylint: disable=too-few-public-methods,  inherit-non-class
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class GroupedVulnerabilitiesInfo(NamedTuple):
    # pylint: disable=unsubscriptable-object
    commit_hash: Optional[str]
    specific: str
    where: str


class FindingGroupedVulnerabilitiesInfo(NamedTuple):
    grouped_ports_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_inputs_vulnerabilities: Tuple[GroupedVulnerabilitiesInfo, ...]
    where: str
