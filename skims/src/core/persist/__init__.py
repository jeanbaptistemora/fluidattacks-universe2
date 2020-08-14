# Standard library
from io import (
    BytesIO,
)
import os
import random
import sys
from typing import (
    Dict,
    Set,
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
    store: EphemeralStore,
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
    results: Tuple[Vulnerability, ...] = (
        await store.get_a_few(len(evidence_ids))
    )
    number_of_samples: int = min(len(results), len(evidence_ids))
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


async def merge_results(
    skims_store: EphemeralStore,
    integrates_store: EphemeralStore,
) -> EphemeralStore:
    """Merge results from Skims and Integrates, closing or creating if needed.

    :param skims_store: Store with the results from Skims
    :type skims_store: EphemeralStore
    :param integrates_store: Store with the results from Integrates
    :type integrates_store: EphemeralStore
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

    # Think of the update as the difference in the generation that
    #   is currently on Integrates, vs the generation that Skims found
    new_generation_hashes: Set[int] = set()
    old_generation_hashes: Set[int] = {
        get_vulnerability_hash(result)
        async for result in integrates_store.iterate()
        # Filter integrates results managed by skims
        if (result.integrates_metadata and
            result.integrates_metadata.source == (
                VulnerabilitySourceEnum.SKIMS
            ))
    }

    # Walk all Skims results
    async for result in skims_store.iterate():
        # Store the Skims result as OPEN in the new generation
        new_generation_hashes.add(get_vulnerability_hash(result))
        await store.store(prepare_result(
            result=result,
            state=VulnerabilityStateEnum.OPEN,
        ))

    # This difference are results that should be CLOSED on Integrates
    generation_difference: Set[int] = (
        old_generation_hashes - new_generation_hashes
    )

    # Walk all integrates results that are in the generation difference
    async for result in integrates_store.iterate():
        if get_vulnerability_hash(result) in generation_difference:
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
            integrates_store=await get_finding_vulnerabilities(
                finding=finding,
                finding_id=finding_id,
            ),
            skims_store=store,
        )

        success = await do_build_and_upload_vulnerabilities(
            finding_id=finding_id,
            store=merged_store,
        ) and await do_release_vulnerabilities(
            finding_id=finding_id,
        ) and await upload_evidences(
            finding_id=finding_id,
            store=store,
        ) and await do_release_finding(
            finding_id=finding_id,
        )

        await log(
            'info', 'persisted: %s, results: %s, success: %s',
            finding.name, store_length, success,
        )
    elif not has_results:
        success = True

        await log(
            'info', 'persisted: %s, results: %s, success: %s',
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
