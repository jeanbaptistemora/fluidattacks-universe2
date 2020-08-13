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
    do_release_vulnerabilities,
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
    results: Tuple[Vulnerability, ...],
) -> bool:
    evidence_ids: Tuple[
        Tuple[FindingEvidenceIDEnum, FindingEvidenceDescriptionIDEnum], ...
    ] = (
        (FindingEvidenceIDEnum.EVIDENCE1,
         FindingEvidenceDescriptionIDEnum.EVIDENCE1),
        (FindingEvidenceIDEnum.EVIDENCE2,
         FindingEvidenceDescriptionIDEnum.EVIDENCE2),
        (FindingEvidenceIDEnum.EVIDENCE3,
         FindingEvidenceDescriptionIDEnum.EVIDENCE3),
        (FindingEvidenceIDEnum.EVIDENCE4,
         FindingEvidenceDescriptionIDEnum.EVIDENCE4),
        (FindingEvidenceIDEnum.EVIDENCE5,
         FindingEvidenceDescriptionIDEnum.EVIDENCE5),
    )
    number_of_samples: int = min(len(results), len(evidence_ids))
    result_samples: Tuple[Vulnerability, ...] = tuple(
        random.sample(results, k=number_of_samples),
    )

    evidence_streams: Tuple[BytesIO, ...] = await collect(
        to_png(string=result.skims_metadata.snippet)
        for result in result_samples
        if result.skims_metadata
    )
    evidence_descriptions: Tuple[str, ...] = tuple(
        result.skims_metadata.description
        for result in result_samples
        if result.skims_metadata
    )

    return all((
        *await collect(
            do_update_evidence(
                evidence_id=evidence_id,
                evidence_stream=evidence_stream.read(),
                finding_id=finding_id,
            )
            for (evidence_id, _), evidence_stream in zip(
                evidence_ids,
                evidence_streams,
            )
        ),
        *await collect(
            do_update_evidence_description(
                evidence_description_id=evidence_description_id,
                evidence_description=evidence_description,
                finding_id=finding_id,
            )
            for (_, evidence_description_id), evidence_description in zip(
                evidence_ids,
                evidence_descriptions,
            )
        )
    ))


def get_results_managed_by_skims(
    results: Tuple[Vulnerability, ...],
) -> Tuple[Vulnerability, ...]:
    results_by_skims: Tuple[Vulnerability, ...] = tuple(
        result
        for result in results
        if (
            result.integrates_metadata and
            result.integrates_metadata.source == (
                VulnerabilitySourceEnum.SKIMS
            )
        )
    )

    return results_by_skims


async def merge_results(
    skims_store: EphemeralStore,
    integrates_results: Tuple[Vulnerability, ...],
) -> EphemeralStore:
    """Merge results from Skims and Integrates, closing or creating if needed.

    :param skims_store: Store with the results from Skims
    :type skims_store: EphemeralStore
    :param integrates_results: Tuple of results from Integrates
    :type integrates_results: Tuple[Vulnerability, ...]
    :return: A new store with the merged results
    :rtype: EphemeralStore
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

    # Filter integrates results managed by skims
    integrates_results = get_results_managed_by_skims(integrates_results)

    # Create a data structure that maps hash to index
    hashes: Dict[int, int] = {
        get_vulnerability_hash(result): index
        for index, result in enumerate(integrates_results)
    }

    # Walk all Skims results
    async for result in skims_store.iterate():
        # Ignore the integrates result because Skims will perform an update
        hashes.pop(get_vulnerability_hash(result), None)

        # Store the Skims result as OPEN
        await store.store(prepare_result(
            result=result,
            state=VulnerabilityStateEnum.OPEN,
        ))

    # This are the integrates results that were not found by Skims
    #   and therefore they should be closed
    for index in hashes.values():
        await store.store(prepare_result(
            result=integrates_results[index],
            state=VulnerabilityStateEnum.OPEN,
        ))

    return store


async def persist_finding(
    *,
    finding: FindingEnum,
    group: str,
    results: Tuple[Vulnerability, ...],
    store: EphemeralStore,
) -> bool:
    """Persist a finding to Integrates

    :param finding: The finding to persist
    :type finding: FindingEnum
    :param group: The group whose state is to be synced
    :type group: str
    :param results: Tuple with the source data to persist
    :type results: Tuple[Vulnerability, ...]
    :param store: Store to read data from
    :type store: EphemeralStore
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = False
    store_length: int = await store.length()
    has_results: bool = store_length > 0

    await log('info', 'persisting: %s, %s results', finding.name, store_length)

    finding_id: str = await get_closest_finding_id(
        affected_systems=await get_affected_systems(store),
        create_if_missing=has_results,
        finding=finding,
        group=group,
        recreate_if_draft=True,
    )

    if finding_id:
        await log('info', 'finding for: %s = %s', finding.name, finding_id)

        merged_store: EphemeralStore = await merge_results(
            integrates_results=await get_finding_vulnerabilities(
                finding=finding,
                finding_id=finding_id,
            ),
            skims_store=store,
        )

        success = await do_build_and_upload_vulnerabilities(
            finding_id=finding_id,
            results=tuple([x async for x in merged_store.iterate()]),
        ) and await do_release_vulnerabilities(
            finding_id=finding_id,
        ) and await upload_evidences(
            finding_id=finding_id,
            results=results,
        ) and await do_release_finding(
            finding_id=finding_id,
        )

        await log(
            'info', 'persisted: %s, results: %s, success: %s',
            finding.name, len(results), success,
        )
    elif not has_results:
        success = True

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
    stores: Dict[FindingEnum, EphemeralStore],
    token: str,
) -> bool:
    """Persist all findings with the data extracted from the store.

    :param group: The group whose state is to be synced
    :type group: str
    :param results: Tuple with the source data to persist
    :type results: Tuple[Vulnerability, ...]
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
            results=results,
            store=stores[finding],
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
