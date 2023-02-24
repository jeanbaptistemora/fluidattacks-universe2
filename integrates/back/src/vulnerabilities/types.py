from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from typing import (
    NamedTuple,
)


class GroupedVulnerabilitiesInfo(NamedTuple):
    commit_hash: str | None
    specific: str
    where: str


class FindingGroupedVulnerabilitiesInfo(NamedTuple):
    grouped_ports_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_inputs_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    where: str


class Treatments(NamedTuple):
    accepted: int
    accepted_undefined: int
    in_progress: int
    untreated: int


class Verifications(NamedTuple):
    requested: int
    on_hold: int
    verified: int


class VulnerabilityDescriptionToUpdate(NamedTuple):
    commit: str | None = None
    source: Source | None = None
    where: str | None = None
    specific: str | None = None


class VulnerabilityTreatmentToUpdate(NamedTuple):
    accepted_until: datetime | None
    assigned: str | None
    justification: str
    status: VulnerabilityTreatmentStatus


ToolItem = dict[str, str]
