from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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

    loaders: Dataloaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    assert len(vulns) == 1
    vuln_accepted: Vulnerability = await loaders.vulnerability.load(
        vuln_accepted_id
    )
    assert vuln_accepted.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vuln_accepted.treatment
    assert (
        vuln_accepted.treatment.status == VulnerabilityTreatmentStatus.ACCEPTED
    )
    assert vuln_accepted.treatment.accepted_until

    await reset_expired_accepted_findings.process_group(
        loaders=loaders, group_name=group_name, progress=0.0
    )

    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    assert len(vulns) == 1
    vuln_accepted_reset: Vulnerability = await loaders.vulnerability.load(
        vuln_accepted_id
    )
    assert (
        vuln_accepted_reset.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    assert vuln_accepted_reset.treatment
    assert (
        vuln_accepted_reset.treatment.status
        == VulnerabilityTreatmentStatus.UNTREATED
    )
    assert vuln_accepted_reset.treatment.accepted_until is None
