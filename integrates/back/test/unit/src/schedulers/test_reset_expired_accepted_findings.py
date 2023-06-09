from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers import (
    reset_expired_accepted_findings,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2021-01-01T00:00:00+00:00")
async def test_reset_expired_accepted_findings() -> None:
    group_name = "lubbock"
    finding_id = "818828206"
    vuln_accepted_id = "429bd683-3654-4dad-9eeb-3f8a2de9afd4"
    vuln_submitted_undefined_id = "1f0ee1d0-9816-49c6-8687-f91de722681b"
    vuln_accepted_no_change_id = "f54d583b-cb1e-4b26-9b88-42baddab33ad"

    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    assert len(vulns) == 3
    vuln_accepted = await loaders.vulnerability.load(vuln_accepted_id)
    assert vuln_accepted
    assert vuln_accepted.state.status == VulnerabilityStateStatus.VULNERABLE
    assert (
        vuln_accepted.treatment
        and vuln_accepted.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED
    )
    assert vuln_accepted.treatment.accepted_until
    vuln_submitted_undefined = await loaders.vulnerability.load(
        vuln_submitted_undefined_id
    )
    assert vuln_submitted_undefined
    assert (
        vuln_submitted_undefined.state.status
        == VulnerabilityStateStatus.VULNERABLE
    )
    assert vuln_submitted_undefined.treatment
    assert (
        vuln_submitted_undefined.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
    )
    assert (
        vuln_submitted_undefined.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.SUBMITTED
    )
    assert vuln_submitted_undefined.treatment.accepted_until is None
    vuln_accepted_no_change = await loaders.vulnerability.load(
        vuln_accepted_no_change_id
    )
    assert vuln_accepted_no_change
    assert (
        vuln_accepted_no_change.state.status
        == VulnerabilityStateStatus.VULNERABLE
    )
    assert vuln_accepted_no_change.treatment
    assert (
        vuln_accepted_no_change.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED
    )
    assert vuln_accepted_no_change.treatment.accepted_until

    await reset_expired_accepted_findings.process_group(
        loaders=loaders, group_name=group_name, progress=0.0
    )

    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    assert len(vulns) == 3
    vuln_accepted = await loaders.vulnerability.load(vuln_accepted_id)
    assert vuln_accepted
    assert vuln_accepted.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vuln_accepted.treatment
    assert (
        vuln_accepted.treatment.status
        == VulnerabilityTreatmentStatus.UNTREATED
    )
    assert vuln_accepted.treatment.accepted_until is None
    vuln_submitted_undefined = await loaders.vulnerability.load(
        vuln_submitted_undefined_id
    )
    assert vuln_submitted_undefined
    assert (
        vuln_submitted_undefined.state.status
        == VulnerabilityStateStatus.VULNERABLE
    )
    assert vuln_submitted_undefined.treatment
    assert (
        vuln_submitted_undefined.treatment.status
        == VulnerabilityTreatmentStatus.UNTREATED
    )
    assert vuln_submitted_undefined.treatment.acceptance_status is None
    assert vuln_submitted_undefined.treatment.accepted_until is None
    vuln_accepted_no_change = await loaders.vulnerability.load(
        vuln_accepted_no_change_id
    )
    assert vuln_accepted_no_change
    assert (
        vuln_accepted_no_change.state.status
        == VulnerabilityStateStatus.VULNERABLE
    )
    assert vuln_accepted_no_change.treatment
    assert (
        vuln_accepted_no_change.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED
    )
    assert vuln_accepted_no_change.treatment.accepted_until
