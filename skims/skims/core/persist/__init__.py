from aioextensions import (
    collect,
)
from aiogqlc.client import (
    GraphQLClient,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from core.vulnerabilities import (
    get_vulnerability_justification,
    vulns_with_reattack_requested,
)
from ctx import (
    CTX,
)
from integrates.dal import (
    do_add_finding_consult,
    do_update_evidence,
    do_update_evidence_description,
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_level_role,
    get_group_open_severity,
    get_group_roots,
    ResultGetGroupFindings,
    ResultGetGroupRoots,
)
from integrates.domain import (
    do_build_and_upload_vulnerabilities,
    do_release_finding,
    ensure_toe_inputs,
    get_closest_finding_id,
)
from integrates.graphql import (
    client as graphql_client,
)
from io import (
    BytesIO,
)
from model import (
    core_model,
)
from os import (
    cpu_count,
)
import random
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
import sys
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)
from utils.fs import (
    path_is_include,
)
from utils.logs import (
    log,
)
from utils.string import (
    to_png,
)


async def upload_evidences(
    *,
    finding_id: str,
    store: EphemeralStore,
    client: Optional[GraphQLClient] = None,
) -> bool:
    evidence_ids: Tuple[
        Tuple[
            core_model.FindingEvidenceIDEnum,
            core_model.FindingEvidenceDescriptionIDEnum,
        ],
        ...,
    ] = (
        (
            core_model.FindingEvidenceIDEnum.EVIDENCE5,
            core_model.FindingEvidenceDescriptionIDEnum.EVIDENCE5,
        ),
    )
    results: core_model.Vulnerabilities = await store.get_a_few(
        len(evidence_ids)
    )
    number_of_samples: int = min(len(results), len(evidence_ids))
    result_samples: core_model.Vulnerabilities = tuple(
        random.sample(results, k=number_of_samples),
    )

    evidence_streams: Tuple[BytesIO, ...] = tuple(
        to_png(string=result.skims_metadata.snippet)
        for result in result_samples
        if result.skims_metadata
    )
    evidence_descriptions: Tuple[str, ...] = tuple(
        result.skims_metadata.description
        for result in result_samples
        if result.skims_metadata
    )

    return all(
        (
            *await collect(
                tuple(
                    do_update_evidence(
                        evidence_id=evidence_id,
                        evidence_stream=evidence_stream.read(),
                        finding_id=finding_id,
                        client=client,
                    )
                    for (evidence_id, _), evidence_stream in zip(
                        evidence_ids,
                        evidence_streams,
                    )
                )
            ),
            *await collect(
                tuple(
                    do_update_evidence_description(
                        evidence_description_id=evidence_description_id,
                        evidence_description=evidence_description,
                        finding_id=finding_id,
                        client=client,
                    )
                    for (
                        _,
                        evidence_description_id,
                    ), evidence_description in zip(
                        evidence_ids,
                        evidence_descriptions,
                    )
                )
            ),
        )
    )


