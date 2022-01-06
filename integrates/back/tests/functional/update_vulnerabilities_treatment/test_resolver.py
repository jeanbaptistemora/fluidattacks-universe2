from . import (
    get_stakeholders,
    get_vulnerability,
    grant_stakeholder,
    put_mutation,
)
from custom_exceptions import (
    InvalidAssigned,
)
from freezegun.api import (  # type: ignore
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned", "acceptance_date"),
    (
        (
            "customer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "IN_PROGRESS",
            "customer@gmail.com",
            "",
        ),
        (
            "customeradmin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            "ACCEPTED_UNDEFINED",
            "customer1@gmail.com",
            "",
        ),
        (
            "customeradmin@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            "ACCEPTED",
            "customer1@gmail.com",
            "2021-03-31 19:45:11",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
    acceptance_date: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date=acceptance_date,
    )
    assert "errors" not in result
    assert result["data"]["updateVulnerabilitiesTreatment"]["success"]
    vulnerability_response: Dict[str, Any] = await get_vulnerability(
        user=email, vulnerability_id=vulnerability
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["treatmentManager"]
        == assigned
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["assigned"]
        == assigned
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["treatment"]
        == treatment
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment"),
    (
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "system_owner@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_fail(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=email,
        acceptance_date="2021-03-31 19:45:11",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned"),
    (
        (
            "customeradmin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "IN_PROGRESS",
            "nonconfirmeduser@test.com",
        ),
    ),
)
async def test_update_vulnerabilities_treatment_non_confirmed(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    group_name: str = "group1"
    result_grant: Dict[str, Any] = await grant_stakeholder(
        user=email,
        stakeholder=assigned,
        group=group_name,
    )
    assert "errors" not in result_grant
    assert result_grant["data"]["grantStakeholderAccess"]["success"]

    stakeholders: Dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )
    for stakeholder in stakeholders["data"]["group"]["stakeholders"]:
        if stakeholder["email"] == assigned:
            assert stakeholder["invitationState"] == "PENDING"

    result: Dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidAssigned())
