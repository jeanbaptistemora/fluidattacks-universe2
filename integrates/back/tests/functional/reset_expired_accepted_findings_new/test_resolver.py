from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
    FindingTreatmentSummary,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers import (
    reset_expired_accepted_findings_new,
)
from typing import (
    cast,
    Dict,
    List,
)
from vulnerabilities import (
    domain as vulns_domain,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reset_expired_accepted_findings_new")
@freeze_time("2021-08-10")
async def test_get_group(populate: bool) -> None:
    assert populate
    finding_id = "475041521"
    loaders: Dataloaders = get_new_context()
    vulns = await loaders.finding_vulns.load(finding_id)
    assert len(vulns) == 3

    accepted_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e61",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("acceptance_date")
    assert historic_treatment[-1].get("treatment") == "ACCEPTED"

    accepted_undefined_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e62",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_undefined_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("acceptance_status") == "SUBMITTED"
    assert historic_treatment[-1].get("treatment") == "ACCEPTED_UNDEFINED"

    accepted_undefined_not_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e63",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_undefined_not_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("acceptance_status") == "SUBMITTED"
    assert historic_treatment[-1].get("treatment") == "ACCEPTED_UNDEFINED"

    await reset_expired_accepted_findings_new.main()

    accepted_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e61",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("treatment") == "NEW"  # Reset

    accepted_undefined_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e62",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_undefined_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("treatment") == "NEW"  # Reset

    # Vuln not modified as it has not "expired"
    accepted_undefined_not_expired = await vulns_domain.get_by_finding(
        finding_id,
        "6401bc87-8633-4a4a-8d8e-7dae0ca57e63",
    )
    historic_treatment = cast(
        List[Dict[str, str]],
        accepted_undefined_not_expired.get("historic_treatment", [{}]),
    )
    assert historic_treatment[-1].get("acceptance_status") == "SUBMITTED"
    assert historic_treatment[-1].get("treatment") == "ACCEPTED_UNDEFINED"

    finding: Finding = await loaders.finding_new.load(finding_id)
    assert (
        finding.unreliable_indicators.unreliable_treatment_summary
        == FindingTreatmentSummary(
            accepted=0,
            accepted_undefined=1,
            in_progress=0,
            new=2,
        )
    )
