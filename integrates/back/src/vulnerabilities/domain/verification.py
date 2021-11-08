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
    get_last_status,
    is_reattack_requested,
)
from typing import (
    cast,
    Dict,
    Optional,
    Tuple,
)


def get_efficacy(vuln: Dict[str, Finding]) -> Decimal:
    cycles: int = get_reattack_cycles(vuln)
    if cycles and get_last_status(vuln) == "closed":
        return Decimal(100 / cycles).quantize(Decimal("0.01"))
    return Decimal(0)


def get_efficacy_new(
    historic: Tuple[VulnerabilityVerification, ...],
    vuln: Vulnerability,
) -> Decimal:
    cycles: int = get_reattack_cycles_new(historic)
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


def get_last_reattack_date_new(
    historic: Tuple[VulnerabilityVerification, ...],
) -> Optional[str]:
    """Get last reattack date in ISO8601 UTC format"""
    return next(
        (
            verification.modified_date
            for verification in historic
            if verification.status == VulnerabilityVerificationStatus.VERIFIED
        ),
        None,
    )


def get_last_requested_reattack_date(vuln: Dict[str, Finding]) -> str:
    historic_verification = get_historic_verification(vuln)
    if is_reattack_requested(vuln):
        return historic_verification[-1]["date"]
    if len(historic_verification) >= 2:
        return historic_verification[-2]["date"]
    return ""


def get_last_requested_reattack_date_new(
    historic: Tuple[VulnerabilityVerification, ...],
    vuln: Vulnerability,
) -> str:
    """Get last requested reattack date in ISO8601 UTC format"""
    if vuln.verification.status == VulnerabilityVerificationStatus.REQUESTED:
        return vuln.verification.modified_date
    if historic and len(historic) >= 2:
        return list(historic)[-2].modified_date
    return ""


def get_reattack_cycles(vuln: Dict[str, Finding]) -> int:
    historic_verification = get_historic_verification(vuln)
    return len(
        [
            verification
            for verification in historic_verification
            if verification["status"] == "REQUESTED"
        ]
    )


def get_reattack_cycles_new(
    historic: Tuple[VulnerabilityVerification, ...]
) -> int:
    return len(
        [
            verification
            for verification in historic
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ]
    )
