# Standard library
from typing import (
    Dict,
    Tuple,
    Union,
)

# Local libraries
from integrates.dal import (
    do_create_draft,
    do_delete_finding,
    do_submit_draft,
    do_update_finding_severity,
    do_upload_vulnerabilities,
    get_finding_current_release_status,
    get_group_findings,
    ResultGetGroupFindings,
)
from utils.aio import (
    unblock,
)
from utils.encodings import (
    yaml_dumps,
)
from utils.model import (
    FindingEnum,
    FindingReleaseStatus,
    IntegratesVulnerabilitiesLines,
    SeverityEnum,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
)
from utils.string import (
    are_similar,
)


async def build_vulnerabilities_stream(
    *,
    results: Tuple[Vulnerability, ...],
) -> str:

    data_type = Dict[
        VulnerabilityKindEnum,
        Tuple[Union[IntegratesVulnerabilitiesLines], ...]
    ]

    def _get_data() -> data_type:
        data: data_type = {
            VulnerabilityKindEnum.LINES: tuple(
                IntegratesVulnerabilitiesLines(
                    line=result.where,
                    path=result.what,
                    source=(
                        result.integrates_metadata.source
                        if (result.integrates_metadata and
                            result.integrates_metadata.source)
                        else VulnerabilitySourceEnum.INTEGRATES
                    ),
                    state=result.state,
                )
                for result in results
                if result.kind == VulnerabilityKindEnum.LINES
            ),
            # More bindings for PORTS and INPUTS go here ...
        }

        return data

    return await yaml_dumps(await unblock(_get_data))


async def get_closest_finding_id(
    *,
    create_if_missing: bool = False,
    finding: FindingEnum,
    group: str,
) -> str:
    existing_findings: Tuple[ResultGetGroupFindings, ...] = \
        await get_group_findings(group=group)

    for existing_finding in existing_findings:
        if are_similar(finding.value, existing_finding.title):
            return existing_finding.identifier

    # No similar finding has been found at this point

    if create_if_missing:
        if await do_create_draft(
            finding=finding,
            group=group,
        ):
            finding_id: str = await get_closest_finding_id(
                create_if_missing=False,
                finding=finding,
                group=group,
            )
            await do_update_finding_severity(
                finding_id=finding_id,
                severity=getattr(SeverityEnum, finding.name),
            )
        else:
            finding_id = ''
    else:
        finding_id = ''

    return finding_id


async def delete_closest_findings(*, group: str, finding: FindingEnum) -> bool:
    success: bool = True

    while True:
        finding_id: str = await get_closest_finding_id(
            finding=finding,
            group=group,
        )

        if finding_id:
            success = success and await do_delete_finding(
                finding_id=finding_id,
            )
        else:
            # All findings have been deleted
            break

    return success


async def do_build_and_upload_vulnerabilities(
    *,
    finding_id: str,
    results: Tuple[Vulnerability, ...],
) -> bool:
    return await do_upload_vulnerabilities(
        finding_id=finding_id,
        stream=await build_vulnerabilities_stream(
            results=results,
        ),
    )


async def do_release_finding(
    *,
    finding_id: str,
) -> bool:
    success: bool = False
    release_status: FindingReleaseStatus = (
        await get_finding_current_release_status(finding_id=finding_id)
    )

    if release_status in (
        FindingReleaseStatus.SUBMITTED,
        FindingReleaseStatus.APPROVED,
    ):
        # Already released
        success = True
    else:
        success = await do_submit_draft(finding_id=finding_id)

    return success
