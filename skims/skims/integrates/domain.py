# Standard library
from typing import (
    Dict,
    List,
    Tuple,
    Union,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from integrates.dal import (
    do_approve_draft,
    do_create_draft,
    do_delete_finding,
    do_submit_draft,
    do_update_finding_severity,
    do_upload_vulnerabilities,
    get_finding_current_release_status,
    get_group_findings,
    ResultGetGroupFindings,
)
from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    deserialize_what_from_vuln,
    yaml_dumps,
)
from utils.logs import (
    log,
)
from utils.repositories import (
    get_repo_head_hash,
)
from utils.string import (
    are_similar,
)
from zone import (
    t,
)


VulnStreamType = Dict[core_model.VulnerabilityKindEnum, Tuple[
    Union[
        core_model.IntegratesVulnerabilitiesLines
    ],
    ...,
]]


def _build_vulnerabilities_stream(
    results: core_model.Vulnerabilities,
) -> VulnStreamType:
    data: VulnStreamType = {
        core_model.VulnerabilityKindEnum.LINES: tuple(
            core_model.IntegratesVulnerabilitiesLines(
                commit_hash=get_repo_head_hash(deserialize_what_from_vuln(
                    core_model.VulnerabilityKindEnum.LINES,
                    result.what,
                )),
                line=result.where,
                path=result.what,
                repo_nickname=CTX.config.namespace,
                state=result.state,
            )
            for result in results
            if result.kind == core_model.VulnerabilityKindEnum.LINES
        ),
        # More bindings for PORTS and INPUTS go here ...
    }

    return data


async def build_vulnerabilities_stream(
    *,
    results: core_model.Vulnerabilities,
) -> str:
    return await yaml_dumps(
        await in_process(_build_vulnerabilities_stream, results),
    )


async def get_closest_finding_id(
    *,
    affected_systems: str = '',
    create_if_missing: bool = False,
    finding: core_model.FindingEnum,
    group: str,
    recreate_if_draft: bool = False,
) -> str:
    finding_id: str = ''

    existing_findings: Tuple[ResultGetGroupFindings, ...] = \
        await get_group_findings(group=group)

    for existing_finding in existing_findings:
        if are_similar(t(finding.value.title), existing_finding.title):
            finding_id = existing_finding.identifier
            break

    if finding_id and recreate_if_draft and await do_delete_if_draft(
        finding_id=finding_id,
    ):
        finding_id = ''

    if not finding_id and create_if_missing and await do_create_draft(
        affected_systems=affected_systems,
        finding=finding,
        group=group,
    ):
        finding_id = await get_closest_finding_id(
            create_if_missing=False,
            finding=finding,
            group=group,
        )

        if finding_id:
            await do_update_finding_severity(
                finding_id=finding_id,
                severity=finding.value.severity,
            )
        else:
            finding_id = ''

    return finding_id


async def delete_closest_findings(
    *,
    group: str,
    finding: core_model.FindingEnum,
) -> bool:
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
    batch_size: int = 50,
    finding_id: str,
    store: EphemeralStore,
) -> bool:
    successes: List[bool] = []
    msg: str = 'Uploading vulnerabilities to %s, batch %s of size %s'

    async def batch_upload() -> None:
        await log('info', msg, finding_id, batch_id, len(batch))
        successes.append(
            await do_upload_vulnerabilities(
                finding_id=finding_id,
                stream=await build_vulnerabilities_stream(
                    results=tuple(batch),
                ),
            ),
        )
        batch.clear()

    batch = []
    batch_id = -1
    async for result in store.iterate():
        batch.append(result)
        if len(batch) == batch_size:
            batch_id += 1
            await batch_upload()

    if batch:
        batch_id += 1
        await batch_upload()

    return all(successes)


async def do_delete_if_draft(
    *,
    finding_id: str,
) -> bool:
    was_deleted: bool = False
    release_status: core_model.FindingReleaseStatusEnum = (
        await get_finding_current_release_status(finding_id=finding_id)
    )

    if release_status == core_model.FindingReleaseStatusEnum.APPROVED:
        # Already released so it's not a draft
        was_deleted = False
    else:
        was_deleted = await do_delete_finding(finding_id=finding_id)

    return was_deleted


async def do_release_finding(
    *,
    auto_approve: bool,
    finding_id: str,
) -> bool:
    """Release a finding to the approver and optionally the client.

    Findings are released to the releaser first who then decides if
    releasing it to the client.

    If `auto_approve` is set then it's approved automatically skipping the
    releaser.
    """
    success: bool = False
    release_status: core_model.FindingReleaseStatusEnum = (
        await get_finding_current_release_status(finding_id=finding_id)
    )

    if release_status == core_model.FindingReleaseStatusEnum.APPROVED:
        # Already released
        success = True
    else:
        if release_status == core_model.FindingReleaseStatusEnum.SUBMITTED:
            # Already submitted
            success = True
        else:
            # Submit it
            success = await do_submit_draft(finding_id=finding_id)

        if auto_approve:
            # Approve it
            success = success and await do_approve_draft(finding_id=finding_id)

    return success