async def diff_results(  # pylint: disable=too-many-arguments
    skims_store: EphemeralStore,
    integrates_store: EphemeralStore,
    namespace: str,
    include_path_patterns: Optional[List[str]] = None,
    exclude_path_patterns: Optional[List[str]] = None,
    has_dast: bool = True,
) -> EphemeralStore:
    """Diff results from Skims and Integrates, closing or creating if needed.

    Args:
        skims_store: Store with the results from Skims.
        integrates_store: Store with the results from Integrates.

    Returns:
        A new store with the exact difference that needs to be
        persisted to Integrates in order to reflect the Skims state.
    """
    store = get_ephemeral_store()

    def prepare_result(
        result: core_model.Vulnerability,
        state: core_model.VulnerabilityStateEnum,
    ) -> core_model.Vulnerability:

        return core_model.Vulnerability(
            finding=result.finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                # Mark them as managed by skims
                source=core_model.VulnerabilitySourceEnum.SKIMS,
            ),
            skims_metadata=result.skims_metadata,
            kind=result.kind,
            namespace=result.namespace,
            state=state,
            stream=result.stream,
            what=result.what,
            where=result.where,
        )

    # Think of the update as the difference in the generation that
    #   is currently on Integrates, vs the generation that Skims found

    # The current state at Integrates
    integrates_hashes: Dict[int, core_model.VulnerabilityStateEnum] = {
        result.digest: result.state
        for result in integrates_store.iterate()
        # Filter integrates results
        # That are within the same namespace
        if result.namespace == namespace
        # And managed by skims
        if result.integrates_metadata
        and result.integrates_metadata.source
        == core_model.VulnerabilitySourceEnum.SKIMS
    }

    # The current state to Skims
    skims_hashes: Dict[int, core_model.VulnerabilityStateEnum] = {}

    # Walk all Skims results
    results_skims = tuple(skims_store.iterate())
    for result in results_skims:
        # All skims results are part of the new generation
        skims_hashes[result.digest] = result.state

    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        worker.map(
            store.store,
            (
                prepare_result(result=result, state=result.state)
                for result in results_skims
            ),
        )

    # Walk all integrates results
    results_integrates = list(
        result
        for result in integrates_store.iterate()
        if (
            # Ensure this is part of the old generation
            result.digest in integrates_hashes
            and (
                # And his result was not found by Skims
                result.digest not in skims_hashes
                and (
                    # the result path is included in the current analysis
                    path_is_include(
                        result.what,
                        include_path_patterns,
                        exclude_path_patterns,
                    )
                    if result.kind == core_model.VulnerabilityKindEnum.LINES
                    else (
                        has_dast
                        if result.kind
                        == core_model.VulnerabilityKindEnum.INPUTS
                        else True
                    )
                )
            )
        )
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        worker.map(
            store.store,
            (
                prepare_result(
                    result=result,
                    state=core_model.VulnerabilityStateEnum.CLOSED,
                )
                for result in results_integrates
            ),
        )

    return store


async def persist_finding(  # pylint: disable=too-many-locals
    *,
    existing_findings: Tuple[ResultGetGroupFindings, ...],
    finding: core_model.FindingEnum,
    group: str,
    roots: Tuple[ResultGetGroupRoots, ...],
    store: EphemeralStore,
    client: Optional[GraphQLClient] = None,
    config: Optional[core_model.SkimsConfig] = None,
) -> core_model.PersistResult:
    """Persist a finding to Integrates

    :param finding: The finding to persist
    :type finding: core_model.FindingEnum
    :param group: The group whose state is to be synced
    :type group: str
    :param store: Store to read data from
    :type store: EphemeralStore
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = False
    success_comment: bool = True
    store_length: int = store.length()
    has_results: bool = store_length > 0
    diff_store: Optional[EphemeralStore] = None
    config = config or CTX.config

    finding_id, new_finding = await get_closest_finding_id(
        existing_findings=existing_findings,
        finding=finding,
        group=group,
        client=client,
        create_if_missing=has_results,
        recreate_if_draft=has_results,
    )

    # Even if there are no results to persist we must give Skims the
    #   opportunity to close
    if finding_id:
        await log("info", "Finding for: %s = %s", finding.name, finding_id)

        integrates_store: EphemeralStore
        if new_finding:
            integrates_store = get_ephemeral_store()
        else:
            integrates_store = await get_finding_vulnerabilities(
                finding=finding, finding_id=finding_id, client=client
            )

        diff_store = await diff_results(
            integrates_store=integrates_store,
            skims_store=store,
            namespace=config.namespace,
            include_path_patterns=[
                *(config.path.include),
                *(config.apk.include),
            ],
            exclude_path_patterns=[
                *(config.path.exclude),
                *(config.apk.exclude),
            ],
            has_dast=config.dast is not None,
        )

        # Get vulnerabilities with a reattack requested
        reattacked_store = vulns_with_reattack_requested(integrates_store)

        justification = get_vulnerability_justification(
            reattacked_store=reattacked_store, store=diff_store, config=config
        )

        await ensure_toe_inputs(group=group, roots=roots, store=store)

        success = await do_build_and_upload_vulnerabilities(
            finding_id=finding_id,
            store=diff_store,
            client=client,
            config=config,
        )

        if success and justification and reattacked_store:
            success_comment = all(
                await collect(
                    do_add_finding_consult(
                        content=item,
                        finding_id=finding_id,
                        parent="0",
                        comment_type="CONSULT",
                        client=client,
                    )
                    for item in justification
                )
            )

        # Evidences and draft submit only make sense if there are results
        if has_results:
            await log(
                "info", "Persisting: %s, %s vulns", finding.name, store_length
            )
            success_release = await do_release_finding(
                auto_approve=finding.value.auto_approve,
                finding_id=finding_id,
                client=client,
            )
            success_upload_evidence = await upload_evidences(
                finding_id=finding_id, store=store, client=client
            )
            success = (
                success
                and success_release
                and success_upload_evidence
                and success_comment
            )

            await log(
                "info",
                "Persisted: %s, modified vulns: %s, success: %s",
                finding.name,
                diff_store.length(),
                success,
            )
    elif not has_results:
        success = True
    else:
        await log("critical", "Could not find or create finding: %s", finding)
        success = False

    return core_model.PersistResult(success=success, diff_result=diff_store)


async def _persist_finding(
    *,
    existing_findings: Tuple[ResultGetGroupFindings, ...],
    finding: core_model.FindingEnum,
    group: str,
    roots: Tuple[ResultGetGroupRoots, ...],
    store: EphemeralStore,
    client: Optional[GraphQLClient] = None,
    config: Optional[core_model.SkimsConfig] = None,
) -> Tuple[core_model.FindingEnum, core_model.PersistResult]:
    result = await persist_finding(
        existing_findings=existing_findings,
        finding=finding,
        group=group,
        roots=roots,
        store=store,
        client=client,
        config=config,
    )
    return (finding, result)


async def persist(
    *,
    group: str,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    roots: Optional[Tuple[ResultGetGroupRoots, ...]] = None,
    config: Optional[core_model.SkimsConfig] = None,
) -> Dict[core_model.FindingEnum, core_model.PersistResult]:
    """Persist all findings with the data extracted from the store.

    :param group: The group whose state is to be synced
    :type group: str
    :param stores: A mapping of findings to results store
    :type stores: Dict[core_model.FindingEnum, EphemeralStore]
    :return: A boolean indicating success
    :rtype: bool
    """

    config = config or CTX.config
    async with graphql_client() as client:
        initial_severity = await get_group_open_severity(group, client=client)
        existing_findings: Tuple[
            ResultGetGroupFindings, ...
        ] = await get_group_findings(group=group, client=client)
        roots = roots or (await get_group_roots(group=group, client=client))
        result = await collect(
            tuple(
                _persist_finding(
                    existing_findings=existing_findings,
                    finding=finding,
                    group=group,
                    roots=roots,
                    store=stores[finding],
                    client=client,
                    config=config,
                )
                for finding in core_model.FindingEnum
                if finding in config.checks
                and finding in stores
                and not stores[finding].has_errors
            ),
            workers=10,
        )
        final_severity = await get_group_open_severity(group, client=client)
        await log("info", "Initial %s's CVSSF: %s", group, initial_severity)
        await log("info", "Current %s's CVSSF: %s", group, final_severity)
        return dict(result)


async def verify_permissions(*, group: str) -> bool:
    success: bool = False

    try:
        role: Optional[str] = await get_group_level_role(group=group)
        if not role:
            return False
        await get_group_findings(group=group)
    except PermissionError as exc:
        await log("critical", "%s: %s", type(exc).__name__, str(exc))
        success = False
    else:
        allowed_roles: Tuple[str, ...] = ("admin",)

        if role in allowed_roles:
            await log("info", "Your role in group %s is: %s", group, role)
            success = True
        else:
            msg: str = " ".join(
                (
                    'Your role in group %s is: "%s".',
                    "This role has not enough privileges",
                    "for persisting results to Integrates.",
                    "You need one of the following roles: %s",
                )
            )
            await log("critical", msg, group, role, ", ".join(allowed_roles))
            success = False

    if not success:
        # Critical, exit
        sys.exit(1)

    return True
