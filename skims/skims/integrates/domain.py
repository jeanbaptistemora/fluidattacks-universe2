from aiogqlc.client import (
    GraphQLClient,
)
from ctx import (
    CTX,
)
from datetime import (
    datetime,
)
from integrates.dal import (
    do_add_execution,
    do_approve_draft,
    do_create_draft,
    do_delete_finding,
    do_finish_execution,
    do_start_execution,
    do_submit_draft,
    do_update_finding_severity,
    do_upload_vulnerabilities,
    get_finding_current_release_status,
    get_group_findings,
    ResultGetGroupFindings,
)
from model import (
    core_model,
    cvss3_model,
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
                skims_method=result.skims_metadata.source_method
                if result.skims_metadata
                else None,
                skims_technique=result.skims_metadata.technique.value
                if result.skims_metadata
                else None,
                developer=result.skims_metadata.developer.value
                if result.skims_metadata
                else None,
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
                skims_method=result.skims_metadata.source_method
                if result.skims_metadata
                else None,
                skims_technique=result.skims_metadata.technique.value
                if result.skims_metadata
                else None,
                developer=result.skims_metadata.developer.value
                if result.skims_metadata
                else None,
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
    client: Optional[GraphQLClient] = None,
) -> Tuple[str, ...]:
    existing_findings: Tuple[
        ResultGetGroupFindings, ...
    ] = await get_group_findings(group=group, client=client)

    return tuple(
        existing_finding.identifier
        for existing_finding in existing_findings
        if t(finding.value.title, locale=locale) == existing_finding.title
    )


async def get_closest_finding_id(
    *,
    existing_findings: Tuple[ResultGetGroupFindings, ...],
    finding: core_model.FindingEnum,
    group: str,
    client: Optional[GraphQLClient] = None,
    create_if_missing: bool = False,
    recreate_if_draft: bool = False,
) -> Tuple[str, bool]:
    finding_created: bool = False
    finding_ids: Tuple[str, ...] = tuple(
        existing_finding.identifier
        for existing_finding in existing_findings
        if t(finding.value.title) == existing_finding.title
    )
    finding_id: str = finding_ids[0] if finding_ids else ""

    if (
        finding_id
        and recreate_if_draft
        and await do_delete_if_draft(finding_id=finding_id, client=client)
    ):
        finding_id = ""

    if (
        not finding_id
        and create_if_missing
        and (
            result := await do_create_draft(
                finding=finding,
                group=group,
                client=client,
            )
        )
    ):
        if result.success:
            finding_created = True
            finding_id = result.id

        if finding_id:
            await do_update_finding_severity(
                finding_id=finding_id,
                severity=cvss3_model.find_score_data(
                    finding.name[1:]
                ).as_dict(),
                client=client,
            )
        else:
            finding_id = ""

    return finding_id, finding_created


async def do_build_and_upload_vulnerabilities(
    *,
    batch_size: int = 100,
    finding_id: str,
    store: EphemeralStore,
    client: Optional[GraphQLClient] = None,
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
                client=client,
            ),
        )
        batch.clear()

    batch = []
    batch_id = -1
    for result in store.iterate():
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
    client: Optional[GraphQLClient] = None,
) -> bool:
    was_deleted: bool = False
    release_status: core_model.FindingReleaseStatusEnum = (
        await get_finding_current_release_status(
            finding_id=finding_id, client=client
        )
    )

    if release_status == core_model.FindingReleaseStatusEnum.APPROVED:
        # Already released so it's not a draft
        was_deleted = False
    else:
        was_deleted = await do_delete_finding(
            finding_id=finding_id, client=client
        )

    return was_deleted


async def do_release_finding(
    *,
    auto_approve: bool,
    finding_id: str,
    client: Optional[GraphQLClient] = None,
) -> bool:
    """Release a finding to the approver and optionally the client.

    Findings are released to the releaser first who then decides if
    releasing it to the client.

    If `auto_approve` is set then it's approved automatically skipping the
    releaser.
    """
    success: bool = False
    release_status: core_model.FindingReleaseStatusEnum = (
        await get_finding_current_release_status(
            finding_id=finding_id,
            client=client,
        )
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
            success = await do_submit_draft(
                finding_id=finding_id,
                client=client,
            )

        if auto_approve:
            # Approve it
            success = success and await do_approve_draft(
                finding_id=finding_id, client=client
            )

    return success


async def do_add_skims_execution(  # pylint: disable=too-many-arguments`
    root: str,
    group_name: str,
    job_id: str,
    start_date: datetime,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
    commit_hash: str,
) -> bool:
    return await do_add_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        start_date=start_date.isoformat(),
        findings_executed=findings_executed,
        commit_hash=commit_hash,
    )


async def do_start_skims_execution(
    root: str,
    group_name: str,
    job_id: str,
    start_date: datetime,
    commit_hash: str,
) -> bool:
    return await do_start_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        start_date=start_date.isoformat(),
        commit_hash=commit_hash,
    )


async def do_finish_skims_execution(
    root: str,
    group_name: str,
    job_id: str,
    end_date: datetime,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
) -> bool:
    return await do_finish_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        end_date=end_date.isoformat(),
        findings_executed=findings_executed,
    )
