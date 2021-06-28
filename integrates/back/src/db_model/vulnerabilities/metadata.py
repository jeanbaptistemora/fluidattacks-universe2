from .historics.state import (
    VulnerabilityState,
)
from .historics.treatment import (
    VulnerabilityTreatment,
)
from .historics.verification import (
    VulnerabilityVerification,
)
from .historics.zero_risk import (
    VulnerabilityZeroRisk,
)
from db_model.enums import (
    Source,
)
from enum import (
    Enum,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)


class VulnerabilityType(Enum):
    INPUTS: str = "INPUTS"
    LINES: str = "LINES"
    PORTS: str = "PORTS"


class Vulnerability(NamedTuple):
    bts_url: Optional[str]
    commit: Optional[str]
    custom_severity: Optional[int]
    finding_id: str
    hash: Optional[int]
    repo: Optional[str]
    source: Source
    specific: str
    state: VulnerabilityState
    stream: Optional[List[str]]
    uuid: str
    tags: Optional[List[str]]
    treatment: Optional[VulnerabilityTreatment]
    type: VulnerabilityType
    verification: Optional[VulnerabilityVerification]
    where: str
    zero_risk: Optional[VulnerabilityZeroRisk]
