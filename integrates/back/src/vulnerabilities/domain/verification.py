from custom_types import (
    Finding,
    Historic,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
from newutils.vulnerabilities import (
    is_reattack_requested,
)
from typing import (
    cast,
    Dict,
    Tuple,
)


def get_efficacy(
    historic: Tuple[VulnerabilityVerification, ...],
    vuln: Vulnerability,
) -> Decimal:
    cycles: int = get_reattack_cycles(historic)
    if cycles and vuln.state.status == VulnerabilityStateStatus.CLOSED:
        return Decimal(100 / cycles).quantize(Decimal("0.01"))
    return Decimal(0)


def get_historic_verification(vuln: Dict[str, Finding]) -> Historic:
    return cast(Historic, vuln.get("historic_verification", []))


def get_last_reattack_date(vuln: Dict[str, Finding]) -> str:
    historic_verification = get_historic_verification(vuln)
    if historic_verification:
        if historic_verification[-1]["status"] == "VERIFIED":
            return historic_verification[-1]["date"]
        if len(historic_verification) >= 2:
            return historic_verification[-2]["date"]
    return ""


def get_last_requested_reattack_date(vuln: Dict[str, Finding]) -> str:
    historic_verification = get_historic_verification(vuln)
    if is_reattack_requested(vuln):
        return historic_verification[-1]["date"]
    if len(historic_verification) >= 2:
        return historic_verification[-2]["date"]
    return ""


def get_reattack_cycles(
    historic: Tuple[VulnerabilityVerification, ...]
) -> int:
    return len(
        [
            verification
            for verification in historic
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ]
    )
