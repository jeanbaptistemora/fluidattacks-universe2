# Standard library
from typing import (
    Dict,
    Tuple,
)

# Local libraries
from apis.integrates.graphql import (
    create_session,
)
from apis.integrates.dal import (
    get_finding_vulnerabilities,
)
from apis.integrates.domain import (
    do_build_and_upload_vulnerabilities,
    get_closest_finding_id,
)
from core.constants import (
    SKIMS_MANAGED_TAG,
)
from model import (
    FindingEnum,
    Vulnerability,
)
from utils.aio import (
    materialize,
    unblock,
)
from utils.logs import (
    log,
)


async def merge_results(
    skims_results: Tuple[Vulnerability, ...],
    integrates_results: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:

    def _merge_results() -> Tuple[Vulnerability, ...]:
        # Add the Integrates results that are currently managed by Skims
        merged_results: Tuple[Vulnerability, ...] = tuple(
            result
            for result in integrates_results
            if result.what.endswith(SKIMS_MANAGED_TAG)
        )

        # Add the Skims results so they replace the current ones at Integrates
        # Also add the Skims tag
        merged_results += tuple(
            Vulnerability(
                finding=result.finding,
                kind=result.kind,
                state=result.state,
                what=f'{result.what} {SKIMS_MANAGED_TAG}',
                where=result.where,
            )
            for result in skims_results
        )

        return merged_results

    return await unblock(_merge_results)


async def persist_finding(
    *,
    finding: FindingEnum,
    group: str,
    results: Tuple[Vulnerability, ...],
) -> bool:
    await log('info', 'persisting: %s, %s results', finding.name, len(results))

    finding_id: str = await get_closest_finding_id(
        group=group,
        title=finding.value,
    )

    success: bool
    if not finding_id:
        # The finding will be created in a near future ;)
        await log('warn', 'no close finding for: %s', finding)
        success = False
        # Let's return for now
        return success

    await log('debug', 'closest finding for: %s is %s', finding, finding_id)

    merged_results: Tuple[Vulnerability, ...] = await merge_results(
        skims_results=results,
        integrates_results=await get_finding_vulnerabilities(
            finding=finding,
            finding_id=finding_id,
        ),
    )

    success = await do_build_and_upload_vulnerabilities(
        finding_id=finding_id,
        results=merged_results,
    )

    await log(
        'info', 'persisted: %s, %s results, success: %s',
        finding.name, len(results), success,
    )

    return success


async def persist(
    *,
    group: str,
    results: Tuple[Vulnerability, ...],
    token: str,
) -> bool:
    create_session(api_token=token)

    persisted_findings: Dict[FindingEnum, bool] = await materialize({
        finding: persist_finding(
            finding=finding,
            group=group,
            results=results,
        )
        for finding in FindingEnum
        for finding_results in [tuple(
            result
            for result in results
            if result.finding == finding
        )]
        if finding_results
    })

    success: bool = all(persisted_findings.values())

    return success
