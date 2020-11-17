# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from core.persist import (
    diff_results,
)
from state.ephemeral import (
    get_ephemeral_store,
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    IntegratesVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)


@run_decorator
async def test_diff_results() -> None:
    skims_store: EphemeralStore = get_ephemeral_store()
    integrates_store: EphemeralStore = get_ephemeral_store()

    common_finding = FindingEnum.F009
    common_integrates_metadata = IntegratesVulnerabilityMetadata(
        source=VulnerabilitySourceEnum.SKIMS,
    )
    common_kind = VulnerabilityKindEnum.LINES
    common_where = 'file'

    # Something that Skims does not manage
    await integrates_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=IntegratesVulnerabilityMetadata(
            source=VulnerabilitySourceEnum.INTEGRATES,
        ),
        kind=common_kind,
        state=VulnerabilityStateEnum.OPEN,
        what='0',
        where=common_where,
    ))

    # Something was open at Integrates and was found open by Skims
    await integrates_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.OPEN,
        what='1',
        where=common_where,
    ))
    await skims_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.OPEN,
        what='1',
        where=common_where,
    ))

    # Something was open at Integrates and not found open by Skims
    await integrates_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.OPEN,
        what='2',
        where=common_where,
    ))

    # Something was closed at Integrates and found open by Skims
    await integrates_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.CLOSED,
        what='3',
        where=common_where,
    ))
    await skims_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.OPEN,
        what='3',
        where=common_where,
    ))

    # Something was closed at Integrates and not found open by Skims
    await integrates_store.store(Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=VulnerabilityStateEnum.CLOSED,
        what='4',
        where=common_where,
    ))

    diff_store: EphemeralStore = await diff_results(
        skims_store=skims_store,
        integrates_store=integrates_store,
    )

    # This is the smallest possible delta, just change what changed!
    assert sorted([(x.what, x.state) async for x in diff_store.iterate()]) == [
        ('2', VulnerabilityStateEnum.CLOSED),
        ('3', VulnerabilityStateEnum.OPEN),
    ]
