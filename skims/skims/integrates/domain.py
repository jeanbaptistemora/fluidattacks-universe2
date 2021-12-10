from datetime import (
    datetime,
)
from integrates.dal import (
    do_add_execution,
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
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    yaml_dumps,
)
from utils.logs import (
    log,
)
from utils.repositories import (
    get_repo_head_hash,
)
from zone import (
    t,
)

VulnStreamType = Dict[
    core_model.VulnerabilityKindEnum,
    Tuple[
        Union[
            core_model.IntegratesVulnerabilitiesInputs,
            core_model.IntegratesVulnerabilitiesLines,
        ],
        ...,
    ],
]


def _build_vulnerabilities_stream(
    results: core_model.Vulnerabilities,
) -> VulnStreamType:
    commit_hash: str = get_repo_head_hash(CTX.config.working_dir)

    data: VulnStreamType = {
        core_model.VulnerabilityKindEnum.INPUTS: tuple(
            core_model.IntegratesVulnerabilitiesInputs(
                field=result.where,
                repo_nickname=CTX.config.namespace,
                state=result.state,
                stream=result.stream,
                url=result.what_on_integrates,
            )
            for result in results
            if result.kind == core_model.VulnerabilityKindEnum.INPUTS
            if result.stream
        ),
        core_model.VulnerabilityKindEnum.LINES: tuple(
            core_model.IntegratesVulnerabilitiesLines(
                commit_hash=commit_hash,
                line=result.where,
                path=result.what_on_integrates,
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
    return await yaml_dumps(_build_vulnerabilities_stream(results))


async def get_closest_finding_ids(
    finding: core_model.FindingEnum,
    group: str,
    locale: Optional[core_model.LocalesEnum] = None,
) -> Tuple[str, ...]:
    existing_findings: Tuple[
        ResultGetGroupFindings, ...
    ] = await get_group_findings(group=group)

    return tuple(
        existing_finding.identifier
        for existing_finding in existing_findings
        if t(finding.value.title, locale=locale) == existing_finding.title
    )


async def get_closest_finding_id(
    *,
    affected_systems: str = "",
    create_if_missing: bool = False,
    finding: core_model.FindingEnum,
    group: str,
    recreate_if_draft: bool = False,
) -> str:
    finding_ids: Tuple[str, ...] = await get_closest_finding_ids(
        finding=finding,
        group=group,
    )
    finding_id: str = finding_ids[0] if finding_ids else ""

    if (
        finding_id
        and recreate_if_draft
        and await do_delete_if_draft(
            finding_id=finding_id,
        )
    ):
        finding_id = ""

    if (
        not finding_id
        and create_if_missing
        and await do_create_draft(
            affected_systems=affected_systems,
            finding=finding,
            group=group,
        )
    ):
        finding_id = await get_closest_finding_id(
            create_if_missing=False,
            finding=finding,
            group=group,
        )

        if finding_id:
            await do_update_finding_severity(
                finding_id=finding_id,
                severity=finding.value.score.as_dict(),
            )
        else:
            finding_id = ""

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
    msg: str = "Uploading vulnerabilities to %s, batch %s of size %s"

    async def batch_upload() -> None:
        await log("info", msg, finding_id, batch_id, len(batch))
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


async def do_add_skims_execution(  # pylint: disable=too-many-arguments
    root: str,
    group_name: str,
    job_id: str,
    start_date: datetime,
    end_date: datetime,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
) -> bool:
    return await do_add_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        findings_executed=findings_executed,
    )
