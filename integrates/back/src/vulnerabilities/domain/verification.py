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
import newrelic.agent
from typing import (
    Any,
    Tuple,
)


@newrelic.agent.function_trace()
async def get_efficacy(
    loaders: Any,
    vuln: Vulnerability,
) -> Decimal:
    cycles: int = await get_reattack_cycles(loaders, vuln)
    if cycles and vuln.state.status == VulnerabilityStateStatus.CLOSED:
        return Decimal(100 / cycles).quantize(Decimal("0.01"))
    return Decimal(0)


@newrelic.agent.function_trace()
async def get_reattack_cycles(
    loaders: Any,
    vuln: Vulnerability,
) -> int:
    historic: Tuple[
        VulnerabilityVerification, ...
    ] = await loaders.vulnerability_historic_verification.load(vuln.id)
    return len(
        [
            verification
            for verification in historic
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ]
    )
