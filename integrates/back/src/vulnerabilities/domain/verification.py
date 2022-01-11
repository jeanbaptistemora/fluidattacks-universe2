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
from typing import (
    Any,
    Tuple,
)


async def get_efficacy(
    loaders: Any,
    vuln: Vulnerability,
) -> Decimal:
    historic: Tuple[
        VulnerabilityVerification, ...
    ] = await loaders.vulnerability_historic_verification.load(vuln.id)
    cycles: int = get_reattack_cycles(historic)
    if cycles and vuln.state.status == VulnerabilityStateStatus.CLOSED:
        return Decimal(100 / cycles).quantize(Decimal("0.01"))
    return Decimal(0)


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
