# Standard library
import sys
from typing import (
    Dict,
    Tuple,
)

# Local libraries
from integrates.graphql import (
    create_session,
)
from integrates.dal import (
    do_release_vulnerability,
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_level_role,
)
from integrates.domain import (
    do_build_and_upload_vulnerabilities,
    get_closest_finding_id,
)
from utils.aio import (
    materialize,
    unblock,
)
from utils.logs import (
    log,
)
from utils.model import (
    FindingEnum,
    IntegratesVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilitySourceEnum,
)


async def approve_skims_vulnerabilities(
    *,
    finding: FindingEnum,
    finding_id: str,
) -> bool:
    return all(
        await materialize(
            do_release_vulnerability(
                finding_id=finding_id,
                vulnerability_uuid=vulnerability.integrates_metadata.uuid
            )
            for vulnerability in await get_finding_vulnerabilities(
                finding=finding,
                finding_id=finding_id,
            )
            if (vulnerability.integrates_metadata
                and vulnerability.integrates_metadata.uuid
                and vulnerability.integrates_metadata.approval_status == (
                    VulnerabilityApprovalStatusEnum.PENDING
                )
                and vulnerability.integrates_metadata.source == (
                    VulnerabilitySourceEnum.SKIMS
                ))
        )
    )


async def merge_results(
    skims_results: Tuple[Vulnerability, ...],
    integrates_results: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:

    def _merge_results() -> Tuple[Vulnerability, ...]:
        # Add Integrates results
        merged_results: Tuple[Vulnerability, ...] = tuple(
            result
            for result in integrates_results
            # We only manage the ones who have been created by skims
            if (result.integrates_metadata and
                result.integrates_metadata.source == (
                    VulnerabilitySourceEnum.SKIMS
                ))
        )

        # Add skims results
        merged_results += tuple(
            Vulnerability(
                finding=result.finding,
                integrates_metadata=IntegratesVulnerabilityMetadata(
                    # Mark them as managed by skims
                    source=VulnerabilitySourceEnum.SKIMS,
                ),
                kind=result.kind,
                state=result.state,
                what=result.what,
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
        create_if_missing=True,
        finding=finding,
        group=group,
    )

    if finding_id:
        await log('debug', 'closest finding for: %s = %s', finding, finding_id)

        merged_results: Tuple[Vulnerability, ...] = await merge_results(
            skims_results=results,
            integrates_results=await get_finding_vulnerabilities(
                finding=finding,
                finding_id=finding_id,
            ),
        )

        success: bool = await do_build_and_upload_vulnerabilities(
            finding_id=finding_id,
            results=merged_results,
        ) and await approve_skims_vulnerabilities(
            finding=finding,
            finding_id=finding_id,
        )

        await log(
            'info', 'persisted: %s, results: %s, success: %s',
            finding.name, len(results), success,
        )
    else:
        await log('critical', 'could not find or create finding: %s', finding)
        success = False

    return success


async def persist(
    *,
    group: str,
    results: Tuple[Vulnerability, ...],
    token: str,
) -> bool:
    create_session(api_token=token)

    await verify_permissions(group=group)

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


async def verify_permissions(*, group: str) -> bool:
    success: bool = False

    try:
        role: str = await get_group_level_role(group=group)
        await get_group_findings(group=group)
    except PermissionError as exc:
        await log('critical', '%s: %s', type(exc).__name__, str(exc))
        success = False
    else:
        allowed_roles: Tuple[str, ...] = (
            'admin',
            'analyst',
        )

        if role in allowed_roles:
            await log('info', 'Your role in group %s is: %s', group, role)
            success = True
        else:
            msg: str = ' '.join((
                'Your role in group %s is: "%s".',
                'This role has not enough privileges',
                'for persisting results to Integrates.',
                'You need one of the following roles: %s'
            ))
            await log('critical', msg, group, role, ', '.join(allowed_roles))
            success = False

    if not success:
        # Critical, exit
        sys.exit(1)

    return True
