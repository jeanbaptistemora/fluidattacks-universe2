from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class ResultGetGroupFindings(NamedTuple):
    identifier: str
    title: str


class ResultGetGroupRoots(NamedTuple):
    id: str
    environment_urls: List[str]
    git_environment_urls: List[Dict[str, List[Dict[str, str]]]]
    nickname: str
    gitignore: List[str]
    download_url: Optional[str] = None


class VulnerabilityVerificationStateEnum(Enum):
    MASKED: str = "MASKED"
    ON_HOLD: str = "ON_HOLD"
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class TechniqueEnum(Enum):
    APK: str = "APK"
    SCA: str = "SCA"
    ADVANCE_SAST: str = "ASAST"
    BASIC_SAST: str = "BSAST"
    DAST: str = "DAST"


class VulnerabilityStateEnum(Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class SkimsVulnerabilityMetadata(NamedTuple):
    cwe: Tuple[int, ...]
    description: str
    snippet: str
    source_method: str
    developer: str
    technique: TechniqueEnum


class VulnerabilitySourceEnum(Enum):
    INTEGRATES: str = "integrates"
    SKIMS: str = "skims"


class VulnerabilityVerification(NamedTuple):
    date: datetime
    state: VulnerabilityVerificationStateEnum


class IntegratesVulnerabilityMetadata(NamedTuple):
    commit_hash: Optional[str] = None
    source: Optional[VulnerabilitySourceEnum] = None
    verification: Optional[VulnerabilityVerification] = None
    uuid: Optional[str] = None


class Vulnerability(NamedTuple):
    finding: str
    kind: VulnerabilityKindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str
    namespace: str
    stream: Optional[str] = "skims"

    integrates_metadata: Optional[IntegratesVulnerabilityMetadata] = None
    skims_metadata: Optional[SkimsVulnerabilityMetadata] = None

    @property
    def digest(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        return hash(
            (
                self.finding,
                self.kind,
                self.namespace,
                self.what,
                self.where,
            )
        )

    @property
    def what_on_integrates(self) -> str:
        if self.kind == VulnerabilityKindEnum.INPUTS:
            what = f"{self.what} ({self.namespace})"
        elif self.kind == VulnerabilityKindEnum.LINES:
            what = f"{self.namespace}/{self.what}"
        elif self.kind == VulnerabilityKindEnum.PORTS:
            what = f"{self.what} ({self.namespace})"
        else:
            raise NotImplementedError()

        return what

    @classmethod
    def what_from_integrates(
        cls, kind: VulnerabilityKindEnum, what_on_integrates: str
    ) -> Tuple[str, str]:
        if kind in {
            VulnerabilityKindEnum.INPUTS,
            VulnerabilityKindEnum.PORTS,
        }:
            if len(chunks := what_on_integrates.rsplit(" (", maxsplit=1)) == 2:
                what, namespace = chunks
                namespace = namespace[:-1]
            else:
                what, namespace = chunks[0], ""
        elif kind == VulnerabilityKindEnum.LINES:
            if len(chunks := what_on_integrates.split("/", maxsplit=1)) == 2:
                namespace, what = chunks
            else:
                namespace, what = "", chunks[0]
        else:
            raise NotImplementedError()

        return namespace, what
