# Standard library
from io import (
    BytesIO,
)
import os
import random
import sys
from typing import (
    Dict,
    Tuple,
    Optional,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
from integrates.graphql import (
    create_session,
)
from integrates.dal import (
    do_update_evidence,
    do_update_evidence_description,
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_level_role,
)
from integrates.domain import (
    do_build_and_upload_vulnerabilities,
    do_release_finding,
    get_closest_finding_id,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
from utils.logs import (
    log,
)
from utils.model import (
    FindingEnum,
    FindingEvidenceIDEnum,
    FindingEvidenceDescriptionIDEnum,
    get_vulnerability_hash,
    IntegratesVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_png,
)


def get_root(vulnerability: Vulnerability) -> str:
    if vulnerability.kind == VulnerabilityKindEnum.LINES:
        return os.path.basename(vulnerability.what[::-1])[::-1]

    raise NotImplementedError(f'Not implemented for: {vulnerability.kind}')


async def get_affected_systems(store: EphemeralStore) -> str:
    """Compute a list of systems from the provided store.

    :param store: Store to read data from
    :type store: EphemeralStore
    :return: A new-line separated string with the affected systems
    :rtype: str
    """
    affected_systems: Tuple[str, ...] = tuple({
        get_root(result) async for result in store.iterate()
    })

    return '\n'.join(affected_systems)


async def upload_evidences(
    *,
    finding_id: str,
    store: EphemeralStore,
) -> bool:
    evidence_ids: Tuple[
        Tuple[FindingEvidenceIDEnum, FindingEvidenceDescriptionIDEnum], ...
    ] = (
        (FindingEvidenceIDEnum.EVIDENCE5,
         FindingEvidenceDescriptionIDEnum.EVIDENCE5),
    )
    results: Tuple[Vulnerability, ...] = (
        await store.get_a_few(len(evidence_ids))
    )
    # Changed to prevent integrates DOS
    # number_of_samples: int = min(len(results), len(evidence_ids))
    number_of_samples: int = 1
    result_samples: Tuple[Vulnerability, ...] = tuple(
        random.sample(results, k=number_of_samples),
    )

    evidence_streams: Tuple[BytesIO, ...] = await collect(tuple(
        to_png(string=result.skims_metadata.snippet)
        for result in result_samples
        if result.skims_metadata
    ))
    evidence_descriptions: Tuple[str, ...] = tuple(
        result.skims_metadata.description
        for result in result_samples
        if result.skims_metadata
    )

    return all((
        *await collect(tuple(
            do_update_evidence(
                evidence_id=evidence_id,
                evidence_stream=evidence_stream.read(),
                finding_id=finding_id,
            )
            for (evidence_id, _), evidence_stream in zip(
                evidence_ids,
                evidence_streams,
            )
        )),
        *await collect(tuple(
            do_update_evidence_description(
                evidence_description_id=evidence_description_id,
                evidence_description=evidence_description,
                finding_id=finding_id,
            )
            for (_, evidence_description_id), evidence_description in zip(
                evidence_ids,
                evidence_descriptions,
            )
        ))
    ))


async def diff_results(
    skims_store: EphemeralStore,
    integrates_store: EphemeralStore,
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
        result: Vulnerability,
        state: VulnerabilityStateEnum,
    ) -> Vulnerability:
        return Vulnerability(
            finding=result.finding,
            integrates_metadata=IntegratesVulnerabilityMetadata(
                # Mark them as managed by skims
                source=VulnerabilitySourceEnum.SKIMS,
            ),
            kind=result.kind,
            state=state,
            what=result.what,
            where=result.where,
        )

    # Think of the update as the difference in the generation that
    #   is currently on Integrates, vs the generation that Skims found

    # The current state at Integrates
    integrates_hashes: Dict[int, VulnerabilityStateEnum] = {
        get_vulnerability_hash(result): result.state
        async for result in integrates_store.iterate()
        # Filter integrates results managed by skims
        if (result.integrates_metadata and
            result.integrates_metadata.source == (
                VulnerabilitySourceEnum.SKIMS
            ))
    }

    # The current state to Skims
    skims_hashes: Dict[int, VulnerabilityStateEnum] = {}

    # Walk all Skims results
    async for result in skims_store.iterate():
        result_hash = get_vulnerability_hash(result)

        # All skims results are part of the new generation
        skims_hashes[result_hash] = result.state

        # Check if this result is in the old generation and changed stated
        if integrates_hashes.get(result_hash) == result.state:
            # The result exists in the old generation and has not changed state
            pass
        else:
            # Either this is a new vulnerability or it has changed state
            # Let's store the Skims result for persistion
            await store.store(prepare_result(
                result=result,
                state=result.state,
            ))

    # Walk all integrates results
    async for result in integrates_store.iterate():
        result_hash = get_vulnerability_hash(result)

        if (
            # Ensure this is part of the old generation
            result_hash in integrates_hashes
            # And his result was not found by Skims
            and result_hash not in skims_hashes
            # And this result is OPEN
            and result.state == VulnerabilityStateEnum.OPEN \
        ):
            # This result must be CLOSED and persisted to Integrates
            await store.store(prepare_result(
                result=result,
                state=VulnerabilityStateEnum.CLOSED,
            ))

    return store


async def persist_finding(
    *,
    finding: FindingEnum,
    group: str,
    store: EphemeralStore,
    persist_evidences: Optional[bool] = True
) -> bool:
    """Persist a finding to Integrates

    :param finding: The finding to persist
    :type finding: FindingEnum
    :param group: The group whose state is to be synced
    :type group: str
    :param store: Store to read data from
    :type store: EphemeralStore
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = False
    store_length: int = await store.length()
    has_results: bool = store_length > 0

    await log('info', 'persisting: %s, %s vulns', finding.name, store_length)

    finding_id: str = await get_closest_finding_id(
        affected_systems=await get_affected_systems(store),
        create_if_missing=has_results,
        finding=finding,
        group=group,
        recreate_if_draft=has_results,
    )

    # Even if there are no results to persist we must give Skims the
    #   opportunity to close
    if finding_id:
        await log('info', 'finding for: %s = %s', finding.name, finding_id)

        diff_store: EphemeralStore = await diff_results(
            integrates_store=await get_finding_vulnerabilities(
                finding=finding,
                finding_id=finding_id,
            ),
            skims_store=store,
        )

        success = await do_build_and_upload_vulnerabilities(
            finding_id=finding_id,
            store=diff_store,
        )

        # Evidences and draft submit only make sense if there are results
        if has_results:
            success_release = await do_release_finding(
                auto_approve=finding.value.auto_approve,
                finding_id=finding_id,
            )
            success_upload_evidence = await upload_evidences(
                finding_id=finding_id,
                store=store,
            ) if persist_evidences else True
            success = success and success_release and success_upload_evidence

        await log(
            'info', 'persisted: %s, modified vulns: %s, success: %s',
            finding.name, await diff_store.length(), success,
        )
    elif not has_results:
        success = True

        await log(
            'info', 'persisted: %s, vulns: %s, success: %s',
            finding.name, store_length, success,
        )
    else:
        await log('critical', 'could not find or create finding: %s', finding)
        success = False

    return success


async def persist(
    *,
    group: str,
    stores: Dict[FindingEnum, EphemeralStore],
    token: str,
    persist_evidences: Optional[bool] = True,
) -> bool:
    """Persist all findings with the data extracted from the store.

    :param group: The group whose state is to be synced
    :type group: str
    :param stores: A mapping of findings to results store
    :type stores: Dict[FindingEnum, EphemeralStore]
    :param token: Integrates API token
    :type token: str
    :return: A boolean indicating success
    :rtype: bool
    """
    create_session(api_token=token)

    await verify_permissions(group=group)

    success: bool = all(await collect(tuple(
        persist_finding(
            finding=finding,
            group=group,
            store=stores[finding],
            persist_evidences=persist_evidences,
        )
        for finding in FindingEnum
    )))

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
