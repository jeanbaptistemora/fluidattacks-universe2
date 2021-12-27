from datetime import (
    datetime,
)
from integrates.dal import (
    get_finding_vulnerabilities,
    get_group_language,
)
from integrates.domain import (
    get_closest_finding_ids,
)
from integrates.graphql import (
    create_session,
)
from model import (
    core_model,
    time_model,
)
import sys
from typing import (
    Tuple,
)


async def main(
    finding_code: str,
    group: str,
    namespace: str,
    token: str,
) -> bool:
    success: bool = True

    create_session(api_token=token)

    locale: core_model.LocalesEnum = await get_group_language(group)
    finding_ids: Tuple[str, ...] = await get_closest_finding_ids(
        finding=core_model.FINDING_ENUM_FROM_STR[finding_code],
        group=group,
        locale=locale,
    )

    max_reattack_date: datetime = time_model.min_posible()

    for finding_id in finding_ids:
        vulnerability: core_model.Vulnerability
        vulnerabilities_store = await get_finding_vulnerabilities(
            # Any finding works well
            finding=core_model.FindingEnum.F004,
            finding_id=finding_id,
        )
        async for vulnerability in vulnerabilities_store.iterate():
            verification = vulnerability.integrates_metadata.verification

            if (
                namespace == vulnerability.namespace
                and verification
                and verification.state
                == core_model.VulnerabilityVerificationStateEnum.REQUESTED
                and verification.date > max_reattack_date
            ):
                max_reattack_date = verification.date

    sys.stdout.write(str(int(max_reattack_date.timestamp())))
    sys.stdout.write("\n")

    return success
