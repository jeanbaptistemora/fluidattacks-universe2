# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from core.persist import (
    diff_results,
)
from core.vulnerabilities import (
    get_vulnerability_justification,
    vulns_with_reattack_requested,
)
from datetime import (
    datetime,
)
from model import (
    core_model,
)
import pytest
import re
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_diff_results() -> None:
    namespace = "test"
    namespace_other = "test-other"
    skims_store: EphemeralStore = get_ephemeral_store()
    integrates_store: EphemeralStore = get_ephemeral_store()

    common_finding = core_model.FindingEnum.F009
    common_integrates_metadata = core_model.IntegratesVulnerabilityMetadata(
        source=core_model.VulnerabilitySourceEnum.SKIMS,
    )
    common_kind = core_model.VulnerabilityKindEnum.LINES
    common_where = "file"

    # Something that Skims does not manage
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.INTEGRATES,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )

    # Something was open at Integrates and was found open by Skims
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="1",
            where=common_where,
        )
    )
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="1",
            where=common_where,
        )
    )

    # Something was open at Integrates and not found open by Skims
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="2",
            where=common_where,
        )
    )
    # put vulnerability that no are in the scope of analysis
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="backend/model/index.js",
            where=common_where,
        )
    )
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.CLOSED,
            what="backend/model/user.js",
            where=common_where,
        )
    )

    # Something was closed at Integrates and found open by Skims
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.CLOSED,
            what="3",
            where=common_where,
        )
    )
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="3",
            where=common_where,
        )
    )
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.CLOSED,
            what="backend/domain/user.js",
            where=common_where,
        )
    )
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="backend/domain/user.js",
            where=common_where,
        )
    )

    # Something was closed at Integrates and not found open by Skims
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.CLOSED,
            what="4",
            where=common_where,
        )
    )

    # Something was open on integrates in other namespace and not
    # found open by skims
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace_other,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="5",
            where=common_where,
        )
    )

    # Something was open on integrates but follows a weird format
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=common_integrates_metadata,
            kind=common_kind,
            namespace=namespace_other,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="...........",
            where=common_where,
        )
    )

    diff_store: EphemeralStore = await diff_results(
        skims_store=skims_store,
        integrates_store=integrates_store,
        namespace=namespace,
        include_path_patterns=["1", "2", "3", "4", "5", "backend/domain/*"],
        exclude_path_patterns=["backend/model/*"],
    )

    assert sorted([(x.what, x.state) for x in diff_store.iterate()]) == [
        ("1", core_model.VulnerabilityStateEnum.OPEN),
        ("2", core_model.VulnerabilityStateEnum.CLOSED),
        ("3", core_model.VulnerabilityStateEnum.OPEN),
        ("4", core_model.VulnerabilityStateEnum.CLOSED),
        ("backend/domain/user.js", core_model.VulnerabilityStateEnum.OPEN),
    ]


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_reattacked_store() -> None:
    namespace = "test"
    integrates_store: EphemeralStore = get_ephemeral_store()
    integrates_store_2: EphemeralStore = get_ephemeral_store()
    common_finding = core_model.FindingEnum.F009
    common_kind = core_model.VulnerabilityKindEnum.LINES
    common_where = "file"
    common_reattack_requested = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.REQUESTED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )
    common_verified_status = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.VERIFIED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )

    # Vulnerability with a reattack requested
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_reattack_requested,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )
    # Vulnerability with a verified status
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )
    # Something that Skims does not manage with a reattack requested
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.INTEGRATES,
                verification=common_reattack_requested,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )
    # Something that Skims does not manage with a verified status
    integrates_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.INTEGRATES,
                verification=common_verified_status,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )
    # Vulnerability with a verified status
    integrates_store_2.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="0",
            where=common_where,
        )
    )

    reattacked_store = vulns_with_reattack_requested(integrates_store)
    reattacked_store_2 = vulns_with_reattack_requested(integrates_store_2)
    assert reattacked_store is not None
    assert False not in [
        bool(
            (
                vuln.integrates_metadata
                and vuln.integrates_metadata.source
                == core_model.VulnerabilitySourceEnum.SKIMS
            )
            and (
                vuln.integrates_metadata.verification
                and vuln.integrates_metadata.verification.state
                == core_model.VulnerabilityVerificationStateEnum.REQUESTED
            )
        )
        for vuln in reattacked_store.iterate()
    ]
    assert reattacked_store.length() == 1
    assert reattacked_store_2 is None


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_vulnerability_justification() -> None:
    namespace = "test"
    skims_store: EphemeralStore = get_ephemeral_store()
    reattacked_store: EphemeralStore = get_ephemeral_store()
    skims_store_2: EphemeralStore = get_ephemeral_store()
    reattacked_store_2: EphemeralStore = get_ephemeral_store()
    skims_store_3: EphemeralStore = get_ephemeral_store()
    reattacked_store_3: EphemeralStore = get_ephemeral_store()
    common_finding = core_model.FindingEnum.F009
    common_kind = core_model.VulnerabilityKindEnum.LINES
    common_reattack_requested = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.REQUESTED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )
    common_verified_status = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.VERIFIED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )
    common_skims_metadata = core_model.SkimsVulnerabilityMetadata(
        cwe=(16,),
        description="Description",
        snippet="> Vulnerable line 1 \n \
                > Vulnerable lines 2 \n \
                > Vulnerable lines 3 \n",
        source_method="SAST",
        developer=core_model.DeveloperEnum.DIEGO_RESTREPO,
        technique=core_model.TechniqueEnum.ADVANCE_SAST,
    )

    # Vulnerability with a reattack requested
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=common_skims_metadata,
        )
    )
    # On integrate_store but not in reattacked store
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="0",
            skims_metadata=common_skims_metadata,
        )
    )
    reattacked_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_reattack_requested,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=None,
        )
    )

    skims_store_2.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="0",
            skims_metadata=common_skims_metadata,
        )
    )
    reattacked_store_2.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=None,
        )
    )

    # Vulnerability with a reattack requested
    skims_store_3.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.CLOSED,
            what="file",
            where="1",
            skims_metadata=common_skims_metadata,
        )
    )
    # On integrate_store but not in reattacked store
    skims_store_3.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="0",
            skims_metadata=common_skims_metadata,
        )
    )
    reattacked_store_3.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_reattack_requested,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=None,
        )
    )
    reattacked_store_3.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_reattack_requested,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="0",
            skims_metadata=None,
        )
    )

    justification = get_vulnerability_justification(
        reattacked_store=reattacked_store, store=skims_store
    )
    justification_2 = get_vulnerability_justification(
        reattacked_store_2, skims_store_2
    )
    justification_3 = get_vulnerability_justification(
        reattacked_store_3, skims_store_3
    )

    assert len(justification) == 1
    assert not justification_2
    assert len(justification_3) == 2


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_comment_to_dast_methods() -> None:
    namespace = "test"
    skims_store: EphemeralStore = get_ephemeral_store()
    reattacked_store: EphemeralStore = get_ephemeral_store()
    common_finding = core_model.FindingEnum.F133
    common_kind = core_model.VulnerabilityKindEnum.LINES
    common_reattack_requested = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.REQUESTED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )
    common_verified_status = core_model.VulnerabilityVerification(
        state=core_model.VulnerabilityVerificationStateEnum.VERIFIED,
        date=datetime.strptime(
            "2020-01-01T00:45:12+0000", "%Y-%m-%dT%H:%M:%S%z"
        ),
    )
    common_skims_metadata = core_model.SkimsVulnerabilityMetadata(
        cwe=(16,),
        description="Description",
        snippet="> Vulnerable line 1 \n \
                > Vulnerable lines 2 \n \
                > Vulnerable lines 3 \n",
        source_method="DAST",
        developer=core_model.DeveloperEnum.DIEGO_RESTREPO,
        technique=core_model.TechniqueEnum.DAST,
    )

    # Vulnerability with a reattack requested
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=common_skims_metadata,
        )
    )
    # On integrate_store but not in reattacked store
    skims_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_verified_status,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="0",
            skims_metadata=common_skims_metadata,
        )
    )
    reattacked_store.store(
        core_model.Vulnerability(
            finding=common_finding,
            integrates_metadata=core_model.IntegratesVulnerabilityMetadata(
                source=core_model.VulnerabilitySourceEnum.SKIMS,
                verification=common_reattack_requested,
                commit_hash="b72bd2c2b3c6d34caec6cd1733eca959a1bfe074",
            ),
            kind=common_kind,
            namespace=namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what="file",
            where="1",
            skims_metadata=None,
        )
    )
    open_vulns_comment = (
        r"^A reattack request was executed on\s"
        + r"+([0-9]{4}\/+[0-9]{2}\/+[0-9]{2}\sat\s"
        + r"[0-9]{2}\:[0-9]{2})\.\n"
        + r"Reported vulnerabilities are still open in commit\s+"
        + r"([a-zA-Z0-9]{40})\: \n"
        + r"   - test/file $"
    )
    justification = get_vulnerability_justification(
        reattacked_store=reattacked_store, store=skims_store
    )

    assert re.search(open_vulns_comment, justification[0])
    assert len(justification) == 1
