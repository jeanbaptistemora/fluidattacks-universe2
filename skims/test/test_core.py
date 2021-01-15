# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from core.persist import (
    diff_results,
)
from model import (
    core_model,
)
from state.ephemeral import (
    get_ephemeral_store,
    EphemeralStore,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_diff_results() -> None:
    namespace = 'test'
    namespace_other = 'test-other'
    skims_store: EphemeralStore = get_ephemeral_store()
    integrates_store: EphemeralStore = get_ephemeral_store()

    common_finding = core_model.FindingEnum.F009
    common_integrates_metadata = core_model.IntegratesVulnerabilityMetadata(
        namespace=namespace,
        source=core_model.VulnerabilitySourceEnum.SKIMS,
    )
    common_integrates_metadata_in_other_ns = \
        core_model.IntegratesVulnerabilityMetadata(
            namespace=namespace_other,
            source=core_model.VulnerabilitySourceEnum.SKIMS,
        )
    common_kind = core_model.VulnerabilityKindEnum.LINES
    common_where = 'file'

    # Something that Skims does not manage
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
            source=core_model.VulnerabilitySourceEnum.INTEGRATES,
        ),
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='0',
        ),
        where=common_where,
    ))

    # Something was open at Integrates and was found open by Skims
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='1',
        ),
        where=common_where,
    ))
    await skims_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='1',
        ),
        where=common_where,
    ))

    # Something was open at Integrates and not found open by Skims
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='2',
        ),
        where=common_where,
    ))

    # Something was closed at Integrates and found open by Skims
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.CLOSED,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='3',
        ),
        where=common_where,
    ))
    await skims_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='3',
        ),
        where=common_where,
    ))

    # Something was closed at Integrates and not found open by Skims
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.CLOSED,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='4',
        ),
        where=common_where,
    ))

    # Something was open on integrates in other namespace and not
    # found open by skims
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata_in_other_ns,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='5',
        ),
        where=common_where,
    ))

    # Something was open on integrates but follows a weird format
    await integrates_store.store(core_model.Vulnerability(
        finding=common_finding,
        integrates_metadata=common_integrates_metadata_in_other_ns,
        kind=common_kind,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what='...........',
        where=common_where,
    ))

    diff_store: EphemeralStore = await diff_results(
        skims_store=skims_store,
        integrates_store=integrates_store,
        namespace=namespace,
    )

    # This is the smallest possible delta, just change what changed!
    assert sorted([(x.what, x.state) async for x in diff_store.iterate()]) == [
        (serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='2',
        ), core_model.VulnerabilityStateEnum.CLOSED),
        (serialize_namespace_into_vuln(
            kind=common_kind,
            namespace=namespace,
            what='3',
        ), core_model.VulnerabilityStateEnum.OPEN),
    ]
